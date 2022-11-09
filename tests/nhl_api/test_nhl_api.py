"""
Tests the `nhl_data_py.nhl_api.nhl_api` module.
"""
import pytest
import responses

from nhl_data_py.nhl_api.nhl_api import NhlApi
from nhl_data_py.nhl_api.nhl_api import ResponseError

BASE_URL = "https://statsapi.web.nhl.com/api/v1"


class TestNhlApi:
    """
    Tests the NhlApi class from the `nhl_data_py.nhl_api.nhl_api` module.
    """

    @responses.activate
    def test_get_200(self):
        """
        Tests `NhlApi.get` method on an endpoint that would return data with
        code 200.
        """
        responses.get(f"{BASE_URL}/random-endpoint", status=200, json={"test": "NHL"})
        resp = NhlApi().get("random-endpoint")
        assert resp.status_code == 200 and resp.data == {"test": "NHL"}

    @responses.activate
    def test_404_exception_thrown(self):
        """
        Tests `NhlApi.get` method on an endpoint that would return no data with
        code 404
        """
        responses.get(f"{BASE_URL}/random-endpoint", status=404)
        with pytest.raises(ResponseError) as error:
            NhlApi().get("random-endpoint")
        
