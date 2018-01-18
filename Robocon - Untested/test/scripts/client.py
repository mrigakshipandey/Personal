#!/usr/bin/env python

import sys
import rospy
from std_msgs.msg import String

def Go(x):
    	pub = rospy.Publisher('chatter', String, queue_size=10)
    	rospy.init_node('talker', anonymous=True)
    
    	try:
        	rospy.loginfo(hello_str)
        	pub.publish(hello_str)
  	
	except rospy.ServiceException, e:
        	print "Service call failed: %s"%e

if __name__ == "__main__":
    	if len(sys.argv) == 2:
        	x = str(sys.argv[1])
    	else:
        	sys.exit(1)
    	print "Requesting..."
