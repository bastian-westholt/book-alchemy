# Flask SQLAlchemy Setup - Methoden Erklärung

## Übersicht
Diese Datei erklärt alle Methoden und Funktionen im `app.py` Setup-Code für Flask mit SQLAlchemy.

---

## Code-Struktur

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import flask
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"

from data_models import db, Author, Book

db.init_app(app)
```

---

## Methoden & Funktionen Erklärung

### 1. `Flask(__name__)` - Flask App Konstruktor
**Zeile:** 6
**Typ:** Konstruktor

```python
app = Flask(__name__)
```

**Was macht die Methode?**
- Erstellt eine neue Flask-Anwendungsinstanz
- Initialisiert das WSGI-Application-Objekt

**Parameter:**
- `__name__`: Name des aktuellen Python-Moduls
  - Bei Hauptdatei: `"__main__"`
  - Bei Import: Modulname (z.B. `"app"`)
  - Wird verwendet, um Template- und Static-Ordner zu finden

**Rückgabe:**
- Flask Application Objekt

---

### 2. `os.path.dirname(__file__)` - Verzeichnis ermitteln
**Zeile:** 8
**Typ:** Funktion

```python
os.path.dirname(__file__)
```

**Was macht die Methode?**
- Extrahiert den Verzeichnispfad aus einem vollständigen Dateipfad

**Parameter:**
- `__file__`: Spezielles Python-Attribut mit dem Pfad zur aktuellen Datei

**Beispiel:**
```python
__file__ = "/Users/bastianwestholt/.../book_alchemy/app.py"
# Ergebnis: "/Users/bastianwestholt/.../book_alchemy"
```

---

### 3. `os.path.abspath()` - Absoluter Pfad
**Zeile:** 8
**Typ:** Funktion

```python
basedir = os.path.abspath(os.path.dirname(__file__))
```

**Was macht die Methode?**
- Wandelt einen relativen Pfad in einen absoluten Pfad um
- Bereinigt `..` und `.` aus dem Pfad

**Parameter:**
- `path`: Pfad (relativ oder absolut)

**Rückgabe:**
- Absoluter, normalisierter Pfad

**Beispiel:**
```python
# Relativ: "./data/../app.py"
# Absolut: "/Users/bastianwestholt/PycharmProjects/MASTERSCHOOL/book_alchemy/app.py"
```

---

### 4. `os.path.join()` - Pfade zusammenfügen
**Zeile:** 9
**Typ:** Funktion

```python
os.path.join(basedir, 'data/library.sqlite')
```

**Was macht die Methode?**
- Fügt mehrere Pfadsegmente plattformunabhängig zusammen
- Verwendet das richtige Trennzeichen (`/` auf Unix, `\` auf Windows)

**Parameter:**
- `*paths`: Beliebig viele Pfadsegmente

**Rückgabe:**
- Zusammengefügter Pfad

**Beispiel:**
```python
# macOS/Linux:
"/Users/bastianwestholt/.../book_alchemy/data/library.sqlite"

# Windows:
"C:\Users\bastianwestholt\...\book_alchemy\data\library.sqlite"
```

---

### 5. `app.config['SQLALCHEMY_DATABASE_URI']` - Konfiguration setzen (DETAILLIERT)
**Zeile:** 9
**Typ:** Dictionary-Zugriff

```python
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"
```

#### Was ist `app.config`?
```python
app.config  # Dictionary mit allen Flask-Einstellungen
```
- **Typ:** Dictionary (Schlüssel-Wert-Speicher)
- **Zweck:** Zentrale Konfiguration für die gesamte Flask-App
- **Zugriff:** `app.config['SCHLÜSSEL'] = WERT`

#### Was ist `SQLALCHEMY_DATABASE_URI`?
**Das ist der Schlüssel, den SQLAlchemy sucht, um zu wissen:**
- **Welche Datenbank** verwendet werden soll (SQLite, PostgreSQL, MySQL, etc.)
- **Wo** die Datenbank liegt (Dateipfad oder Server-Adresse)
- **Wie** die Verbindung aufgebaut wird (Credentials, Port, etc.)

#### URI-Format Beispiele:

```python
# SQLite (lokale Datei)
'sqlite:///absolute/pfad/zur/datenbank.sqlite'

