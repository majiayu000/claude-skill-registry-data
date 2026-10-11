---
name: setup
description: |
  Use when the user asks to "verify Flask project setup", "check Flask structure", "is my Flask app set up correctly", "validate Flask project", or needs to confirm that a Flask project follows recommended patterns and has correct file structure.
---

# Flask Project Setup Verification

Verify that a Flask project is correctly structured and follows recommended patterns.

## Project Structure Check

Inspect the project root for these expected elements:

| Item | Purpose | Required? |
|------|---------|-----------|
| `app.py` or `wsgi.py` | Application entry point with factory function | Yes |
| `requirements.txt` or `pyproject.toml` | Python dependencies | Yes |
| `extensions.py` | `db`, `migrate`, `login_manager`, `csrf` created without an app | Recommended |
| `models.py` or `models/` | SQLAlchemy models | If using DB |
| `routes/` or `blueprints/` | Blueprint modules | Recommended |
| `templates/` | Jinja2 HTML templates | If rendering HTML |
| `static/` | CSS, JS, images | If serving static files |
| `instance/` | Instance-specific config and SQLite DB | Common |
| `.env` / `.flaskenv` or `config.py` | Configuration (`.env` private and gitignored, `.flaskenv` public defaults) | Recommended |

## Verification Steps

### 1. Check Application Factory

Read the main app file and verify it uses the application factory pattern:

```python
# Expected pattern
def create_app():
    app = Flask(__name__)
    app.config.from_object(...)
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    # Register blueprints
    app.register_blueprint(auth_bp)
    return app
```

If the app uses a global `app = Flask(__name__)` instead, flag it — the factory pattern is strongly recommended for testability and multiple instances.

### 2. Check Dependencies

Read `requirements.txt` or `pyproject.toml` and verify core Flask packages:

| Package | Purpose |
|---------|---------|
| `Flask` | Core framework |
| `Flask-SQLAlchemy` | Database ORM integration |
| `SQLAlchemy` | Pinned `<2.1` next to Flask-SQLAlchemy (see below) |
| `Flask-Login` | Session-based authentication |
| `Flask-WTF` | Forms and `CSRFProtect` (recommended for any app that renders HTML forms) |
| `Flask-Migrate` | Database migrations via Alembic (recommended) |
| `python-dotenv` | Environment variable loading (recommended) |
| `gunicorn` | Production WSGI server (recommended) |

```bash
pip install Flask Flask-SQLAlchemy "SQLAlchemy<2.1" Flask-Login Flask-Migrate Flask-WTF python-dotenv gunicorn
```

Python: use 3.10 or newer. Flask 3.1 still runs on 3.9, but Flask 3.2 and Flask-WTF 1.3 need 3.10, and Flask-Caching 2.5 needs 3.11.

**Why `SQLAlchemy<2.1`.** As of 2026-10 the latest Flask-SQLAlchemy is 3.1.1 (2023-09). It declares `sqlalchemy>=2.0.16` with no upper bound, so a plain install resolves SQLAlchemy 2.1. A `MappedAsDataclass` base fails on SQLAlchemy 2.1 with `InvalidRequestError ... is already a dataclass` ([pallets-eco/flask-sqlalchemy#1420](https://github.com/pallets-eco/flask-sqlalchemy/issues/1420), open); a plain `db.Model` still works, so the pin is a precaution. Pin `SQLAlchemy<2.1` to be safe until a Flask-SQLAlchemy release supports 2.1, and re-check the issue before dropping it. Pin it in `requirements.txt` / `pyproject.toml` too, not only on the command line.

If you need dataclass models on SQLAlchemy 2.1 now, drop `MappedAsDataclass` or move to [Flask-SQLAlchemy-Lite](https://flask-sqlalchemy-lite.readthedocs.io/en/stable/), the lighter extension the Flask-SQLAlchemy maintainers point to in that issue.

### 3. Check Blueprint Registration

Verify that routes are organized into blueprints and registered in the factory:

```python
# In routes/auth.py
auth_bp = Blueprint('auth', __name__)

# In app.py create_app()
app.register_blueprint(auth_bp)
```

### 4. Check Configuration

Verify that sensitive values use environment variables, not hardcoded strings, and that the app refuses to start without them:

```python
# Good: a missing key is an error, not a silent default
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

# Bad: hardcoded secret
app.config['SECRET_KEY'] = 'my-secret-key'

# Bad: hardcoded fallback (every deployment that forgets the variable shares one key)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'change-me')
```

Debug mode must come from `--debug` / `FLASK_DEBUG`, and the config class from an app-level variable such as `APP_ENV`. `FLASK_ENV` was removed in Flask 2.3 (with the `ENV` config key and `app.env`) and is ignored: flag it if you find it in `.flaskenv`, `.env` or a Dockerfile.

### 5. Check CSRF Protection

Any app that renders HTML forms needs `CSRFProtect` (or `FlaskForm` for every form):

```python
# extensions.py
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect()

# app.py create_app()
csrf.init_app(app)
```

Without it `{{ csrf_token() }}` in a template raises `UndefinedError`, and plain `<form method="post">` handlers accept cross-site requests.

### 6. Common Setup Issues

| Issue | Symptom | Fix |
|-------|---------|-----|
| No app factory | Tests fail, circular imports | Wrap in `create_app()` function |
| Hardcoded `SECRET_KEY` or a fallback value | Security risk, shared key | Read it with `os.environ['SECRET_KEY']` or fail in `create_app()` |
| No `CSRFProtect` | `csrf_token` undefined, unprotected POST routes | `csrf = CSRFProtect()` in `extensions.py`, `csrf.init_app(app)` |
| `db.create_all()` in the factory next to Flask-Migrate | `flask db migrate` says "No changes in schema detected" and creates no revision | Remove it; use `flask db upgrade`; keep `create_all()` in test fixtures only |
| `SQLAlchemy` 2.1 installed with Flask-SQLAlchemy 3.1.x | `InvalidRequestError ... is already a dataclass` with a `MappedAsDataclass` base | `pip install "SQLAlchemy<2.1"`, or drop `MappedAsDataclass` |
| Python below 3.10 | pip quietly resolves older Flask and Flask-WTF releases; Flask 3.2 will not install | Use Python 3.10+ |
| Missing `__init__.py` in routes/ | Import errors | Add empty `__init__.py` |
| No `.gitignore` for `instance/` | Database committed to git | Add `instance/` to `.gitignore` |
| No `Flask-Migrate` | Schema changes drop data | Add Alembic migrations |

## What This Skill Does NOT Cover

- Creating a new Flask project from scratch (see `project-scaffold` skill; patterns in `app-patterns`)
- Login, registration and password handling (see `auth-flask-login` skill)
- Database model design (see sqlalchemy-dev plugin)
- Deployment configuration (belongs in project template)