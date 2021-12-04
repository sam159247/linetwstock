class CustomException(Exception):
    pass


class RequestMethodNotSupportError(CustomException):
    """Only support GET and POST HTTP request methods."""

    def __init__(self, method: str) -> None:
        msg = f"{method} request method is not supported. (GET and POST only)"
        super().__init__(msg)
