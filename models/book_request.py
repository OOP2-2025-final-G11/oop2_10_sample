from peewee import Model, ForeignKeyField, CharField, DateTimeField
from .db import db
from .user import User

class BookRequest(Model):
    user = ForeignKeyField(User, backref='requests')
    title = CharField()       # 申請したい本のタイトル
    author = CharField()      # 著者
    request_date = DateTimeField()

    class Meta:
        database = db
