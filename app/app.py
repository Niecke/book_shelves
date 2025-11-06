from flask import Flask
from models import db
from flask_migrate import upgrade, Migrate
import env


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql+psycopg://{env.SQLALCHEMY_DATABASE_USER}:{env.SQLALCHEMY_DATABASE_PASSWORD}@{env.SQLALCHEMY_DATABASE_HOST}:{env.SQLALCHEMY_DATABASE_PORT}/{env.SQLALCHEMY_DATABASE_DATABASE}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = env.SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)
migrate = Migrate(app, db)


if env.FLASK_AUTO_UPGRADE == "true":
    with app.app_context():
        upgrade()


@app.route("/")
def hello_world():
    return "Hello, World! Version 4"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=env.DEBUG)
