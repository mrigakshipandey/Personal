#!/usr/bin/env python

import sys
import rospy
from sample_2.srv import * #package name.srv

def client(x):
    	rospy.wait_for_service('sample')
    	try:
        	attempt_algo = rospy.ServiceProxy('sample', general) #service file used in CMakeList.txt
        	success = attempt_algo(str(x)) #The service name used as a function
		print "%s"%success
    	except rospy.ServiceException, e:
        	print "Service call failed: %s"%e

if __name__ == "__main__":
    	if len(sys.argv) == 2:
        	x = int(sys.argv[1])
    	else:
        	sys.exit(1)
    	print "Requesting destination %s"%x
	client(x)
