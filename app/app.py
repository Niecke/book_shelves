from flask import (
    jsonify,
    redirect,
    session,
    render_template,
)
import env
from models import InviteCode
from decorators import login_required
from factory import create_app

app = create_app()


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
