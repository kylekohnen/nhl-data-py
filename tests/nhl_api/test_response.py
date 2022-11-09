"""
Tests the `nhl_data_py.nhl_api.response` module.
"""
import pytest
import requests
import responses

from nhl_api.core.response import Response


class TestResponse:
    """
    Tests the NHL API Response class.
    """

    def test_from_requests_incorrect_type(self):
        """
        Tests `Response.from_requests` method when an improper type is passed.
        """
        wrong = {}
        with pytest.raises(AssertionError) as error:
            Response.from_requests(wrong)
        assert f"{wrong} not of proper type" in str(error.value)

    @responses.activate
    def test_from_requests_proper_response(self):
        """
        Tests `Response.from_requests` method when the `request.Response` object
        is passed.
        """
        responses.get(
            "https://statsapi.web.nhl.com/api/v1/random-endpoint", json={"msg": "NHL"}
        )
        resp = requests.get(
            "https://statsapi.web.nhl.com/api/v1/random-endpoint", timeout=10
        )
        result = Response.from_requests(resp)
        assert result.status_code == 200
        assert result.data == {"msg": "NHL"}
