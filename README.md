```
██████╗  ██████╗  ██████╗ ██╗  ██╗      █████╗ ██╗      ██████╗██╗  ██╗███████╗███╗   ███╗██╗   ██╗
██╔══██╗██╔═══██╗██╔═══██╗██║ ██╔╝     ██╔══██╗██║     ██╔════╝██║  ██║██╔════╝████╗ ████║╚██╗ ██╔╝
██████╔╝██║   ██║██║   ██║█████╔╝█████╗███████║██║     ██║     ███████║█████╗  ██╔████╔██║ ╚████╔╝
██╔══██╗██║   ██║██║   ██║██╔═██╗╚════╝██╔══██║██║     ██║     ██╔══██║██╔══╝  ██║╚██╔╝██║  ╚██╔╝
██████╔╝╚██████╔╝╚██████╔╝██║  ██╗     ██║  ██║███████╗╚██████╗██║  ██║███████╗██║ ╚═╝ ██║   ██║
╚═════╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═╝     ╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝   ╚═╝
```

Eine Flask-Webanwendung zur Verwaltung einer Buchbibliothek mit modernem UI.

## Features

- **Bücher verwalten**: Hinzufügen, Anzeigen, Löschen von Büchern
- **Autoren verwalten**: Autoren mit Geburts- und Todesdatum anlegen
- **Suche**: Durchsuche Bücher und Autoren
- **Sortierung**: Nach Titel oder Autor sortieren
- **Cover-Bilder**: Automatische Cover-Anzeige via Open Library API
- **Modern UI**: Gradient-Design mit Material Icons

## Tech Stack

- **Backend**: Flask + SQLAlchemy 2.0
- **Database**: SQLite
- **Frontend**: HTML/CSS + Jinja2 Templates
- **Icons**: Material Symbols Outlined

## Installation

```bash
# Dependencies installieren
pip install flask flask-sqlalchemy

# Datenbank initialisieren (erste Ausführung)
python app.py
```

## Usage

```bash
# Server starten
python app.py

# Browser öffnen
http://localhost:5001
```

## Projektstruktur

```
book_alchemy/
├── app.py              # Flask App & Routes
├── data_models.py      # SQLAlchemy Models (Author, Book)
├── data/
│   └── library.sqlite  # SQLite Datenbank
└── templates/
    ├── home.html       # Hauptseite (Bücherliste)
    ├── add_book.html   # Buch hinzufügen
    └── add_author.html # Autor hinzufügen
```

## SQLAlchemy 2.0

Dieses Projekt verwendet **moderne SQLAlchemy 2.0 Syntax**:

```python
# ✅ So (SQLAlchemy 2.0)
db.session.execute(select(Book).where(Book.id == book_id)).scalar()

# ❌ Nicht so (Legacy)
Book.query.filter_by(id=book_id).first()
```

---

**Übungsprojekt** | Masterschool
