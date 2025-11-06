from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class InviteCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.CHAR(16), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