# PostgreSQL (Server)
'postgresql://username:password@localhost:5432/datenbankname'

# MySQL
'mysql://username:password@localhost:3306/datenbankname'

# SQLite relativ (nicht empfohlen)
'sqlite://relative/pfad/datenbank.sqlite'
```

#### Was passiert intern?

**1. Du setzt die Config:**
```python
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data/library.sqlite"
```

**2. SQLAlchemy liest sie aus:**
```python
db.init_app(app)  # <-- Hier liest SQLAlchemy app.config aus
```

**3. SQLAlchemy erstellt die Verbindung:**
- Parst die URI
- Erkennt Datenbank-Typ (sqlite)
- Erstellt Connection-Pool
- Verbindet bei Bedarf zur Datenbank

#### Analogie:
```
app.config['SQLALCHEMY_DATABASE_URI'] ist wie eine Adresse:

"Fahre zu: sqlite:///data/library.sqlite"
            ^^^^^^   ^^^^^^^^^^^^^^^^^^^^
            |        └─ Wo ist die Datenbank?
            └─ Welche Datenbank-Software?
```

#### Wichtig bei SQLite:
```python
# 3 Slashes = absoluter Pfad (empfohlen)
'sqlite:///absolute/pfad/zur/datenbank.sqlite'

# 2 Slashes = relativer Pfad (nicht empfohlen)
'sqlite://relative/pfad/datenbank.sqlite'
```

#### Weitere wichtige Config-Keys:
```python
# Tracking deaktivieren (bessere Performance)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SQL-Queries in der Konsole anzeigen (für Debugging)
app.config['SQLALCHEMY_ECHO'] = True

# Geheimer Schlüssel für Sessions
app.config['SECRET_KEY'] = 'geheimer-schlüssel'

# Debug-Modus
app.config['DEBUG'] = True
```

**Zusammenfassung:** `app.config['SQLALCHEMY_DATABASE_URI']` ist die "Wegbeschreibung" für SQLAlchemy zur Datenbank.

---

### 6. `db.init_app(app)` - Datenbank initialisieren
**Zeile:** 13
**Typ:** Methode

```python
db.init_app(app)
```

**Was macht die Methode?**
- Verbindet die SQLAlchemy-Instanz (`db`) mit der Flask-App
- Registriert Lifecycle-Hooks (z.B. Verbindungsmanagement)
- Liest Konfiguration aus `app.config`

**Wichtige Reihenfolge:**
1. ✅ App erstellen: `app = Flask(__name__)`
2. ✅ Konfiguration setzen: `app.config['SQLALCHEMY_DATABASE_URI'] = ...`
3. ✅ DB importieren: `from data_models import db`
4. ✅ DB initialisieren: `db.init_app(app)`

**Falsche Reihenfolge führt zu Fehlern!**

---

### 7. `with app.app_context(): db.create_all()` - Tabellen erstellen
**Typ:** Context Manager + Methode

```python
with app.app_context():
    db.create_all()
