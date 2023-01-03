import pytest

from nhl_api_py.models.schedule import ScheduleDate


class TestScheduleDate:
    """
    Tests the `nhl_api_py.models.game.Play` class
    """

    @pytest.mark.parametrize(
        "input, expected",
        [
            (dict(), ScheduleDate()),
            ({"non_real_kwarg": 55}, ScheduleDate()),
            ({"date": "2000-01-01"}, ScheduleDate(date="2000-01-01")),
            ({"games": []}, ScheduleDate()),
        ],
        ids=["missing_parameters", "non_real_kwarg", "real_kwarg", "games_nested_list"],
    )
    def test_from_dict(self, input, expected):
        result = ScheduleDate.from_dict(input)
        assert expected == result
