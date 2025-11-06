from flask import Flask, jsonify
from flask_migrate import upgrade, Migrate
from models import db, InviteCode
import env


app = Flask(__name__)
if env.SQLALCHEMY_CONNECTION_NAME:
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"postgresql+psycopg://{env.SQLALCHEMY_DATABASE_USER}:{env.SQLALCHEMY_DATABASE_PASSWORD}@{env.SQLALCHEMY_DATABASE_HOST}:{env.SQLALCHEMY_DATABASE_PORT}/{env.SQLALCHEMY_DATABASE_DATABASE}"
    )
elif env.SQLALCHEMY_DATABASE_HOST:
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"postgresql+psycopg://{env.SQLALCHEMY_DATABASE_USER}:{env.SQLALCHEMY_DATABASE_PASSWORD}@/{env.SQLALCHEMY_DATABASE_DATABASE}?host=/cloudsql/{env.SQLALCHEMY_CONNECTION_NAME}"
    )
else:
    print("No database connection config set!")
    exit(1)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = env.SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)
migrate = Migrate(app, db)


if env.FLASK_AUTO_UPGRADE == "true":
    with app.app_context():
        upgrade()


@app.route("/", methods=["GET"])
def index():
    return "Hello, World! Version 4"


@app.route("/codes", methods=["GET"])
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
