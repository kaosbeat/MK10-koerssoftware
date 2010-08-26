#!/usr/bin/env python
# encoding: utf-8
"""
getpos.py

Created by Kasper Jordaens & Lode Nachtergaele on 2010-03-23.
Copyright (c) 2010 VRT__. All rights reserved.
"""

import sys
import os
import urllib2
import urllib
import simplejson
import time
import random
from gislib import getDistance
from bp_latlngdata import latlngdata
from distancedatabp import distancedata
from bp_data import data

def getclosestpoint (curpos,lastpos):
	for pos in range(len(latlngdata)-1):
		#~ savedpos = pos # iterate only over future positions
		#~ pos = savedpos + pos # iterate only over future positions
		pathpos =  (latlngdata[pos+lastpos][0], latlngdata[pos+lastpos][1])
		dist = getDistance(pathpos,curpos)
		pathpos =  (latlngdata[pos+lastpos+1][0], latlngdata[pos+lastpos+1][1])
		nextdist = getDistance(pathpos,curpos)
		if nextdist >= dist:
			break
		#~ print dist
		#~ print pos
		#~ savedpos = pos # iterate only over future positions
	return (sum(distancedata[0:pos+lastpos]),pos+lastpos)
		

def main():
	i=0
	position = {}
	position['device_label'] = "pulsar.py"
	position['device_key'] = 666
	position['timestamp'] = 1267351872468
	position['latitude'] = 51.04388
	position['longitude'] = 3.80218
	position['altitude'] = 50
	position['speed'] = str(random.randint(30,70)/3.6)
	position['heading'] = 200
	position['distance'] = 0.0
	lastpos = 0
	while True :
		position['timestamp'] = position['timestamp'] + 5
		#~ position['altitude'] = str(random.randint(40,50))
		position['speed'] = str(random.randint(30,70)/3.6)
		position['latitude'] = float(data[3*i+0]) + (random.random()  / 10000)
		position['longitude'] = float(data[3*i+1]) +(random.random()  / 10000)
		position['altitude'] = float(data[3*i+2]) + (random.random()  / 10000)
		#~ print ((random.rand(1,99) +2) / 1000)
		
		curpos = (position['latitude'], position['longitude'])
		curdist,lastpos = getclosestpoint(curpos,lastpos)
		#~ print curdist
		position['distance'] = float(int(curdist)/100)/10
		#~ print position['curdist']
		if i == len(latlngdata) -1:
			i=0
		else:
			i = i + 1
		jsondata = {'json': position}
		form_data = urllib.urlencode(position)
		print form_data
		for tries in range(3):
			try:
			    
			    #this function runs on appengine and and reads in all the positions and puts them out to the realtime map
				result = urllib2.urlopen(url = 'http://meulestedekoers.appspot.com/updateRealPos',
							data = form_data)
				break
			except:
				pass
			time.sleep(1)
		time.sleep(5)
		
if __name__ == '__main__':
	main()