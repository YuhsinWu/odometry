#!/usr/bin/env python
import socket

import serial

import json

import syslog,time,sys

import time

import rospy
from duckietown_msgs.msg import Twist2DStamped
port = '/dev/ttyACM0'

UDP_IP = "192.168.0.10"  #######change here########

UDP_PORT = 5005

sock = socket.socket(socket.AF_INET,

		     socket.SOCK_DGRAM)

sock.bind((UDP_IP,UDP_PORT))

target=[0,1, 1,1, 1,3, 0,3, 0,4, 0,3, 1,3, 1,0]
for i in range(0,15):
    target[i]=target[i]*48+23
print target
class Tracking:
    def __init__(self):
        self.node_name = rospy.get_name()   
        rospy.on_shutdown(self.custom_shutdown)
        self.pub_car_cmd = rospy.Publisher("~car_cmd", Twist2DStamped, queue_size=1)
        self.posx=0
        self.posy=0
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
            self.follow()

    def follow(self):
        cmd = Twist2DStamped()
        if self.posx<t_cen[self.index]:
            cmd.v=1
            cmd.omega=-1

    def custom_shutdown(self):
        rospy.loginfo("[%s] Shutting down..." %self.node_name)

if __name__ == '__main__':

    try:
        rospy.init_node('tracking', anonymous = False)
        Track = Tracking()

    except KeyboardInterrupt:

        ser.close()
