#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import memcache
from google.appengine.ext.db import GqlQuery
import logging
import os
from django.utils import simplejson
from smallarray import positions1096523158
import itertools
from latlngdata import latlngdata
from distancedata import distancedata
import math
from gislib import getDistance


class POSjson(db.Model):
    json = db.TextProperty()
    date = db.DateTimeProperty(auto_now_add=True)

class ELEjson(db.Model):
    json = db.TextProperty() #{'elevation': 42.937473300000001, 'location': {'lat': 50.768859999999997, 'lng': 3.9170199999999999}}
    dist = db.IntegerProperty() #10meterincrement from start

class formPosition(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'form2.html')
        html = template.render(path,{})
        self.response.out.write(html)
        
class putElevation(webapp.RequestHandler): #url for putting the sequentiallist of  elevation points in the database
    def post(self):
        elejson = ELEjson()
        json= self.request.get('json')
        dist = self.request.get('dist')
        elejson.json = json
        elejson.dist = int(dist)
        elejson.put()
        
class getProfiledata(webapp.RequestHandler):
    def get(self):
        list = positions1096523158
        #~ maxsamples = 512
        maxsamples = int(self.request.get('samples') )
        samplelength = 10.96523158
        startpos = int(int(self.request.get('startpos')) / samplelength)
        endpos = int(int(self.request.get('endpos')) / samplelength)
        
        totallength = endpos - startpos
        if totallength > maxsamples:
            interval = int(totallength/maxsamples) + 1
        else:
            interval = 1
        returnlist = itertools.islice(list,startpos, endpos, interval)
        #~ total = int(endpos-startpos/interval)
        elevationlist = []
        #~ i = 0
        for item in returnlist:
            self.response.out.write(str(item[0]))
            #~ if item != returnlist[-1]:
            self.response.out.write(',')
            
            #~ elevationlist.append(item[0])
        #~ data = str(elevationlist)
        #~ self.response.headers["Content-Type"] = "text/javascript"
        #~ self.response.out.write(data)
    

    
def getclosestpoint (curpos):
    for pos in range(len(latlngdata)-1):
        pathpos =  (latlngdata[pos][0], latlngdata[pos][1])
        dist = getDistance(pathpos,curpos)
        pathpos =  (latlngdata[pos+1][0], latlngdata[pos+1][1])
        nextdist = getDistance(pathpos,curpos)
        if nextdist >= dist:
            break
        #~ print dist
        #~ print pos
    return sum(distancedata[0:pos])
    
