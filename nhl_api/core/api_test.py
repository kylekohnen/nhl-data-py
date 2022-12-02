from nhl_api_dir.core.nhl_api import NhlApi

api = NhlApi()

games = api.games(2017010001)
