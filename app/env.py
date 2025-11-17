import os

DEBUG = os.environ.get("DEBUG", "false")

FLASK_AUTO_UPGRADE = os.environ.get("FLASK_AUTO_UPGRADE", "true")
FLASK_SESSION_SECRET = os.environ.get(
    "FLASK_SESSION_SECRET", "test"
)  # Use secret manager or environment

SQLALCHEMY_DATABASE_HOST = os.environ.get("SQLALCHEMY_DATABASE_HOST")
SQLALCHEMY_CONNECTION_NAME = os.environ.get("CLOUDSQL_CONNECTION_NAME")

SQLALCHEMY_DATABASE_USER = os.environ.get("SQLALCHEMY_DATABASE_USER", "book_shelves")
SQLALCHEMY_DATABASE_PASSWORD = os.environ.get(
    "SQLALCHEMY_DATABASE_PASSWORD", "book_shelves"
)
SQLALCHEMY_DATABASE_DATABASE = os.environ.get(
    "SQLALCHEMY_DATABASE_DATABASE", "book_shelves"
)
SQLALCHEMY_DATABASE_PORT = os.environ.get("SQLALCHEMY_DATABASE_PORT", 5432)
SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get(
    "SQLALCHEMY_TRACK_MODIFICATIONS", "false"
)

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
SERVER_METADATA_URL = os.environ.get(
    "SERVER_METADATA_URL",
    "https://accounts.google.com/.well-known/openid-configuration",
)
CLIENT_KWARGS = os.environ.get("CLIENT_KWARGS", {"scope": "openid email profile"})
