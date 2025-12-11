from peewee import Model, ForeignKeyField, DateTimeField
from .db import db
from .user import User
from .books import Books


class Rental(Model):
    user = ForeignKeyField(User, backref='rental')
    books = ForeignKeyField(Books, backref='rental')
    rental_date = DateTimeField()
    return_date = DateTimeField(null=True)

    class Meta:
        database = db