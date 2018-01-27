#!/usr/bin/env python
import RPi.GPIO as io
import Adafruit_MCP3008
import time
import cPickle as pickle
from valuesnpins import *
from readsensor import *

io.setmode(io.BCM)
io.setwarnings(False)

'''
def motor():
    io.setmode(io.BCM)
    io.setwarnings(False)
    for i in range(4):
	io.setup(motordir[i],io.OUT)
	io.setup(motorpwm[i],io.OUT)
	motorin[i] = io.PWM(motorpwm[i],90)
	motorin[i].start(0)
	motorin[i].ChangeDutyCycle(0)

def setmotor(number,pwmvalue,d):
    io.output(motordir[number],d)
    motorin[number].ChangeDutyCycle(pwmvalue)
def rotate(i):
        if i>0:
                setmotor(0,sp[0],1)
                setmotor(1,sp[1],1)
                setmotor(2,sp[2],0)
                setmotor(3,sp[3],0)
        else :
                setmotor(0,sp[0],0)
                setmotor(1,sp[1],0)
                setmotor(2,sp[2],1)
                setmotor(3,sp[3],1)
def stop():
	setmotor(0,0,0)
	setmotor(1,0,0)
	setmotor(2,0,0)
	setmotor(3,0,0)
'''
def calibrate():
	print('Reading Front values, press Ctrl-C to quit...')
	print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*range(8)))
	print('-' * 57)
	#rotate()
	x=time.time()

	'''u=1'''

	# 10 sec take readings on white
		# find max min range
	print "Take readings on white in 2 seconds"
	time.sleep(2)
	while True:
		for k in range(4):
			read_sensor(k)
			for i in range(8):
				if values[k][i] <= mini[k][i]:
					mini[k][i] = values[k][i]
				if values[k][i] > maxi[k][i]:
					maxi[k][i] = values[k][i]
			wmax[k]=max(maxi[k])
			wmin[k]=min(mini[k])	
		time.sleep(0.1)
	# Print the ADC values.
	#print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values))
		if time.time()-x >10:
			break
	
	# stop
	# blink led
	io.setup(led,io.output)
	io.output(led,1)
	time.sleep(0.5)
	io.output(led,0)
	# wait for 2 sec
	print "Take readings on green in 2 seconds"
	time.sleep(2)
	# 10 sec take readings on green
		# find max min range
	x=time.time()
	while True:
		for k in range(4):
			read_sensor(k)
			for i in range(8):
				if values[k][i] <= mini[k][i]:
					mini[k][i] = values[k][i]
				if values[k][i] > maxi[k][i]:
					maxi[k][i] = values[k][i]
			gmax[k]=max(maxi[k])
			gmin[k]=min(mini[k])
		time.sleep(0.1)
	# Print the ADC values.
	#print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values))
		if time.time()-x >10:
			break

	# save gmax, calculate diff
	for k in range(4):
		raingg[k]=wmax[k]-gmin[k]
		diff[k]=wmin[k]-gmax[k]
		diff[k]=diff[k]+(diff[k]*0.05) #exceptable error of 5%
	
'''
	while True:
                rotate(u)
		for k in range(4):
			read_sensor(k)
			for i in range(8):
				if values[k][i] <= mini[k][i]:
					mini[k][i] = values[k][i]
				if values[k][i] > maxi[k][i]:
					maxi[k][i] = values[k][i]
				if raingg[k]<= maxi[k][i]-mini[k][i]:
					raingg[k]= maxi[k][i]-mini[k][i]
		time.sleep(0.1)
	# Print the ADC values.
	#print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values))
                if time.time()-x >5:
                        u=u*(-1)
		if time.time()-x >15:
			break
'''
	#print(mini)
	#print(maxi)
	for j in range(4):
		for i in range(8):
			avg[j][i] = (mini[j][i] + maxi[j][i]) / 2
	for i in range(4):
		print "%s - %s - %s"%(avg[i],raingg[i],diff[k])
	filer = open('avgline', "wb")
	pickle.dump(avg, filer)
	filer.close()

	filer = open('diff', "wb")
	pickle.dump(diff, filer)
	filer.close()

	filer = open('raingg', "wb")
	pickle.dump(raingg, filer)
	filer.close()

	filer = open('wmax', "wb")
	pickle.dump(wmax, filer)
	filer.close()

	filer = open('gmin', "wb")
	pickle.dump(gmin, filer)
	filer.close()

	# dump the global variables
	time.sleep(1)
calibrate()
stop()
