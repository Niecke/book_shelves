from flask import Flask, jsonify, redirect, url_for, session
from flask_migrate import upgrade, Migrate
from authlib.integrations.flask_client import OAuth
from authlib.common.security import generate_token
import env
from models import db, InviteCode
from decorators import login_required


app = Flask(__name__)
if env.SQLALCHEMY_DATABASE_HOST:
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"postgresql+psycopg://{env.SQLALCHEMY_DATABASE_USER}:{env.SQLALCHEMY_DATABASE_PASSWORD}@{env.SQLALCHEMY_DATABASE_HOST}:{env.SQLALCHEMY_DATABASE_PORT}/{env.SQLALCHEMY_DATABASE_DATABASE}"
    )
elif env.SQLALCHEMY_CONNECTION_NAME:
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"postgresql+psycopg://{env.SQLALCHEMY_DATABASE_USER}:{env.SQLALCHEMY_DATABASE_PASSWORD}@/{env.SQLALCHEMY_DATABASE_DATABASE}?host=/cloudsql/{env.SQLALCHEMY_CONNECTION_NAME}"
    )
else:
    print("No database connection config set!")
    exit(1)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = env.SQLALCHEMY_TRACK_MODIFICATIONS

app.secret_key = env.FLASK_SESSION_SECRET

oauth = OAuth(app)
oauth.register(
    name="google",
    client_id=env.GOOGLE_CLIENT_ID,
    client_secret=env.GOOGLE_CLIENT_SECRET,
    server_metadata_url=env.SERVER_METADATA_URL,
    client_kwargs=env.CLIENT_KWARGS,
)

db.init_app(app)
migrate = Migrate(app, db)

if env.FLASK_AUTO_UPGRADE == "true":
    with app.app_context():
        upgrade()


@app.route("/")
def home():
    user = dict(session).get("user", None)
    return (
        f'Hello, {user["email"]}' if user else '<a href="/login">Login with Google</a>'
    )


@app.route("/login")
def login():
    session["nonce"] = generate_token()
    redirect_uri = url_for("auth", _external=True)
    return oauth.google.authorize_redirect(redirect_uri, nonce=session["nonce"])


@app.route("/login/callback")
def auth():
    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token, nonce=session["nonce"])
    session["user"] = user
    return redirect("/")


@app.route("/logout")
@login_required
def logout():
    session.pop("user", None)
    return redirect("/")


@app.route("/codes", methods=["GET"])
@login_required
def get_invite_codes():
    invite_codes = InviteCode.query.all()  # Fetch all rows
    result = [
        {
            "id": invite_code.id,
            "code": invite_code.code,
            "created_at": invite_code.created_at,
        }
        for invite_code in invite_codes
    ]
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=env.DEBUG)
