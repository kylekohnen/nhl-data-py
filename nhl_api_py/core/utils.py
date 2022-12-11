import re


def camel_to_snake_case(value: str) -> str:
    r_string = r"(?<!^)(?=[A-Z])"
    return re.sub(r_string, "_", value).lower()


def flatten_dictionary(d: dict, parent_key="", sep="_") -> dict:
    """
    Flattens a dictionary; takes any nested dictionaries and adds them to the top
    level. The key of nested dictionaries would be in the form of `parent_key`_`key`.

    :param d: the dictionary we want to flatten
    :param parent_key: helper kwarg to label what the key name should be, defaults to ""
    :param sep: what the separator is for the new keys, defaults to "_"
    :return: the dictionary inputted but flattened
    """
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dictionary(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)
