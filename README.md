# Game microservice

This is the main microservice that implements the game interface

## Database

Game table:

- gameId
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
- state
- handNum

Hand table:
- gameId
- handNum
- scoreN
- scoreW
- scoreS
- scoreE
- state
- bidN
- bidW
- bidS
- bidE
- handN
- handW
- handE
- handS
- trickN
- trickW
- trickS
- trickE
- playNum

Trick table
- gameId
- handNum
- playNum
- cardN
- cardW
- cardE
- cardS
- winner 

## REST api

GET /game

POST /game/{id} - set new game with 4 players and max score

GET /game/{id}

GET /game/{id}/hands

GET /hand/{gameId}/{handNum}

GET /hand/{gameId}/{handNum}/trick

GET /trick/{gameId}/{handNum}/{trickNum}

POST /hand/{gameId}/{handNum} - create new hand (deal cards)

POST /hand/{gameId}/{handNum}/bid/{playerId} - submit bid

POST /trick/{gameId}/{handNum}/{trickNum}/play/{playerId} - submit card

POST /hand/{gameId}/{handNum}/finish - complete hand - recalculate score

POST /game/{gameId}/finish - complete game - recalculate rank for players



