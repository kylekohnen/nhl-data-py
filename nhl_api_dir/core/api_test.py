from nhl_api_dir.core.nhl_api import NhlApi

api = NhlApi()

id = 2017020001

for boxscore in [False, True]:
    for linescore in [False, True]:
        game = api.games(game_id=id, boxscore=boxscore, linescore=linescore)
        print(game)

# print(type(game))
# to_type = game.data["gameData"]["teams"]
# print(type(to_type))
