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

# Step 1:
#      leader sends "Hello" 5 times while follower listens 5 times
#      follower checks received data for "Hello"
# Step 2:
#      leader listens 5 times while follower sends "H-ACK" 5 times
#      leader checks received data for "H-ACK"
# Step 3:
#      leader sends "ACK" 5 times while follower listens 5 times
#      follower checks received data for "ACK"

# both agents should start running at the same time or else the leader and follower algorithms might get out of sync with each other

# the leader pi is A
if (rpi.ID == "leader\n"):
    # pick which transceiver to start searching with
    trans = (int)(rpi.start)
    # conditions for the steps of the handshake
    handshake1 = False
    handshake2 = False
    handshake3 = False
    # iterate through each transceiver
    for i in range(0,16):
        rpi.chooseIrda(trans)
        input_arr = [""]
        # on each transceiver, send "Hello" 5 times
        for step_1_attempt in range(0,5):
            rpi.ser.reset_output_buffer()
            outMessage = "Hello"
            print("Sending \"" + str(outMessage) + "\" on " + str(trans))
            time.sleep(0.5)
            rpi.ser.write(outMessage.encode('utf-8'))
        # after sending 5 times, listen for "H-ACK" 5 times and add the inputs to an array
        for step_2_attempt in range(0,5):
            rpi.ser.reset_input_buffer()
            inBuffer = 0
            inMessage = ""
            print("Waiting for \"H-ACK\" on " + str(trans))
            time.sleep(0.5)
            # inBuffer is the size of the received serial data
            # if inBuffer is 0 then there is nothing waiting to be read
            inBuffer = rpi.ser.in_waiting
            # if there is an input, try to decode it
            if(inBuffer != 0):
                try:
                    # step 1 complete
                    handshake1 = True
                    inMessage = rpi.ser.read(inBuffer).decode('utf-8')
                # if the input data cannot be decoded then add "00001" to the array instead
                except Exception as e:
                    print(e)
                    input_arr.append("00001")
                    continue
                # add the input to the array
                print(inMessage)
                input_arr.append(inMessage)
            # if there is no input data then add "00000" to the array
            else:
                input_arr.append("00000")
        # check if the array of inputs includes "H-ACK"
        for j in range(1,6):
            s2_input = input_arr[j]
            if(s2_input[0:5] == "H-ACK"):
                # step 2 complete
                handshake2 = True
        # if step 1 is complete but step 2 is not then end algorithm
        if (handshake1 == True and handshake2 == False):
            break
        # if step 1 and step 2 are complete then move on to step 3
        if (handshake2):
            print("Received: \"H-ACK\" on " + str(trans))
            print("Step 2 Complete")
            # send "ACK" 5 times
            for step_3_attempt in range(0,5):
                rpi.ser.reset_output_buffer()
                outMessage = "ACK"
                print("Sending \"" + str(outMessage) + "\" on " + str(trans))
                time.sleep(0.5)
                rpi.ser.write(outMessage.encode('utf-8'))
            # handshake complete; end algorithm
            print("Step 3 Complete")
            print("Connected")
            break
        # iterate through the transceivers
        if (trans == 15):
            trans = 0
        else:
            trans += 1
            
# the follower pi is B
# there is an issue with the algorithm:
#    sometimes B receives data from a transceiver that B's selected transceiver is not facing
#    B then completes step 1 and sends "H-ACK" 5 times
#    since B's transceiver is not facing A's transceiver, A does not read "H-ACK" and switches to the next transceiver while B is waiting for "ACK"
elif (rpi.ID == "follower\n"):
    # conditions for the steps of the handshake
    handshake1 = False
    handshake2 = False
    handshake3 = False
    # pick which transceiver to start searching with
    trans = (int)(rpi.start)
    # iterate through each transceiver
    for i in range(0,16):
        rpi.chooseIrda(trans)
        input_arr = [""]
        # listen 5 times and add the received data to input_arr
        for step_1_attempt in range(0,5):
            rpi.ser.reset_input_buffer()
            inBuffer = 0
            print("Waiting for \"Hello\" on " + str(trans))
            time.sleep(0.5)
            inBuffer = rpi.ser.in_waiting
            inMessage = ""
            # if there is an input, try to decode it
            if (inBuffer != 0):
                try:
                    inMessage = rpi.ser.read(inBuffer).decode('utf-8')
                # if the input data cannot be decoded then add "00001" to the array instead
                except Exception as e:
                    print(e)
                    input_arr.append("00001")
                    continue
                # add input data to the array
                print(inMessage)
                input_arr.append(inMessage)
            # if there is no input data then add "00000" to the array
            else:
                input_arr.append("00000")
        # check if the array of inputs includes "Hello"
        for j in range(1,6):
            s1_input = input_arr[j]
            if (s1_input[0:5] == "Hello"):
                # step 1 complete
                handshake1 = True
        # if step 1 is complete, move on to step 2
        if (handshake1):
            print("Received: \"Hello\" on " + str(trans))
            print("Step 1 Complete")
            # send "H-ACK" 5 times
            for step_2_attempt in range(0,5):
                rpi.ser.reset_output_buffer()
                outMessage = "H-ACK"
                print("Sending \"" + str(outMessage) + "\" on " + str(trans))
                rpi.ser.write(outMessage.encode('utf-8'))
                time.sleep(0.5)
            # step 3
            # repeat step 1 algorithm, but search for "ACK"
            input_2_arr = [""]
            for step_3_attempt in range(0,5):
                rpi.ser.reset_input_buffer()
                inBuffer = 0
                inMessage = ""
                print("Waiting for \"ACK\" on " + str(trans))
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
                    # step 3 complete
                    handshake3 = True
            if (handshake3):
                print("Received: \"ACK\" on " + str(trans))
                print("Step 3 Complete")
                print("Connected")
            break # break out of for i in range(0,16)
        # if step 1 is not complete then wait 5 times for the leader to finish listening
        # this condition is meant to keep the two agents in sync
        else:
            for l in range(0,5):
                time.sleep(0.5)
        # iterate through the transceivers
        if (trans == 15):
            trans = 0
        else:
            trans += 1

rpi.clean()
            
