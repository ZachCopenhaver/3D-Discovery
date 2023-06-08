import random
from random import choice
import serial
import time
import RPi.GPIO as GPIO
import json

A = [0,1,0,1]
B = [0,0,1,1]

class Node:
    ID = None
    pins = None
    ser = None
    isFacing = None
    lora = False
    start = None

    def __init__(self):
        self.pins = [29, 31, 38, 40] #[mux1selectorB, mux1selectorA, mux2&3selectorB, mux2&3selectorA]

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pins, GPIO.OUT, initial = 0)

        self.ser = serial.Serial('/dev/ttyS0', 9600, stopbits = serial.STOPBITS_TWO, 
        parity = serial.PARITY_NONE, timeout = 1)   # serial.Serial('/dev/ttyS0', 9600)
        f = open("ID.txt", "r")
        self.ID = f.readline()
        self.start = f.readline()
        f.close()
        isFacing = False

    def chooseIrda(self, iId): #iId: the irda number between 1 and 8, 0 for lora;
        GPIO.output(self.pins, 0)
        if iId == 0:
            GPIO.output(self.pins[2], 1)
            GPIO.output(self.pins[3], 0)
        else:
            mux = int(iId/4) 
            if iId % 4 == 0:
                mux -= 1
            GPIO.output(self.pins[2], B[mux])
            GPIO.output(self.pins[3], A[mux])

            iId = (iId-1) % 4

            GPIO.output(self.pins[0], B[iId])
            GPIO.output(self.pins[1], A[iId])
    def clean(self):
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        self.ser.close()
        GPIO.cleanup()

