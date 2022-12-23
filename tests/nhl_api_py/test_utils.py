import pytest

from nhl_api_py.core.utils import camel_to_snake_case, convert_keys_to_snake_case


@pytest.mark.parametrize(
    "test_value, expected",
    [
        ("", ""),
        ("is_snake_case", "is_snake_case"),
        ("camelCase", "camel_case"),
        ("simpletextthatisalllower", "simpletextthatisalllower"),
        ("snake_thenCamelCase", "snake_then_camel_case"),
    ],
)
def test_camel_to_snake_case(test_value, expected):
    result = camel_to_snake_case(test_value)
    assert expected == result


@pytest.mark.parametrize(
    "test_value, expected",
    [
        (dict(), dict()),
        (
            {"helloWorld": None, "fine_world": None},
            {"hello_world": None, "fine_world": None},
        ),
        (
            {"hiThere": {"nestedHiThere": None, "nested_fine": None}},
            {"hi_there": {"nested_hi_there": None, "nested_fine": None}},
        ),
    ],
    ids=["empty_dict", "normal_level", "nested_dict"],
)
def test_convert_keys_to_snake_case(test_value, expected):
    result = convert_keys_to_snake_case(test_value)
    assert expected == result
