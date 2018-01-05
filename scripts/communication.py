#!/usr/bin/env python
import socket
import serial
import json
import syslog,time,sys
import time
import rospy
from duckietown_msgs.msg import Twist2DStamped
port = '/dev/ttyACM0'
UDP_IP = "192.168.1.194"  #######change here########
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
        self.node_name = rospy.get_name()   
        rospy.on_shutdown(self.custom_shutdown)
        self.pub_car_cmd = rospy.Publisher("~car_cmd", Twist2DStamped, queue_size=1)
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
        cmd = Twist2DStamped()
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
            cmd.v= 0.05
            cmd.omega=-0.3
        elif d_error>tolrce:#turn_left
            print'turn_left'
            cmd.v=0.05
            cmd.omega=0.3
        else:  #straight_forward
            print 'straight_forward'
            cmd.v=0.05
            cmd.omega=0
        if abs(d_target)<tolrce: #reach goal
            if turn_dir[self.turn_index]==1: #turn_right_90
                print 'turn_right_90'
                cmd.v=0.05
                cmd.omega=-1.57
                self.pub_car_cmd.publish(cmd)
		rospy.sleep(0.25)
            else: #turn_left_90
                print 'turn_left_90'
                cmd.v=0.05
                cmd.omega=1.57
                self.pub_car_cmd.publish(cmd)
		rospy.sleep(0.25)
            self.turn_index+=1
            self.index+=2
        self.pub_car_cmd.publish(cmd)
        rospy.sleep(0.1)
        cmd.v=0
        cmd.omega=0
        self.pub_car_cmd.publish(cmd)
    def follow_backward(self):
        cmd = Twist2DStamped()
	cmd.v=0
	self.pub_car_cmd.publish(cmd)
	   	    
    def custom_shutdown(self):
        rospy.loginfo("[%s] Shutting down..." %self.node_name)

if __name__ == '__main__':

    try:
        rospy.init_node('tracking', anonymous = False)
        Track = Tracking()

    except KeyboardInterrupt:

        ser.close()
