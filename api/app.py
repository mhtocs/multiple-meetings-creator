from flask import Flask, session
from dotenv import load_dotenv
from config import Config
from api.oauth import oauth_bp
from api.meetings import meetings_bp
from api.core import core_bp
from api import celery, init_celery
from flask_session import Session

import coloredlogs


def create_app():
    load_dotenv()
    app = Flask(__name__)
    coloredlogs.install(logger=app.logger)
    app.url_map.strict_slashes = True
    app.config.from_object(Config)
    init_celery(app, celery)
    Session(app)

    app.register_blueprint(oauth_bp)
    app.register_blueprint(meetings_bp, url_prefix="/api/meetings")
    app.register_blueprint(core_bp, url_prefix="/api/core")

    @app.route("/no_login")
    def no_login():
        print(session)
        return "You are not logged in <br><a href = '/login'>" + "click here to log in</a>"

    @app.route("/")
    def index():
        return "Hello world!"

    return app
