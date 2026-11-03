"""Flask app for managing a personal book collection."""

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Float
import os
from dotenv import load_dotenv

# Load the database path from the project's .env file.
load_dotenv()

DB_PATH = os.getenv("DATABASE_PATH")

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"

db = SQLAlchemy(app)


class BookList(db.Model):
    """Store a book's title, author, and rating."""

    __tablename__ = "books"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)


@app.route("/")
def home():
    """Show all books ordered by title."""
    books = (
        db.session.execute(db.select(BookList).order_by(BookList.title)).scalars().all()
    )
    return render_template("index.html", books=books)


@app.route("/add", methods=["GET", "POST"])
def add():
    """Add a book from the form or display the form."""
    if request.method == "POST":
        new_book = BookList(
            title=request.form["title"],
            author=request.form["author"],
            rating=request.form["rating"],
        )
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for("home"))
    return render_template("add.html")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    """Update a book's rating or display its edit form."""
    book = db.session.get_one(BookList, id)
    if request.method == "POST":
        book.rating = float(request.form["rating"])
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit.html", book=book)

@app.route("/delete/<int:id>", methods=["GET", "POST"])
def delete(id):
    """Delete a book after confirmation or show the confirmation page."""
    book = db.session.get_one(BookList, id)
    if request.method == "POST":
        db.session.delete(book)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("delete.html", book=book)

if __name__ == "__main__":
    # Start the development server when this file runs directly.
    app.run(debug=True)
