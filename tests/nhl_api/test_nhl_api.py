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
    @pytest.mark.parametrize("expected_status", [200, 300, 400, 500])
    def test_get_json_is_available(self, expected_status):
        """
        Tests `NhlApi.get` method on an endpoint that would return JSON data.
        """
        responses.get(
            f"{TestNhlApi.BASE_URL}/random-endpoint",
            status=expected_status,
            json={"test": "NHL"},
        )
        if expected_status < 400:
            resp = NhlApi().get("random-endpoint")
            assert resp.status_code == expected_status and resp.data == {"test": "NHL"}
        else:
            with pytest.raises(ResponseError) as error:
                NhlApi().get("random-endpoint")
            assert error.match(f"GET method returns HTTP status code {expected_status}")

    @responses.activate
    @pytest.mark.parametrize("expected_status", [200, 300, 400, 500])
    def test_get_json_is_unavailable(self, expected_status):
        """
        Tests `NhlApi.get` method on an endpoint that does not return JSON data.
        """
        responses.get(
            f"{TestNhlApi.BASE_URL}/random-endpoint",
            status=expected_status,
            body="test: NHL",
        )
        if expected_status < 400:
            resp = NhlApi().get("random-endpoint")
            assert resp.status_code == expected_status and resp.data == {}
        else:
            with pytest.raises(ResponseError) as error:
                NhlApi().get("random-endpoint")
            assert error.match(f"GET method returns HTTP status code {expected_status}")

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
