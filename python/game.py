from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app)
# DATABASE_URI = "postgresql+psycopg2://postgres:abc@127.0.0.1:5432/postgres" old: 'sqlite:///database.db'


# GET /game
# POST /game/{id} - set new game with 4 players and max score
# GET /game/{id}
# GET /game/{id}/hands
# GET /hand/{gameId}/{handNum}
# GET /hand/{gameId}/{handNum}/trick
# GET /trick/{gameId}/{handNum}/{trickNum}
# POST /hand/{gameId}/{handNum} - create new hand (deal cards)
# POST /hand/{gameId}/{handNum}/bid/{playerId} - submit bid
# POST /trick/{gameId}/{handNum}/{trickNum}/play/{playerId} - submit card
# POST /hand/{gameId}/{handNum}/finish - complete hand - recalculate score
# POST /game/{gameId}/finish - complete game - recalculate rank for players



class GameModel(db.Model):
    #__tablename__= "gameTable"

    gameId = db.Column(db.String(80), primary_key=True, nullable=False)
    maxScore = db.Column(db.Integer, default=100)
    playerN = db.Column(db.String(80), default="")
    playerS = db.Column(db.String(80), default="")
    playerE = db.Column(db.String(80), default="")
    playerW = db.Column(db.String(80), default="")
    scoreN = db.Column(db.Integer, default=0)
    scoreS = db.Column(db.Integer, default=0)
    scoreE = db.Column(db.Integer, default=0)
    scoreW = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default="start")
    currentHand = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"User(id = {self.id}, maxScore = {self.maxScore}, playerN = {self.playerN}, playerS = {self.playerS}, playerE = {self.playerE}, playerW = {self.playerW}, scoreN = {self.scoreN}, scoreS = {self.scoreS}, scoreE = {self.scoreE}, scoreW = {self.scoreW}, status = {self.status}, currentHand = {self.currentHand})"

class HandModel(db.Model):
    #__tablename__ = "handTable"

    gameId = db.Column(db.String(80), primary_key=True, nullable=False)
    handNum = db.Column(db.String(80), primary_key=True, nullable=False)
    scoreN = db.Column(db.Integer, default=0)
    scoreS = db.Column(db.Integer, default=0)
    scoreE = db.Column(db.Integer, default=0)
    scoreW = db.Column(db.Integer, default=0)
    state = db.Column(db.String(20), default="bid")
    trumpSuit = db.Column(db.String(10), default="")
    bidN = db.Column(db.String(2), default="")
    bidS = db.Column(db.String(2), default="")
    bidE = db.Column(db.String(2), default="")
    bidW = db.Column(db.String(2), default="")
    handN = db.Column(db.String(26), default="")
    handS = db.Column(db.String(26), default="")
    handE = db.Column(db.String(26), default="")
    handW = db.Column(db.String(26), default="")
    currentTrick = db.Column(db.Integer, default=0)

class TrickModel(db.Model):
    #__tablename__ = "trickTable"

    gameId = db.Column(db.String(80), primary_key=True, nullable=False)
    handNum = db.Column(db.String(80), primary_key=True, nullable=False)
    playNum = db.Column(db.String(80), primary_key=True, nullable=False)
    cardN = db.Column(db.String(2), default="")
    cardS = db.Column(db.String(2), default="")
    cardE = db.Column(db.String(2), default="")
    cardW = db.Column(db.String(2), default="")

@app.route("/")
def home():
    return "<h1>Truf</h1>"

if __name__ == '__main__':
    app.run(debug=True)