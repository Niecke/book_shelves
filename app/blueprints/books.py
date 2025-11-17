# auth.py
from flask import (
    Blueprint,
    redirect,
    url_for,
    abort,
    request,
    render_template,
)
from utils.user_utils import get_current_user
from models import db, Book
from decorators import login_required


book_bp = Blueprint("book", __name__, template_folder="templates")


@book_bp.route("/books_create", methods=["GET", "POST"])
@login_required
def create_book():
    if request.method == "GET":
        return render_template("create_book.html")
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
    return redirect(url_for("book.list_books"))


@book_bp.route("/books")
@login_required
def list_books():
    current_user = get_current_user()
    books = current_user.books
    return render_template("list_books.html", books=books)