class updateRealPos(webapp.RequestHandler):
    def post(self):
        posjson = POSjson()
        device_label= self.request.get('device_label')
        device_key = self.request.get('device_key')
        timestamp = self.request.get('timestamp')
        altitude = self.request.get('altitude')
        longitude = self.request.get('longitude')
        latitude = self.request.get('latitude')
	distance = self.request.get('distance')
	speed = self.request.get('speed')
	logging.debug(distance)
        if speed == "":
	        speed = 0.0
        speed = str(3.6*float(speed)) #conversie m/s --> km/h
        heading = self.request.get('heading')
        try:
            prevtimestamp = int(memcache.get('prevtimestamp'))
            prevspeed = float(memcache.get('prevspeed'))
            prevaltitude = float(memcache.get('prevaltitude'))
            progresspeed = (float(speed) + float(prevspeed))/2/3.6 
            progresstime = float(int(timestamp)-prevtimestamp)
            progress = progresspeed * progresstime
            climbrate =  str(int((float(altitude) - prevaltitude)/progress*100))
        except:
            memcache.set('prevspeed', '0')
            memcache.set('prevtimestamp', '12222220')
            memcache.set('prevaltitude', '0')
            climbrate = '0'
            
        memcache.set('prevtimestamp', timestamp)
        memcache.set('prevaltitude', altitude)
        memcache.set('prevspeed', speed)
        polltime = str(5001)
        ###dist betwen GPSpos en polylinePOS
        #curpos = (float(latitude), float(longitude))
        #logging.debug("closestpoint=")
        #distance = str(int(getclosestpoint (curpos)))
        distance = "0.0"
       
        
        jsondata = '{ "longitude" :' + longitude + ',"latitude" : ' + latitude + ' , "speed" : ' + speed + ' ,"heading" : ' + heading + ' ,"altitude" : ' + altitude + ',"climbrate":' + climbrate + ',"distance":' + distance  +',"polltime":' + polltime  +'}'
        memcache.set('realPosData',  jsondata)	
        #~ posjson.json = str(jsoncode)
        posjson.json = str(jsondata)
        self.response.out.write(posjson.json)
        posjson.put()
        #self.redirect('/')
        self.createhtml()
        
        
    #~ self.createpoly()
    

    
        
    def createhtml(self):
        #~ logging.debug("entered create html")
        q = db.GqlQuery("SELECT * FROM POSjson ORDER BY date DESC")
        finalpositions = db.Query(POSjson).fetch(limit=1)
        #~ finalpositions = q.fetch(1)
        logging.debug(finalpositions)
    #~ poly
        for finalpos in finalpositions:
            logging.debug(finalpos.json)
            #json = '['+finalpos.json+']'
            json = finalpos.json
            #~ logging.debug('json =' + json) 
            pos = simplejson.loads(json)
            template_values = {
                           'device_label': pos['device_label'],
                           'device_key': pos['device_key'],
                           'timestamp': pos['timestamp'],
                           'altitude': pos['altitude'],
                           'longitude': pos['longitude'],
                           'latitude': pos['latitude'],
                           'speed': pos['speed'],
                           'heading': pos['heading']
                           #~ 'distance': pos['distance'],
                           #~ 'polltime': pos['polltime']
                           }
                       
        path = os.path.join(os.path.dirname(__file__), 'maps.html')
        html = template.render(path, template_values)
        memcache.set('maphtml', html)
        #~ logging.debug("mapnhtml in cahche")
        
        path = os.path.join(os.path.dirname(__file__), 'main.html')
        html = template.render(path, template_values)
        memcache.set('mainhtml', html)
        
        #~ distance, difference between memcache and database?
class updateRealDist(webapp.RequestHandler):
	def post(self):
		distance = self.request.get('distance')
		memcache.set('realDistData',  distance)
    
        
class displayMap(webapp.RequestHandler):
    def get(self):
        html = memcache.get('maphtml')
        #~ logging.debug('having phun yet?')
        #~ logging.debug(html)
        self.response.out.write(html)

class dePanne(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'depanne.html')
        template_values = {}
        html = template.render(path, template_values)
        self.response.out.write(html)

class realPos(webapp.RequestHandler):
    def get(self):
        jsondata = memcache.get('realPosData')  
        if not jsondata:
            jsondata = '{"longitude" : 51.1,"latitude" : 3.1, "speed" : 0, "heading" : 180,  "climbrate" : 0  , "distance" : 0, "polltime" :5100}'
        self.response.headers["Content-Type"] = "text/javascript"
        self.response.out.write(jsondata)
	
class realDist(webapp.RequestHandler):
	def get(self):
		realdist = memcache.get('realDistData')
		self.response.headers["Content-Type"] = "text/javascript"
		self.response.out.write(realdist)

class MainHandler(webapp.RequestHandler):
    def get(self):
        try:
            mainhtml = memcache.get('mainhtml')
            self.response.out.write(mainhtml)
        except:
	        path = os.path.join(os.path.dirname(__file__), 'noservice.html')
	        template_values = {}
	        html = template.render(path, template_values)
	        self.response.out.write(html)

def main():
  application = webapp.WSGIApplication([('/', MainHandler),
                                                                ('/updateRealPos', updateRealPos),
                                                                ('/putElevation', putElevation),
                                                                ('/displayMap', displayMap),
                                                                ('/formPosition',formPosition),
                                                                ('/getProfiledata',getProfiledata),
                                                                ('/dePanne',dePanne),
                                                                ('/realPos',realPos),
								('/realDist',realDist),
								('/updateRealDist',updateRealDist)
                                                                ],debug=True)
  util.run_wsgi_app(application)

if __name__ == '__main__':
  main()
