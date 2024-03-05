from fastapi import Depends, Header, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from flask import request
import logging
from werkzeug.exceptions import Unauthorized

from swiftlane import settings
import google.auth.transport.requests
from google.oauth2 import id_token
from fastapi import status
from swiftlane.utilities import exceptions

logger = logging.getLogger(__file__)


def service_account_auth(service_accounts=None):
    def get_user_data(authorization: str = Header(None)):
        if not authorization:
            raise HTTPException(status_code=401, detail="No authorization token provided")
        authorization = extract_auth_token_from_header(authorization)
        authenticate_service_account_token(service_accounts, authorization)

    return get_user_data



def authenticate_service_account_token(service_accounts=None, token=None):
    audience = settings.HOST_NAME
    certs_url = "https://www.googleapis.com/oauth2/v1/certs"
    google_request = google.auth.transport.requests.Request()
    try:
        result = id_token.verify_token(token, google_request, certs_url=certs_url)
    except Exception as e:
        logger.info(f"Invalid token:{e}")
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Token expired or invalid, please log in",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if audience in result["aud"] and result["email"] in service_accounts:
        return token
    logger.info("aud or email not present in token for svc account")
    raise HTTPException(
        status_code=status.HTTP_200_OK,
        detail="Unauthorized",
        headers={"WWW-Authenticate": "Bearer"},
    )


def extract_auth_token_from_header(auth_token):
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
