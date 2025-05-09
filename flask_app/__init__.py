# 3rd-party packages
from flask import Flask, render_template, request, redirect, url_for
from flask_mongoengine import MongoEngine
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
import certifi


# stdlib
from datetime import datetime
import os

# Environment variables
MONGO_HOST = os.getenv("MONGO_HOST")
SECRET_KEY = os.getenv("SECRET_KEY")
GOOGLE_KEY = os.getenv("GOOGLE_API")



# import google api library
from .client import GoogleClient

db = MongoEngine()
login_manager = LoginManager()
bcrypt = Bcrypt()
# google client variable
google_client = GoogleClient(GOOGLE_KEY)

from .users.routes import users
from .moments.routes import moments

def custom_404(e):
    return render_template("404.html"), 404

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_pyfile("config.py", silent=False)
    if test_config is not None:
        app.config.update(test_config)

    app.config['MONGODB_SETTINGS'] = {
        'host': MONGO_HOST,
        'tlsCAFile': certifi.where()
    }
    
    # Set the secret key properly
    app.config['SECRET_KEY'] = SECRET_KEY

    db.init_app(app)
    # uncomment when doing login stuff
    #login_manager.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(users)
    app.register_blueprint(moments)
    app.register_error_handler(404, custom_404)

    # uncomment when doing login stuff
    # login_manager.login_view = "users.login"

    return app
