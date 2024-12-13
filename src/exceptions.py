class HttpError(Exception):
    pass


class HttpNotFoundError(HttpError):
    pass


class HttpBadRequestError(HttpError):
    pass


class HttpInternalServerError(HttpError):
    pass
