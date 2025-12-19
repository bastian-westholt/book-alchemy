from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=True)
    date_of_death = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return f"Author(id={self.id}, name={self.name})"

    def __str__(self):
        return self.name

class Book(db.Model):
    __tablename__ = "books"

    id = Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = Column(db.Integer, nullable=False)
    title = Column(db.String(100), nullable=False)
    publication_year = Column(db.Integer, nullable=True)
    author_id = Column(db.Integer, db.ForeignKey('authors.id'))

    def __repr__(self):
        return f"Book(title={self.title}, publication_year={self.publication_year}, isbn={self.isbn})"

    def __str__(self):
        return self.title