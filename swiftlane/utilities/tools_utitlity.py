import base64
import datetime
import json

import firebase_admin
import requests
from firebase_admin import firestore

from swiftlane import settings


def get_access_token_from_refresh_token(refresh_token) -> str:
    """

    Defines end points for getting access token from refresh token

    **url : /api/v1/get_access_token/**

    **Method : POST**

    Content-Type: application/x-www-form-urlencoded

    request payload::

       "grant_type=refresh_token&refresh_token=tGzv3JOkF0XG5Qx2TlKWIA"

    Response data::

        {
           "access_token":"2YotnFZFEjr1zCsicMWpAA",
           "token_type":"example",
           "expires_in":3600,
           "refresh_token":"tGzv3JOkF0XG5Qx2TlKWIA",
        }
    :param refresh_token:
    :return:
    """
    url = "https://admin.swiftlane.com/api/v1/get_access_token/"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = f"grant_type=refresh_token&refresh_token={refresh_token}"
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code != 200:
        raise Exception(f"Failed to get access token: {response.text}")
    return response.json()["access_token"]


def get_firestore_client_based_on_project():
    firebase_app_name = "swiftlane-dev-instance"
    firestore_client = firestore.client(
        app=firebase_admin.get_app(name=firebase_app_name)
    )
    return firestore_client


def set_admin_tokens_in_firestore(doc_id: str, access_token: str, refresh_token: str):
    firestore_client = get_firestore_client_based_on_project()
    doc_ref = firestore_client.collection(
        "{}".format("sl-agents-admin-tokens")
    ).document("{}".format(doc_id))
    doc_ref.set(
        {
            # set ex
            "access_token": access_token,
            "refresh_token": refresh_token,
            "updated_at": datetime.datetime.utcnow(),
            "expires_at": datetime.datetime.utcnow() + datetime.timedelta(hours=3),
        }
    )


def get_access_tokens_from_firestore(doc_id: str):
    firestore_client = get_firestore_client_based_on_project()
    doc_ref = firestore_client.collection(
        "{}".format("sl-agents-admin-tokens")
    ).document("{}".format(doc_id))
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        return None


def check_and_refresh_access_token(doc_id: str):
    tokens = get_access_tokens_from_firestore(doc_id=doc_id)
    if not tokens:
        access_token = get_access_token_from_refresh_token(refresh_token=settings.ADMIN_REFRESH_TOKEN)
        set_admin_tokens_in_firestore(doc_id=doc_id, access_token=access_token,
                                      refresh_token=settings.ADMIN_REFRESH_TOKEN)
        return access_token
    return tokens.get("access_token")


async def post_internal_comment_on_ticket(ticket_id, body):
    zendesk_url = f"https://swiftlane.zendesk.com/api/v2/tickets/{ticket_id}"
    payload = {
        "ticket": {
            "comment": {
                "body": body,
                "public": False,
            },
        }
    }

    api_token = settings.ZENDESK_API_TOKEN
    agent_email = "nagesh@swiftlane.com"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {base64.b64encode(f'{agent_email}/token:{api_token}'.encode()).decode()}",
    }

    res = requests.put(
        zendesk_url,
        json=payload,
        headers=headers,
    )
    return {
        "status_code": res.status_code,
        "response": res.json(),
    }