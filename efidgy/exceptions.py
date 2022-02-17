class EfidgyException(Exception):
    pass


class BadRequest(EfidgyException):
    pass


class ValidationError(BadRequest):
    pass


class AuthenticationFailed(EfidgyException):
    pass


class PermissionDeined(EfidgyException):
    pass


class NotFound(EfidgyException):
    pass


class MethodNotAllowed(EfidgyException):
    pass


class InternalServerError(EfidgyException):
    pass
