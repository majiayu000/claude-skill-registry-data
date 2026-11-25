---
name: django-rules
description: Standing rules for Django code covering app layout, where business logic lives, querysets without N+1, safe migrations, forms and validation, settings per environment and security defaults.
license: CC0-1.0
metadata:
  version: 1.0.0
  kind: rule
  category: conventions
  source: https://hermes-ide.com/prompts/django-rules
  catalog: 2026.1014.1
---

# Django rules

Apply these rules to files matching: `**/*.py`, `**/templates/**/*.html`.

When you write or change code in this Django project:

**Layout and where logic lives**
- Follow the project's existing app structure. Put a new feature in the app that owns its models; create a new app only for a genuinely separate domain concept.
- Keep views thin: parse the request, call the domain code, return a response. Put rules that belong to one model on the model or its custom manager or queryset. Put workflows that touch several models, external services or side effects in a plain function in a `services.py` (or the project's equivalent), and call it from views, commands and tasks alike.
- Reference the user model through `settings.AUTH_USER_MODEL` in models and `get_user_model()` in code, never `django.contrib.auth.models.User` directly.

**Queries**
- Every list view or loop over a queryset that touches a related object uses `select_related` (foreign key, one-to-one) or `prefetch_related` (many-to-many, reverse foreign key). If you add a template or serializer field that follows a relation, update the queryset in the same change.
- Never query inside a loop. Use `bulk_create`, `bulk_update`, `in_bulk`, `Subquery`, `annotate` or `aggregate` instead.
- Use `F()` expressions or `select_for_update()` inside `transaction.atomic()` for counters and read-modify-write updates, so concurrent requests cannot lose writes.
- Use `.exists()` rather than `len()` or truthiness to test for rows, `.count()` rather than `len(qs)` when you do not need the objects, and `.only()` or `.values()` for wide tables when you need a few fields.
- Raw SQL is a last resort and always uses query parameters, never string formatting.

**Migrations**
- Generate migrations with `makemigrations`, read them, and commit them with the model change. Never edit a migration that has already been applied on a shared environment; add a new one.
- Every data migration with `RunPython` has a reverse function (or `RunPython.noop` with a reason) and uses `apps.get_model`, never a direct model import.
- On large or busy tables, make changes in deploy-safe steps: add a nullable column, backfill in batches, then add the constraint. Remove a field in two releases (stop using it, then drop it). Use the project's concurrent-index approach on PostgreSQL rather than locking the table.

**Forms, serializers and validation**
- Validate all input through forms, model forms or the API framework's serializers. Put cross-field rules in `clean()` or `validate()`, and model invariants in model constraints (`CheckConstraint`, `UniqueConstraint`), not only in Python.
- Never trust hidden fields or client-side checks for permissions or prices.

**Side effects and transactions**
- Wrap multi-step writes in `transaction.atomic()`. Send email, enqueue tasks and call webhooks with `transaction.on_commit` so they never fire for a rolled-back write.
- Pass primary keys to background tasks, not model instances, and re-fetch inside the task.

**Settings**
- Read secrets and per-environment values from environment variables (or the project's settings tool), never hard-code them. `SECRET_KEY`, database credentials and API keys never appear in the repository.
- Production runs with `DEBUG = False`, an explicit `ALLOWED_HOSTS`, `SECURE_*` and `*_COOKIE_SECURE` settings enabled, and the security, CSRF, session and clickjacking middleware in place. Do not disable `CsrfViewMiddleware` or add `csrf_exempt` to a view used by browsers.

**Templates and output**
- Rely on auto-escaping. Never call `mark_safe`, `|safe` or `format_html` with untrusted content unescaped.
- Use `{% url %}` and `reverse()` with named routes instead of hard-coded paths.

**Tests and checks**
- Add or update tests with the project's runner (Django's `TestCase` or pytest-django) for every behaviour change, including a test that asserts the query count (`assertNumQueries` or `django_assert_num_queries`) for list endpoints you touched.
- Before finishing, run the tests, `python manage.py check`, and `makemigrations --check` to prove no migration is missing.
