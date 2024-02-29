from flask import request
import logging

from werkzeug.exceptions import Unauthorized

from slagents import settings
import google.auth.transport.requests
from google.oauth2 import id_token

from slagents.utilities import exceptions

logger = logging.getLogger(__file__)


class RequiresServiceAccountAuth:
    def __init__(self, service_accounts=None):
        """
        This init method is called when you decorate a new method with RequiresAuth in the rest API
        This can be used to set the roles etc for the api access
        """
        self.service_accounts = service_accounts

    def __call__(self, f):
        """
        This is also called at decoration! Put any runtime logic in the wrapped function
        """

        def wrapped_f(*args, **kwargs):
            token = authenticate_service_account_token(
                service_accounts=self.service_accounts
            )
            wrapped_f.__name__ = f.__name__
            wrapped_f.__doc__ = f.__doc__
            kwargs["token"] = token
            return f(*args, **kwargs)

        return wrapped_f


def authenticate_service_account_token(service_accounts=None):
    audience = settings.HOST_NAME
    bearer_token = request.headers.get("Authorization")
    token = extract_auth_token_from_header()
    certs_url = "https://www.googleapis.com/oauth2/v1/certs"
    google_request = google.auth.transport.requests.Request()
    try:
        result = id_token.verify_token(token, google_request, certs_url=certs_url)
    except Exception as e:
        logger.info(f"Invalid token:{e}")
        raise exceptions.ApplicationErrorWithStatus200(message=f"Invalid token")
    if audience in result["aud"] and result["email"] in service_accounts:
        return bearer_token
    logger.info("aud or email not present in token for svc account")
    raise exceptions.ApplicationErrorWithStatus200(message=f"Unauthorized")


def extract_auth_token_from_header():
    auth_token = request.headers.get("Authorization")
    if auth_token:
        auth_token = auth_token.encode()
        if b"Basic" in auth_token:
            logger.error("Basic authentication not supported")
            raise Unauthorized("Invalid token header")
        access_token_parts = auth_token.split(b"Bearer ")
        if len(access_token_parts) != 2:
            raise Unauthorized("Invalid token header")
        auth_token = access_token_parts[1]
    else:
        raise Unauthorized("Invalid token header")
    return auth_token
