from peewee import Model, ForeignKeyField, DateTimeField
from .db import db
from .user import User
from .books import Books


class Rental(Model):
    user = ForeignKeyField(User, backref='rentals', column_name='user_id')
    books = ForeignKeyField(Books, backref='rentals', column_name='books_id')
    rental_date = DateTimeField()
    return_date = DateTimeField(null=True)

    class Meta:
        database = db