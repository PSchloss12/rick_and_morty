
# Programming Paradigms Full Stack Project
This Flask App uses a SQL database in the background to load in data on the Rick and Morty show. Data was taken from the Rick and Morty API. 

All data is manipulated in OOP fashion using SQLAlchemy, Python, Flask, HTML, and CSS.

git 
### Running Rick and Morty (local)

Simple Flask app that caches Rick & Morty API data into a local SQLite DB and serves HTML pages from the `templates/` folder.

Files of interest:
- [rick_api.py](rick_api.py) — Flask app and routes (home, characters, locations).
- [db_manager.py](db_manager.py) — DB setup and helper [`init_db`](db_manager.py).
- [rick_classes.py](rick_classes.py) — domain classes: [`Character`](rick_classes.py), [`Location`](rick_classes.py), [`Episode`](rick_classes.py).
- templates: `templates/index.html`, `templates/gallery.html`, `templates/character.html`, `templates/location.html`, `templates/loc_list.html`, `templates/null.html`, `templates/header.html`.

Requirements
- Python 3.8+ (I'm using 3.10)
- Internet access for initial population (calls the public API)
- Packages: Flask, Flask-Bootstrap, Flask-Markdown, SQLAlchemy, requests

Quick setup (UNIX / macOS)
1. Create and activate a virtualenv:
   - python -m venv .venv
   - source .venv/bin/activate
2. Install dependencies using uv:
   - uv install Flask flask-bootstrap Flask-Markdown SQLAlchemy requests
   (or add a requirements.txt and run `uv install -r requirements.txt`)

Windows (PowerShell)
1. python -m venv .venv
2. .\.venv\Scripts\Activate.ps1
3. uv install Flask flask-bootstrap Flask-Markdown SQLAlchemy requests

Initialize the local database
- The DB file is `rick.sqlite` created in the project root by SQLAlchemy.
- To populate the DB from the Rick & Morty API run:
  - python -c "from db_manager import init_db; init_db()"
  This calls the initializer defined in [`db_manager.py`](db_manager.py). Note: the script fetches API pages and inserts characters/locations into the database.

Run the app locally
- Start the Flask server:
  - python rick_api.py
- By default the app runs on host `0.0.0.0` and port `12322`. Open:
  - http://127.0.0.1:12322/

UI overview
- Home: `/` — [templates/index.html](templates/index.html)
- Characters gallery & search: `/characters/` — search box posts back to `/characters/`; blank loads random groups (see [`gallery`](rick_api.py))
- Character detail: `/characters/<id>/` — shows character details and episodes (uses `Character.scrape(eps=True, locs=True)` in [`rick_api.py`](rick_api.py))
- Locations list: `/locations/` — list of locations (4 columns)
- Location detail: `/locations/<id>/` — shows residents (uses [`Location.scrape`](rick_classes.py))
- If a location URL is `None`, the app serves `templates/null.html`

Notes & troubleshooting
- DB file: `rick.sqlite` in repo root — delete to rebuild from scratch.
- If the DB is empty, the gallery/routes may raise errors; run `init_db()` to populate.
- If imports like `flaskext.markdown` fail, install `Flask-Markdown`.
- The project expects internet to fetch the Rick & Morty API during init or when a `scrape()` call is made.

Quick commands summary
- Create venv: python -m venv .venv
- Activate (mac/linux): source .venv/bin/activate
- Install deps: uv install Flask flask-bootstrap Flask-Markdown SQLAlchemy requests
- Init DB: python -c "from db_manager import init_db; init_db()"
- Run server: python rick_api.py

Notes:
- This README now shows dependency installation via the uv package manager. If you do not have uv installed, install it per its documentation (for example, `pip install uv`) or use your preferred installer.

License / Disclaimer
- This project uses data from the public Rick & Morty API (https://rickandmortyapi.com/). Use per their terms.
