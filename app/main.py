from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField
from wtforms.validators import DataRequired, Email
import os
import google_auth
import json

def create_app(test_config):
    global app
    app = Flask(__name__, instance_relative_config=True)
    csrf = CSRFProtect(app)
    app.config.from_mapping(
        SECRET_KEY="""b'\xf3,\x0b\x11\xa9n\x0b"\x1b}\xb1\x1d\tBZ\xca\xe78\xeeY\x0b\xeaW\x8f'""",
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(google_auth.app)

create_app(None)

@app.route("/", methods=["GET", "POST"])
def index():

    logged_in = google_auth.is_logged_in()

    session["logged_in"] = logged_in

    if logged_in:
        user_info = google_auth.get_user_info()
        return render_template("index.html", profile_picture=user_info["picture"])

    return render_template("index.html")

if __name__ == "__main__":
    app.run()