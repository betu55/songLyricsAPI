from flask_marshmallow import Marshmallow
from model import *

ma = Marshmallow()

class SongSchema(ma.Schema):
    class Meta:
        fields = ("songTitle", "lyrics", "artist", "album", "year", "thumbnail", "sender", "ratings")

        model = Song

class UsersSchema(ma.Schema):
    class Meta:
        fields = ("username", "password")

        model = Clients
