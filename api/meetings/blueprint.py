import functools
from flask import Blueprint, request, session
from api.meetings import client
from api.meetings.payload import Session
from flask import current_app as app

meetings_bp = Blueprint("mmc_meetings", __name__)


def login_required(func):
    """A decorator to secure the routes,
    just checks if user is logged in or not.
    If user is not logged in it returns 401.
    If ZSOID is not present in session, fetches
    it and adds to session
    """

    @functools.wraps(func)
    def inner(*args, **kwargs):
        if "oauth_token" not in session:
            return {"message": "unauthorized"}, 401

        if "ZSOID" not in session:
            app.logger.info("taking org from session")

            # token & zuid is set by oauth endpoint after authenticating
            token = session.get("oauth_token", None)
            ZUID = session["ZUID"]

            # fetch zsoid & store it for later use
            session["ZSOID"] = client.get_zsoid(token, ZUID)
        else:
            app.logger.info("Taking ZSOID from session")

        return func(*args, **kwargs)

    return inner


@meetings_bp.route("/", methods=['GET'])
@login_required
def get_meetings():
    """Endpoint that returns all the meetings of current user
    """
    token = session.get("oauth_token", None)
    ZSOID = session.get("ZSOID", None)
    assert type(ZSOID) == int
    return client.get_meetings(token, ZSOID)


@meetings_bp.route("/", methods=['POST'])
@login_required
def create_meeting():
    """Endpoint to create a new meetings,
    The payload should have same schema as
    api.meetings.payload.Session
    """
    try:
        js = Session.from_json(request.data)
        token = session.get("oauth_token", None)
        ZSOID = session.get("ZSOID", None)
        assert type(ZSOID) == int
        return client.create_meeting(token, ZSOID, js)
    except KeyError as e:
        return dict(error="required key missing", key=e.args[0]), 400


@meetings_bp.route("/<string:key>", methods=['GET'])
@login_required
def get_meeting(key):
    """Endpoint to get meeting by meeting key
    """
    token = session.get("oauth_token", None)
    ZSOID = session.get("ZSOID", None)
    assert type(ZSOID) == int
    return client.get_meeting(token, ZSOID, key)
