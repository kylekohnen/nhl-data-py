"""
Tests the `nhl_api.core.nhl_api` module.
"""
from contextlib import nullcontext

import pytest
import responses

from nhl_api_py.core.api import NhlApi, ResponseError
from nhl_api_py.core.models import Boxscore, Game, Play, Team


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
        "resp_data, expected",
        [
            ({"gameData": {"game": {"pk": None}}}, Game()),
            ({"gameData": {"game": {"pk": 2017020001}}}, Game(pk=2017020001)),
            ({"GameData": {"not_valid_key": "f"}}, Game()),
        ],
        ids=[
            "empty_data_with_game_id",
            "game_with_id",
            "team_with_unknown_key",
        ],
    )
    def test_game(
        self,
        status,
        status_error,
        resp_data,
        expected,
    ):
        responses.get(
            f"{TestNhlApi.BASE_URL}/game/2017020001/feed/live",
            status=status,
            json=resp_data,
        )
        with status_error:
            result = NhlApi().game(game_id=2017020001)
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
        "resp_data, expected",
        [
            (
                {"teams": {"away": {"teamStats": dict()}}},
                Boxscore(away_team_stats=dict()),
            ),
            ({"not_valid_key": "f"}, Boxscore()),
            ({"teams": {"away": {"team": {"id": 1}}}}, Boxscore(away_team=Team(id=1))),
        ],
        ids=[
            "empty_data",
            "team_with_unknown_key",
            "team_created",
        ],
    )
    def test_boxscore(
        self,
        status,
        status_error,
        resp_data,
        expected,
    ):
        responses.get(
            f"{TestNhlApi.BASE_URL}/game/2017020001/boxscore",
            status=status,
            json=resp_data,
        )
        with status_error:
            result = NhlApi().boxscore(game_id=2017020001)
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
        "scoring_plays_only, penalty_plays_only, resp_data, expected",
        [
            (False, False, {"liveData": {"plays": dict()}}, []),
            (
                False,
                False,
                {
                    "liveData": {
                        "plays": {
                            "allPlays": [{"result": {"event": None}}],
                            "scoringPlays": [0],
                            "penaltyPlays": [0],
                        }
                    }
                },
                [Play(event=None)],
            ),
            (
                False,
                False,
                {
                    "liveData": {
                        "plays": {
                            "allPlays": [
                                {"result": {"event": "event0"}},
                                {"result": {"event": "event1"}},
                            ],
                            "scoringPlays": [0],
                            "penaltyPlays": [1],
                        }
                    }
                },
                [Play(event="event0"), Play(event="event1")],
            ),
            (
                False,
                True,
                {
                    "liveData": {
                        "plays": {
                            "allPlays": [
                                {"result": {"event": "event0"}},
                                {"result": {"event": "event1"}},
                            ],
                            "scoringPlays": [0],
                            "penaltyPlays": [1],
                        }
                    }
                },
                [Play(event="event1")],
            ),
            (
                True,
                False,
                {
                    "liveData": {
                        "plays": {
                            "allPlays": [
                                {"result": {"event": "event0"}},
                                {"result": {"event": "event1"}},
                            ],
                            "scoringPlays": [0],
                            "penaltyPlays": [1],
                        }
                    }
                },
                [Play(event="event0")],
            ),
            (
                True,
                True,
                {
                    "liveData": {
                        "plays": {
                            "allPlays": [
                                {"result": {"event": "event0"}},
                                {"result": {"event": "event1"}},
                            ],
                            "scoringPlays": [0],
                            "penaltyPlays": [1],
                        }
                    }
                },
                [Play(event="event0"), Play(event="event1")],
            ),
        ],
        ids=[
            "play_data_missing",
            "play_data_empty",
            "get_all_plays",
            "get_penalty_plays",
            "get_scoring_plays",
            "get_penalty_scoring_plays",
        ],
    )
    def test_plays(
        self,
        status,
        status_error,
        scoring_plays_only,
        penalty_plays_only,
        resp_data,
        expected,
    ):
        responses.get(
            f"{TestNhlApi.BASE_URL}/game/2017020001/feed/live",
            status=status,
            json=resp_data,
        )
        with status_error:
            result = NhlApi().plays(
                game_id=2017020001,
                scoring_plays_only=scoring_plays_only,
                penalty_plays_only=penalty_plays_only,
            )
            assert result == expected
