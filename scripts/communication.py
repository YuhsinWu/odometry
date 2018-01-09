#!/usr/bin/env python
import socket
import serial
import json
import syslog,time,sys
import time
import math
from Adafruit_MotorHAT import Adafruit_MotorHAT
UDP_IP = "192.168.0.7"  #######change here########
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET,
		     socket.SOCK_DGRAM)

sock.bind((UDP_IP,UDP_PORT))
#target coordinate
target=[22,50, 60,55 ,68,107, 68,140, 42,150, 24,190, 25,72, 69,67, 69,19]
#1:toward front
#2:toward right
#3:toward left
#4:toward back
direc=[1, 2, 1 , 1, 3, 1, 4, 2, 4]
#0:turn left 90
#1:turn right 90
#2:don't turn
#3:the end
turn_dir=[1, 0, 2, 0, 1, 2, 1, 0, 3]
old_posx=0
old_posy=0
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
        self.leftMotor.setSpeed(50)
        self.rightMotor.setSpeed(50)
        self.leftMotor.run(Adafruit_MotorHAT.BACKWARD)
        self.rightMotor.run(Adafruit_MotorHAT.FORWARD)
        time.sleep(0.78/3)
        self.leftMotor.setSpeed(0)
        self.rightMotor.setSpeed(0)
        self.leftMotor.run(Adafruit_MotorHAT.FORWARD)
        self.rightMotor.run(Adafruit_MotorHAT.FORWARD)
        

        self.communication()

    def communication(self):
        while(1):
            data,addr = sock.recvfrom(1024)

            print time.time()

            send = data

            #ard.flush()

            print (send)

            slist = send.split('.') 
            self.posx = int(slist[0])
            self.posy = int(slist[1].strip(','))
            print self.posx, self.posy
            if self.index<11:
                self.follow_forward()
            else:
                self.follow_backward()


    def follow_forward(self):
        print self.index/2
        if direc[self.turn_index]==1:  #front
            print 'front'
            d_error = self.posx-target[self.index]
            d_target = self.posy-target[self.index+1]
        elif direc[self.turn_index]==2:#right
            print 'right'
            d_error = -(self.posy-target[self.index+1])
            d_target = self.posx-target[self.index]
        elif direc[self.turn_index]==3: #left
            print 'left'
            d_error = self.posy-target[self.index+1]
            d_target = -(self.posx-target[self.index])
        if d_error<-tolrce:#if error is negative, turn right
            print 'turn right'
            self.leftMotor.setSpeed(60)
            self.rightMotor.setSpeed(50)
        elif d_error>tolrce:#if error is positive, turn_left
            print'turn_left'
            self.leftMotor.setSpeed(50)
            self.rightMotor.setSpeed(60)
        else:  #straight_forward
            print 'straight'
            self.leftMotor.setSpeed(50)
            self.rightMotor.setSpeed(50)
        if d_target>-7: #reach goal
        #---------------------angle control----------------------
            dir_x=self.posx-old_posx
            dir_y=self,posy-old_posy
            if direc[self.turn_index]==1:  #front
                angle_error=(math.pi/2)-math.atan(dir_y/dir_x)    
            elif direc[self.turn_index]==2:#right
                angle_error= -math.atan(dir_y/dir_x)
            elif direc[self.turn_index]==3: #left
                angle_error=(math.pi)-math.atan(dir_y/dir_x)
            print angle_error    
            if angle_error>math.pi/18:
                self.leftMotor.setSpeed(50)
                self.rightMotor.setSpeed(50)
                self.leftMotor.run(Adafruit_MotorHAT.BACKWARD)
                self.rightMotor.run(Adafruit_MotorHAT.FORWARD)
                time.sleep(0.78*angle_error/(math.pi/2))
            elif angle_error<-math.pi/18:
                self.leftMotor.setSpeed(50)
                self.rightMotor.setSpeed(50)
                self.leftMotor.run(Adafruit_MotorHAT.FORWARD)
                self.rightMotor.run(Adafruit_MotorHAT.BACKWARD)
                time.sleep(0.8*angle_error/(math.pi/2))    
        #---------------------------------------------------------    
            if turn_dir[self.turn_index]==1: #turn_right_90
                print '---------turn_right_90-----------'
                self.leftMotor.setSpeed(150)
                self.rightMotor.setSpeed(0)
                self.leftMotor.run(Adafruit_MotorHAT.FORWARD)
                self.rightMotor.run(Adafruit_MotorHAT.FORWARD)
                time.sleep(0.35)
            elif turn_dir[self.turn_index]==0: #turn_left_90
                print '---------turn_left_90------------'
                self.leftMotor.setSpeed(0)
                self.rightMotor.setSpeed(150)
                self.leftMotor.run(Adafruit_MotorHAT.FORWARD)
                self.rightMotor.run(Adafruit_MotorHAT.FORWARD)
                time.sleep(0.38)
            else:#reach final goal
                print '-----------no turn---------------'
            self.turn_index+=1
            self.index+=2
        self.leftMotor.run(Adafruit_MotorHAT.FORWARD)
        self.rightMotor.run(Adafruit_MotorHAT.FORWARD)
        time.sleep(0.05)
        self.leftMotor.setSpeed(0)
        self.rightMotor.setSpeed(0)
        self.leftMotor.run(Adafruit_MotorHAT.FORWARD)
        self.rightMotor.run(Adafruit_MotorHAT.FORWARD)
        old_posx=self.posx
        old_posy=self.posy
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
            #---------------------angle control----------------------
            dir_x=self.posx-old_posx
            dir_y=self,posy-old_posy
            if direc[self.turn_index]==4:  
                angle_error=(math.pi*3/2)-math.atan(dir_y/dir_x)    
            elif direc[self.turn_index]==2:#right
                angle_error= -math.atan(dir_y/dir_x)
            elif direc[self.turn_index]==3: #left
                angle_error=(math.pi)-math.atan(dir_y/dir_x)
            print angle_error    
            if angle_error>math.pi/18:
                self.leftMotor.setSpeed(50)
                self.rightMotor.setSpeed(50)
                self.leftMotor.run(Adafruit_MotorHAT.BACKWARD)
                self.rightMotor.run(Adafruit_MotorHAT.FORWARD)
                time.sleep(0.78*angle_error/(math.pi/2))
            elif angle_error<-math.pi/18:
                self.leftMotor.setSpeed(50)
                self.rightMotor.setSpeed(50)
                self.leftMotor.run(Adafruit_MotorHAT.FORWARD)
                self.rightMotor.run(Adafruit_MotorHAT.BACKWARD)
                time.sleep(0.8*angle_error/(math.pi/2))    
        #---------------------------------------------------------    
            
            if turn_dir[self.turn_index]==1: #turn_right_90
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
            elif turn_dir[self.turn_index]==3:#reach final goal
                print 'the end'
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
