import RPi.GPIO as io
import Adafruit_MCP3008
import time
import cPickle as pickle
import numpy as np
from valuesnpins import *
from align import *
from motion import *
from readsensor import *
################## make a new message type with one integer (face) and one float (pwm) include the message file
from sample_2.msg import *

def linekeep(face,pwm):
    	pub = rospy.Publisher('adaptive_pwm', apwm, queue_size=10)
    	rospy.init_node('line keep pub', anonymous=True)
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
	

def conditioncheck() :
	print "checking condition..."
	pos = biCalculate()
 	global node

	#getting diff
	filer = open('diff', "rb")
	diff=pickle.load(diff, filer)
	filer.close()

	for i in range (4):
		print(pos[i])
	print face

	# checking difference to know if line if present in front of face array
	if (max(values[face])-min(values[face]))>diff[face]:
		# map values and get direction & pwm
		if face==0:
		for i in range(4):
			setmotor(i,sp[i],0)
		elif face==1:
			setmotor(0,0)
			setmotor(1,1)
			setmotor(2,0)
			setmotor(3,1)
		elif face==2:
			setmotor(0,1)
			setmotor(1,1)
			setmotor(2,1)
			setmotor(3,1)
		elif face==3:
			setmotor(0,1)
			setmotor(1,0)
			setmotor(2,1)
			setmotor(3,0)

		pwm=np.interp(pos,[-3.5,3.5],[-20,20])
		linekeep(face,pwm)

		# check if any side array shows presence of white line, stop
		if ((max(values[(face+1)%2])-min(values[(face+1)%2]))>diff[(face+1)%2] or ((max(values[(face+3)%2])-min(values[(face+3)%2]))>diff[(face+3)%2]:
			node=node+1
	else: stop()
	return node
	
	'''
	if bi[face][0]==1 and bi[face][1]==1 and bi[face][2]==1 and bi[face][3]==1 and bi[face][4]==1 and bi[face][5]==1 and bi[face][6]==1 and bi[face][7]==1:
		forward()
		flag=1
	elif bi[face][3]==1 or bi[face][4]==1 :
		biCalculate()
		if (bi[(face + 2) % 4][3]==1 or bi[(face + 2) % 4][4]==1) :
			forward()
		elif bi[(face + 2) % 4][0]==1 or bi[(face + 2) % 4][1]==1 or bi[(face + 2) % 4][2]==1:
			backleft()
		elif bi[(face + 2) % 4][5]==1 or bi[(face + 2) % 4][6]==1 or bi[(face + 2) % 4][7]==1:
			backright()
		else:
			forward()

	elif bi[face][0]==1 or bi[face][1]==1 or bi[face][2]==1 :
		left()
	elif bi[face][5]==1 or bi[face][6]==1 or bi[face][7]==1 :
		right()
	else:
		print "stop case"
		stop()
	global flag
	
	if flag==1:
		print "check"
		if (bi[(face+3)%4][0]==1 or bi[(face+3)%4][1]==1 or bi[(face+3)%4][2]==1 or bi[(face+3)%4][3]==1 or bi[(face+3)%4][4]==1 or bi[(face+3)%4][5]==1 or bi[(face+3)%4][6]==1 or bi[(face+3)%4][7]==1) and ( bi[(face+1)%4][0]==1 or bi[(face+1)%4][1]==1 or bi[(face+1)%4][2]==1 or bi[(face+1)%4][3]==1 or bi[(face+1)%4][4]==1 or bi[(face+1)%4][5]==1 or bi[(face+1)%4][6]==1 or bi[(face+1)%4][7]==1 ) :
			node = node + 1
			flag=0
		
	return node
	'''
	
def specialconditioncheck() :
	print "checking condition..."
	pos = biCalculate()
	global node

	#getting diff
	filer = open('diff', "rb")
	diff=pickle.load(diff, filer)
	filer.close()

	for i in range(4):
		print(pos[i])
	print face

	# checking difference to know if line if present in front of face array
	if (max(values[face])-min(values[face]))<diff[face]:
		# map values and get direction & pwm
		if face==0:
		for i in range(4):
			setmotor(i,sp[i],0)
		elif face==1:
			setmotor(0,0)
			setmotor(1,1)
			setmotor(2,0)
			setmotor(3,1)
		elif face==2:
			setmotor(0,1)
			setmotor(1,1)
			setmotor(2,1)
			setmotor(3,1)
		elif face==3:
			setmotor(0,1)
			setmotor(1,0)
			setmotor(2,1)
			setmotor(3,0)

		pwm=np.interp(pos,[-3.5,3.5],[-20,20])
		linekeep(face,pwm)

		# check if "right" side array shows presence of white line but left side does not, stop, node increament
		if ((max(values[(face+1)%2])-min(values[(face+1)%2]))>diff[(face+1)%2] or ((max(values[(face+3)%2])-min(values[(face+3)%2]))<diff[(face+3)%2]:
			node=node+1
	else: stop
	return node
	'''
	if bi[face][3]==1 or bi[face][4]==1 :
		biCalculate() # for real time maybe
		if (bi[(face + 2) % 4][3]==1 or bi[(face + 2) % 4][4]==1) :
			forward()
		elif bi[(face + 2) % 4][0]==1 or bi[(face + 2) % 4][1]==1 or bi[(face + 2) % 4][2]==1:
			backleft()
		elif bi[(face + 2) % 4][5]==1 or bi[(face + 2) % 4][6]==1 or bi[(face + 2) % 4][7]==1:
			backright()

	elif bi[face][0]==1 or bi[face][1]==1 or bi[face][2]==1 :
		left()
	elif bi[face][5]==1 or bi[face][6]==1 or bi[face][7]==1 :
		right()
	else:
		while True:
			forward()
			print ("SPECIAL")
			print (face)
			biCalculate()
			if (bi[(face+1)%4][2]==1 or bi[(face+1)%4][3]==1 or bi[(face+1)%4][4]==1 or bi[(face+1)%4][5]==1 ):
				print("IFK ANDR")
				node=node+1
				break
		
	return node
	'''
	
def initialfunc():
    motor()
    global avg
    filer = open('avgline', "rb")
    avg = pickle.load(filer)
    for i in range(4):
            print avg[i]
    filer.close()

def mainfunc(f,special=0):
        global node,face
        node=0
        face=f
        if special==0:
            while conditioncheck() == 0:
                pass
        elif special==2 :
            while conditioncheck()==0:
                pass
            align(face)
            #time.sleep(2)
                
        else:
                while specialconditioncheck() == 0:
                        pass    
        
"""
initialfunc()
while True:
	conditioncheck()
	#time.sleep(0.1)
"""
