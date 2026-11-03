"""Create the books table and add an example book."""

import sqlite3

db = sqlite3.connect("books-collection.db")

cursor = db.cursor()

# Create the table used to store books.
cursor.execute(
    "CREATE TABLE books (id INTEGER PRIMARY KEY,"
    "title varchar(250) NOT NULL UNIQUE,"
    "author varchar(250) NOT NULL,"
    "rating FLOAT NOT NULL)"
)

# Add one example record to the collection.
cursor.execute(
    "INSERT INTO books VALUES(1, 'The Monk Who Sold His Ferrari', "
    "'Robin Sharma', '7.5')"
)
db.commit()
