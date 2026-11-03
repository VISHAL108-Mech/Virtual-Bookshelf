# Book Collection

A small Flask web app for keeping track of the books I've read. You can add a book with its author and a rating, see the whole list, change a rating and delete a book. The data is stored in a SQLite database.

I built it to practice the basics of a database-backed web app: creating, reading, updating and deleting records (CRUD) with Flask and SQLAlchemy.

<img width="400" height="300" alt="Screenshot 2026-11-03 204608" src="https://github.com/user-attachments/assets/f188dde8-80da-4436-b546-3ca15798e4f6" />
<img width="400" height="300" alt="Screenshot 2026-11-03 204305" src="https://github.com/user-attachments/assets/bab2c1fe-501b-437d-8735-703819f22e16" />

## What it can do

- Show all books, sorted by title
- Add a new book (title, author, rating)
- Edit the rating of an existing book
- Delete a book, with a confirmation page first

## Pages

| Route | What it does |
|---|---|
| `/` | Lists all books |
| `/add` | Shows the add form (GET) and saves the new book (POST) |
| `/edit/<id>` | Shows the edit form (GET) and updates the rating (POST) |
| `/delete/<id>` | Shows a confirmation page (GET) and deletes the book (POST) |

## Built with

- Python 3
- Flask
- Flask-SQLAlchemy and SQLAlchemy
- SQLite
- `python-dotenv` for the database path
- HTML and Jinja templates

## Project structure

```
Book Collection/
├── main.py              # Flask app, database model and routes
├── database.py          # one-off script that creates the table
├── books-collection.db  # SQLite database
├── requirements.txt
├── .env                 # database path (not committed)
├── templates/
│   ├── index.html       # book list
│   ├── add.html
│   ├── edit.html
│   └── delete.html
└── README.md
```

## Setup

Install the packages:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project folder with the location of the database file:

```
DATABASE_PATH=path/to/books-collection.db
```

A full path is the safest choice, because Flask-SQLAlchemy treats a relative path as relative to the app's `instance` folder.

Create the database and the books table. Run this once:

```bash
python database.py
```

It also adds one example book. Running it a second time will fail because the table already exists.

Start the app:

```bash
python main.py
```

Then open `http://127.0.0.1:5000` in your browser.

## How it works

**The model.** One class describes the `books` table. The title is unique, so the same book can't be added twice.

```python
class BookList(db.Model):
    """Store a book's title, author, and rating."""

    __tablename__ = "books"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
```

**Reading.** The home page selects every book, ordered by title, and passes the list to the template.

```python
books = (
    db.session.execute(db.select(BookList).order_by(BookList.title)).scalars().all()
)
return render_template("index.html", books=books)
```

**Creating.** The add route shows the form on GET. On POST it builds a new `BookList` from the form fields, saves it and redirects back to the home page.

```python
new_book = BookList(
    title=request.form["title"],
    author=request.form["author"],
    rating=request.form["rating"],
)
db.session.add(new_book)
db.session.commit()

return redirect(url_for("home"))
```

**Updating.** The edit route looks up the book by its id and changes the rating. `get_one` returns a 404 page automatically if the id doesn't exist.

```python
book = db.session.get_one(BookList, id)
if request.method == "POST":
    book.rating = float(request.form["rating"])
    db.session.commit()
    return redirect(url_for("home"))
return render_template("edit.html", book=book)
```

**Deleting.** Deleting uses two steps. A GET request only shows a confirmation page, and the book is removed only when the confirmation form is submitted with POST. That way a link can't delete a book by accident.

```python
book = db.session.get_one(BookList, id)
if request.method == "POST":
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for("home"))
return render_template("delete.html", book=book)
```

## What I learned

- Defining a database model with SQLAlchemy and connecting it to Flask
- The four CRUD operations and how they map to routes
- Using GET to show a form and POST to save it
- Redirecting after a form submission
- Keeping the database path in a `.env` file

## Things to improve

This is a learning project, so there are rough edges.

- Adding a title that already exists causes an error page instead of a friendly message
- The rating isn't validated, so it accepts any value. It should be limited to a range, and converted with `float()` in the add route like in the edit route
- `requirements.txt` lists both `dotenv` and `python-dotenv`. Only `python-dotenv` is needed, since that's the package that provides `load_dotenv`
- The table is created by a separate script. Calling `db.create_all()` in the app would make setup one step shorter
- Add search, a way to edit the title and author, and a short review or notes field

## Developer

**VISHAL YADAV**
- GitHub: [@VISHAL108-Mech](https://github.com/VISHAL108-Mech)
- LinkedIn: [vishal-yadav-2a91a7428](https://www.linkedin.com/in/vishal-yadav-2a91a7428)
- Email: [vy4122000@gmail.com](mailto:vy4122000@gmail.com)
