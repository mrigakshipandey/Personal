#!/usr/bin/env python

from test.srv import * #package name.srv
import rospy

import RPi.GPIO as io
import Adafruit_MCP3008
import time


def handle(req):
	# The test algo goes here
		#Initializing the variables
	pins=[52,46,48,51]
	temp_pwm=[50,50,50,50]
	m11 =3
	m21 =11
	m31 =8
	m41 =5
	m12 =4
	m22 =12
	m32 =9
	m42 =6
	pwm=[50,50,50,50]
	thresh=800
	spd=50
	kp=3

			#These variables were not initialized in the original program (caution)
	flag=[False,False,False,False]
	count=[0,0,0,0]
	vals = [[False for _ in range(1000)]for _1 in range(4)]
	startt=0
	diff=0
	prev=[0,0,0,0]

		#Setting up the gpio
	io.setmode(io.BCM)
    	io.setwarnings(False)

	io.setup(m11,io.OUT)
	io.setup(m21,io.OUT)
	io.setup(m31,io.OUT)
	io.setup(m41,io.OUT)
	io.setup(m12,io.OUT)
	io.setup(m22,io.OUT)
	io.setup(m32,io.OUT)
	io.setup(m42,io.OUT)
	for i in range(4):
		io.setup(pin[i],io.IN)
	
	io.output(m11,io.LOW)
	io.output(m21,io.LOW)
	io.output(m31,io.LOW)
	io.output(m41,io.LOW)
	
	pm12=io.PWM(m12,90)
	pm22=io.PWM(m22,90)
	pm32=io.PWM(m32,90)
	pm42=io.PWM(m42,90)

	pm12.start(0)
	pm22.start(0)
	pm32.start(0)
	pm42.start(0)

	pm12.ChangeDutyCycle(0)
	pm22.ChangeDutyCycle(0)
	pm32.ChangeDutyCycle(0)
	pm42.ChangeDutyCycle(0)

	while(True):
		for _ in range(4):
			flag[_]=False
			count[_]=0

		for _ in range(1000):
			for _1 range(4):
				vals[_][_1]=io.input(pins[_1])
		
		for _ in range(1000):
			for _1 range(4):
				if not vals[_][_1]== flag[_1]:
					if vals[_][_1]==True:
						count[_1]+=1
					vals[_][_1]= flag[_1]
		for i in range(4):
    			prev[i]=temp_pwm[i]-pwm[i]

		for i in range(4):
      			factor = int((count[i] -40)/kp)
      			temp_pwm[i] = pwm[i] - factor + prev[i]
      			print "%s-%s=%s|	"%factor%prev[i]%temp_pwm[i]
      			print " "

		pm12.ChangeDutyCycle(temp_pwm[0])
		pm22.ChangeDutyCycle(temp_pwm[1])
		pm32.ChangeDutyCycle(temp_pwm[2])
		pm42.ChangeDutyCycle(temp_pwm[3])
		
		print "------------"

	#c=str(int(req.x) + 3) #The result
	print "Returning %s"%1
    	return generalResponse(1)

def add_two_ints_server():
    	rospy.init_node('server')
    	s = rospy.Service('sample', general, handle) #Service Name, CMakeList File, Call
    	print "Server Ready."
    	rospy.spin()

if __name__ == "__main__":
    	add_two_ints_server()


