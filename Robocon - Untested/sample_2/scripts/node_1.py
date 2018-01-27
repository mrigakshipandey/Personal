#!/usr/bin/env python

##################################################################
# Import Libraries
##################################################################

import rospy
import numpy as np
import re


##################################################################
# Messages ans Services used
##################################################################

from sample_2.srv import *

##################################################################
# Initializations
##################################################################

definition ={'START' :0 ,
            'RIGHT_NODE':1 ,
            'LOADING':2 ,
            'LAST' :3 ,
            'TZ1'  :4 ,
            'TZ2'  :5 ,
            'TZ3'  :6 }
pathtotake=[]
#numerical=[]
walk=[]
graph={ 'START'     :['RIGHT_NODE'],
        'RIGHT_NODE':['LOADING','START'],
        'LOADING'   :['LAST','TZ1','RIGHT_NODE'] ,
        'TZ1'       :['LOADING'],
        'LAST'      :['LOADING','TZ2'],
        'TZ2'       :['TZ3','LAST'],
        'TZ3'       :['TZ2'] }

##################################################################
# Function Definitions
##################################################################

from automove import *

def updateloc(x):
	try:
    		file = open('/home/ubuntu/catkin_ws/src/sample_2/files/loc.txt', 'r+')
		# read 1 line from the end, return the value
    		a=file.read()
		file.close()
		wordList=re.sub("[^\w]"," ",a).split()
		ab=wordList[-1]
		# print "ab= %s"%ab
		return generalResponse(ab)
	
	except IOError:
		file=open('/home/ubuntu/catkin_ws/src/sample_2/files/loc.txt', 'a+')
		file.write('\n0')
		file.close()
		return generalResponse('0')
 
def searchpath(graph,source,dest):
    explored =[]
    queue=[[source]]
    #print (queue)
    if source==dest:
        return "NO MOVEMENT"

    while queue:
        path=queue.pop(0)
        #print (path)
        node =path[-1]
        #print (node)
        if node not in explored:
            adjacent= graph[node]
            #print (adjacent)
            for adj in adjacent:
                new_path = list(path)
                new_path.append(adj)
                queue.append(new_path)
                if adj == dest:
                    return new_path

            explored.append(node)



    return "NO PATH"
def traverse(src,dest):
	
    	pathtotake = searchpath(graph,src,dest)
    	print(pathtotake)
    	faceposition=[[5,0,5,5,5,5,5],[2,5,1,5,5,5,5],[5,3,5,1,0,5,5],[5,5,3,5,5,0,5],[5,5,2,5,5,5,5],[5,5,5,2,5,5,0],[5,5,5,5,5,2,5]]
    	index = len(pathtotake)-1
    	for i in range(index):
		I=faceposition[definition[pathtotake[i]]][definition[pathtotake[i+1]]]
			if pathtotake[i+1] == 'RIGHT_NODE':
			mainfunc(I,1)
		elif (dest=='TZ1' and pathtotake[i+1]=='TZ1') or (dest=='TZ2'and pathtotake[i+1]=='TZ2') or(dest=='TZ3' and  pathtotake[i+1]=='TZ3'):
			mainfunc(I,2)
		else:
			mainfunc(I)
	updateloc(str(I))
	
    	stop()

def getsource():
	try:
    		file = open('/home/ubuntu/catkin_ws/src/sample_2/files/loc.txt', 'r+')
		# read 1 line from the end, return the value
    		a=file.read()
		file.close()
		wordList=re.sub("[^\w]"," ",a).split()
		ab=wordList[-1]
		# print "ab= %s"%ab
		return generalResponse(ab)
	
	except IOError:
		file=open('/home/ubuntu/catkin_ws/src/sample_2/files/loc.txt', 'a+')
		file.write('\n0')
		file.close()
		return generalResponse('0')
 



def handle(resp):
	print "Requested destination %s."%resp.x
	#Algo goes here
	initialfunc()

	source=getsource()
	print "I am at %s."%source
	traverse(int(source),int(resp.x)+3)
		
	
	print "location updated %s."%resp.x
    	return generalResponse("Done")

def random_result():
	rospy.init_node('node_1')
	s = rospy.Service('main_traverse', general, handle) #Service Name, CMakeList File, Call
    	
	


##################################################################
#Main Program
##################################################################

if __name__ == '__main__':
    	random_result()
	rospy.spin()
