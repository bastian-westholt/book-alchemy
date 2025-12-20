# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Book Alchemy is a Flask web application for managing a book library. It provides CRUD operations for books and authors with a clean, modern UI featuring search, sorting, and cover image display.

## Running the Application

```bash
# Start the development server
python app.py

# Access at http://localhost:5001
```

The app runs on port 5001 with debug mode enabled by default.

## Database Architecture

### SQLAlchemy 2.0 Query Pattern

This project uses **modern SQLAlchemy 2.0 syntax**, not the legacy `.query` API:

```python
# ✅ Correct (used in this project)
db.session.execute(select(Book).where(Book.id == book_id)).scalar()

# ❌ Wrong (legacy, don't use)
Book.query.filter_by(id=book_id).first()
```

### Data Models (`data_models.py`)

- `db = SQLAlchemy()` - Shared database instance (initialized in `app.py`)
- `Author` model: name, birth_date, date_of_death
- `Book` model: isbn, title, publication_year, author_id (foreign key)
- **No `db.relationship()` used** - JOINs are manual using SQLAlchemy select()

### Important SQLAlchemy Methods

**`.scalar()` vs `.scalars()` vs `.all()`:**
- `.scalar()` - Returns single object or None
- `.scalars().all()` - Returns list of objects (single column)
- `.all()` - Returns list of tuples (multi-column, e.g., JOINs)

**Example from codebase:**
```python
# JOIN query returns tuples: [(Book, Author), (Book, Author)]
joined_tables = db.session.execute(
    select(Book, Author).join(Author, Book.author_id == Author.id)
).all()

# Single model returns objects: [Author, Author]
authors = db.session.execute(select(Author)).scalars().all()
```

### Database Location

SQLite database: `data/library.sqlite` (relative to project root)

## Application Routes

### Route Pattern
- Use `url_for('function_name')` not `url_for('/route/path')`
- Example: `redirect(url_for('home'))` not `redirect(url_for('/'))`

### Key Routes
- `/` (home) - GET: Display books, POST: Apply sorting
- `/add_book` - GET: Show form, POST: Create book
- `/add_author` - GET: Show form, POST: Create author
- `/book/<int:book_id>/delete` - POST: Delete book

### Query Patterns in Routes

**Home route** combines POST (sorting) and GET (search):
```python
# POST for sorting dropdown (form submission)
sort_mode = request.form.get('sorting-menu')

# GET for search query (URL parameter)
search_query = request.args.get('search')
```

**Success messages** via URL parameters:
```python
return redirect(url_for('add_book', success=True))
# Then in template: {% if success %}
```

## Template Architecture

### Template Structure
- `templates/home.html` - Main book listing with search/sort/delete
- `templates/add_book.html` - Form for adding books
- `templates/add_author.html` - Form for adding authors

### Design System
- Font: "Avenir Next", sans-serif
- Color scheme: #333 (dark), #f0f0f0 (light gray), #667eea-#764ba2 (purple gradient)
- Fixed action buttons: Left side, gradient purple circles with Material Icons
- Material Symbols Outlined icons via Google Fonts

### Cover Image Handling
```html
<!-- Open Library API with placeholder fallback -->
<img src="https://covers.openlibrary.org/b/isbn/{{ book.isbn }}-M.jpg"
     onerror="this.src='https://via.placeholder.com/80x120?text=No+Cover'">
```

### Template Data Flow
Templates receive data via `render_template()`:
- `home.html`: `table` (joined Book/Author tuples), `sort_mode`, `deleted`
- `add_book.html`: `success`, `authors` (list of Author objects)
- `add_author.html`: `success`

**Important:** In Jinja2, access object attributes with dot notation:
```html
{{ book.title }}  <!-- ✅ Correct -->
{{ book['title'] }}  <!-- ❌ Wrong - this is for dictionaries -->
```

## Common Pitfalls

1. **DELETE operations must use POST**, not GET (security best practice)
2. **Date parsing**: Use `dt.datetime.strptime(date_string, '%Y-%m-%d').date()` for HTML date inputs
3. **Form alignment**: Fixed buttons/forms need explicit `width` to match header columns
4. **Jinja2 empty check**: Use `{% if not table %}` not `{% if table is None %}` (handles empty lists)
5. **Query result types**: JOINs return tuples, single models return objects - affects `.scalars()` usage

## Tutorial Resources

Learning materials stored in `.tutorials/` directory contain detailed explanations of Flask/SQLAlchemy concepts used in this project.
