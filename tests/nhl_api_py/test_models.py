from dataclasses import fields

import pandas as pd
import pytest

from nhl_api_py.core.models import Play, Team


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
        ],
        ids=["missing_parameters", "expected_kwarg", "non_real_kwarg", "nested_attr"],
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
