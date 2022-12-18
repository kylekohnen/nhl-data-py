import pytest

from nhl_api_py.core.utils import (
    append_string_to_keys,
    camel_to_snake_case,
    convert_keys_to_snake_case,
)


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


@pytest.mark.parametrize(
    "test_value, expected",
    [
        (dict(), dict()),
        (
            {"key1": None, "key2": None},
            {"append_key1": None, "append_key2": None},
        ),
        (
            {"key1": {"nested1": None, "nested2": None}},
            {"append_key1": {"nested1": None, "nested2": None}},
        ),
    ],
    ids=["empty_dict", "normal_level", "nested_dict"],
)
def test_append_string_to_keys(test_value, expected):
    result = append_string_to_keys("append_", test_value)
    assert expected == result
