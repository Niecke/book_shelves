from flask import (
    Flask,
    jsonify,
    redirect,
    url_for,
    session,
    request,
    render_template,
    abort,
)
from flask_migrate import upgrade, Migrate
from authlib.integrations.flask_client import OAuth
from authlib.common.security import generate_token
import env
from models import db, InviteCode, User, Book
from decorators import login_required

# TODO move app creation to seperate file
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


def get_currrent_user(user: dict):
    email = user.get("email")
    user_obj = User().query.filter_by(email=email).first()
    db.session.add(user_obj)
    return user_obj


@app.route("/")
def home():
    user = dict(session).get("user", None)
    if user:
        return redirect("/profile")
    return render_template("index.html")


@app.route("/profile")
def profile():
    user = dict(session).get("user", None)
    return render_template("profile.html", user=user)


@app.errorhandler(400)
def bad_request(error):
    return render_template("400.html", error=error), 400


@app.route("/login")
def login():
    session["nonce"] = generate_token()
    redirect_uri = url_for("login_callback", _external=True)
    return oauth.google.authorize_redirect(redirect_uri, nonce=session["nonce"])


@app.route("/login/callback")
def login_callback():
    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token, nonce=session["nonce"])
    session["user"] = user
    return redirect("/")


@app.route("/logout")
@login_required
def logout():
    session.pop("user", None)
    return redirect("/")


@app.route("/register", methods=["GET"])
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

    redirect_uri = url_for("register_callback", _external=True)
    return oauth.google.authorize_redirect(redirect_uri, nonce=session["nonce"])


@app.route("/register/callback")
def register_callback():
    # Validate OAuth login
    token = oauth.google.authorize_access_token()
    user_info = oauth.google.parse_id_token(token, nonce=session["nonce"])
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
    db.session.add(user)
    db.session.commit()
    session["user"] = {"email": user.email}  # Log in user

    return redirect(url_for("home"))


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


@app.route("/books")
@login_required
def list_books():
    current_user = get_currrent_user(session["user"])
    # Assuming 'current_user.books' returns all linked books
    books = current_user.books
    return render_template("list_books.html", books=books)


@app.route("/books_create", methods=["GET", "POST"])
@login_required
def create_book():
    current_user = get_currrent_user(session["user"])
    if request.method == "GET":
        return render_template("create_book.html")
    data = request.form
    isbn = data.get("isbn")
    if not isbn:
        abort(400, "ISBN required")

    # See if book exists by ISBN
    book = Book.query.filter_by(isbn=isbn).first()
    if book:
        # Link user to the book if not already linked
        if book not in current_user.books:
            current_user.books.append(book)
            db.session.commit()
        return redirect(url_for("home"))

    # Create a new book and link to user
    book = Book(
        title=data.get("title"),
        authors=data.get("authors"),  # Should be a list
        language=data.get("language"),  # Short code
        description=data.get("description"),
        isbn=isbn,
        genre=data.get("genre"),
    )
    db.session.add(book)
    current_user.books.append(book)
    db.session.commit()
    # TODO change to list of book
    return redirect(url_for("list_books"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=env.DEBUG)
