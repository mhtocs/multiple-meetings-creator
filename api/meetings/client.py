"""Provides API to interact with zoho-meetings
API using a oauth2

A oauth2 token is required to use the API
"""
from typing import Dict
from requests_oauthlib import OAuth2Session
from .payload import Session
import os
import json

MEETINGS_URL = "https://meeting.zoho.com/api"
CLIENT_ID = os.environ.get("ZOHO_CLIENT_ID")
HEADERS = {"X-ZSOURCE": os.environ.get("ZOHO_X_ZSOURCE")}


def get_meetings(token: Dict, zsoid: int) -> Dict:
    """Get list of all upcoming meetings for the current user"""
    client = OAuth2Session(CLIENT_ID, token=token)
    param = "listtype=upcoming&sessionType=meeting"
    return client.get(
        f"{MEETINGS_URL}/v0/{zsoid}/sessions.json?{param}").json()


def get_meeting(token: Dict, zsoid: int, meeting_key: str) -> Dict:
    """Get details of a specific meetings of current user"""
    client = OAuth2Session(CLIENT_ID, token=token)
    json = client.get(
        f"{MEETINGS_URL}/v0/{zsoid}/sessions/{meeting_key}.json").json()
    return json


def delete_meeting(token: Dict, meeting_key: str) -> bool:
    pass


def create_meeting(token: Dict, zsoid: int, payload: Session) -> bool:
    """Create a meeting using the given provided params in
    payload
    """
    client = OAuth2Session(CLIENT_ID, token=token)
    print({"session": json.loads(payload.to_json())})
    js = client.post(f"{MEETINGS_URL}/v1/{zsoid}/sessions.json",
                     json={
                         "session": payload.to_json()
                     }).json()

    return js


def update_meeting(token: Dict, payload: Session) -> bool:
    pass


def get_zsoid(token: Dict, zuid: int) -> int:
    """Fetch ZSOID i.e Org ID of Org to which current
    user belongs to
    """
    client = OAuth2Session(CLIENT_ID, token=token)
    json = client.get(
        f"{MEETINGS_URL}/v0/{zuid}/org.json",
        headers=HEADERS,
    ).json()

    zsoid = json["org"]["zsoid"]
    assert type(zsoid) == int
    return zsoid
