class APIException(Exception):
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code


class NotFoundError(APIException):
    def __init__(self, message="Resource not found"):
        super().__init__(message, 404)


class UnauthorizedError(APIException):
    def __init__(self, message="Unauthorized"):
        super().__init__(message, 401)


class ForbiddenError(APIException):
    def __init__(self, message="Forbidden"):
        super().__init__(message, 403)
