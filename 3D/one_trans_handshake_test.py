import random
from random import choice
import serial
import time
import RPi.GPIO as GPIO
import json

S3 = [0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1] # mux_prime_B; GPIO5
S2 = [0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1] # mux_prime_A; GPIO6
S1 = [0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1] # mux_second_B; GPIO20
S0 = [0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1] # mux_second_A; GPIO21

class Node:
    ID = None
    pins = None
    ser = None
    isFacing = None
    lora = False
    start = None
    
    def __init__(self):
        self.pins = [29, 31, 38, 40] # [S3, S2, S1, S0]
        
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pins, GPIO.OUT, initial = 0)
        
        self.ser = serial.Serial('/dev/ttyS0', 9600, stopbits = serial.STOPBITS_TWO,
                                 parity = serial.PARITY_NONE, timeout = 1) # serial.Serial('/dev/ttyS0', 9600)
        self.isFacing = False
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
    handshake1 = False
    handshake2 = False
    handshake3 = False
    rpi.chooseIrda(trans)
    input_arr = [""]
    for step_1_attempt in range(0,5):
        rpi.ser.reset_output_buffer()
        outMessage = "Hello"
        print("Sending \"" + str(outMessage) + "\"")
        time.sleep(0.5) # maybe change to 1
        rpi.ser.write(outMessage.encode('utf-8'))
    for step_2_attempt in range(0,5):
        rpi.ser.reset_input_buffer()
        inBuffer = 0
        inMessage = ""
        print("Waiting for \"H-ACK\"")
        time.sleep(0.5)
        inBuffer = rpi.ser.in_waiting
        if(inBuffer != 0):
            try:
                handshake1 = True
                inMessage = rpi.ser.read(inBuffer).decode('utf-8')
            except Exception as e:
                print(e)
                input_arr.append("00001")
                continue
            print(inMessage)
            input_arr.append(inMessage)
        else:
            input_arr.append("00000")
    for j in range(1,6):
        s2_input = input_arr[j]
        if(s2_input[0:5] == "H-ACK"):
            handshake2 = True
    if (handshake2):
        print("Received: \"H-ACK\"")
        print("Step 2 Complete")
        for step_3_attempt in range(0,5):
            rpi.ser.reset_output_buffer()
            outMessage = "ACK"
            print("Sending \"" + str(outMessage) + "\"")
            time.sleep(0.5)
            rpi.ser.write(outMessage.encode('utf-8'))
        print("Step 3 Complete")
        print("Connected")
        # no other transceivers to iterate through
# the follower pi is B
elif (rpi.ID == "follower\n"):
    handshake1 = False
    handshake2 = False
    handshake3 = False
    trans = (int)(rpi.start)
    rpi.chooseIrda(trans)
    input_arr = [""]
    for step_1_attempt in range(0,5):
        rpi.ser.reset_input_buffer()
        inBuffer = 0
        print("Waiting for \"Hello\"")
        time.sleep(0.5)
        inBuffer = rpi.ser.in_waiting
        inMessage = ""
        if (inBuffer != 0):
            try:
                inMessage = rpi.ser.read(inBuffer).decode('utf-8')
            except Exception as e:
                print(e)
                input_arr.append("00001")
                continue
            print(inMessage)
            input_arr.append(inMessage)
        else:
            input_arr.append("00000")
    for j in range(1,6):
        s1_input = input_arr[j]
        if (s1_input[0:5] == "Hello"):
            handshake1 = True
    if (handshake1):
        print("Received: \"Hello\"")
        print("Step 1 Complete")
        for step_2_attempt in range(0,5):
            rpi.ser.reset_output_buffer()
            outMessage = "H-ACK"
            print("Sending \"" + str(outMessage) + "\"")
            rpi.ser.write(outMessage.encode('utf-8'))
            time.sleep(0.5)
        input_2_arr = [""]
        for step_3_attempt in range(0,5):
            rpi.ser.reset_input_buffer()
            inBuffer = 0
            inMessage = ""
            print("Waiting for \"ACK\"")
            time.sleep(0.5)
            inBuffer = rpi.ser.in_waiting
            if(inBuffer != 0):
                try:
                    inMessage = rpi.ser.read(inBuffer).decode('utf-8')
                except Exception as e:
                    print(e)
                    input_2_arr.append("00001")
                    continue
                print(inMessage)
                input_2_arr.append(inMessage)
            else:
                input_2_arr.append("00000")
        for k in range(1,6):
            s3_input = input_2_arr[k]
            if(s3_input[0:3] == "ACK"):
                handshake3 = True
        if (handshake3):
            print("Received: \"ACK\"")
            print("Step 3 Complete")
            print("Connected")

rpi.clean()
            