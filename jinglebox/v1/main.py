


#for parsing the spreadsheet
from xml.dom.minidom import parse, parseString
from xml.dom import minidom
import csv
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util
from google.appengine.api import urlfetch
from django.utils import simplejson as json
import os
import logging
import urllib2
import models
from google.appengine.ext import db
from google.appengine.api import memcache
from google.appengine.ext.db import GqlQuery

class Coureur(db.Model):
    RugID = db.IntegerProperty()
    Voornaam = db.StringProperty()
    Familienaam = db.StringProperty()
    Geslacht = db.StringProperty()
    Geboortedatum = db.StringProperty()
    Gewicht = db.IntegerProperty()
    Doping = db.StringProperty()
    Ploeg = db.StringProperty()
    Lengte = db.IntegerProperty()
    Awards = db.StringListProperty()
    Events = db.StringListProperty()

  
class showProfile(webapp.RequestHandler):
    def get(self):
        rugid = int(self.request.get('rugid'))
        # The Query interface prepares a query using instance methods.
        q = Coureur.all()
        q.filter("RugID =", rugid)
        p = q.fetch(1)
        #print p[0].Awards[0]
        #print results
        #for p in results:
        #    logging.debug( "%s %s, %s inches tall" % (p.Voornaam, p.Familienaam, p.Lengte))
        #    p.events = ["moederkind", "memepepe", "crisis"]
        path = os.path.join(os.path.dirname(__file__), 'profile.html')
        html = template.render(path,{
                           'Voornaam': p[0].Voornaam,
                           'RugID': p[0].RugID,
                           'Familienaam': p[0].Familienaam,
                           'Geslacht': p[0].Geslacht,
                           'Geboortedatum': p[0].Geboortedatum,
                           'Gewicht' : p[0].Gewicht,
                           'Doping' : p[0].Doping,
                           'Ploeg' : p[0].Ploeg,
                           'Lengte' : p[0].Lengte,
                           'Events' : p[0].Events,
                           'Awards' : p[0].Awards,
                           
                           
                           #'Eventslen' : 30/len(p.events)
                                     })
        self.response.out.write(html)  


# The query is not executed until results are accessed.

class addCoureur(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'form.html')
        html = template.render(path,{})
        self.response.out.write(html)   
        
        
class addAward(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'awardform.html')
        html = template.render(path,{})
        self.response.out.write(html)     
        
class addCoureur2DB(webapp.RequestHandler):
    def post(self):
        eventsstr = self.request.get('events')
        #print eventsstr
        events = eventsstr.split(',')
        del events[-1]
        coureur = Coureur()
        coureur.Voornaam = self.request.get('Voornaam')
        coureur.Familienaam = self.request.get('Familienaam')
        coureur.Geslacht = self.request.get('Geslacht')
        coureur.Geboortedatum = self.request.get('Geboortedatum')
        coureur.Gewicht = int(self.request.get('Gewicht'))
        coureur.Doping = self.request.get('Doping')
        coureur.Ploeg = self.request.get('Ploeg')
        coureur.Lengte = int(self.request.get('Lengte'))
        coureur.Events = events
        #print coureur.Events
        coureur.Awards = []
        coureur.RugID = int(self.request.get('RugID'))
        coureur.put()

class addAward2DB(webapp.RequestHandler):
    def post(self):
        award = self.request.get('award')
        rugid = int(self.request.get('rugid'))
        # The Query interface prepares a query using instance methods.
        q = Coureur.all()
        q.filter("RugID =", rugid)
        p = q.fetch(1)
        p[0].Awards.append(award)
        p[0].put()
        path = os.path.join(os.path.dirname(__file__), 'showaward.html')
        html = template.render(path,{
                            'award': award,
                            'RugID': rugid,
        })
        self.response.out.write(html) 
        
        
class showKlassement(webapp.RequestHandler):
    def get(self):
        een = self.request.get('een')
        twee = self.request.get('twee')
        drie = self.request.get('drie')
        path = os.path.join(os.path.dirname(__file__), 'klassement.html')
        html = template.render(path,{
                            'een': int(een),
                            'twee': (twee),
                            'drie': (drie),
                            
        })
        self.response.out.write(html) 
        
class MainHandler(webapp.RequestHandler):
    def post(self):
        print"blah"



def main():
  application = webapp.WSGIApplication([('/', MainHandler),
                                        ('/showProfile', showProfile),
                                        ('/addCoureur', addCoureur),
                                        ('/addCoureur2DB',addCoureur2DB),
                                        ('/addAward', addAward),
                                        ('/addAward2DB',addAward2DB),
                                        ('/showKlassement', showKlassement)
                                        
                                        ],debug=True)
  util.run_wsgi_app(application)

if __name__ == '__main__':
  main()
    
    
