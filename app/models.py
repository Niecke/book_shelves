from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Association table for the many-to-many relationship between Books and Users
user_books = db.Table(
    "user_books",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("book_id", db.Integer, db.ForeignKey("book.id"), primary_key=True),
)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    authors = db.Column(db.String(1024), nullable=False)
    language = db.Column(db.CHAR(2), nullable=False)  # ISO 639-1 code, max 2 chars
    description = db.Column(db.Text, nullable=True)
    isbn = db.Column(db.CHAR(13), unique=True, nullable=False)
    genre = db.Column(db.String(64), nullable=True)
    users = db.relationship("User", secondary=user_books, back_populates="books")


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
    books = db.relationship("Book", secondary=user_books, back_populates="users")
