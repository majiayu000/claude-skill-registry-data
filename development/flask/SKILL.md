---
name: flask
description: "Build Flask applications with app factories, blueprints, JSON or Jinja responses, extensions, and pytest checks."
category: development
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["flask", "python", "blueprints", "wsgi", "api", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Flask Python Web AI Skill Guide

## Overview & Engine Architecture

Flask is a WSGI microframework with explicit application factories, blueprints for modular routes, and a request/app context stack. Agents prefer factory + blueprint layout over a single global `app`, keep config in environment-backed objects, and run production traffic behind gunicorn/uwsgi - not the built-in server.

```
WSGI server (gunicorn)
        |
   create_app()
   +----+----+----+
   | blueprints    |
   | extensions    |
   | errorhandlers |
   +---------------+
```

## When to use this skill

- Building small-to-medium Python HTTP APIs or server-rendered apps
- Structuring multi-module Flask projects
- Adding auth, DB, or migrations via extensions
- Writing route tests with the Flask test client

## Operational directives

1. Use `create_app()` so tests and CLI can construct fresh apps.
2. Register blueprints with URL prefixes; avoid circular imports via late imports or extension init.
3. Load secrets from env (`SECRET_KEY`, DB URLs) - never hardcode.
4. Prefer JSON error handlers with correct status codes for APIs.
5. Use the production WSGI server in deploy; `app.run()` is local-only.

## App factory sketch

```python
from flask import Flask, Blueprint, jsonify, request

api = Blueprint("api", __name__)

@api.get("/health")
def health():
    return jsonify(ok=True)

@api.post("/items")
def create_item():
    body = request.get_json(silent=True) or {}
    sku = body.get("sku")
    if not isinstance(sku, str) or not sku:
        return jsonify(error="sku required"), 400
    return jsonify(id=1, sku=sku), 201

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(SECRET_KEY="dev-only-change-me")
    app.register_blueprint(api, url_prefix="/api")
    return app
```

## Commands

```bash
flask --app "app:create_app" run --debug
gunicorn "app:create_app()"
pytest -q
```

## Testing sketch

```python
from app import create_app

def test_health():
    app = create_app()
    client = app.test_client()
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.get_json()["ok"] is True
```

## Best practices

- Separate config classes (`Development`, `Production`, `Testing`).
- Use Flask-SQLAlchemy / Alembic or a thin DB layer - keep models out of route modules when possible.
- Enable CSRF protection for cookie-session form posts.
- Log exceptions once in a central handler; avoid duplicate noise.

## Limitations

- Async views exist in newer Flask but most extensions remain sync-first.
- Large async-native APIs may fit FastAPI better.
- Application context mistakes surface as "Working outside of application context" - fix factory/CLI wiring.

## Related skills

- `@fastapi` - async-first alternative for OpenAPI-heavy APIs
- `@python-packaging` - project layout, tooling, publishing
- `@docker` - containerizing gunicorn workers
