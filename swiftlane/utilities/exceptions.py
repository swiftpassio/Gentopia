from flask import jsonify
from marshmallow import ValidationError


class SwiftpassError(Exception):
    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv


class NotFoundError(SwiftpassError):
    status_code = 404


class BadRequestError(SwiftpassError):
    status_code = 400


class AuthError(SwiftpassError):
    status_code = 403


class SwiftpassValidationError(SwiftpassError):
    status_code = 422


class ApplicationErrorWithStatus200(SwiftpassError):
    status_code = 200


def make_standard_handler(status_code):
    def handler(e):
        response = jsonify(e.args)
        response.status_code = status_code
        return response

    return handler


EXTERNAL_EXCEPTION_HANDLERS = {ValidationError: make_standard_handler(422)}