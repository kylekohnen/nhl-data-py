from dataclasses import fields

import pandas as pd
import pytest

from nhl_api_py.core.models import BoxscoreGame, GeneralGame, Play, Team


class TestTeam:
    """
    Tests the `nhl_api_py.core.models.Team` class.
    """

    @pytest.mark.parametrize(
        "input, expected",
        [
            (dict(), Team()),
            ({"name": "Team Name"}, Team(name="Team Name")),
            ({"nonExistentField": "f"}, Team()),
        ],
        ids=["missing_parameters", "expected_kwarg", "non_real_kwarg"],
    )
    def test_from_dict(self, input, expected):
        result = Team.from_dict(input)
        assert expected == result

    @pytest.mark.parametrize(
        "team_input, remove_na, expected",
        [
            (Team(), True, pd.Series()),
            (Team(), False, pd.Series(index=[f.name for f in fields(Team)])),
            (Team(name="Team Name"), True, pd.Series({"name": "Team Name"})),
            (
                Team(name="Team Name"),
                False,
                pd.Series(
                    {**{f.name: None for f in fields(Team)}, "name": "Team Name"}
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
    def test_to_series(self, team_input, remove_na, expected):
        result = team_input.to_series(remove_missing_values=remove_na)
        pd.testing.assert_series_equal(expected, result, check_dtype=False)


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


class TestGeneralGame:
    """
    Tests the `nhl_api_py.core.models.GeneralGame` class
    """

    @pytest.mark.parametrize(
        "input, expected",
        [
            (dict(), GeneralGame()),
            ({"gameData": {"game": {"pk": 0}}}, GeneralGame(pk=0)),
            ({"gameData": {"game": {"nonExistentField": "f"}}}, GeneralGame()),
            (
                {"GameData": {"teams": {"away": {"id": 1}}}},
                GeneralGame(away=Team(id=1)),
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
        result = GeneralGame.from_dict(input)
        assert expected == result

    @pytest.mark.parametrize(
        "game_input, remove_na, expected",
        [
            (GeneralGame(), True, pd.Series()),
            (
                GeneralGame(),
                False,
                pd.Series(index=[f.name for f in fields(GeneralGame)]),
            ),
            (GeneralGame(pk=0), True, pd.Series({"pk": 0})),
            (
                GeneralGame(pk=0),
                False,
                pd.Series({**{f.name: None for f in fields(GeneralGame)}, "pk": 0}),
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


class TestBoxscoreGame:
    """
    Tests the `nhl_api_py.core.models.BoxscoreGame` class
    """

    @pytest.mark.parametrize(
        "input, expected",
        [
            (dict(), BoxscoreGame()),
            ({"officials": {}}, BoxscoreGame(officials={})),
            ({"teams": {"away": {"id": 1}}}, BoxscoreGame(away=Team(id=1))),
        ],
        ids=[
            "missing_parameters",
            "empty_dict",
            "teams_created",
        ],
    )
    def test_from_dict(self, input, expected):
        result = BoxscoreGame.from_dict(input)
        assert expected == result

    @pytest.mark.parametrize(
        "game_input, remove_na, expected",
        [
            (BoxscoreGame(), True, pd.Series()),
            (
                BoxscoreGame(),
                False,
                pd.Series(index=[f.name for f in fields(BoxscoreGame)]),
            ),
            (BoxscoreGame(officials=dict()), True, pd.Series({"officials": {}})),
            (
                BoxscoreGame(officials=dict()),
                False,
                pd.Series(
                    {**{f.name: None for f in fields(BoxscoreGame)}, "officials": {}}
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
