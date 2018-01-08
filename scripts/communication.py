#!/usr/bin/env python
import socket
import serial
import json
import syslog,time,sys
import time
from Adafruit_MotorHAT import Adafruit_MotorHAT
UDP_IP = "192.168.0.7"  #######change here########
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET,
		     socket.SOCK_DGRAM)

sock.bind((UDP_IP,UDP_PORT))

target=[22,54, 60,70, 70,140, 38,156, 24,190, 25,72, 69,67, 69,19]
direc=[1, 2, 1, 3, 1, 4, 2, 4]
turn_dir=[1, 0, 0, 1, 2, 1, 0, 2]
print target
tolrce=3
class Tracking:
    def __init__(self):
        self.motorhat = Adafruit_MotorHAT(addr= 0x60)
        self.leftMotor  = self.motorhat.getMotor(1)
        self.rightMotor = self.motorhat.getMotor(2)
        self.posx=0
        self.posy=0
        self.index=0
        self.turn_index=0
        self.communication()

    def communication(self):
        while(1):
            data,addr = sock.recvfrom(1024)

            print time.time()

            send = data

            #ard.flush()

            print "data"

            print (send)

            slist = send.split('.') 
            self.posx = int(slist[0])
            self.posy = int(slist[1].strip(','))
            print self.posx, self.posy
            if self.index<9:
                self.follow_forward()
            else:
                self.follow_backward()


    def follow_forward(self):
        print self.index/2
        if direc[self.turn_index]==1:  #forward
            print 'forward'
            d_error = self.posx-target[self.index]
            d_target = self.posy-target[self.index+1]
        elif direc[self.turn_index]==2:
              #right
            print 'right'
            d_error = -(self.posy-target[self.index+1])
            d_target = self.posx-target[self.index]
        elif direc[self.turn_index]==3: #left
            print 'left'
            d_error = self.posy-target[self.index+1]
            d_target = -(self.posx-target[self.index])
        if d_error<-tolrce:#turn right
            print 'turn right'
            self.leftMotor.setSpeed(60)
            self.rightMotor.setSpeed(50)
        elif d_error>tolrce:#turn_left
            print'turn_left'
            self.leftMotor.setSpeed(50)
            self.rightMotor.setSpeed(60)
        else:  #straight_forward
            print 'straight'
            self.leftMotor.setSpeed(50)
            self.rightMotor.setSpeed(50)
        if d_target>-7: #reach goal
            if urn_dir[self.turn_index]==1: #turn_right_90
                print 'turn_right_90'
                self.leftMotor.setSpeed(150)
                self.rightMotor.setSpeed(0)
                self.leftMotor.run(Adafruit_MotorHAT.FORWARD)
                self.rightMotor.run(Adafruit_MotorHAT.FORWARD)
                time.sleep(0.35)
            elif turn_dir[self.turn_index]==0: #turn_left_90
                print 'turn_left_90'
                self.leftMotor.setSpeed(0)
                self.rightMotor.setSpeed(150)
                self.leftMotor.run(Adafruit_MotorHAT.FORWARD)
                self.rightMotor.run(Adafruit_MotorHAT.FORWARD)
                time.sleep(0.4)
            else:#reach final goal
                print 'finish forward part'
            self.turn_index+=1
            self.index+=2
        self.leftMotor.run(Adafruit_MotorHAT.FORWARD)
        self.rightMotor.run(Adafruit_MotorHAT.FORWARD)
        time.sleep(0.05)
        self.leftMotor.setSpeed(0)
        self.rightMotor.setSpeed(0)
        self.leftMotor.run(Adafruit_MotorHAT.FORWARD)
        self.rightMotor.run(Adafruit_MotorHAT.FORWARD)
    def follow_backward(self):
        print self.index/2
        if direc[self.turn_index]==4:  #backward
            print 'backward'
            d_error = self.posx-target[self.index]
            d_target = -(self.posy-target[self.index+1])
        elif direc[self.turn_index]==2:
              #right
            print 'right'
            d_error = -(self.posy-target[self.index+1])
            d_target = self.posx-target[self.index]
        elif direc[self.turn_index]==3: #left
            print 'left'
            d_error = self.posy-target[self.index+1]
            d_target = -(self.posx-target[self.index])
        if d_error<-tolrce:#turn right
            print 'turn right'
            self.leftMotor.setSpeed(60)
            self.rightMotor.setSpeed(50)
        elif d_error>tolrce:#turn_left
            print'turn_left'
            self.leftMotor.setSpeed(50)
            self.rightMotor.setSpeed(60)
        else:  #straight_forward
            print 'straight'
            self.leftMotor.setSpeed(50)
            self.rightMotor.setSpeed(50)
        if d_target>-7: #reach goal
            if urn_dir[self.turn_index]==1: #turn_right_90
                print 'turn_right_90'
                self.leftMotor.setSpeed(150)
                self.rightMotor.setSpeed(0)
                self.leftMotor.run(Adafruit_MotorHAT.BACKWARD)
                self.rightMotor.run(Adafruit_MotorHAT.BACKWARD)
                time.sleep(0.35)
            elif turn_dir[self.turn_index]==0: #turn_left_90
                print 'turn_left_90'
                self.leftMotor.setSpeed(0)
                self.rightMotor.setSpeed(150)
                self.leftMotor.run(Adafruit_MotorHAT.BACKWARD)
                self.rightMotor.run(Adafruit_MotorHAT.BACKWARD)
                time.sleep(0.38)
            else:#reach final goal
                print 'finish'
                self.__del__
            self.turn_index+=1
            self.index+=2
        self.leftMotor.run(Adafruit_MotorHAT.BACKWARD)
        self.rightMotor.run(Adafruit_MotorHAT.BACKWARD)
        time.sleep(0.05)
        self.leftMotor.setSpeed(0)
        self.rightMotor.setSpeed(0)
        self.leftMotor.run(Adafruit_MotorHAT.BACKWARD)
        self.rightMotor.run(Adafruit_MotorHAT.BACKWARD)
    def __del__(self):
        print 'died'
        self.leftMotor.setSpeed(0)
        self.rightMotor.setSpeed(0)
        self.leftMotor.run(Adafruit_MotorHAT.FORWARD)
        self.rightMotor.run(Adafruit_MotorHAT.FORWARD)

if __name__ == '__main__':

    try:
        Track = Tracking()

    except KeyboardInterrupt:
        print 'died'
