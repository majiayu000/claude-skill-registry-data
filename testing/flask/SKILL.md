---
name: flask
description: "Expert skill for Flask web framework development. Covers application factory, blueprints, routing, request/response handling, Jinja2 templates, application and request context (g, current_app), configuration, extensions ecosystem (SQLAlchemy, Login, WTF, CORS, Migrate), error handling, testing, and deployment. WHEN: \"Flask\", \"flask\", \"Werkzeug\", \"Jinja2\", \"Blueprint\", \"Flask blueprint\", \"flask factory\", \"create_app\", \"Flask-SQLAlchemy\", \"Flask-Login\", \"Flask-WTF\", \"Flask-Migrate\", \"Flask-CORS\", \"Flask-JWT-Extended\", \"Flask-Caching\", \"Flask-Smorest\", \"flask test_client\", \"flask extension\", \"flask context\", \"current_app\", \"g object\", \"flask deployment\", \"flask gunicorn\". Do NOT use for general Python scripting, automation, or CLI-tool questions unrelated to the Flask framework — that's the `cli-scripting` plugin's `python` skill."
license: MIT
---

# Flask

This skill covers Flask web framework development. Flask is a lightweight WSGI micro-framework built on Werkzeug (routing, request/response) and Jinja2 (templating). It provides a minimal core -- routing, request handling, and templates -- with an extensive extensions ecosystem for everything else. Flask 3.1 runs on Python 3.10+ and supports async views via `asgiref`. There is no version-specific reference material (single stable 3.x line).

## How to Approach Tasks

1. **Classify** the request:
   - **Architecture** -- Load `references/architecture.md` for application factory, context stacks, Werkzeug foundation, routing internals, Jinja2, signals, extension loading, WSGI interface, async support
   - **Best practices** -- Load `references/best-practices.md` for project structure, extensions integration, testing, security, deployment, performance, Flask vs FastAPI decision guide

2. **Gather context** -- Check Python version (3.10+ for Flask 3.x), Flask version, which extensions are in use, sync vs async views, deployment target (Gunicorn, Docker, serverless).

3. **Load context** -- Read the relevant reference file before answering.

4. **Analyze** -- Apply Flask-specific reasoning. Consider application factory pattern, context stack behavior, extension initialization order, and the sync-first nature of Flask.

5. **Recommend** -- Provide concrete Python code examples with explanations. Always qualify trade-offs.

6. **Verify** -- Suggest validation steps: run tests with `pytest`, check route registration with `flask routes`, verify extension initialization order.

## Core Architecture

### Application Factory

The cornerstone of production Flask applications. Instead of a global `app`, a `create_app()` function constructs and configures the application.

```python
# myapp/__init__.py
from flask import Flask
from .extensions import db, migrate, login_manager, cache
from .config import config_by_name

def create_app(config_name: str = "production") -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    # Load configuration
    app.config.from_object(config_by_name[config_name])
    app.config.from_pyfile("config.py", silent=True)

    # Initialize extensions (order matters -- db before migrate)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    cache.init_app(app)

    # Register blueprints
    from .api.v1 import api_v1_bp
    from .auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(api_v1_bp, url_prefix="/api/v1")

    register_error_handlers(app)
    return app
```

```python
# myapp/extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_caching import Cache

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
cache = Cache()
```

**Key benefits:** Multiple instances for testing, deferred extension initialization, clean import graphs (no circular imports).

### Blueprints

Flask's modular unit. Blueprints carry routes, templates, static files, error handlers, and before/after request hooks.

```python
from flask import Blueprint

auth_bp = Blueprint("auth", __name__, template_folder="templates", url_prefix="/auth")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    return render_template("auth/login.html")

# Nesting (Flask 2.0+)
parent_bp = Blueprint("parent", __name__, url_prefix="/parent")
child_bp = Blueprint("child", __name__)
parent_bp.register_blueprint(child_bp, url_prefix="/child")

# Blueprint-scoped hooks
@auth_bp.before_request
def require_json():
    if request.method in ("POST", "PUT", "PATCH") and not request.is_json:
        abort(415)
```

