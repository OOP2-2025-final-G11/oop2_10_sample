#グラフで登録日時が欲しい
from peewee import Model, CharField, IntegerField, DateTimeField
from datetime import datetime
from .db import db

class User(Model):
    name = CharField()
    age = IntegerField()
    #グラフで登録日時が欲しい
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = db