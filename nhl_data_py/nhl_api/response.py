from __future__ import annotations


class Response:
    """
    Represents responses received from the NHL API.
    Ordinary responses usually contain much more info than what is needed.
    This limits the responses to only contain the important information.
    """

    def __init__(self, status_code: int, data: dict):
        self.status_code = status_code
        self.data = data
