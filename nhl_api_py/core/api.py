"""
NHL API client.
"""
import logging

from requests import request

from nhl_api_py.core.decorators import timing
from nhl_api_py.core.error_exceptions import ResponseError
from nhl_api_py.core.models import Team
from nhl_api_py.core.response import Response

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
        response = self.get(teams_endpoint)
        data = response.data.get("teams", [])
        if len(data) == 0:
            logger.warning(
                "Response Data did not have proper team data. "
                + "Either the `teams` key was missing or no data exists."
            )
            logger.debug(response.data)
        return [Team.from_dict(team_entry) for team_entry in data]

    def game(
        self,
        game_id: int,
        boxscore: bool = False,
        linescore: bool = False,
    ) -> list[Team]:
        """
        Sends a GET request to retrieve game data from the NHL API.

        If `boxscore` is True, the response will contain only the boxscore.

        If `linescore` is True, the response will contain only the linescore.

        `linescore` and `boxscore` may not both be True.

        If neither `linescore` nor `boxscore` are passed, the response will
        contain all of the data for the specified game.

        :param game_id: the ID of the specific game for which we want to see data.
        :param boxscore: whether the response should return the boxscore for the game.
        :param linescore: whether the response should return the linescore for the game.
        :return: list of Team models
        """
        logger.debug((game_id, boxscore, linescore))

        if boxscore and linescore:
            raise ValueError("You may request boxscore or linescore, not both.")

        games_endpoint = "game/" + str(game_id)
        if boxscore:
            games_endpoint += "/boxscore"
        elif linescore:
            games_endpoint += "/linescore"
        else:
            games_endpoint += "/feed/live"
        return self.get(games_endpoint)
