import csv

from flask import Flask, request
from model import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:14159265@localhost:5432/songlyricsdb"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def main():
    f = open('Songs.csv', encoding='utf8')
    reader = csv.reader(f)
    print("hello")
    for SongTitle, Lyrics, Artist, Album, Year, Thumbnail, Sender, Ratings in reader:
        if SongTitle == "SongTitle":
            continue
        Songs = Song(songTitle=SongTitle, lyrics=Lyrics, artist=Artist, album=Album, year=Year, thumbnail=Thumbnail, sender=Sender, ratings=Ratings)
        print(Songs)
        db.session.add(Songs)

    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        main()