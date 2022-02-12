from flask import redirect, request, session, url_for
from flask import current_app as app
from flask import Blueprint
from requests_oauthlib import OAuth2Session
from api.oauth import client as accounts_client
import os
import functools
import json

oauth_bp = Blueprint("mmc_oauth", __name__)

# client secrets for zoho api
config = os.environ
client_id = config.get("ZOHO_CLIENT_ID")
client_secret = config.get("ZOHO_CLIENT_SECRET")
redirect_uri = config.get("ZOHO_REDIRECT_URI")
scope = config.get("ZOHO_SCOPE")


@oauth_bp.route("/")
def auth_grant():
    """Redirect the user to the zoho's accounts url
    with required oauth params. After the user logins,
    they are redirected to .oauth_callback route

    # https://www.zoho.com/crm/developer/docs/api/v2/auth-request.html
    """

    # redirect to .authorized if user's already logged in
    token = session.get("oauth_token", None)
    client = OAuth2Session(client_id, token=token)
    if client.authorized:
        return redirect(url_for(".authorized"))

    # redirect to zoho's accounts url if user's not logged in
    client = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)
    auth_url = "https://accounts.zoho.com/oauth/v2/auth"
    auth_url, state = client.authorization_url(auth_url, access_type="offline")

    # This is to protect against CSRF attacks
    session["oauth_state"] = state
    return redirect(auth_url)


@oauth_bp.route("/oauth", methods=["GET"])
def oauth_callback():
    """The user gets redirected here after logging in to their zoho account,
    with this redirection a grant token (code) is included in redirect url,
    we use this grant token to generate access_token

    # https://www.zoho.com/crm/developer/docs/api/v2/access-refresh.html
    """
    error = request.args.get("error")

    # user rejected the request
    if error:
        return {"response", error}

    account_url = request.args.get("accounts-server")
    client = OAuth2Session(client_id,
                           redirect_uri=redirect_uri,
                           state=session["oauth_state"])

    token = client.fetch_token(
        f"{account_url}/oauth/v2/token",
        client_secret=client_secret,
        authorization_response=request.url,
    )

    session["oauth_token"] = token
    return redirect(url_for(".user"))


def login_required(func):
    """A decrorator to secure the routes,
    just checks if user is logged in or not.
    If user is not logged returns 401.
    Adds USER & ZUID to session, if
    USER key is not present in session.
    """

    @functools.wraps(func)
    def inner(*args, **kwargs):
        if "oauth_token" not in session:
            return {"message": "unauthorized"}, 401

        if "USER" not in session:
            token = session.get("oauth_token", None)
            session["USER"] = accounts_client.get_currentuser(token)
            session["ZUID"] = accounts_client.get_zuid(token)
        return func(*args, **kwargs)

    return inner


@oauth_bp.route("/user")
@login_required
def user():
    app.logger.info(f"SESSION OBJECT -> {json.dumps(session, indent=4)}")
    token = session.get("oauth_token", None)
    if "USER" in session:
        app.logger.info("taking user from session")
        return session.get("USER"), 200

    # we fetch from tp if user object is not in session
    session["USER"] = accounts_client.get_currentuser(token)
    return session["USER"]
