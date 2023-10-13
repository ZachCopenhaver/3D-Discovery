import random
from random import choice
import serial
import time
import RPi.GPIO as GPIO
import json
import sys
import socket
import csv

S3 = [0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1] # mux_prime_B; GPIO5
S2 = [0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1] # mux_prime_A; GPIO6
S1 = [0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1] # mux_second_B; GPIO20
S0 = [0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1] # mux_second_A; GPIO21

class Node:
    ID = None
    pins = None
    ser = None
    start = None
    
    def __init__(self):
        # output pins
        self.pins = [29, 31, 38, 40] # [S3, S2, S1, S0]
        
        # set up GPIO
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pins, GPIO.OUT, initial = 0)
        
        # set up serial port and library
        self.ser = serial.Serial('/dev/ttyS0', 9600, stopbits = serial.STOPBITS_TWO,
                                 parity = serial.PARITY_NONE, timeout = 1) # serial.Serial('/dev/ttyS0', 9600)
        
        # use ID.txt to determine whether this agent is the leader or follower
        # ID.txt has the following information:
        #      "leader" or "follower"
        #      number of the transceiver the algorithm should start on
        # on one agent ID.txt should have "leader" and on the other it should have "follower"
        f = open("ID.txt","r")
        self.ID = f.readline()
        self.start = f.readline()
        f.close()
    
    def chooseIrda(self, trans): # trans: the irda transceiver number between 0 and 15
        GPIO.output(self.pins, 0) # reset all pin outputs to zero
        
        GPIO.output(self.pins[0], S3[trans]) # set S3
        GPIO.output(self.pins[1], S2[trans]) # set S2
        GPIO.output(self.pins[2], S1[trans]) # set S1
        GPIO.output(self.pins[3], S0[trans]) # set S0
            
    def clean(self):
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        self.ser.close()
        GPIO.cleanup()
        

rpi = Node()
et = time.time()

# the leader pi is A
if (rpi.ID == "leader\n"):
    trans = (int)(rpi.start)
    rpi.chooseIrda(trans)
    
    UDP_IP = "172.25.249.217"
    UDP_PORT = 5005
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, UDP_PORT))

    for i in range(0,300):
        rpi.ser.reset_output_buffer()
        # listen for packet from follower and then send
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        print("received message: %s" % data)
        time.sleep(0.5)
        outMessage = "Hello"
        print("Attempt: " + (str)(i))
        rpi.ser.write(outMessage.encode('utf-8'))
        
elif (rpi.ID == "follower\n"):
#     trans = (int)(rpi.start)
    trans = 1
    rpi.chooseIrda(trans)
    success = 0
    fail = 0
    i = 0
    
    outFile = open(sys.argv[1], 'w')
    csvFile = csv.writer(outFile)
    csvFile.writerow(["Attempt", "Bytes_Received", "Success/Fail"])
    
    UDP_IP = "172.25.249.34"
    UDP_PORT = 5005
    MESSAGE = b"SEND_NOW"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP    

    for i in range(0,300):
        rpi.ser.reset_input_buffer()
        inBuffer = 0
        
        # wait 0.5 sec then send a message to sender to send packet and proceed
        time.sleep(0.5)
        sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
        
        time.sleep(0.5)
        inBuffer = rpi.ser.in_waiting
        inMessageByte = ""
        inMessageStr = ""
        if (inBuffer != 0):
            inMessageByte = rpi.ser.read(inBuffer)
            try:
                inMessageStr = inMessageByte.decode('utf-8')
            except Exception as e:
                fail += 1
                print("Received: " + (str)(inMessageByte) + "\tAttempts: " + (str)(i) + "\tFails: " + (str)(fail))
                csvFile.writerow([i, inMessageByte, 'f'])
                continue
            if (inMessageStr == "Hello"):
                success += 1
                print("Received: " + (str)(inMessageStr) + "\tAttempts: " + (str)(i) + "\tSuccesses: " + (str)(success))
                csvFile.writerow([i, inMessageStr, 's'])
            else:
                fail += 1
                print("Received: " + (str)(inMessageStr) + "\tAttempts: " + (str)(i) + "\tFails: " + (str)(fail))
                csvFile.writerow([i, inMessageStr, 'f'])
        else:
            fail += 1
            print("Received: null\tAttempts: " + (str)(i) + "\tFails: " + (str)(fail))
            csvFile.writerow([i, 'null', 'f'])
    print("Attempts: " + (str)(i+1))
    print("Successes: " + (str)(success))
    print("Fails: " + (str)(fail))
    
    # write number of successes to file
    csvFile.writerow(["Total Attempts", "Total Success", "Total Fail"])
    csvFile.writerow([i+1,success,fail])
    outFile.close()


rpi.clean()
            
