#!/usr/bin/env python

import sys
import rospy
from test.srv import * #package name.srv

def Go(x):
    	rospy.wait_for_service('sample')
    	try:
        	attempt_algo = rospy.ServiceProxy('sample', general) #service file used in CMakeList.txt
        	success= attempt_algo(x)#The service name used as a function
		return success.y
    	except rospy.ServiceException, e:
        	print "Service call failed: %s"%e

if __name__ == "__main__":
    	if len(sys.argv) == 2:
        	x = str(sys.argv[1])
    	else:
        	sys.exit(1)
    	print "Requesting..."
	print "Received: %s"%Go(x)
