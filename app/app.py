import os
from flask import Flask
from models import db
from flask_migrate import upgrade, Migrate


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql+psycopg://myuser:mypassword@db:5432/mydatabase"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)


if os.environ.get("FLASK_AUTO_UPGRADE", "false") == "true":
    with app.app_context():
        upgrade()


@app.route("/")
def hello_world():
    return "Hello, World! Version 4"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
