#!/usr/bin/env python

from sample_2.srv import * #package name.srv
import rospy

def maintraversal(x):
	rospy.wait_for_service('main_traverse')
	try:
        	attempt_algo = rospy.ServiceProxy('main_traverse', general) #service file used in CMakeList.txt
        	success = attempt_algo(x) #The service name used as a function
		print "%s"%success
    	except rospy.ServiceException, e:
        	print "Service call failed: %s"%e


def loadposition(x):
	rospy.wait_for_service('load_position')
	try:
        	attempt_algo = rospy.ServiceProxy('load_position', general) #service file used in CMakeList.txt
        	success = attempt_algo(x) #The service name used as a function
		print "%s"%success
    	except rospy.ServiceException, e:
        	print "Service call failed: %s"%e

def updateloc(x):
	file = open('/home/ubuntu/catkin_ws/src/sample_2/files/loc.txt', 'a+')
    	file.seek(-1)
	file.truncate()
	file.close()
    	return generalResponse('1')


def handle(req):
    	print "Requested destination %s."%req.x
	#Algo goes here
	
	'''
	0 - start zone
	1 - tz 1
	2 - tz 2
	3 - tz 3
	4 - tz 1 throwing position
	5 - tz 2 throwing position
	6 - tz 3 throwing position

	'''
	if int(req.x)<4:
		maintraversal(req.x)
	else:
		maintraversal(str(int(req.x)-3))
		loadposition(req.x)
		updateloc(req.x)
	
    	return generalResponse("Done")

def server():
    	rospy.init_node('server')
	print "Server Ready."
    	s = rospy.Service('sample', general, handle) #Service Name, CMakeList File, Call
       	rospy.spin()

if __name__ == "__main__":
    server()