### Routing

```python
# Variable rules with converters: string, int, float, path, uuid
@app.route("/users/<int:user_id>")
def get_user(user_id: int):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

# Class-based views
from flask.views import MethodView

class UserResource(MethodView):
    def get(self, user_id: int | None = None):
        if user_id is None:
            return jsonify([u.to_dict() for u in User.query.all()])
        return jsonify(User.query.get_or_404(user_id).to_dict())

    def post(self):
        data = request.get_json(force=True)
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        return jsonify(user.to_dict()), 201

user_view = UserResource.as_view("user_resource")
app.add_url_rule("/users/", view_func=user_view, methods=["GET", "POST"])
app.add_url_rule("/users/<int:user_id>", view_func=user_view, methods=["GET", "DELETE"])
```

### Request and Response

```python
from flask import request, jsonify, make_response, redirect, url_for, abort

# Incoming data
request.args          # query string (ImmutableMultiDict)
request.form          # form data
request.files         # uploaded files
request.json          # parsed JSON body
request.get_json(force=True, silent=True)
request.data          # raw body bytes
request.headers       # case-insensitive dict

# Response helpers
return jsonify({"status": "ok"}), 200
return redirect(url_for("auth.login"), 302)
abort(404)

# Full control
resp = make_response(jsonify({"error": "not found"}), 404)
resp.headers["X-Custom"] = "value"
resp.set_cookie("session_id", "abc123", httponly=True, samesite="Lax")
return resp
```

### Application and Request Context

Flask uses two context stacks pushed around each request and CLI command.

| Object | Context | Purpose |
|---|---|---|
| `current_app` | App context | Proxy to the active Flask application |
| `g` | App context (per-request) | Request-scoped scratch space |
| `request` | Request context | Incoming HTTP request data |
| `session` | Request context | Signed cookie-based session |

```python
from flask import g, current_app, session

@app.before_request
def load_logged_in_user():
    user_id = session.get("user_id")
    g.user = User.query.get(user_id) if user_id else None

# Manual context (scripts, Celery tasks, tests)
with app.app_context():
    db.create_all()
```

### Configuration

```python
class BaseConfig:
    SECRET_KEY: str = os.environ["SECRET_KEY"]
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

class DevelopmentConfig(BaseConfig):
    DEBUG: bool = True
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///dev.db"

class TestingConfig(BaseConfig):
    TESTING: bool = True
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///:memory:"
    WTF_CSRF_ENABLED: bool = False

class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI: str = os.environ["DATABASE_URL"]
    SESSION_COOKIE_SECURE: bool = True
    SESSION_COOKIE_HTTPONLY: bool = True

config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
```

### Jinja2 Templates

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html>
<head><title>{% block title %}My App{% endblock %}</title></head>
<body>
    <main>{% block content %}{% endblock %}</main>
</body>
</html>

<!-- templates/users/list.html -->
{% extends "base.html" %}
{% block content %}
  <ul>
    {% for user in users %}
      <li>{{ user.name | title }}</li>
    {% else %}
      <li>No users found.</li>
    {% endfor %}
  </ul>
{% endblock %}
```

### Extensions Ecosystem

| Extension | Purpose |
|---|---|
| **Flask-SQLAlchemy** | SQLAlchemy integration with session management |
| **Flask-Migrate** | Alembic migrations via `flask db` CLI |
| **Flask-Login** | Session-based user authentication |
| **Flask-WTF** | WTForms integration with CSRF protection |
| **Flask-CORS** | Cross-Origin Resource Sharing headers |
| **Flask-JWT-Extended** | JWT authentication for APIs |
| **Flask-Caching** | Response and function caching (Redis, Memcached) |
| **Flask-Smorest** | OpenAPI-first REST APIs with Marshmallow |
| **Flask-Mail** | Email sending |
| **Flask-Talisman** | Security headers (CSP, HSTS) |

### Error Handling

```python
from werkzeug.exceptions import HTTPException

