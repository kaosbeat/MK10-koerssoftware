from google.appengine.ext import db

class Coureur(db.Model):
    timestamp = db.DateTimeProperty()
    Voornaam = db.StringProperty()
    Familienaam = db.StringProperty()
    Geslacht = db.StringProperty()
    Geboortedatum = db.DateProperty()
    Gewicht = db.IntegerProperty()
    Doping = db.StringProperty()
    Ploeg = db.StringProperty()
    email = db.EmailProperty()
    Lengte = db.IntegerProperty()

