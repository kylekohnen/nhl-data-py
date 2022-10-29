

class APIException(Exception):
    pass

class NullDatabase(APIException):
    """Raise when user requests a database that does not exist."""
    pass