if __name__ == '__main__':
    rpi = Node()
    et = time.time()
    
    # the leader is A
    if (rpi.ID == "leader\n"):
        # these are used to get data about all of the trials
        success = 0
        sig_sent = 0
        sig_received = 0
        error = 0
        # code runs for 100 trials
        for z in range(0,100):
            handshake1 = False
            handshake2 = False
            handshake3 = False
            # select initial transceiver
            transceiver = (int)(rpi.start)
            
            # iterate through each transceiver
            for i in range(1,9):
                rpi.chooseIrda(transceiver)
                input_arr = [""]
                # on each transceiver, send "Hello" 5 times
                for step_1_attempt in range(1,6):
                    rpi.ser.reset_output_buffer()
                    outMessage = "Hello"
                    print("Sending \"" + (str)(outMessage) + "\" on transceiver " + (str)(transceiver))
                    sig_sent += 1
                    time.sleep(0.5)
                    rpi.ser.write(outMessage.encode('utf-8'))
                # after sending 5 times, listen for "H-ACK" 5 times and add the inputs to an array
                for step_2_attempt in range(1,6):
                    rpi.ser.reset_input_buffer()
                    inBuffer = 0
                    inMessage = ""
                    print("Waiting for \"H-ACK\" on transceiver " + str(transceiver))
                    time.sleep(0.5)
                    inBuffer = rpi.ser.in_waiting
                    # if there is an input, try to decode it
                    if (inBuffer != 0):
                        try:
                            sig_received += 1
                            handshake1 = True
                            inMessage = rpi.ser.read(inBuffer).decode('utf-8')
                        # if the input cannot be decoded then add "00001" to the array instead
                        except Exception as e:
                            print(e)
                            input_arr.append("00001")
                            error += 1
                            continue
                        # add input to the array
                        print(inMessage)
                        input_arr.append(inMessage)
                    # if there is no input then add "00000" to the array
                    else:
                        input_arr.append("00000")
                # check if the array includes "H-ACK"
                for j in range(1,6):
                    s2_input = input_arr[j]
                    if(s2_input[0:5] == "H-ACK"):
                        handshake2 = True
                # if the hello step has been completed but H-ACK has not been received then break out of transceiver loop
                if (handshake1 == True and handshake2 == False):
                    break
                # if H-ACK was received then start step 3
                if (handshake2):
                    print("Received: \"H-ACK\"")
                    print("Step 2 Complete")
                    # try to send ACK 5 times
                    for step_3_attempt in range(1,6):
                        rpi.ser.reset_output_buffer()
                        outMessage = "ACK"
                        print("Sending \"" + (str)(outMessage) + "\" on transceiver " + (str)(transceiver))
                        sig_sent += 1
                        time.sleep(0.5)
                        rpi.ser.write(outMessage.encode('utf-8'))
                        
                    print("Step 3 Complete")
                    print("Connected")
                    success += 1
                    break # break out of transceiver loop
                # iterate through transceivers
                if (transceiver == 7):
                    transceiver = 8
                else:
                    transceiver = (transceiver + 1) % 8
            # reset program for next trial
            rpi.ser.reset_input_buffer()
            rpi.ser.reset_output_buffer()
            print("\nSuccesses: " + (str)(success) + "\n")
        # show data found
        print("Successes: " + str(success) + "/100")
        print("Number of Signals Sent: " + str(sig_sent))
        print("Number of Signals Received: " + str(sig_received))
        print("Number of Signals Received with Error: " + str(error))
        
    # the follower is B
    elif (rpi.ID == "follower\n"):
        # these are used to get data from the trials
        success = 0
        sig_sent = 0
        sig_received = 0
        error = 0
        # execute this program 100 times
        for z in range(0,100):
            handshake1 = False
            handshake3 = False
            # pick the transceiver opposite of the leader's transceiver
            transceiver = (int)(rpi.start)
            if (transceiver == 4):
                transceiver = 8
            else:
                transceiver = (transceiver + 4) % 8
                
            # try on each transceiver
            for i in range(1,9):
                rpi.chooseIrda(transceiver)
                input_arr = [""]
                # listen 5 times on each transceiver and append inputs to input_arr
                # if there are no inputs or there is an error then append "00000" to input_arr
                for step_1_attempt in range(1,6):
                    # reset buffers for the loop
                    rpi.ser.reset_input_buffer()
                    inBuffer = 0
                    # receive potential input
                    print("Waiting for \"Hello\" on transceiver " + (str)(transceiver))
                    time.sleep(0.5)
                    inBuffer = rpi.ser.in_waiting
                    inMessage = ""
                    # if there is an input, decode it and add it to input_arr
                    if (inBuffer != 0):
                        # if the input cannot be decoded in utf-8 then this line throws an exception
                        try:
                            sig_received += 1
                            inMessage = rpi.ser.read(inBuffer).decode('utf-8')
                        # if the input cannot be decoded then catch the exception, append "00000" to input_arr, and continue through loop
                        except Exception as e:
                            print(e)
                            input_arr.append("00001")
                            error += 1
                            continue
                        # these 2 lines are only reached if the input can be decoded
                        print(inMessage)
                        input_arr.append(inMessage)
                    # if there is not an input, append "00000" to input_arr
                    else:
                        input_arr.append("00000")
                # after listening 5 times, check every element of input_arr
                # if at least one element of input_arr is valid then step 1 of the handshake is complete
                for j in range(1,6):
                    s1_input = input_arr[j]
                    if (s1_input[0:5] == "Hello"):
                        handshake1 = True
                if (handshake1):
                    print("Received: \"Hello\"")
                    print("Step 1 Complete")
                    # step 2: send H-ACK
                    for step_2_attempt in range(1,6):
                        rpi.ser.reset_output_buffer()
                        outMessage = "H-ACK." + str(transceiver) + "." + str(step_2_attempt)
                        print("Sending \"" + str(outMessage) + "\" on transceiver " + str(transceiver))
                        sig_sent += 1
                        rpi.ser.write(outMessage.encode('utf-8'))
                        time.sleep(0.5)
                    # step 3: receive ACK
                    input_2_arr = [""]
                    for step_3_attempt in range(1,6):
                        rpi.ser.reset_input_buffer()
                        inBuffer = 0
                        inMessage = ""
                        print("Waiting for \"ACK\" on transceiver " + str(transceiver))
                        time.sleep(0.5)
                        inBuffer = rpi.ser.in_waiting
                        if (inBuffer != 0):
                            try:
                                sig_received += 1
                                inMessage = rpi.ser.read(inBuffer).decode('utf-8')
                            except Exception as e:
                                print(e)
                                input_2_arr.append("00001")
                                error += 1
                                continue
                            print(inMessage)
                            input_2_arr.append(inMessage)
                        else:
                            input_2_arr.append("00000")
                    for k in range(1,6):
                        s3_input = input_2_arr[k]
                        if (s3_input[0:3] == "ACK"):
                            handshake3 = True
                    if (handshake3):
                        print("Received: \"ACK\"")
                        print("Step 3 Complete")
                        print("Connected")
                        success += 1
                    break # break out of transceiver loop
                # iterate through the transceivers
                else:
                    for l in range(1,6):
                        time.sleep(0.5)
                # iterate through transceivers
                if (transceiver == 7):
                    transceiver = 8
                else:
                    transceiver = (transceiver + 1) % 8
                
            rpi.ser.reset_input_buffer()
            rpi.ser.reset_output_buffer()
            print("\nSuccesses: " + (str)(success) + "\n")
        # end for z in range(0,100)
        print("Successes: " + str(success) + "/" + str(z))
        print("Number of Signals Sent: " + str(sig_sent))
        print("Number of Signals Received: " + str(sig_received))
        print("Number of Signals Received with Error: " + str(error))
    # end if (rpi.ID == "follower\n")
    rpi.clean()
