from requests import request, Response
import error_exceptions


class NhlApi:
    """
    Class representing the NHL API.
    """

    _base_url: str = "https://statsapi.web.nhl.com/api"

    def __init__(self, api_version: int = 1):
        self.url: str = f"{NhlApi._base_url}/v{api_version}"

    def _request(self, http_method: str, endpoint: str) -> Response:
        """
        Sends an HTTP request to the NHL API.

        :param http_method: the request method used
        :param endpoint: where we want to connect to with the API
        :return: the data / response returned by the API
        """
        url = f"{self.url}/{endpoint}"
        data = request(http_method, url, timeout=60)
        if (data.status_code//100 == 4):
            raise error_exceptions.ClientError( 
                f"HTTP status code: {data.status_code}"
            )
        elif (data.status_code//100 == 5):
            raise error_exceptions.ServerError( 
                f"HTTP status code: {data.status_code}"
            )
        else:
            return data

    def get(self, endpoint: str) -> Response:
        """
        Sends a GET request to a specific endpoint to the NHL API.

        :param endpoint: where we want to connect to with the API
        :return: the data / response returned by the API
        """
        return self._request("GET", endpoint)
