from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app)
# DATABASE_URI = "postgresql+psycopg2://postgres:abc@127.0.0.1:5432/postgres" old: 'sqlite:///database.db'


# GET /hand/{gameId}/{handNum}
# GET /hand/{gameId}/{handNum}/trick
# GET /trick/{gameId}/{handNum}/{trickNum}
# POST /hand/{gameId}/{handNum} - create new hand (deal cards)
# POST /hand/{gameId}/{handNum}/bid/{playerId} - submit bid
# POST /trick/{gameId}/{handNum}/{trickNum}/play/{playerId} - submit card
# POST /hand/{gameId}/{handNum}/finish - complete hand - recalculate score
# POST /game/{gameId}/finish - complete game - recalculate rank for players


# Fields variables for @marshals_with
gameFields = {
    'gameId':fields.String,
    'maxScore':fields.Integer,
    'playerN':fields.String,
    'playerS':fields.String,
    'playerE':fields.String,
    'playerW':fields.String,
    'scoreN':fields.Integer,
    'scoreS':fields.Integer,
    'scoreE':fields.Integer,
    'scoreW':fields.Integer,
    'status':fields.String,
    'currentHand':fields.Integer
}

handFields = {
    'gameId':fields.String,
    'handNum':fields.String,
    'scoreN':fields.Integer,
    'scoreS':fields.Integer,
    'scoreE':fields.Integer,
    'scoreW':fields.Integer,
    'state':fields.String,
    'trumpSuit':fields.String,
    'bidN':fields.String,
    'bidS':fields.String,
    'bidE':fields.String,
    'bidW':fields.String,
    'handN':fields.String,
    'handS':fields.String,
    'handE':fields.String,
    'handW':fields.String,
    'currentTrick':fields.Integer
}

trickFields = {
    'gameId':fields.String,
    'handNum':fields.String,
    'playNum':fields.String,
    'cardN':fields.String,
    'cardS':fields.String,
    'cardE':fields.String,
    'cardW':fields.String
}

# Models for database for game, hand, and trick
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
    status = db.Column(db.String(20), default="inprogress")
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

# JSON input parsers
game_args = reqparse.RequestParser()
game_args.add_argument('gameId', type=str, required=True, help="Game ID cannot be blank")

hand_args = reqparse.RequestParser()

trick_args = reqparse.RequestParser()
trick_args.add_argument('cardPlayed', type=str)

# implement api commands

class Game(Resource):
    # gets the list of games, the list of inprogress games, a specific game instance, or the hands of a game instance
    @marshal_with(gameFields)
    def get(self, gameId, status, hands):
        if gameId=="null":
            if status=="1":
                return GameModel.query.filter(GameModel.status == 'inprogress').all(), 201
            return GameModel.query.all(), 201
        if hands=="1":
            hands = HandModel.query.filter_by(gameId=gameId).first()
            return hands, 201
        game = GameModel.query.filter_by(gameId=gameId).first()
        return game, 201
    
    # creates a game instance and updates game status to complete
    @marshal_with(gameFields)
    def post(self, gameId):
        if gameId=="null":
            args = game_args.parse_args()
            game = GameModel(gameId=args['gameId'])
            db.session.add(game)
            db.session.commit()
            return game, 201
        game = GameModel.query.filter_by(gameId=gameId).first()
        game.status = "complete"
        db.session.commit()
        return game, 201

    # deletes a game for testing
    @marshal_with(gameFields)
    def delete(self, gameId):
        game = GameModel.query.filter_by(gameId=gameId).first()
        if not game:
            abort(404, "Game not found")
        db.session.delete(game)
        db.session.commit()
        games = GameModel.query.all()
        return games, 204

class Hand(Resource):
    @marshal_with(handFields)
    def post(self, gameId):
        args = hand_args.parse_args()
        game = GameModel.query.filter_by(gameId=gameId).first()
        game.currentHand = game.currentHand + 1
        hands = HandModel(gameId=args['gameId'])
        db.session.add(hands)
        db.session.commit()
        return hands, 201

class Trick(Resource):
    @marshal_with(trickFields)
    def get(self, gameId, handNum, trickNum):
        trick = TrickModel.query.filter_by(gameId=gameId, handNum=handNum, trickNum=trickNum).first()
        return trick, 201
    
    @marshal_with(trickFields)
    def post(self, gameId, handNum, trickNum, playerId):
        args = trick_args.parse_args()
        game = GameModel.query.filter_by(gameId=gameId).first()
        hand = HandModel.query.filter_by(gameId=gameId, handNum=handNum).first()
        trick = TrickModel.query.filter_by(gameId=gameId, handNum=handNum, trickNum=trickNum).first()
        if playerId == game.playerN:
            if args['cardPlayed'] not in hand.handN:
                abort(404, "Card not found")
            trick.cardN = args['cardPlayed']
        if playerId == game.playerS:
            if args['cardPlayed'] not in hand.handN:
                abort(404, "Card not found")
            trick.cardS = args['cardPlayed']
        if playerId == game.playerE:
            if args['cardPlayed'] not in hand.handN:
                abort(404, "Card not found")
            trick.cardE = args['cardPlayed']
        if playerId == game.playerW:
            if args['cardPlayed'] not in hand.handN:
                abort(404, "Card not found")
            trick.cardW = args['cardPlayed']
        db.session.commit()
        return trick, 201

api.add_resource(Game, "/game/<string:gameId>", "/game/<string:gameId>/<string:status>/<string:hands>")
api.add_resource(Hand, "/hand")
api.add_resource(Trick, "/trick/<string:gameId>/<string:handNum>/<string:trickNum>", "/trick/<string:gameId>/<string:handNum>/<string:trickNum>/<string:playerId>")

@app.route("/")
def home():
    return "<h1>Truf</h1>"

if __name__ == '__main__':
    app.run(debug=True)