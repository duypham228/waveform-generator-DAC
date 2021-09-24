import adafruit_mcp4725
import busio
import board
import numpy as np
import time
from time import sleep
import sys
import RPi.GPIO as GPIO
from signal import pause
import math

# VCC = 5

GPIO.setup(21,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

i2c = busio.I2C(board.SCL, board.SDA)

dac = adafruit_mcp4725.MCP4725(i2c)

dac.value = 65535

dac.raw_value = 4095
dac.normalized_value = 1.0



def square_wave(maxVolDig, half_period):
    while True and GPIO.input(21) != GPIO.HIGH:
        #print("Low")
        dac.raw_value=0
        sleep(half_period)
        #print("High")
        dac.raw_value=int(maxVolDig)
        sleep(half_period)

def triangle_wave(maxVolDig, half_period):
    while True and GPIO.input(21) != GPIO.HIGH:
        #print('Going up')
        for i in np.arange(0, half_period, 0.001):
            #start = time.time()
            dac.raw_value = int(maxVolDig*i/half_period)
            #end = time.time()
            #print(end-start)
            sleep(0.0003)
            #print(int(maxVolDig*i/half_period), " ", i, " ", half_period)
        #print("first half done")
        #sleep(half_period)
        #print('Going down')
        for i in np.arange(half_period, 0, -0.001):
            dac.raw_value = int(maxVolDig*i/half_period)
            sleep(0.0003)
        #sleep(half_period)

def sin_wave(maxVolDig, freq):
    t = 0.0
    tStep = 0.001
    while True and GPIO.input(21) != GPIO.HIGH:
        #start = time.time()
        voltage = maxVolDig*(1.0+0.5*math.sin(6.2832*t*freq))
        #print(int(voltage))
        dac.raw_value = int(voltage)
        t+= tStep
        #end = time.time()
        #print(end-start)
        sleep(0.0003)
        
def function(freq, maxVol):
    period = 1/freq
    half_period = period / 2
    maxVolDig = (maxVol / 5) * (4095)
    return half_period, maxVolDig
    
def main(channel):
    

    maxVol = float(input('Enter your maximum voltage up to 5V: '))
    while maxVol > 5:
        print("Invalid value")
        maxVol = float(input('Enter your maximum voltage up to 5V: '))
        
    freq = float(input('Enter your frequency up to 20Hz: '))
    while freq > 20:
        print('Invalid value')
        freq = float(input('Enter your frequency up to 20Hz: '))
        
    shape = int(input('Square Wave is 0, Triangle Wave is 1, Sin Wave is 2: '))
    while (shape != 0) and (shape != 1) and (shape != 2):
        print('Invalid value')
        shape = int(input('Square Wave is 0, Triangle Wave is 1, Sin Wave is 2'))
        
    half_period, maxVolDig = function(freq, maxVol)
    
    if shape == 0:
        square_wave(maxVolDig, half_period)
    if shape == 1:
        triangle_wave(maxVolDig, half_period)
    if shape == 2:
        sin_wave(maxVolDig,freq)
    
            
                
GPIO.add_event_detect(21, GPIO.RISING, callback = main)
pause()



"""
while True:
    #square_wave(maxVolDig, half_period)
    #triangle_wave(maxVolDig, half_period)
    sin_wave(maxVolDig,freq)
    
    """

        
        
    
    