# auth.py
from flask import (
    Blueprint,
    redirect,
    url_for,
    abort,
    request,
    render_template,
    flash,
    current_app,
)
import requests
from utils.user_utils import get_current_user
from models import db, Book
from decorators import login_required


book_bp = Blueprint(
    "book", __name__, template_folder="templates/books", url_prefix="/book"
)


@book_bp.route("/search", methods=["GET", "POST"])
@login_required
def search():
    book_data = None
    if request.method == "POST":
        isbn = request.form.get("isbn")
        if isbn:
            google_api = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
            resp = requests.get(google_api)
            data = resp.json()
            current_app.logger.debug(data)
            if "items" in data and data["items"]:
                info = data["items"][0]["volumeInfo"]
                book_data = {
                    "title": info.get("title"),
                    "authors": info.get("authors", []),
                    "language": info.get("language"),
                    "description": info.get("description"),
                    "isbn": isbn,
                    "genre": ", ".join(info.get("categories", [])),
                }
            else:
                flash("No book found for that ISBN.", "warning")
    return render_template("books/search.html", book=book_data)


@book_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "GET":
        return render_template("books/create.html")
    data = request.form
    isbn = data.get("isbn")
    if not isbn:
        abort(400, "ISBN required")

    # See if book exists by ISBN
    book = Book.query.filter_by(isbn=isbn).first()
    current_user = get_current_user()
    # db.session.add(current_user)
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
    return redirect(url_for("home"))


@book_bp.route("/delete/<int:book_id>", methods=["POST"])
@login_required
def delete_book(book_id):
    current_user = get_current_user()
    book = Book.query.get_or_404(book_id)
    # Only remove link between user and this book
    if book in current_user.books:
        current_user.books.remove(book)
        db.session.commit()
    # Optionally, delete book object if no users are left
    if not book.users:
        db.session.delete(book)
        db.session.commit()
    flash("Book removed.", "success")
    return redirect(url_for("home"))
