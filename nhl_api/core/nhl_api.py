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

    def teams(self) -> Response:
        """
        Sends a GET request to retrieve team data from the NHL API.
        If no additional parameters are passed in, then all
        data on the present NHL teams will be returned.

        :return: data on all NHL teams
        """
        teams_endpoint = "teams"
        return self.get(teams_endpoint)
