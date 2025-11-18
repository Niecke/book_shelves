# registration.py
from flask import (
    Blueprint,
    session,
    redirect,
    url_for,
    request,
    abort,
    current_app,
)
from authlib.common.security import generate_token
from models import InviteCode, User

registration_bp = Blueprint("registration", __name__, template_folder="templates")


@registration_bp.route("/register", methods=["GET"])
def register():
    invite_code = request.args.get("invite_code")
    if not invite_code:
        abort(400, description="Missing invite code")

    # Ensure invite code is not already used:
    invite_obj = InviteCode.query.filter_by(code=invite_code).first()
    if not invite_obj:
        abort(400, description="Invalid invite code")

    if invite_obj.user:
        abort(400, description="Invite code already in use")

    session["pending_invite_code"] = invite_code

    # Start OAuth flow – will come back at /register/callback
    session["nonce"] = generate_token()

    redirect_uri = url_for("registration.register_callback", _external=True)
    return current_app.oauth.google.authorize_redirect(
        redirect_uri, nonce=session["nonce"]
    )


@registration_bp.route("/register/callback")
def register_callback():
    # Validate OAuth login
    token = current_app.oauth.google.authorize_access_token()
    user_info = current_app.oauth.google.parse_id_token(token, nonce=session["nonce"])
    email = user_info["email"]

    # Check if invite code is valid and unused
    invite_code_val = session.pop("pending_invite_code", None)
    invite_obj = InviteCode.query.filter_by(code=invite_code_val).first()
    if not invite_obj:
        abort(400, description="Invalid invite code")

    # Ensure invite code is not already used:
    if invite_obj.user:
        abort(400, description="Invite code already in use")

    if User.query.filter_by(email=email).first():
        abort(400, description="User already exists")

    # Create new user with invite_code_id
    user = User(email=email, invite_code=invite_obj)
    current_app.db.session.add(user)
    current_app.db.session.commit()
    session["user"] = {"email": user.email}  # Log in user

    return redirect(url_for("home"))
