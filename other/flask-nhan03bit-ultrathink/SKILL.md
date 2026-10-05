---
name: flask
description: Flask web framework patterns, Blueprints, extensions, SQLAlchemy integration, and REST API design.
layer: domain
category: backend
triggers:
  - "flask"
  - "flask blueprint"
  - "flask extension"
  - "flask sqlalchemy"
  - "flask rest"
inputs:
  - "Flask application architecture questions"
  - "Blueprint organization and registration"
  - "Extension integration (SQLAlchemy, Migrate, etc.)"
  - "REST API endpoint design"
outputs:
  - "Flask application structure with Blueprints"
  - "SQLAlchemy model and query patterns"
  - "REST API endpoints with proper error handling"
  - "Extension configuration and initialization"
linksTo:
  - python
  - postgresql
  - redis
linkedFrom: []
preferredNextSkills:
  - python
  - postgresql
  - docker
fallbackSkills:
  - fastapi
  - django
riskLevel: low
memoryReadPolicy: selective
memoryWritePolicy: none
sideEffects: []
---

# Flask Web Framework Patterns

## Purpose

Provide expert guidance on Flask application architecture, Blueprint organization, extension integration, REST API design, and production deployment patterns. Covers Flask 3.x with modern Python async support and type hints.

## Application Factory Pattern

Always use the application factory pattern for testability and multiple configurations:

```python
# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name: str = "default") -> Flask:
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, resources={r"/api/*": {"origins": app.config["ALLOWED_ORIGINS"]}})

    # Register blueprints
    from app.api.auth import auth_bp
    from app.api.users import users_bp
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(users_bp, url_prefix="/api/users")

    # Register error handlers
    register_error_handlers(app)

    return app
```

## Blueprint Organization

Structure Blueprints by domain, not by technical layer:

```
app/
  __init__.py          # create_app factory
  models/
    __init__.py
    user.py
    order.py
  api/
    auth/
      __init__.py      # Blueprint definition
      routes.py        # Route handlers
      schemas.py       # Marshmallow/Pydantic schemas
      services.py      # Business logic
    users/
      __init__.py
      routes.py
      schemas.py
      services.py
  core/
    config.py
    errors.py
    middleware.py
```

**Blueprint definition:**

```python
# app/api/users/__init__.py
from flask import Blueprint

users_bp = Blueprint("users", __name__)

from app.api.users import routes  # noqa: E402, F401 — register routes
```

**Route handlers — keep thin, delegate to services:**

```python
# app/api/users/routes.py
from flask import request, jsonify
from app.api.users import users_bp
from app.api.users.schemas import UserCreateSchema, UserResponseSchema
from app.api.users.services import UserService

@users_bp.route("/", methods=["POST"])
def create_user():
    schema = UserCreateSchema()
    data = schema.load(request.get_json())
    user = UserService.create(data)
    return jsonify(UserResponseSchema().dump(user)), 201

@users_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id: int):
    user = UserService.get_or_404(user_id)
    return jsonify(UserResponseSchema().dump(user))
```

## SQLAlchemy Integration

**Model patterns with proper relationships:**

```python
# app/models/user.py
from datetime import datetime
from app import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    orders = db.relationship("Order", back_populates="user", lazy="dynamic")

    def __repr__(self) -> str:
        return f"<User {self.email}>"
```

**Query patterns — use service layer:**

```python
# app/api/users/services.py
from flask import abort
from app import db
from app.models.user import User

class UserService:
    @staticmethod
    def get_or_404(user_id: int) -> User:
        return db.get_or_404(User, user_id, description=f"User {user_id} not found")

    @staticmethod
    def create(data: dict) -> User:
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def list_active(page: int = 1, per_page: int = 20):
        return User.query.filter_by(is_active=True).paginate(
            page=page, per_page=per_page, error_out=False
        )
```

## REST API Patterns

**Consistent error handling:**

