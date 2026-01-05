# Game microservice

This is the main microservice that implements the game interface

## Database

The bolded columns are primary keys 

Game table:

- **gameId**
- maxScore
- playerN
- playerW
- playerS
- playerE
- scoreN
- scoreW
- scoreS
- scoreE
- status
- currentHand

Hand table:
- **gameId** (foreign key to game table)
- **handNum**
- scoreN
- scoreW
- scoreS
- scoreE
- state
- trumpSuit
- bidN
- bidW
- bidS
- bidE
- handN (list of cards - array of 13)
- handW (list of cards - array of 13)
- handS (list of cards - array of 13)
- handE (list of cards - array of 13)
- currentTrick

Trick table
- **gameId** (foreign key to game table)
- **handNum** (foreign key to hand table)
- **playNum**
- cardN
- cardW
- cardE
- cardS

## REST api

`GET /game` - list games

`GET /game?state=inprogress` list active games (status is inprogress and complete)

`POST /game` - create new game with 4 players and max score; status = start, currentHand = 0 - returns game object

`GET /game/{gameId}` - retrieve existing game info

`GET /game/{gameId}/hands` - list all available hands for the game

`DELETE /game/{gameId}` - deletes a game from the database (for testing)

`POST /hand/{gameId}` - initiate new Hand and adds count to currentHand - state = 'bid' - return hand information - deals 

`GET /hand/{gameId}/{handNum}` - get specific hand information

`GET /hand/{gameId}/{handNum}?hand=N|S|E|W` - specific hand for a specific player

`GET /hand/{gameId}/{handNum}/trick` - lists the trick for the hand

`POST /hand/{gameId}/{handNum}/bid/{playerId}` - submit bid - checks other player - finalize the bid if all bids are received - set trumpSuit - reset state to play

`POST /hand/{gameId}/{handNum}/{trickNum}/play/{playerId}` - submit card only for state = play

`POST /hand/{gameId}/{handNum}/finish` - complete hand - recalculate score - roll up to the game level

`GET /trick/{gameId}/{handNum}/{trickNum}` get specific trick information

`POST /game/{gameId}` - complete game - recalculate rank for players



