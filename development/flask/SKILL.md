---
name: flask
description: |
  Build Python web applications with Flask, using the application factory pattern, Blueprints,
  and Flask-SQLAlchemy. Covers project structure, authentication, and configuration management.

  Use when: creating Flask projects, organizing with blueprints, implementing authentication,
  or troubleshooting circular imports, application context errors, or blueprint registration.
---

# Flask Skill

Production-tested patterns for Flask with the application factory pattern, Blueprints, and Flask-SQLAlchemy.

**Latest Versions** (verified December 2025):
- Flask: 3.1.2
- Flask-SQLAlchemy: 3.1.1
- Flask-Login: 0.6.3
- Flask-WTF: 1.2.2
- Werkzeug: 3.1.3

---

## Quick Start

### Project Setup with uv

```bash
# Create project
uv init my-flask-app
cd my-flask-app

# Add dependencies
uv add flask flask-sqlalchemy flask-login flask-wtf python-dotenv

# Run development server
uv run flask --app app run --debug
```

### Minimal Working Example

```python
# app.py
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return {"message": "Hello, World!"}

if __name__ == "__main__":
    app.run(debug=True)
```

Run: `uv run flask --app app run --debug`

---

## Project Structure (Application Factory)

For maintainable applications, use the factory pattern with blueprints:

```
my-flask-app/
├── pyproject.toml
├── config.py                # Configuration classes
├── run.py                   # Entry point
│
├── app/
│   ├── __init__.py          # Application factory (create_app)
│   ├── extensions.py        # Flask extensions (db, login_manager)
│   ├── models.py            # SQLAlchemy models
│   │
│   ├── main/                # Main blueprint
│   │   ├── __init__.py
│   │   └── routes.py
│   │
│   ├── auth/                # Auth blueprint
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── forms.py
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── main/
│   │   └── auth/
│   │
│   └── static/
│       ├── css/
│       └── js/
│
└── tests/
    ├── conftest.py
    └── test_main.py
```

---

## Core Patterns

### Application Factory

```python
# app/__init__.py
from flask import Flask
from app.extensions import db, login_manager
from config import Config


def create_app(config_class=Config):
    """Application factory function."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Register blueprints
    from app.main import bp as main_bp
    from app.auth import bp as auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")

    # Create database tables
    with app.app_context():
        db.create_all()

    return app
```

**Key Benefits**:
- Multiple app instances with different configs (testing)
- Avoids circular imports
- Extensions initialized once, bound to app later

### Extensions Module

```python
# app/extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "info"
```

**Why separate file?**: Prevents circular imports - models can import `db` without importing `app`.

### Configuration

```python
# config.py
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
```

### Entry Point

```python
# run.py
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
```

Run: `flask --app run run --debug`

---

## Blueprints

### Creating a Blueprint

```python
# app/main/__init__.py
from flask import Blueprint

bp = Blueprint("main", __name__)

from app.main import routes  # Import routes after bp is created!
```

```python
# app/main/routes.py
from flask import render_template, jsonify
from app.main import bp


@bp.route("/")
def index():
    return render_template("main/index.html")


@bp.route("/api/health")
def health():
    return jsonify({"status": "ok"})
```

### Blueprint with Templates

```python
# app/auth/__init__.py
from flask import Blueprint

bp = Blueprint(
    "auth",
    __name__,
    template_folder="templates",  # Blueprint-specific templates
    static_folder="static",       # Blueprint-specific static files
)

from app.auth import routes
```

---

## Database Models

```python
# app/models.py
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db, login_manager


class User(UserMixin, db.Model):
    """User model for authentication."""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.email}>"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
```

---

## Authentication with Flask-Login

### Auth Forms

```python
# app/auth/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import User


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    confirm = PasswordField("Confirm Password", validators=[
        DataRequired(), EqualTo("password", message="Passwords must match")
    ])
    submit = SubmitField("Register")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already registered.")
```

### Auth Routes

```python
# app/auth/routes.py
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm
from app.extensions import db
from app.models import User


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            flash("Logged in successfully!", "success")
            return redirect(next_page or url_for("main.index"))
        flash("Invalid email or password.", "danger")

    return render_template("auth/login.html", form=form)


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.index"))
```

### Protecting Routes

```python
from flask_login import login_required, current_user

@bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("main/dashboard.html", user=current_user)
```

