---
name: django
description: Use when building Django applications. Covers ORM query performance, model design, migrations, Django REST Framework, security defaults, and testing.
metadata:
  category: backend
  version: 1.0.0
  tags: [django, orm, drf, migrations, python]
---

# Django

## Purpose

Build Django applications that use the ORM efficiently and the framework's security defaults correctly. Most Django performance problems are one missing `select_related` away from being fixed.

## When to Use

- Building or reviewing a Django application or DRF API.
- Diagnosing slow views caused by the ORM.
- Writing migrations that must run against a large table.
- Auditing Django security settings before launch.

## Capabilities

- ORM: `select_related`, `prefetch_related`, annotations, subqueries, bulk operations.
- Model design: constraints, indexes, and validation at the database level.
- Migrations, including zero-downtime patterns for large tables.
- Django REST Framework: serializers, viewsets, permissions, pagination.
- Security: the settings that must not be wrong in production.

## Inputs

- The application, its models, and the slow view or endpoint if there is one.
- Table sizes, for anything involving migrations.
- Deployment environment and settings module.

## Outputs

- Views with a bounded, predictable query count.
- Migrations that do not lock a large table.
- Settings that pass `manage.py check --deploy`.

## Workflow

1. **Count the queries** — `assertNumQueries` in tests, `django-debug-toolbar` in development. An N+1 is invisible until you count.
2. **Fix them at the queryset** — `select_related` for forward foreign keys (a join), `prefetch_related` for reverse and many-to-many (a second query). Not both, not neither.
3. **Push work into the database** — `annotate`, `aggregate`, `bulk_create`, `update`. A loop that saves each object issues one query per iteration.
4. **Constrain at the database** — `UniqueConstraint`, `CheckConstraint`. Application-level validation does not survive concurrency or a shell script.
5. **Migrate safely** — On a large table, adding a column with a default rewrites it. Add nullable, backfill in batches, then set the default.
6. **Check the deploy settings** — `DEBUG = False`, `ALLOWED_HOSTS`, `SECURE_*`, `SECRET_KEY` from the environment.

## Best Practices

- `queryset.count()` inside a template loop is a query per iteration. Annotate the count once.
- `.only()` and `.defer()` are traps if the deferred field is later accessed — each access is a new query. Use them only when profiling shows they help.
- Never use `objects.all()` in a view without pagination. It will work fine until the table has a million rows.
- Signals create action at a distance and make tests fragile. Prefer explicit calls in a service function.
- `bulk_create` does not call `save()` or fire signals — which is the point, and also the footgun. Know which behavior you need.
- Run `manage.py check --deploy` in CI. It catches the settings that turn into vulnerabilities.

## Examples

**Removing an N+1 and pushing aggregation into the database:**

```python
# Before: 1 query for orders + 1 per customer + 1 per line-item count = ~2N+1.
orders = Order.objects.filter(status="open")
for order in orders:
    print(order.customer.name, order.items.count())

# After: 2 queries total, count computed by the database.
orders = (
    Order.objects
    .filter(status="open")
    .select_related("customer")                       # join
    .annotate(item_count=Count("items"))              # aggregate in SQL
)
for order in orders:
    print(order.customer.name, order.item_count)
```

**Database-level constraint rather than a hopeful `clean()`:**

```python
class Subscription(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    period_start = models.DateField()
    period_end = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["tenant", "period_start"],
                name="uniq_subscription_period",
            ),
            models.CheckConstraint(
                check=models.Q(period_end__gt=models.F("period_start")),
                name="period_end_after_start",
            ),
        ]
```

## Notes

- `select_related` on a nullable foreign key produces a LEFT JOIN and can multiply rows through a chain. Check the generated SQL with `str(qs.query)` when the query count looks right but the latency does not.
- Adding an index on a large PostgreSQL table blocks writes unless you use `AddIndexConcurrently` inside a `NonAtomic` migration.
- DRF's `ModelSerializer` will happily expose every field on the model. Always list `fields` explicitly; `__all__` is how private fields end up in a public API.
