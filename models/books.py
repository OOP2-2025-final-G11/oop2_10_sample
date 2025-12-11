from peewee import Model, CharField, SqliteDatabase
from .db import db

class Books(Model):
    title = CharField()
    author = CharField()
    isbn = CharField()

    class Meta:
        database = db