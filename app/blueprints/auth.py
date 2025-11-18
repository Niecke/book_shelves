# auth.py
from flask import Blueprint, session, redirect, url_for, current_app, flash
from authlib.common.security import generate_token
from models import User

auth_bp = Blueprint("auth", __name__, template_folder="templates")


@auth_bp.route("/login")
def login():
    session["nonce"] = generate_token()
    redirect_uri = url_for("auth.login_callback", _external=True)
    return current_app.oauth.google.authorize_redirect(
        redirect_uri, nonce=session["nonce"]
    )


@auth_bp.route("/login/callback")
def login_callback():
    token = current_app.oauth.google.authorize_access_token()
    user = current_app.oauth.google.parse_id_token(token, nonce=session["nonce"])
    # check that the user is already registered
    user_obj = User.query.filter_by(email=user["email"]).first()
    if not user_obj:
        flash(
            "You are not registered. Please register first with an invite code.",
            "error",
        )
        return redirect(url_for("home"))
    session["user"] = user
    return redirect("/")


@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")
