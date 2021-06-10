from flask import Flask
from model import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:14159265@localhost:5432/songlyricsdb"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def main():
    db.create_all()

if __name__ =='__main__':
    with app.app_context():
        main()
