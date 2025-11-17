from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class InviteCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.CHAR(16), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    user = db.relationship("User", back_populates="invite_code", uselist=False)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), unique=True, nullable=False)
    invite_code_id = db.Column(
        db.Integer, db.ForeignKey("invite_code.id"), unique=True, nullable=False
    )
    invite_code = db.relationship("InviteCode", back_populates="user")
    registered_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
