from flask import Flask

app = Flask(__name__)

myMessages = []

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



@app.get("/game")
def get_games():
    print("Request for game list received.")
    gamelist = "{\"games\":[]}"
    return gamelist

@app.get("/game/<gameId>")
def get_game(gameId):
    print("Request game detail for ",gameId)
    gamedata = "{\"game\": {\"id\":\""+gameId+"\"}}"
    return gamedata

@app.post("/game")
def create_game():
    print("Request new game received.")
    # adding new row to database
    gameId = "A1234"
    gamedata = "{\"game\": {\"id\":\""+gameId+"\"}}"
    return gamedata