


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
    timestamp = db.DateTimeProperty()
    RugID = db.IntegerProperty()
    Voornaam = db.StringProperty()
    Familienaam = db.StringProperty()
    Geslacht = db.StringProperty()
    Geboortedatum = db.DateProperty()
    Gewicht = db.IntegerProperty()
    Doping = db.StringProperty()
    Ploeg = db.StringProperty()
    email = db.EmailProperty()
    Lengte = db.IntegerProperty()
    Avatar = db.BlobProperty()


def getdom ():

    url = "https://spreadsheets.google.com/feeds/list/0At25_ezMnvvWdEIxUmVXUWdfN1RnVFQtV1J0b0dYQkE/1/private/full"
    urlpublic = "https://spreadsheets.google.com/feeds/list/0AtwfWMwMK9ijdGFGeVdzc0hDS0lQb21sdGozUDZuMEE&hl/1/public/full"
    urlcsv = "https://spreadsheets.google.com/feeds/download/spreadsheets/Export?key=0At25_ezMnvvWdEIxUmVXUWdfN1RnVFQtV1J0b0dYQkE&exportFormat=csv"

    result = urlfetch.fetch(urlcsv,' ','get')
    
    print result.content
  
class showProfile(webapp.RequestHandler):
    def get(self):
        rugid = int(self.request.get('rugid'))
        #print rugid                                   
        
      
        
        # The Query interface prepares a query using instance methods.
        q = Coureur.all()
        q.filter("RugID =", rugid)
        results = q.fetch(1)
        #print results
        for p in results:
            logging.debug( "%s %s, %s inches tall" % (p.Voornaam, p.Familienaam, p.Lengte))
        path = os.path.join(os.path.dirname(__file__), 'profile.html')
        html = template.render(path,{
                           'Voornaam': p.Voornaam,
                           'RugID': p.RugID,
                           'Familienaam': p.Familienaam,
                           'Geslacht': p.Lengte,
                           #'Geboortedatum': p.GeboorteDatum,
                           'Gewicht' : p.Gewicht,
                           'Doping' : p.Doping,
                           'Ploeg' : p.Ploeg,
                           'email' : p.email,
                           'Lengte' : p.Lengte,
                           'Avatar' : p.Avatar
                                     })
        self.response.out.write(html)  


# The query is not executed until results are accessed.

class addCoureur(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'form.html')
        html = template.render(path,{})
        self.response.out.write(html)                                                   
        
class addCoureur2DB(webapp.RequestHandler):
    def post(self):
        coureur = Coureur()
        coureur.Voornaam = self.request.get('Voornaam')
        coureur.Familienaam = self.request.get('Familienaam')
        coureur.Geslacht = self.request.get('Geslacht')
        coureur.RugID = int(self.request.get('RugID'))
        avatar = self.request.get("img")
        coureur.avatar = db.Blob(avatar)
        
        
        coureur.put()
        
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

class Image(webapp.RequestHandler):
    def get(self):
      coureur = db.get(self.request.get("img_id"))
      if coureur1.avatar:
          self.response.headers['Content-Type'] = "image/png"
          self.response.out.write(greeting.avatar)
      else:
          self.error(404)


def main():
  application = webapp.WSGIApplication([('/', MainHandler),
                                        ('/showProfile', showProfile),
                                        ('/addCoureur', addCoureur),
                                        ('/addCoureur2DB',addCoureur2DB),
                                        ('/showKlassement', showKlassement),
                                        ('/dbimg', Image)
                                        ],debug=True)
  util.run_wsgi_app(application)

if __name__ == '__main__':
  main()
    
    
