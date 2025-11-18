# auth.py
from flask import (
    Blueprint,
    redirect,
    url_for,
    abort,
    request,
    render_template,
    flash,
)
import requests
from utils.user_utils import get_current_user
from models import db, Book
from decorators import login_required
import env


book_bp = Blueprint(
    "book", __name__, template_folder="templates/books", url_prefix="/book"
)


def request_google_books_api(isbn: str, authors: str) -> dict:
    if isbn:
        query = f"isbn:{isbn}"
    elif authors:
        query = f"inauthor:{authors}"
    else:
        return {}
    google_api = f"{env.GOOGLE_BOOKS_API}?q={query}"
    resp = requests.get(google_api)
    return resp.json()


@book_bp.route("/search", methods=["GET", "POST"])
@login_required
def search():
    book_data = []
    if request.method == "POST":
        isbn = request.form.get("isbn", "")
        authors = request.form.get("authors", "")
        # first search for isbn
        data = request_google_books_api(isbn, "")
        for item in data.get("items", []):
            info = item["volumeInfo"]
            book_data.append(
                {
                    "title": info.get("title"),
                    "authors": info.get("authors", ""),
                    "language": info.get("language"),
                    "description": info.get("description"),
                    "isbn": isbn,
                    "genre": ", ".join(info.get("categories", [])),
                }
            )
        # now search for authors
        data = request_google_books_api("", authors)
        for item in data.get("items", []):
            info = item["volumeInfo"]
            # Extract ISBN if available
            isbn_list = [
                identifier["identifier"]
                for identifier in info.get("industryIdentifiers", [])
                if identifier["type"] in ["ISBN_10", "ISBN_13"]
            ]
            isbn = isbn_list[0] if isbn_list else "N/A"
            book_data.append(
                {
                    "title": info.get("title"),
                    "authors": info.get("authors", ""),
                    "language": info.get("language"),
                    "description": info.get("description"),
                    "isbn": isbn,
                    "genre": ", ".join(info.get("categories", [])),
                }
            )
        # if no books where found flash a message
        if not book_data:
            flash("No books found.", "warning")
    return render_template("books/search.html", books=book_data)


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
