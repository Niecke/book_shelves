# app_factory.py
from flask import Flask
from flask_migrate import Migrate
from authlib.integrations.flask_client import OAuth
import env
from models import db
from blueprints.auth import auth_bp
from blueprints.registration import registration_bp
from blueprints.books import book_bp

# Import anything else you need


def create_app():
    # App and config
    app = Flask(__name__)
    if env.SQLALCHEMY_DATABASE_HOST:
        app.config["SQLALCHEMY_DATABASE_URI"] = (
            f"postgresql+psycopg://{env.SQLALCHEMY_DATABASE_USER}:{env.SQLALCHEMY_DATABASE_PASSWORD}@"
            f"{env.SQLALCHEMY_DATABASE_HOST}:{env.SQLALCHEMY_DATABASE_PORT}/{env.SQLALCHEMY_DATABASE_DATABASE}"
        )
    elif env.SQLALCHEMY_CONNECTION_NAME:
        app.config["SQLALCHEMY_DATABASE_URI"] = (
            f"postgresql+psycopg://{env.SQLALCHEMY_DATABASE_USER}:{env.SQLALCHEMY_DATABASE_PASSWORD}@/"
            f"{env.SQLALCHEMY_DATABASE_DATABASE}?host=/cloudsql/{env.SQLALCHEMY_CONNECTION_NAME}"
        )
    else:
        raise Exception("No database connection config set!")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = env.SQLALCHEMY_TRACK_MODIFICATIONS
    app.secret_key = env.FLASK_SESSION_SECRET

    # DB and migrations
    db.init_app(app)
    Migrate(app, db)

    app.db = db

    # OAuth
    oauth = OAuth(app)
    oauth.register(
        name="google",
        client_id=env.GOOGLE_CLIENT_ID,
        client_secret=env.GOOGLE_CLIENT_SECRET,
        server_metadata_url=env.SERVER_METADATA_URL,
        client_kwargs=env.CLIENT_KWARGS,
    )
    app.oauth = oauth

    # Auto-migrate if needed
    if env.FLASK_AUTO_UPGRADE == "true":
        with app.app_context():
            from flask_migrate import upgrade

            upgrade()

    # Blueprint registration
    app.register_blueprint(auth_bp)
    app.register_blueprint(registration_bp)
    app.register_blueprint(book_bp)

    return app