---

## API Routes (JSON)

For REST APIs without templates:

```python
# app/api/__init__.py
from flask import Blueprint

bp = Blueprint("api", __name__)

from app.api import routes
```

```python
# app/api/routes.py
from flask import jsonify, request
from flask_login import login_required, current_user
from app.api import bp
from app.extensions import db
from app.models import User


@bp.route("/users", methods=["GET"])
@login_required
def get_users():
    users = User.query.all()
    return jsonify([
        {"id": u.id, "email": u.email}
        for u in users
    ])


@bp.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already exists"}), 409

    user = User(email=data["email"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()

    return jsonify({"id": user.id, "email": user.email}), 201
```

Register with prefix:
```python
app.register_blueprint(api_bp, url_prefix="/api/v1")
```

---

## Critical Rules

### Always Do

1. **Use application factory pattern** - Enables testing, avoids globals
2. **Put extensions in separate file** - Prevents circular imports
3. **Import routes at bottom of blueprint `__init__.py`** - After `bp` is created
4. **Use `current_app` not `app`** - Inside request context
5. **Use `with app.app_context()`** - When accessing db outside requests

### Never Do

1. **Never import `app` in models** - Causes circular imports
2. **Never access `db` before app context** - RuntimeError
3. **Never store secrets in code** - Use environment variables
4. **Never use `app.run()` in production** - Use Gunicorn
5. **Never skip CSRF protection** - Keep Flask-WTF enabled

---

## Common Errors & Fixes

### Circular Import Error

**Error**: `ImportError: cannot import name 'X' from partially initialized module`

**Cause**: Models importing app, app importing models

**Fix**: Use extensions.py pattern:
```python
# WRONG - circular import
# app/__init__.py
from app.models import User  # models.py imports db from here!

# RIGHT - deferred import
# app/__init__.py
def create_app():
    # ... setup ...
    from app.models import User  # Import inside factory
```

### Working Outside Application Context

**Error**: `RuntimeError: Working outside of application context`

**Cause**: Accessing `current_app`, `g`, or `db` outside request

**Fix**:
```python
# WRONG
from app import create_app
app = create_app()
users = User.query.all()  # No context!

# RIGHT
from app import create_app
app = create_app()
with app.app_context():
    users = User.query.all()  # Has context
```

### Blueprint Not Found

**Error**: `werkzeug.routing.BuildError: Could not build url for endpoint`

**Cause**: Using wrong blueprint prefix in `url_for()`

**Fix**:
```python
# WRONG
url_for("login")

# RIGHT - include blueprint name
url_for("auth.login")
```

### CSRF Token Missing

**Error**: `Bad Request: The CSRF token is missing`

**Cause**: Form submission without CSRF token

**Fix**: Include token in templates:
```html
<form method="post">
    {{ form.hidden_tag() }}  <!-- Adds CSRF token -->
    <!-- form fields -->
</form>
```

---

## Testing

```python
# tests/conftest.py
import pytest
from app import create_app
from app.extensions import db
from config import TestingConfig


@pytest.fixture
def app():
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
```

```python
# tests/test_main.py
def test_index(client):
    response = client.get("/")
    assert response.status_code == 200


def test_register(client):
    response = client.post("/auth/register", data={
        "email": "test@example.com",
        "password": "testpass123",
        "confirm": "testpass123",
    }, follow_redirects=True)
    assert response.status_code == 200
```

Run: `uv run pytest`

---

## Deployment

### Development
```bash
flask --app run run --debug
```

### Production with Gunicorn
```bash
uv add gunicorn
uv run gunicorn -w 4 -b 0.0.0.0:8000 "run:app"
```

### Docker
```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY . .

RUN pip install uv && uv sync

EXPOSE 8000
CMD ["uv", "run", "gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "run:app"]
```

### Environment Variables (.env)
```
SECRET_KEY=your-production-secret-key
DATABASE_URL=postgresql://user:pass@localhost/dbname
FLASK_ENV=production
```

---

## References

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.readthedocs.io/)
- [Flask-Login](https://flask-login.readthedocs.io/)
- [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
- [Application Factory Pattern](https://flask.palletsprojects.com/en/stable/patterns/appfactories/)

---

**Last Updated**: December 2025
**Maintainer**: Jezweb | jeremy@jezweb.net
