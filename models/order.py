from peewee import Model, ForeignKeyField, DateTimeField
from .db import db
from .user import User
from .books import Books

class Order(Model):
    user = ForeignKeyField(User, backref='orders')
    books = ForeignKeyField(Books, backref='orders')
    order_date = DateTimeField()

    class Meta:
        database = db
