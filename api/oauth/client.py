"""Provides API to interact with zoho-accounts
API using a oauth2

A oauth2 token is required to use the API

token is a dict generated in api.oauth.blueprint`
"""

from typing import Dict
from requests_oauthlib import OAuth2Session
import os

ACCOUNTS_URL = "https://accounts.zoho.com"
CLIENT_ID = os.environ.get("ZOHO_CLIENT_ID")


def get_zuid(token: Dict) -> int:
    """Fetch ZUID of current user"""
    client = OAuth2Session(CLIENT_ID, token=token)
    user = client.get(f"{ACCOUNTS_URL}/oauth/user/info").json()
    zuid = user["ZUID"]
    assert type(zuid) == int
    return zuid


def get_currentuser(token: Dict) -> Dict:
    """Fetch info of current user"""
    client = OAuth2Session(CLIENT_ID, token=token)
    user = client.get(f"{ACCOUNTS_URL}/oauth/user/info").json()
    return user