```python
# app/core/errors.py
from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

def register_error_handlers(app: Flask):
    @app.errorhandler(HTTPException)
    def handle_http_error(error):
        return jsonify({
            "error": error.name,
            "message": error.description,
            "status": error.code,
        }), error.code

    @app.errorhandler(422)
    def handle_validation_error(error):
        return jsonify({
            "error": "Validation Error",
            "messages": error.description,
            "status": 422,
        }), 422
```

**Request validation with Marshmallow:**

```python
# app/api/users/schemas.py
from marshmallow import Schema, fields, validate

class UserCreateSchema(Schema):
    email = fields.Email(required=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    password = fields.Str(
        required=True, validate=validate.Length(min=8), load_only=True
    )

class UserResponseSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email()
    name = fields.Str()
    is_active = fields.Bool()
    created_at = fields.DateTime()
```

## Configuration Management

```python
# app/core/config.py
import os

class Config:
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "postgresql://localhost/myapp_dev"
    )
    ALLOWED_ORIGINS = ["http://localhost:3000"]

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 10,
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    ALLOWED_ORIGINS = os.environ["ALLOWED_ORIGINS"].split(",")

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    ALLOWED_ORIGINS = ["*"]

config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
```

## Middleware and Hooks

```python
# app/core/middleware.py
import time
from flask import Flask, g, request
import logging

logger = logging.getLogger(__name__)

def register_middleware(app: Flask):
    @app.before_request
    def before_request():
        g.start_time = time.monotonic()

    @app.after_request
    def after_request(response):
        if hasattr(g, "start_time"):
            duration = time.monotonic() - g.start_time
            logger.info(
                "request_completed",
                extra={
                    "method": request.method,
                    "path": request.path,
                    "status": response.status_code,
                    "duration_ms": round(duration * 1000, 2),
                },
            )
        return response
```

## Testing

```python
# tests/conftest.py
import pytest
from app import create_app, db as _db

@pytest.fixture(scope="session")
def app():
    app = create_app("testing")
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def db_session(app):
    with app.app_context():
        yield _db.session
        _db.session.rollback()

# tests/api/test_users.py
def test_create_user(client):
    response = client.post("/api/users/", json={
        "email": "test@example.com",
        "name": "Test User",
        "password": "securepass123",
    })
    assert response.status_code == 201
    assert response.json["email"] == "test@example.com"
```

## Best Practices

1. **Always use the application factory** — Never use a global `app` object directly.
2. **Keep route handlers thin** — Delegate business logic to a service layer.
3. **Use Blueprints for all routes** — Even small apps benefit from modular organization.
4. **Configure SQLAlchemy connection pooling** — Set `pool_size`, `pool_recycle`, and `pool_pre_ping` in production.
5. **Use Flask-Migrate for schema changes** — Never run `db.create_all()` in production.
6. **Validate all input** — Use Marshmallow or Pydantic schemas on every endpoint.
7. **Return consistent error responses** — Register global error handlers for uniform JSON errors.
8. **Use `g` for request-scoped data** — Not module-level globals.
9. **Pin extension versions** — Flask extensions can have breaking changes between minors.
10. **Use Gunicorn or uWSGI in production** — Never use the Flask dev server.

## Common Pitfalls

| Pitfall | Problem | Fix |
|---------|---------|-----|
| Circular imports | Models import app, app imports models | Use application factory + `init_app()` pattern |
| Missing `db.session.commit()` | Data never persists | Always commit in service layer or use context manager |
| No connection pool tuning | DB connection exhaustion under load | Set `SQLALCHEMY_ENGINE_OPTIONS` with pool settings |
| Global app object | Untestable, config locked at import | Use `create_app()` factory |
| `request` outside context | RuntimeError in background tasks | Pass data explicitly or use `app.app_context()` |
| Dev server in production | Single-threaded, no SSL, debug mode | Use Gunicorn: `gunicorn -w 4 "app:create_app()"` |
