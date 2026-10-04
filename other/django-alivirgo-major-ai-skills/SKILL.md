---
name: django
description: "Build Django models, views, routes, and admin features; review ORM queries, migrations, and deployment settings."
category: development
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["django", "orm", "python", "migrations", "admin", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Django Web Framework AI Skill Guide

## Overview & Engine Architecture

Django is a batteries-included Python web framework with an ORM, migrations, URL routing, forms/admin, and a middleware stack. Requests flow through middleware to URL resolvers and views; the ORM maps models to SQL. Agents write migrations carefully, prevent N+1 queries, keep `DEBUG=False` in production, and never commit `SECRET_KEY`.

```
HTTP -> WSGI/ASGI -> middleware -> URLconf -> view
                                      |
                                   ORM / templates / DRF
```

## When to use this skill

- Building server-rendered or API-backed Django apps
- Designing models and migrations
- Fixing ORM performance (N+1, missing indexes)
- Hardening settings for deployment

## Operational directives

1. Make migrations for every model change; review generated SQL for locks.
2. Use `select_related` / `prefetch_related` to avoid N+1.
3. Validate with forms/serializers; never trust raw `request.POST` for critical fields.
4. Store secrets in environment; rotate `SECRET_KEY` if exposed.
5. Prefer explicit `related_name` on relationships used in reverse.

## Model + migration sketch

```python
from django.db import models

class Order(models.Model):
    customer = models.ForeignKey("customers.Customer", on_delete=models.PROTECT, related_name="orders")
    status = models.CharField(max_length=32, db_index=True)
    total_cents = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["customer", "-created_at"]),
        ]
```

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
python manage.py test
```

## Query hygiene

```python
# Bad: N+1
for o in Order.objects.all():
    print(o.customer.email)

# Good:
for o in Order.objects.select_related("customer"):
    print(o.customer.email)
```

## Production settings checklist

| Setting | Expectation |
| --- | --- |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | explicit hosts |
| `CSRF_TRUSTED_ORIGINS` | https origins when needed |
| `SECURE_SSL_REDIRECT` | True behind TLS |
| Database | pooled connections; not sqlite in prod |

## Best practices

- Thin views; put domain logic in services/model methods thoughtfully.
- Use `TransactionTestCase` only when required - prefer `TestCase`.
- Constrain admin to staff users; audit dangerous actions.
- Collect static files in deployment pipelines.

## Limitations

- Async views/ORM support is partial depending on version and DB driver.
- Django REST Framework is a related but separate skill surface.
- Multi-tenant schemes need explicit design (schemas vs row filters).

## Related skills

- `@postgresql` - SQL and indexing behind the ORM
- `@fastapi` - alternative Python API stack
- `@docker` - containerizing gunicorn/uvicorn deployments
