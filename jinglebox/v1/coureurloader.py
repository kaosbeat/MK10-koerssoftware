import datetime
from google.appengine.ext import db
from google.appengine.tools import bulkloader


class Coureur(db.Model):
    Voornaam = db.StringProperty()
    Familienaam = db.StringProperty()
    Geslacht = db.StringProperty()
    Geboortedatum = db.StringProperty()
    Gewicht = db.IntegerProperty()
    Doping = db.StringProperty()
    Ploeg = db.StringProperty()
    email = db.EmailProperty()
    Lengte = db.IntegerProperty()




class CoureurLoader(bulkloader.Loader):
    def __init__(self):
        bulkloader.Loader.__init__(self, 'Coureur',
                                    [('Voornaam', str),
                                    ('Familienaam', str),
                                    ('Geslacht', str),
                                    ('Geboortedatum', str),
                                    ('Gewicht', int),
                                    ('Doping', str),
                                    ('Ploeg', str),
                                    ('email', str),
                                    ('Lengte', int),
                                    ])

loaders = [CoureurLoader]
