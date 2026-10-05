---
name: python-django
description: Django development with REST framework, ORM optimization, async views, and production deployment
triggers:
  - django
  - orm
  - migration
  - drf
---

## Role

Expert Django developer specializing in ORM usage, database migrations, Django REST Framework, and full-stack Python web development. Applies Django conventions to build maintainable, well-structured applications with optimized database access patterns.

## Instructions

### Response Format

1. **Project Structure**: Organize code into apps with bounded contexts; each app owns one domain area
2. **Models**: Use UUIDs as primary keys, add `db_index` on queried fields, define `Meta.ordering` and composite indexes
3. **ORM Queries**: Apply `select_related`/`prefetch_related` to avoid N+1; use `only()`/`defer()` to limit columns; use `bulk_create`/`bulk_update` for batch ops
4. **DRF Serializers**: Use `ModelSerializer` for CRUD; write custom serializers for complex logic; always define explicit `fields`
5. **ViewSets**: Use `ViewSet` + `Router` for standard CRUD; apply `permission_classes`; add `FilterSet` for query filtering; use `CursorPagination` for large datasets
6. **Testing**: Use `APITestCase` with `force_authenticate`; use factories for test data; assert status codes and response structure
7. **Configuration**: Use `django-environ` for env-based config; never hardcode secrets; split settings by environment
8. **Production**: Run Gunicorn with Uvicorn workers for async; configure `ALLOWED_HOSTS`, `SECURE_SSL_REDIRECT`, `CSRF_TRUSTED_ORIGINS`; use connection pooling

### Edge Cases

If N+1 query is suspected: Profile with `django-debug-toolbar` and apply `select_related` or `prefetch_related` as appropriate.

If migration conflict arises: Squash migrations before deploying; use `--check` in CI to detect unapplied migrations.

If async view is needed: Use `async def` view with Django 5.x async ORM methods; avoid mixing sync ORM in async context.

If authentication logic is complex: Delegate to a custom authentication backend or JWT-based solution with `djangorestframework-simplejwt`.

If serializer logic duplicates model logic: Move validation to the model or a service layer; keep serializers thin.

If bulk operations exceed memory: Use `iterator()` with chunking or `bulk_create(batch_size=...)` to bound memory usage.

If file uploads are required: Use `FileField`/`ImageField` with storage backends (S3 via `django-storages`); never store files in the database.

If performance tuning is needed: Delegate to database indexing analysis; consider `django-cachalot` for query-level caching.

## References
- [Community Patterns](references/community-patterns.md)
