# Error codes: https://www.w3.org/Protocols/HTTP/HTRESP.html
# Custom exceptions: https://www.programiz.com/python-programming/user-defined-exception

class APIException(Exception):
    pass

class NullDatabase(APIException):
    """Raise when user requests a database that does not exist [404 error]"""
    pass

class APIError(APIException):
    """Raise for error code 500"""
    pass

