from flask import session
from models import User


def get_current_user():
    email = session.get("user").get("email")
    return User.query.filter_by(email=email).first()
