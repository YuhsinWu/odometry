#!/usr/bin/env python
import RPi.GPIO as gpio
import sys
import readchar
from Adafruit_MotorHAT import Adafruit_MotorHAT
motorhat = Adafruit_MotorHAT(addr= 0x60)
leftMotor  = motorhat.getMotor(1)
rightMotor = motorhat.getMotor(2)
gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
#gpio.setup(7, gpio.OUT)

while True:
    leftMotor.setSpeed(0)
    rightMotor.setSpeed(0)
    leftMotor.run(Adafruit_MotorHAT.FORWARD)
    rightMotor.run(Adafruit_MotorHAT.FORWARD)
    print("Reading a char:")
    cmd = readchar.readchar()
    print cmd 
    if cmd == 'q':
        break
    elif cmd == '2':
        print 'forward'
        leftMotor.setSpeed(50)
        rightMotor.setSpeed(50)
        leftMotor.run(Adafruit_MotorHAT.FORWARD)
        rightMotor.run(Adafruit_MotorHAT.FORWARD)
    elif cmd == '8':
        print 'back'
        leftMotor.setSpeed(50)
        rightMotor.setSpeed(50)
        leftMotor.run(Adafruit_MotorHAT.BACKWARD)
        rightMotor.run(Adafruit_MotorHAT.BACKWARD)
    elif cmd == '6':
        print 'turn right'
        leftMotor.setSpeed(50)
        rightMotor.setSpeed(50)
        leftMotor.run(Adafruit_MotorHAT.FORWARD)
        rightMotor.run(Adafruit_MotorHAT.BACKWARD)
    elif cmd == '4':
        print 'turn left'
        leftMotor.setSpeed(50)
        rightMotor.setSpeed(50)
        leftMotor.run(Adafruit_MotorHAT.BACKWARD)
        rightMotor.run(Adafruit_MotorHAT.FORWARD)    






