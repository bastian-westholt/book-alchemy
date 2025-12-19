import datetime as dt
import os
from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy import select, or_, and_
from data_models import db, Author, Book

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"

db.init_app(app)


def get_joined_tables(sort_mode):
    if sort_mode == 'by_title':
        joined_tables_query = (
            select(Book, Author)
            .join(Author, Book.author_id == Author.id)
            .order_by(Book.title)
        )

    elif sort_mode == 'by_author':
        joined_tables_query = (
            select(Book, Author)
            .join(Author, Book.author_id == Author.id)
            .order_by(Author.name)
        )

    joined_tables = (
        db.session.execute(joined_tables_query).all()
    )

    return joined_tables

def search_joined_tables(query):
    joined_tables_query = (
        select(Book, Author)
        .join(Author, Book.author_id == Author.id)
        .where(
            or_(
            Book.title.contains(query),
            Author.name.contains(query)
            )
        )
        .order_by(Book.title)
    )
    joined_tables = (
        db.session.execute(joined_tables_query).all()
    )
    print(joined_tables)
    return joined_tables

def get_list_of_all_authors():
    all_authors_query = (
        select(Author)
        .order_by(Author.name)
    )
    all_authors = db.session.execute(all_authors_query).scalars().all()
    return all_authors


@app.route('/', methods=['GET', 'POST'])
def home():
    # Post - Sorting/filtering
    if request.method == 'POST':
        sort_mode = request.form.get('sorting-menu')
    else:
        sort_mode = 'by_title'

    # GET - Search query
    search_query = request.args.get('search')

    if search_query:
        joined_table = search_joined_tables(search_query)
    else:
        joined_table = get_joined_tables(sort_mode)

    is_deleted = request.args.get('deleted') is not None
    return render_template('home.html', table=joined_table, sort_mode=sort_mode, deleted=is_deleted)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        name = request.form.get('name')
        birthdate = request.form.get('birthdate')
        date_of_death = request.form.get('date_of_death')

        if birthdate:
            birthdate_date_obj = dt.datetime.strptime(birthdate, '%Y-%m-%d').date()
        else:
            birthdate_date_obj = None

        if date_of_death:
            date_of_death_date_obj = dt.datetime.strptime(date_of_death, '%Y-%m-%d').date()
        else:
            date_of_death_date_obj = None

        new_author = Author(
            name = name,
            birth_date = birthdate_date_obj,
            date_of_death = date_of_death_date_obj
        )

        db.session.add(new_author)
        db.session.commit()

        return redirect(url_for('add_author', success='true'))

    is_success = request.args.get('success') is not None
    return render_template('add_author.html', success=is_success)


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    all_authors = get_list_of_all_authors()

    if request.method == 'POST':
        isbn = request.form.get('isbn')
        title = request.form.get('title')
        publication_year = request.form.get('publication_year')
        author_id = request.form.get('author_id')

        new_book = Book(
            isbn = isbn,
            title = title,
            publication_year = publication_year,
            author_id = author_id
        )

        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('add_book', success=True))

    is_success = request.args.get("success") is not None
    return render_template('add_book.html', success=is_success, authors=all_authors)

@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book_by_book_id(book_id):
    if request.method == 'POST':
        book = db.session.execute(select(Book).where(Book.id == book_id)).scalar()
        db.session.delete(book)
        db.session.commit()

        return redirect(url_for('home', deleted=True))

    return redirect(url_for('home'))

if __name__ == '__main__':
    # Initialisiert die Datenbank und erstellt Ihre Tabellen
    '''with app.app_context():
        db.create_all()
        print(f'Datenbank initialisiert.')'''
    app.run(host='0.0.0.0', port=5001, debug=True)