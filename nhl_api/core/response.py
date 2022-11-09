"""
Represents a simple Response received from the NHL API.
"""
from __future__ import annotations

from requests import Response as RequestResponse


class Response:
    """
    Represents responses received from the NHL API.
    Ordinary responses usually contain much more info than what is needed.
    This limits the responses to only contain the important information.
    """

    def __init__(self, status_code: int, data: dict):
        self.status_code = status_code
        self.data = data

    @classmethod
    def from_requests(cls, response: RequestResponse) -> Response:
        """
        Utility method to create a response object from the `requests` Response
        object.

        :param response: the response object from the `requests` package
        :return: NHL API Response Object
        """
        assert isinstance(response, RequestResponse), f"{response} not of proper type."
        return cls(response.status_code, response.json())