```

**Was macht dieser Code?**
- Erstellt **alle** Datenbanktabellen basierend auf deinen Model-Klassen
- Muss im Flask Application Context ausgeführt werden

#### Zeile für Zeile Erklärung:

**`app.app_context()`**
- Erstellt einen **Application Context** (App-Kontext)
- Flask braucht das, um zu wissen: "Welche App ist gerade aktiv?"
- Ohne Context weiß SQLAlchemy nicht, mit welcher Datenbank es sich verbinden soll

**`with ... :`**
- **Context Manager**: Führt Code in einem bestimmten Kontext aus
- Öffnet den Context → Führt Code aus → Schließt Context automatisch

**`db.create_all()`**
- Erstellt **ALLE** Tabellen aus deinen Modellen (`Author`, `Book`, etc.)
- Liest deine Model-Klassen
- Generiert SQL CREATE TABLE Befehle
- Führt sie in der Datenbank aus

#### Praktisches Beispiel:

**Deine Modelle:**
```python
# data_models.py
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    birth_date = db.Column(db.Date)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
```

**Code ausführen:**
```python
with app.app_context():
    db.create_all()
```

**Was intern passiert (generiertes SQL):**
```sql
CREATE TABLE author (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100),
    birth_date DATE
);

CREATE TABLE book (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200),
    author_id INTEGER,
    FOREIGN KEY (author_id) REFERENCES author(id)
);
```

#### Warum braucht man `app_context()`?

**Ohne Context:**
```python
db.create_all()  # ❌ RuntimeError: Working outside of application context!
```

**Mit Context:**
```python
with app.app_context():
    db.create_all()  # ✅ Funktioniert!
```

**Grund:** SQLAlchemy braucht die App-Config (`SQLALCHEMY_DATABASE_URI`), um zu wissen, wo die Datenbank ist.

#### Wann nutzt man das?

**Szenario 1: Beim ersten Start**
```python
# app.py
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Tabellen erstellen
    app.run()
```

**Szenario 2: Separate Init-Datei**
```python
# init_database.py
from app import app, db

with app.app_context():
    db.create_all()
    print("✅ Datenbank erstellt!")
```

Dann ausführen:
```bash
python init_database.py
```

**Szenario 3: In der Python-Console**
```python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
...
✅ Tabellen erstellt!
```

#### Wichtig zu wissen:

**✅ `create_all()` ist sicher:**
- Erstellt nur **fehlende** Tabellen
- Überschreibt **keine** existierenden Tabellen
- Löscht **keine** Daten

```python
# Erste Ausführung:
with app.app_context():
    db.create_all()  # Erstellt: author, book

# Zweite Ausführung:
with app.app_context():
    db.create_all()  # Tut nichts (Tabellen existieren bereits)
```

**❌ Änderungen an Modellen werden NICHT übernommen:**
```python
# Später fügst du ein Feld hinzu:
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))  # ⬅️ NEU!

with app.app_context():
    db.create_all()  # ❌ Fügt 'email' NICHT hinzu!
```

Für Änderungen an existierenden Tabellen brauchst du **Database Migrations** (z.B. Flask-Migrate).

#### Alternative: Ohne `with` (nicht empfohlen)

```python
# Manuell Context erstellen & schließen:
ctx = app.app_context()
ctx.push()
db.create_all()
ctx.pop()

# ❌ Umständlich! Besser: with-Statement verwenden
```

#### Zusammenfassung:

```python
with app.app_context():    # 1. Öffnet Flask-Kontext
    db.create_all()         # 2. Erstellt alle Tabellen
                            # 3. Context wird automatisch geschlossen
```

**In einem Satz:** Erstellt die Datenbanktabellen für alle deine Model-Klassen, innerhalb des Flask-Application-Context.

---

## Vollständiger Ablauf

```
1. Flask-App erstellen
   └─> app = Flask(__name__)

2. Projektverzeichnis ermitteln
   └─> basedir = /Users/.../book_alchemy

3. Datenbank-URI zusammenbauen
   └─> sqlite:////Users/.../book_alchemy/data/library.sqlite

4. URI in Config speichern
   └─> app.config['SQLALCHEMY_DATABASE_URI'] = URI

5. Datenmodelle importieren
   └─> from data_models import db, Author, Book

6. Datenbank mit App verbinden
   └─> db.init_app(app)
