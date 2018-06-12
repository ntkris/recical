from app.data import models, Author

author1 = Author('Ivan Vazov') # 1
db.session.add(author1)        # 2
db.session.commit()

# Create table of authors
CREATE TABLE author (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, names TEXT NOT NULL);

# Create table of books
CREATE TABLE book (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, rating INTEGER, IMAGE TEXT, AUTHOR_ID INTEGER);


SELECT author.qui.id AS author_id, author.names AS author_names, book_1.id AS book_1_id, book_1.title AS book_1_title, book_1.rating AS book_1_rating, book_1.image AS book_1_image, book_1.author_id AS book_1_author_id \nFROM author LEFT OUTER JOIN book AS book_1 ON author.id = book_1.author_id'

id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    rating = db.Column(db.Integer)
    image = db.Column(db.String(30))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    author = db.relationship('Author',