@app.errorhandler(404)
def not_found(e):
    if request.accept_mimetypes.accept_json:
        return jsonify(error=str(e), code=404), 404
    return render_template("errors/404.html"), 404

@app.errorhandler(HTTPException)
def handle_http_exception(e: HTTPException):
    return jsonify(code=e.code, name=e.name, description=e.description), e.code

# Custom exceptions
class ResourceNotFound(Exception):
    def __init__(self, resource: str, id: int):
        self.resource = resource
        self.id = id

@app.errorhandler(ResourceNotFound)
def handle_not_found(e):
    return jsonify(error=str(e), resource=e.resource, id=e.id), 404
```

### Testing

```python
import pytest

@pytest.fixture(scope="session")
def app():
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def cli_runner(app):
    return app.test_cli_runner()

def test_create_user(client, db):
    resp = client.post("/api/v1/users/", json={"email": "new@example.com", "password": "strong"})
    assert resp.status_code == 201
    assert resp.json["email"] == "new@example.com"

def test_protected_route_requires_auth(client):
    resp = client.get("/api/v1/protected")
    assert resp.status_code == 401
```

### Deployment

| Method | Command / Config |
|---|---|
| Development | `flask run --debug` |
| Gunicorn (Linux) | `gunicorn "myapp:create_app('production')" -w 4 -b 0.0.0.0:8000` |
| Waitress (Windows) | `waitress-serve --port=8000 "myapp:create_app('production')"` |
| Docker | Gunicorn + Nginx reverse proxy, non-root user |

**Never use the Flask development server in production.** Always use a WSGI server (Gunicorn, Waitress).

## Key Patterns

| Pattern | When to Use |
|---|---|
| Application factory | Always in production. Enables testing, multiple configs |
| Blueprints | Any app with more than one logical module |
| `before_request` hooks | Auth checks, request logging, loading user into `g` |
| Extension `init_app()` | Deferred initialization in factory pattern |
| `url_for()` | Always. Never hardcode URLs |
| `MethodView` | RESTful resource endpoints |
| Instance folder | Machine-specific secrets, git-ignored config |

## Async Support

Flask 2.0+ supports `async def` views via `asgiref`, but Flask remains WSGI at the server level. Async views run in a thread pool, not on an event loop.

```python
@app.route("/async-view")
async def async_view():
    async with httpx.AsyncClient() as client:
        resp = await client.get("https://api.example.com/data")
    return jsonify(resp.json())
```

**Limitations:** One request per thread. No true concurrency. For high-concurrency I/O, use FastAPI or Celery for background tasks.

## Anti-Patterns

1. **Global `app` without factory** -- Breaks testing, prevents multiple configs.
2. **Circular imports** -- Import blueprints inside `create_app()`, not at module top.
3. **Business logic in routes** -- Use service layer. Routes handle HTTP only.
4. **`db.session.commit()` without error handling** -- Always catch `IntegrityError` and rollback.
5. **Hardcoded URLs** -- Use `url_for()` everywhere.
6. **Flask dev server in production** -- Always use Gunicorn or Waitress.

## Reference Files

Load these for deep knowledge on specific topics:

- `references/architecture.md` -- Application factory, context stacks (app context, request context, g object), Werkzeug foundation, routing internals, Jinja2 template engine, signal system, extension loading, WSGI interface, async support. **Load when:** architecture questions, context stack confusion, extension initialization, routing mechanics.
- `references/best-practices.md` -- Project structure (functional vs divisional), extensions integration (SQLAlchemy, Migrate, Login, WTF), testing (test_client, pytest fixtures), security (CSRF, sessions, cookies), deployment (Gunicorn, Docker), performance, Flask vs FastAPI decision guide. **Load when:** "how should I structure", extension setup, testing strategy, security hardening, deployment configuration.
