---
name: flask
description: Flask Python microframework. Use when building Flask apps, blueprints for modular routes, Jinja2 templates, SQLAlchemy ORM, Flask-RESTful APIs, or using extensions.
---

## flask

Lightweight Python microframework with minimal core and rich extension ecosystem.

### Core Concepts
- Blueprints: modular route organization with `Blueprint` objects, mounted at URL prefixes
- Jinja2 templates: server-side rendering with template inheritance, filters, and macros
- SQLAlchemy ORM: `db.Model` for declarative models, `db.session` for transactional queries
- App factory: `create_app()` function for configurable, testable application instances

### Common Patterns
- Flask-RESTful: `Resource` subclasses with method-based routing for REST endpoints
- Error handlers: `@app.errorhandler(404)` for custom JSON or HTML error responses
- Extensions: Flask-Login for auth, Flask-Migrate for schema changes, Flask-Mail for email
- Request hooks: `before_request`/`after_request` for cross-cutting concerns like DB sessions

### Best Practices
- Use the app factory pattern to enable multiple config profiles (dev, test, production)
- Keep configuration in environment variables with `app.config.from_prefixed_env()`
- Organize views into blueprints by domain rather than dumping all routes in one file
- Use `g` object sparingly for request-scoped data, clean up with `teardown_appcontext`

### Common Code Patterns
- `Blueprint("auth", __name__, url_prefix="/auth")` with `register_blueprint` in factory
- `db.relationship("Post", backref="author", lazy="dynamic")` for one-to-many ORM access
