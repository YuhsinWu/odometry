#!/usr/bin/env python
import rospy

from std_msgs.msg import Float64MultiArray
from duckietown_msgs.msg import Twist2DStamped

target=[0,0, 0,1, 1,1, 1,3, 0,3, 0,4, 0,3, 1,3, 1,0]
turn_dir=[1,0,0,1]
for i in range(0,17):
	target[i]=target[i]*48+23

tolrce=5

class wheelOdometry(object):
	def __init__(self):
		self.node_name = rospy.get_name()
		self.posx = 0 # robot position x in meter
		self.posy = 0 # robot position y in meter
		self.yaw = 0 # robot pose theta in radian
		self.index=2
		self.turn_index=0
		self.sub_pose = rospy.Subscriber("/serial_node/pose", Float64MultiArray, self.cbPose)
		self.pub_car_cmd = rospy.Publisher("~car_cmd", Twist2DStamped, queue_size=1)
		
		rospy.on_shutdown(self.custom_shutdown) # shutdown method
		rospy.loginfo("[%s] Initialized " %self.node_name)
		self.now = rospy.get_time() # start

	def custom_shutdown(self):
		rospy.loginfo("[%s] Shutting down..." %self.node_name)
		cmd = Twist2DStamped()
		cmd.v=0
		cmd.omega=0
		self.pub_car_cmd.publish(cmd)

	def cbPose(self, msg):
		self.posx = msg.data[0]*100
		self.posy = msg.data[1]*100
		self.yaw = msg.data[2]
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
			d_error = self.posx-target[self.index]
			d_target = self.posy-target[self.index+1]
		elif dir_y==0:
			if dir_x>0:  #right
				d_error = -(self.posy-target[self.index+1])
				d_target = self.posx-target[self.index]
			elif dir_x<0: #left
				d_error = self.posx-target[self.index]
				d_target = self.posy-target[self.index+1]
		if d_error<-tolrce:#turn right
			cmd.v= 0.05
			cmd.omega=-0.5
		elif d_error>tolrce:#turn_left
			cmd.v=0.05
			cmd.omega=0.5
		else:  #straight_forward
			cmd.v=0.05
			cmd.omega=0
		if abs(d_target)<tolrce:
			if turn_dir[self.turn_index]==0: #turn_right_90
				cmd.v=0.05
				cmd.omega=-3.14
			else: #turn_left_90
				cmd.v=0.05
				cmd.omega=3.14
			self.turn_index+=1
			self.index+=2

		self.pub_car_cmd.publish(cmd)

	def follow_backward(self):
		cmd.v=-0.05
		cmd.omega=0
		self.pub_car_cmd.publish(cmd)
if __name__ == "__main__":
	rospy.init_node("odometry", anonymous = False)
	odometry_node = wheelOdometry()
	rospy.spin()
