import pytest

from nhl_api_py.core.utils import camel_to_snake_case


@pytest.mark.parametrize(
    "test_value, expected",
    [
        ("", ""),
        ("is_snake_case", "is_snake_case"),
        ("camelCase", "camel_case"),
        ("simpletextthatisalllower", "simpletextthatisalllower"),
    ],
)
def test_camel_to_snake_case(test_value, expected):
    result = camel_to_snake_case(test_value)
    assert expected == result
