import pytest

from nhl_api_py.core.models import Team


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
    def test_from_kwargs(self, input, expected):
        result = Team.from_kwargs(**input)
        assert expected == result
