#!/usr/bin/env python

##################################################################
# Import Libraries
##################################################################

import rospy
import numpy as np
import RPi.GPIO as io
import Adafruit_MCP3008
import time
import cPickle as pickle
from valuesnpins import *
from align import *
from motion import *
from readsensor import *


##################################################################
# Messages ans Services used
##################################################################

from sample_2.srv import *
from sample_2.srv import *

##################################################################
# Function Definitions
##################################################################

def reached_manual()
	print "Moving towards manual..."
	if np.random.rand(1)>0.7:
		return 1
		
	else:
		return 0
	

def linekeep(face,pwm):
    	pub = rospy.Publisher('adaptive_pwm', apwm, queue_size=10)
    	rospy.init_node('line keep pub 2', anonymous=True)
	my_msg=apwm()
	my_msg.face=face
	my_msg.pwm=pwm
    	rospy.loginfo(my_msg)
        pub.publish(my_msg)

def biCalculate():
	for k in range(4):
		read_sensor(k)
		print values[k]
		print "determining position.."
		v = values[k]
		ma = max(v)
		gmin = min(v)
		d = ma - gmin
		p = v.index(ma)
		if not p==0 and not p==7:
			if v[p-1] <= v[p+1]:
				mi = v[p-1]
			else:
				mi = v[p+1]
			d = ma - mi
			n = v[p+1] - v[p-1]
			r = (n*1.0)/(d*2.0)
			pos[k] = p + r -3.5
		elif p == 0:
			n = d - v[p] + v[p+1]
			r = (n*1.0)/(d*2.0)
			pos[k] = p + r -3.5
		elif p == 7:
			n = d - v[p-1] + v[p]
			r = (n*1.0)/(d*2.0)
			pos[k] = p + r -3.5
	
	return pos

def handle(resp):
	print "Traversing..."
	#rewrite
	# biCalculate to find pos[]
	
	# face is 2
	setmotor(0,1)
	setmotor(1,1)
	setmotor(2,1)
	setmotor(3,1)
		
	# linekeep
	
	while (not reached_manual()):
		pos=biCalculate()
		pwm=np.interp(pos,[-3.5,3.5],[-20,20])
		linekeep(2,pwm)
	stop()
	return generalResponse('1')

def random_result():
	rospy.init_node('node_2')
	s = rospy.Service('load_position', general, handle) #Service Name, CMakeList File, Call
    	
	


##################################################################
#Main Program
##################################################################

if __name__ == '__main__':
    	random_result()
	rospy.spin()
