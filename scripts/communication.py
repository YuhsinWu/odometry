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

target=[0,0, 0,1, 1,1, 1,3, 0,3, 0,4, 0,3, 1,3, 1,0]
turn_dir=[1,0,0,1]
for i in range(0,17):
    target[i]=target[i]*48+23
print target
tolrce=5
class Tracking:
    def __init__(self):
        self.motorhat = Adafruit_MotorHAT(addr= 0x60)
        self.leftMotor  = self.motorhat.getMotor(1)
        self.rightMotor = self.motorhat.getMotor(2)
        self.posx=0
        self.posy=0
        self.index=2
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
            if self.index<=11:
                self.follow_forward()
            else:
                self.follow_backward()


    def follow_forward(self):
        dir_x = target[self.index] - target[self.index-2]
        dir_y = target[self.index+1] - target[self.index-1]
        if dir_x==0:  #front
            print 'front'
            d_error = self.posx-target[self.index]
            d_target = self.posy-target[self.index+1]
        elif dir_y==0:
            if dir_x>0:  #right
                print 'right'
                d_error = -(self.posy-target[self.index+1])
                d_target = self.posx-target[self.index]
            elif dir_x<0: #left
                print 'left'
                d_error = self.posy-target[self.index+1]
                d_target = self.posx-target[self.index]
        if d_error<-tolrce:#turn right
            print 'turn right'
            self.leftMotor.setSpeed(60)
            self.rightMotor.setSpeed(40)
        elif d_error>tolrce:#turn_left
            print'turn_left'
            self.leftMotor.setSpeed(40)
            self.rightMotor.setSpeed(60)
        else:  #straight_forward
            print 'straight_forward'
            self.leftMotor.setSpeed(50)
            self.rightMotor.setSpeed(50)
        if abs(d_target)<tolrce: #reach goal
            if turn_dir[self.turn_index]==1: #turn_right_90
                print 'turn_right_90'
                self.leftMotor.setSpeed(60)
                self.rightMotor.setSpeed(40)
                self.leftMotor.run(Adafruit_MotorHAT.FORWARD)
                self.rightMotor.run(Adafruit_MotorHAT.FORWARD)
                time.sleep(0.25)
            else: #turn_left_90
                print 'turn_left_90'
                self.leftMotor.setSpeed(40)
                self.rightMotor.setSpeed(60)
                self.leftMotor.run(Adafruit_MotorHAT.FORWARD)
                self.rightMotor.run(Adafruit_MotorHAT.FORWARD)
                time.sleep(0.25)
            self.turn_index+=1
            self.index+=2
        self.leftMotor.run(Adafruit_MotorHAT.FORWARD)
        self.rightMotor.run(Adafruit_MotorHAT.FORWARD)
        time.sleep(0.1)
        self.leftMotor.setSpeed(0)
        self.rightMotor.setSpeed(0)
        self.leftMotor.run(Adafruit_MotorHAT.FORWARD)
        self.rightMotor.run(Adafruit_MotorHAT.FORWARD)
    def follow_backward(self):
        pwml=0
        pwmr=0
        self.leftMotor.setSpeed(pwml)
        self.rightMotor.setSpeed(pwmr)
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
