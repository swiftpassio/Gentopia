import logging

import firebase_admin
import flask
from flask import jsonify
from flask_restful import Api

from slagents import settings
from slagents.controllers.zendesk_support_resource import ZendeskSupportCloudTaskHandler
from slagents.utilities import exceptions


class SwiftlaneAPI(Api):
    def handle_error(self, e):
        custom_handler = exceptions.EXTERNAL_EXCEPTION_HANDLERS.get(e.__class__)
        if custom_handler:
            return custom_handler(e)

        if not isinstance(e, exceptions.SwiftpassError):
            return super().handle_error(e)
        response = jsonify(e.to_dict())
        response.status_code = e.status_code
        return response


def create_app(test_config=None):
    app = flask.Flask("swiftlane")
    if test_config is None:
        app.config.from_object(settings)

    else:
        app.config.from_object(test_config)
    api = SwiftlaneAPI(app)

    api.add_resource(ZendeskSupportCloudTaskHandler, "/api/v1/zendesk-support-ai-agent")

    @app.route("/healthz")
    def health():
        return "ok!"

    if settings.INIT_FIREBASE:
        if len(firebase_admin._apps) == 0:
            firebase_admin.initialize_app()
    return app


app = None
if not app:
    app = create_app()


@property
def get_current_app():
    global app
    if not app:
        app = create_app()
    return app


def set_current_app(new_app):
    global app
    app = new_app
