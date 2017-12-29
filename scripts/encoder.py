#!/usr/bin/python

import rospy


from std_msgs.msg import Float64MultiArray
from std_msgs.msg import Int16


class wheelOdometry(object):
	def __init__(self):
		self.node_name = rospy.get_name()
		# subsrciber
		self.sub_encoderL = rospy.Subscriber("/serial_node/encoderL", Int16, self.cbEncoderL)
		self.sub_encoderR = rospy.Subscriber("/serial_node/encoderR", Int16, self.cbEncoderR)
		rospy.on_shutdown(self.custom_shutdown) # shutdown method
		rospy.loginfo("[%s] Initialized " %self.node_name)
		self.now = rospy.get_time() # start

	def custom_shutdown(self):
		rospy.loginfo("[%s] Shutting down..." %self.node_name)


	def cbEncoderL(self, msg):
		print msg.data
	def cbEncoderR(self, msg):
		print msg.data

if __name__ == "__main__":
	rospy.init_node("encoder", anonymous = False)
	odometry_node = wheelOdometry()
	rospy.spin()
