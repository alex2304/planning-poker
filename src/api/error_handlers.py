from exceptions import HttpBadRequestError, HttpInternalServerError, HttpNotFoundError
from flask import jsonify

from . import bp


def default_error_handler(message, code):
    return jsonify({"error": message}), code


@bp.errorhandler(HttpNotFoundError)
def handle_not_found(error):
    return default_error_handler(error, 404)


@bp.errorhandler(HttpBadRequestError)
def handle_bad_request(error):
    return default_error_handler(error, 400)


@bp.errorhandler(HttpInternalServerError)
def handle_internal_server_error(error):
    return default_error_handler(error, 500)
