from peewee import Model, CharField, DecimalField
from .db import db

class Books(Model):
    name = CharField()

    class Meta:
        database = db