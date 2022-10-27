import pytest
import responses

from nhl_data_py.nhl_api.nhl_api import NhlApi

BASE_URL = "https://statsapi.web.nhl.com/api/v1"


class TestNhlApi:
    """
    Tests the NhlApi class from the `nhl_data_py.nhl_api.nhl_api` module.
    """

    @responses.activate
    def test_get_200(self):
        responses.get(f"{BASE_URL}/random-endpoint", status=200, json={"test": "NHL"})
        r = NhlApi().get("random-endpoint")
        assert r.status_code == 200 and r.data == {"test": "NHL"}

    @responses.activate
    def test_get_404_no_json(self):
        responses.get(f"{BASE_URL}/random-endpoint", status=404)
        with pytest.raises(Exception):
            NhlApi().get("random-endpoint")
