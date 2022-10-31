class APIException(Exception):
    """Raise for 4xx and 5xx HTTP status codes."""
    pass

class ClientError(APIException):
    """Raise for 4xx HTTP status codes."""
    pass

class ServerError(APIException):
    """Raise for 5xx HTTP status codes."""
    pass