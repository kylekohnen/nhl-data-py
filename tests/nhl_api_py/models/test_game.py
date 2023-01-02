from dataclasses import fields

import pandas as pd
import pytest

from nhl_api_py.models.game import Boxscore, Game, Play
from nhl_api_py.models.team import Team


class TestPlay:
    """
    Tests the `nhl_api_py.core.models.Play` class
    """

    @pytest.mark.parametrize(
        "input, expected",
        [
            (dict(), Play()),
            ({"players": []}, Play(players=[])),
            ({"nonExistentField": "f"}, Play()),
            ({"result": {"event": "some_event"}}, Play(event="some_event")),
            ({"team": {"id": 1}}, Play(team=Team(id=1))),
        ],
        ids=[
            "missing_parameters",
            "expected_kwarg",
            "non_real_kwarg",
            "nested_attr",
            "teams_created",
        ],
    )
    def test_from_dict(self, input, expected):
        result = Play.from_dict(input)
        assert expected == result

    @pytest.mark.parametrize(
        "team_input, remove_na, expected",
        [
            (Play(), True, pd.Series()),
            (Play(), False, pd.Series(index=[f.name for f in fields(Play)])),
            (Play(players=[]), True, pd.Series({"players": []})),
            (
                Play(players=[]),
                False,
                pd.Series({**{f.name: None for f in fields(Play)}, "players": []}),
            ),
        ],
        ids=[
            "empty_remove_na",
            "empty_keep_na",
            "one_kwarg_remove_na",
            "one_kwarg_keep_na",
        ],
    )
    def test_to_series(self, team_input, remove_na, expected):
        result = team_input.to_series(remove_missing_values=remove_na)
        pd.testing.assert_series_equal(expected, result, check_dtype=False)


class TestGame:
    """
    Tests the `nhl_api_py.core.models.Game` class
    """

    @pytest.mark.parametrize(
        "input, expected",
        [
            (dict(), Game()),
            ({"gameData": {"game": {"pk": 0}}}, Game(pk=0)),
            ({"gameData": {"game": {"nonExistentField": "f"}}}, Game()),
            (
                {"GameData": {"teams": {"away": {"id": 1}}}},
                Game(away=Team(id=1)),
            ),
        ],
        ids=[
            "missing_parameters",
            "nested_expected_attr",
            "nested_nonreal_attr",
            "teams_created",
        ],
    )
    def test_from_dict(self, input, expected):
        result = Game.from_dict(input)
        assert expected == result

    @pytest.mark.parametrize(
        "game_input, remove_na, expected",
        [
            (Game(), True, pd.Series()),
            (
                Game(),
                False,
                pd.Series(index=[f.name for f in fields(Game)]),
            ),
            (Game(pk=0), True, pd.Series({"pk": 0})),
            (
                Game(pk=0),
                False,
                pd.Series({**{f.name: None for f in fields(Game)}, "pk": 0}),
            ),
        ],
        ids=[
            "empty_remove_na",
            "empty_keep_na",
            "one_kwarg_remove_na",
            "one_kwarg_keep_na",
        ],
    )
    def test_to_series(self, game_input, remove_na, expected):
        result = game_input.to_series(remove_missing_values=remove_na)
        pd.testing.assert_series_equal(expected, result, check_dtype=False)


class TestBoxscore:
    """
    Tests the `nhl_api_py.core.models.Boxscore` class
    """

    @pytest.mark.parametrize(
        "input, expected",
        [
            (dict(), Boxscore()),
            (
                {"teams": {"away": {"teamStats": dict()}}},
                Boxscore(away_team_stats=dict()),
            ),
            (
                {"teams": {"away": {"team": {"id": 1}}}},
                Boxscore(away_team=Team(id=1)),
            ),
        ],
        ids=[
            "missing_parameters",
            "empty_attribute",
            "teams_created",
        ],
    )
    def test_from_dict(self, input, expected):
        result = Boxscore.from_dict(input)
        assert expected == result

    @pytest.mark.parametrize(
        "game_input, remove_na, expected",
        [
            (Boxscore(), True, pd.Series()),
            (
                Boxscore(),
                False,
                pd.Series(index=[f.name for f in fields(Boxscore)]),
            ),
            (Boxscore(away_on_ice=[1]), True, pd.Series({"away_on_ice": [1]})),
            (
                Boxscore(away_on_ice=[1]),
                False,
                pd.Series(
                    {**{f.name: None for f in fields(Boxscore)}, "away_on_ice": [1]}
                ),
            ),
        ],
        ids=[
            "empty_remove_na",
            "empty_keep_na",
            "one_kwarg_remove_na",
            "one_kwarg_keep_na",
        ],
    )
    def test_to_series(self, game_input, remove_na, expected):
        result = game_input.to_series(remove_missing_values=remove_na)
        pd.testing.assert_series_equal(expected, result, check_dtype=False)
