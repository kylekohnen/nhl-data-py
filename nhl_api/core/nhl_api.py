"""
NHL API client.
"""
import logging

from requests import request

from nhl_api.core.decorators import timing
from nhl_api.core.error_exceptions import ResponseError
from nhl_api.core.response import Response

logger = logging.getLogger(__name__)


class NhlApi:
    """
    Class representing the NHL API.
    """

    _base_url: str = "https://statsapi.web.nhl.com/api"

    def __init__(self, api_version: int = 1):
        self.url: str = f"{NhlApi._base_url}/v{api_version}"

    @timing
    def _request(self, http_method: str, endpoint: str) -> Response:
        """
        Sends an HTTP request to the NHL API.

        :param http_method: the request method used
        :param endpoint: where we want to connect to with the API
        :return: the data / response returned by the API
        """
        url = f"{self.url}/{endpoint}"
        logger.debug(f"{http_method} request sent to: {url}")
        data = request(http_method, url, timeout=60)

        if data.status_code // 100 in [4, 5]:
            raise ResponseError(
                f"{data.request.method} method returns HTTP status code "
                + f"{data.status_code} on {data.url}"
            )
        else:
            return Response.from_requests(data)

    def get(self, endpoint: str) -> Response:
        """
        Sends a GET request to a specific endpoint to the NHL API.

        :param endpoint: where we want to connect to with the API
        :return: the data / response returned by the API
        """
        return self._request("GET", endpoint)

    def teams(
        self,
        team_ids: list[int] | int = None,
        season: int = None,
        roster: bool = None,
        stats: bool = None,
    ) -> Response:
        """
        Sends a GET request to retrieve team data from the NHL API.

        If `team_ids` is specified, it will filter the data to those specified teams.

        If `season` is specified, it will find all teams for the specified season.
        The input should be the season's start year (e.g.
        `season=2010` correlates to the 2010 - 2011 season).

        If `roster` is specified, it will display the entire roster for that team.

        If `stats` is specified, it will display the entire roster for that team.

        If no parameters are passed in, then all data on the
        current NHL teams will be returned.

        :param team_ids: all the specific teams we want to see data for
        :param season: the start year of the season
        :param roster: whether the teams entire roster should be included
        :param stats: whether the teams season stats will be included
        :return: data on all NHL teams
        """
        logger.debug((team_ids, season, roster, stats))
        teams_endpoint = "teams?"
        if team_ids:
            team_ids = [team_ids] if isinstance(team_ids, int) else team_ids
            all_ids = ",".join(str(x) for x in team_ids)
            teams_endpoint += f"teamId={all_ids}&"
        if season:
            season = f"{season}{season + 1}"
            teams_endpoint += f"season={season}&"
        if roster:
            teams_endpoint += "expand=team.roster&"
        if stats:
            teams_endpoint += "expand=team.stats&"
        return self.get(teams_endpoint)

    def games(
        self,
        game_id: int = None,
        plays: bool = False,
        boxscore: bool = False,
        teams: bool = False,
    ) -> Response:
        """
        Sends a GET request to retrieve game data from the NHL API.

        `game_id` is the ID of the game of interest.

        If `plays` is not none, the response will contain the all game plays.

        If `boxscore` is not none, the response will contain the box score.

        If `teams` is not none, the response will contain the game's teams data.

        If no bool parameters are passed, the response will
        contain all of the data for the specified game.

        :param game_id: the ID number of the specific game we want to see data for.
        :param plays: whether the response should return all plays in the game.
        :param boxscore: whether the response should return the boxscore for the game.
        :param teams: whether the response should return the team data for the game.
        """
        assert game_id is not None, "You must request a specific game."
        game_id = str(game_id)
        if len(game_id) != 10:
            raise ValueError("Invalid game ID.")
        games_endpoint = "games/" + game_id

        if not (plays and boxscore and teams):
            games_endpoint += "/feed/live"
            return self.get(games_endpoint)

        elif plays:
            # I need to access liveData -> plays
            games_endpoint += "/feed/live"
            json_gamedata = self.get(games_endpoint)

        elif boxscore:
            games_endpoint += "/boxscore"

        elif teams:
            # I need to access gameData -> teams
            x = 1
