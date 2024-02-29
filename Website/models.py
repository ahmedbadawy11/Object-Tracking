from . import db
from flask_login import UserMixin
# from flask_sqlalchemy import func


class user(db.Model,UserMixin):
    id=db.Column (db.Integer,primary_key=True)
    email=db.Column (db.String(150),unique=True)
    name=db.Column (db.String(150))
    password=db.Column (db.String(150))
