from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Song(db.Model):
    __tablename__ = "song"
    songid = db.Column(db.Integer, primary_key=True)
    songTitle = db.Column(db.String(50), unique=False, nullable=False)
    lyrics = db.Column(db.String(1000), unique=True)
    artist = db.Column(db.String(50), unique=False, nullable=False)
    album = db.Column(db.String(150), unique=False, nullable=False)
    year = db.Column(db.String(10), unique=False, nullable=False)
    thumbnail = db.Column(db.String(500), unique=True, nullable=False)
    sender = db.Column(db.String(50), default="")
    ratings = db.Column(db.String(10), default="", unique=False)
    

class Clients(db.Model):
    __tablename__ = "clients"
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100))