```

---

## Fehlende Datei: `data_models.py`

**Problem:** Die Datei `data_models.py` existiert nicht im Projekt!

**Sollte enthalten:**
```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # ... weitere Felder

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    # ... weitere Felder
```

---

## Tipps & Best Practices

### ✅ Empfohlen:
- Absolute Pfade für Datenbanken verwenden
- `basedir` für portable Pfade nutzen
- Konfiguration vor `db.init_app()` setzen

### ❌ Vermeiden:
- Relative Pfade ohne `basedir`
- `db.init_app()` vor Konfiguration
- Hardcodierte Pfade (z.B. `/Users/bastian/...`)

---

## Häufige Fehler & Missverständnisse

### ❌ Fehler: `import SQLAlchemy as db` statt `db = SQLAlchemy()`

**Falsche Annahme:**
```python
# ❌ FALSCH - funktioniert NICHT!
from flask_sqlalchemy import SQLAlchemy as db

class Author(db.Model):  # AttributeError!
    pass
```

**Warum funktioniert das nicht?**

#### Klasse vs. Instanz
```python
# SQLAlchemy = Bauplan (Klasse)
# db = SQLAlchemy() = Fertiges Objekt (Instanz)

# Analogie:
Auto = Klasse          # Bauplan für Autos
mein_auto = Auto()     # Konkretes Auto gebaut

# Mit "as db":
from Auto import Auto as db   # Bauplan nur umbenennen
# Du hast KEIN Auto gebaut!
```

#### Was passiert:
```python
# Variante 1: FALSCH
from flask_sqlalchemy import SQLAlchemy as db
# db ist jetzt die KLASSE SQLAlchemy (Bauplan)

class Author(db.Model):  # ❌ Fehler!
    # AttributeError: type object 'SQLAlchemy' has no attribute 'Model'
```

```python
# Variante 2: RICHTIG
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
# db ist jetzt eine INSTANZ der Klasse (fertiges Objekt)

class Author(db.Model):  # ✅ Funktioniert!
    pass
```

#### Warum brauchst du die Instanz?

**Nur die Instanz hat:**
- `db.Model` - Basisklasse für Datenmodelle
- `db.Column` - Für Tabellenspalten
- `db.Integer`, `db.String`, etc. - Datentypen
- `db.init_app(app)` - Instanz-Methode zum Verbinden

**Die Klasse selbst hat diese Attribute NICHT!**

#### Technische Erklärung:
```python
# SQLAlchemy-Klasse (Bauplan):
class SQLAlchemy:
    def __init__(self):
        # Hier werden Model, Column, etc. ERST erstellt
        self.Model = declarative_base()
        self.Column = Column
        # ...

# Wenn du nur importierst:
from flask_sqlalchemy import SQLAlchemy as db
# db.Model existiert NICHT (noch nicht initialisiert)

# Wenn du instanziierst:
db = SQLAlchemy()
# db.Model existiert JETZT (durch __init__ erstellt)
```

#### Zusammenfassung:
| Variante | Was ist `db`? | Funktioniert? |
|----------|---------------|---------------|
| `import SQLAlchemy as db` | Klasse (Bauplan) | ❌ Nein |
| `db = SQLAlchemy()` | Instanz (Objekt) | ✅ Ja |

**Merke:** `as db` benennt nur um, `db = SQLAlchemy()` erschafft das Objekt!

---

## Zusammenfassung

| Methode | Zweck | Rückgabe |
|---------|-------|----------|
| `Flask(__name__)` | App-Instanz erstellen | Flask-Objekt |
| `os.path.dirname()` | Verzeichnis aus Pfad extrahieren | String (Pfad) |
| `os.path.abspath()` | Absoluten Pfad erzeugen | String (Pfad) |
| `os.path.join()` | Pfade zusammenfügen | String (Pfad) |
| `db.init_app()` | DB mit App verbinden | None |

---

**Erstellt:** 2025-12-17
**Projekt:** book_alchemy
