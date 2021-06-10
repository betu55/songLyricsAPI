from flask import Flask, abort, session, render_template, request, redirect, url_for
from flask_session import Session
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from flask_restplus import Api, Resource, fields
from flask_cors import CORS
from sqlalchemy import create_engine, exc

from model import *
from schemas import *

app = Flask(__name__)
bcrypt = Bcrypt(app)

CORS(app)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:14159265@localhost:5432/songlyricsdb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
ma = Marshmallow(app)

api = Api(app)

song_schema = SongSchema()
songs_schema = SongSchema(many=True)
users_schema = UsersSchema()

song = api.model(
    "Song",
    {
        "songTitle": fields.String,
        "lyrics": fields.String,
        "artist": fields.String,
        "album": fields.String,
        "year": fields.Integer,
        "thumbnail": fields.Integer,
        "sender": fields.String,
        "ratings": fields.Integer,
    },
)

user = api.model(
    "User",
    {
        "username": fields.String,
        "password": fields.String,
    },
)


@app.route("/register", methods=["GET", "POST"])
def register():
    # if request.method == "POST":
    try:
        usern = request.form.get("username")
        passw = request.form.get("password")
        passw_hash = bcrypt.generate_password_hash(passw).decode("utf-8")

        user = Clients(username=usern, password=passw_hash)
        db.session.add(user)
        db.session.commit()
    except exc.IntegrityError:
        db.session.execute("ROLLBACK")
        db.session.commit()
        abort(404, "Username already exists!")
    return users_schema.dump(user)

@api.route("/api/search/<string:keyword>")
class Search(Resource):
    def get(self, keyword):
        result = Song.query.filter(Song.songTitle.ilike(f"{keyword}%")).all()
        if not result:
            abort(404, "No results")
        if len(result) > 1:
            return songs_schema.dump(result)
        else:
            return song_schema.dump(result)


@api.route("/api/songs/<int:id>")
class Songs(Resource):
    def get(self, id):
        song = Song.query.filter_by(songid=id).first()
        if not song:
            abort(404, "Could not find the song")
        return song_schema.dump(song)

    @api.expect(song)
    @api.response(204, "Song Updated")
    def put(self, id):
        song = Song.query.filter_by(songid=id).first()

        song.songTitle = request.json["songTitle"]
        song.artist = request.json["artist"]
        song.lyrics = request.json["lyrics"]
        song.album = request.json["album"]
        song.year = request.json["year"]
        song.thumbnail = request.json["thumbnail"]

        db.session.add(song)
        db.session.commit()

        return song_schema.dump(song)


@api.route("/api/songs")
class AllSongs(Resource):
    def get(self):
        songs = Song.query.all()
        return songs_schema.dump(songs)

    @api.expect(song)
    def post(self):
        new_song = Song()

        new_song.songTitle = request.json["songTitle"]
        new_song.artist = request.json["artist"]
        new_song.lyrics = request.json["lyrics"]
        new_song.album = request.json["album"]
        new_song.year = request.json["year"]
        new_song.thumbnail = request.json["thumbnail"]

        db.session.add(new_song)
        db.session.commit()

        return song_schema.dump(new_song)


@api.route("/api/artists")
class Artists(Resource):
    def get(self):
        artists = Song.query.order_by(Song.artist).all()
        temp = []
        for artist in artists:
            temp.append(artist.artist)
        print(temp)

        return {"All Artists": temp}
