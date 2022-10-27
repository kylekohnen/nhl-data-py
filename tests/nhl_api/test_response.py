import pytest
import requests
import responses

from nhl_data_py.nhl_api.response import Response


class TestResponse:
    """
    Tests the NHL API Response class.
    """

    def test_from_requests_incorrect_type(self):
        wrong = dict()
        with pytest.raises(AssertionError) as error:
            Response.from_requests(wrong)
        assert f"{wrong} not of proper type" in str(error.value)

    @responses.activate
    def test_from_requests_proper_response(self):
        responses.get(
            "https://statsapi.web.nhl.com/api/v1/random-endpoint", json={"msg": "NHL"}
        )
        resp = requests.get("https://statsapi.web.nhl.com/api/v1/random-endpoint")
        result = Response.from_requests(resp)
        assert result.status_code == 200
        assert result.data == {"msg": "NHL"}
