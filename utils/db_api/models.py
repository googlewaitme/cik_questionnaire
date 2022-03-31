from peewee import *
import datetime


database = SqliteDatabase('app.db')


def create_tables():
    with database:
        database.create_tables([User, LoginToken], fail_silently=True)


class BaseModel(Model):
    class Meta:
        database = database


class LoginToken(BaseModel):
    login = CharField(max_length=16, unique=True)
    name = CharField(max_length=100, default='Noname')


class User(BaseModel):
    telegram_id = IntegerField(unique=True)
    is_baned = BooleanField(default=False)
    join_date = DateTimeField(default=datetime.datetime.now)
    name = CharField(max_length=100, default='Noname')


if __name__ == '__main__':
    create_tables()
