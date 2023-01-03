"""
NHL API client.
"""
import logging
from typing import Iterable

from requests import request

from nhl_api_py.core.decorators import timing
from nhl_api_py.core.error_exceptions import ResponseError
from nhl_api_py.core.response import Response
from nhl_api_py.models.game import Boxscore, Game, Play
from nhl_api_py.models.schedule import ScheduleDate
from nhl_api_py.models.team import Team

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
    ) -> Game:
        """
        Sends a GET request to retrieve game data from the NHL API.

        :param game_id: the ID of the specific game for which we want to see data.
        :return: Game model.
        """
        logger.debug(game_id)

        games_endpoint = "game/" + str(game_id) + "/feed/live"
        response = self.get(games_endpoint)
        return Game.from_dict(response.data)

    def boxscore(
        self,
        game_id: int,
    ) -> Boxscore:
        """
        Sends a GET request to retrieve boxscore data from the NHL API.

        :param game_id: the ID of the specific game for which we want to see data.
        :return: Boxscore model.
        """
        logger.debug(game_id)

        games_endpoint = "game/" + str(game_id) + "/boxscore"
        response = self.get(games_endpoint)
        return Boxscore.from_dict(response.data)

    def plays(
        self,
        game_id: int,
        scoring_plays_only: bool = False,
        penalty_plays_only: bool = False,
    ) -> list[Play]:
        """
        Sends a GET request to retrieve plays data from the NHL API.

        :param game_id: the ID of the specific game for which we want to see data.
        :param scoring_plays_only: whether the response contains scoring plays.
        :param penalty_plays_only: whether the response contains penalty plays.
        :return: list of Play model.
        """
        response = self.game(game_id=game_id)
        data = response.all_plays
        if data is None:
            logger.warning(
                "Response Data did not have proper plays data. "
                + "Either the `game_id` was invalid or no data exists."
            )
            logger.debug(response)
            return []
        plays_to_return = []
        plays_to_return += response.scoring_plays if scoring_plays_only else []
        plays_to_return += response.penalty_plays if penalty_plays_only else []
        if len(plays_to_return) == 0:
            return data
        else:
            return [data[play_index] for play_index in plays_to_return]

    def schedule(
        self,
        team_ids: list[int] | int = None,
        season_start_year: int = None,
        game_type: str = None,
        date_range: Iterable[str] = None,
    ) -> list[ScheduleDate]:
        """
        Sends a GET request to retrieve a schedule of games/events for a
        specified date range.
        By default, the API will specify the date range as the current date only.

        :param team_ids: limits the schedule to the specific team(s) inserted
        :param season_start_year: the start year of the specific NHL Season you want
            to look at
        :param game_type: limits the schedule to specific type of games, such as
            regular season games ("R")
        :param date_range: searches for games specified within a specific
            range of dates
        :return: a list of dates which keep info about the games played on a day
        """
        schedule_endpoint = "schedule?"
        if team_ids:
            team_ids = [team_ids] if isinstance(team_ids, int) else team_ids
            all_ids = ",".join(str(x) for x in team_ids)
            schedule_endpoint += f"teamId={all_ids}&"
        if season_start_year:
            schedule_endpoint += f"season={season_start_year}{season_start_year+1}&"
        if game_type:
            schedule_endpoint += f"gameType={game_type}&"
        if date_range:
            schedule_endpoint += f"startDate={game_type[0]}&endDate={date_range[1]}&"
        response = self.get(schedule_endpoint)
        all_dates = response.data.get("dates", [])
        return [ScheduleDate.from_dict(date) for date in all_dates]
