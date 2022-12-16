"""
Tests the `nhl_api.core.nhl_api` module.
"""
from contextlib import nullcontext

import pytest
import responses

from nhl_api_py.core.api import NhlApi, ResponseError
from nhl_api_py.core.models import BoxscoreGame, GeneralGame, Team


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
    @pytest.mark.parametrize(
        "status, error_raise",
        [
            (200, nullcontext()),
            (300, nullcontext()),
            (400, pytest.raises(ResponseError)),
            (500, pytest.raises(ResponseError)),
        ],
        ids=["status=200", "status=300", "status=400", "status=500"],
    )
    @pytest.mark.parametrize(
        "team_ids", [None, 1, [1, 2, 3]], ids=(lambda x: f"team_ids={x}")
    )
    @pytest.mark.parametrize("season", [None, 2000], ids=(lambda x: f"season={x}"))
    @pytest.mark.parametrize(
        "roster", [None, True, False], ids=(lambda x: f"roster={x}")
    )
    @pytest.mark.parametrize("stats", [None, True, False], ids=(lambda x: f"stats={x}"))
    @pytest.mark.parametrize(
        "resp_data, expected",
        [
            ({"teams": []}, []),
            (dict(), []),
            ({"teams": [dict()]}, [Team()]),
            ({"teams": [{"id": 1}]}, [Team(id=1)]),
            ({"teams": [{"not_valid_key": "ooga"}]}, [Team()]),
            (
                {"teams": [{"id": {"key1": None, "key2": "hi"}}]},
                [Team(id={"key1": None, "key2": "hi"})],
            ),
        ],
        ids=[
            "empty_data_with_team_key",
            "empty_data",
            "empty_team_data",
            "team_with_id",
            "team_with_unknown_key",
            "team_with_nested_dict",
        ],
    )
    def test_teams(
        self, status, error_raise, team_ids, season, roster, stats, resp_data, expected
    ):
        responses.get(
            f"{TestNhlApi.BASE_URL}/teams",
            status=status,
            json=resp_data,
        )
        with error_raise:
            result = NhlApi().teams(
                team_ids=team_ids, season=season, roster=roster, stats=stats
            )
            assert result == expected

    @responses.activate
    @pytest.mark.parametrize(
        "status, status_error",
        [
            (200, nullcontext()),
            (300, nullcontext()),
            (400, pytest.raises(ResponseError)),
            (500, pytest.raises(ResponseError)),
        ],
        ids=["status=200", "status=300", "status=400", "status=500"],
    )
    @pytest.mark.parametrize(
        "boxscore, linescore, game_error",
        [
            (False, False, nullcontext()),
            (False, True, nullcontext()),
            (True, False, nullcontext()),
            (True, True, pytest.raises(ValueError)),
        ],
    )
    def test_games(
        self,
        status,
        status_error,
        boxscore,
        linescore,
        game_error,
    ):
        if boxscore:
            url = "boxscore"
            resp_data = {}
            expected = BoxscoreGame()
        elif linescore:
            url = "linescore"
            resp_data = {"game": "random_data_here"}
            expected = resp_data
        else:
            url = "feed/live"
            resp_data = {"gameData": {"game": {"pk": 0}}}
            expected = GeneralGame(pk=0)
        responses.get(
            f"{TestNhlApi.BASE_URL}/game/2017020001/" + url,
            status=status,
            json=resp_data,
        )
        with game_error:
            with status_error:
                result = NhlApi().game(
                    game_id=2017020001, boxscore=boxscore, linescore=linescore
                )
                assert result == expected
