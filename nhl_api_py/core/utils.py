import re


def camel_to_snake_case(value: str) -> str:
    r_string = r"(?<!^)(?=[A-Z])"
    return re.sub(r_string, "_", value).lower()
