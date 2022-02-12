from flask import request, session
from flask import current_app as app
from flask import Blueprint
from api import celery
from werkzeug.utils import secure_filename
import os
import hashlib
import functools
import time

from api.core import tasks

core_bp = Blueprint("mmc_core", __name__)


def login_required(func):
    """A decorator to check if user is logged in
    """

    @functools.wraps(func)
    def inner(*args, **kwargs):
        if "oauth_token" not in session:
            return {"message": "unauthorized"}, 401
        return func(*args, **kwargs)

    return inner


@core_bp.route("/upload", methods=["POST"])
@login_required
def upload_csv():
    """route to upload file and add it to task queue
    to validate & create meetings in background
    """

    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename == '':
        return {"message": "invalid file"}, 400

    email = session["USER"]["Email"]
    filename = hash_it(email + filename)

    filepath = get_upload_path(filename)
    uploaded_file.save(filepath)
    tasks.process_file.delay(filepath)
    return {
        "message": "uploaded sucessfull",
        "extra": f"processing started for file: {filename} in background"
    }, 200


def get_upload_path(filename: str):
    path = app.config['UPLOAD_PATH']
    os.makedirs(path, exist_ok=True)
    return os.path.join(path, filename)


def hash_it(string: str):
    return hashlib.md5(string.encode()).hexdigest()
