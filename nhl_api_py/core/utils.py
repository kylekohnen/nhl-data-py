import re


def camel_to_snake_case(value: str) -> str:
    r_string = r"(?<!^)(?=[A-Z])"
    return re.sub(r_string, "_", value).lower()


def convert_keys_to_snake_case(d: dict) -> dict:
    """
    Converts all the keys in a given dictionary to snake case.
    It will traverse through nested dictionaries as well.

    :param d: the dictionary we want to convert keys for
    :return: the same dictionary with converted keys
    """
    new_data = {}
    for k, v in d.items():
        new_key = camel_to_snake_case(k)
        if isinstance(v, dict):
            new_data[new_key] = convert_keys_to_snake_case(v)
        else:
            new_data[new_key] = v
    return new_data
