from flask import Flask
from dotenv import load_dotenv
from config import Config
from api.oauth import oauth_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(oauth_bp)

    @app.route("/")
    def index():
        return "Hello world!"

    return app
