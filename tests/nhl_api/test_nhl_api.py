"""
Tests the `nhl_api.core.nhl_api` module.
"""
import pytest
import responses

from nhl_api.core.nhl_api import NhlApi, ResponseError


class TestNhlApi:
    """
    Tests the NhlApi class from the `nhl_data_py.nhl_api.nhl_api` module.
    """

    BASE_URL = "https://statsapi.web.nhl.com/api/v1"

    @responses.activate
    def test_get_200(self):
        """
        Tests `NhlApi.get` method on an endpoint that would return data with
        code 200.
        """
        responses.get(
            f"{TestNhlApi.BASE_URL}/random-endpoint", status=200, json={"test": "NHL"}
        )
        resp = NhlApi().get("random-endpoint")
        assert resp.status_code == 200 and resp.data == {"test": "NHL"}

    @responses.activate
    def test_404_exception_thrown(self):
        """
        Tests `NhlApi.get` method on an endpoint that would return no data with
        code 404
        """
        responses.get(f"{TestNhlApi.BASE_URL}/random-endpoint", status=404)
        with pytest.raises(ResponseError):
            NhlApi().get("random-endpoint")

    @responses.activate
    @pytest.mark.parametrize("expected_status", [200, 300, 400, 500])
    def test_teams_default_behaviour(self, expected_status):
        """
        Tests the `NhlApi.teams` method's default behaviour.
        """
        responses.get(
            f"{TestNhlApi.BASE_URL}/teams", status=expected_status, json={"teams": {}}
        )
        if expected_status < 400:
            resp = NhlApi().teams()
            assert resp.status_code == expected_status and resp.data == {"teams": {}}
        else:
            with pytest.raises(ResponseError):
                NhlApi().teams()
