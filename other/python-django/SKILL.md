---
name: epci:python-django
description: >-
  Patterns for Python/Django with service layer architecture. Includes DRF,
  pytest, Celery, HTMX/React integration. Use when: Django Python development, pyproject toml django detected, requirements django dependency.
  Not for: Flask applications, FastAPI projects, plain Python scripts.
user-invocable: false
---

# Python/Django Development Patterns

## Overview

Modern Django patterns emphasizing service layer architecture, optimized ORM usage, and clean separation of concerns. See `references/` for detailed examples.

## Auto-detection

Loaded when detecting:
- `requirements.txt` or `pyproject.toml` containing `django`
- Files: `manage.py`, `settings.py`, `wsgi.py`
- Structure: `apps/`, `models.py`, `views.py`

## Architecture

### Project Structure

```
backend/
├── config/
│   ├── settings/{base,dev,test,prod}.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   └── <domain>/
│       ├── models/
│       ├── services/{usecases,domain,integrations,etl}/
│       ├── api/{serializers,viewsets,routers}.py
│       ├── views/
│       ├── forms/
│       ├── tasks/
│       └── tests/
└── shared/
```

→ See `${CLAUDE_PLUGIN_ROOT}/skills/stack/python-django/references/architecture.md` for complete structure

### Service Layer Pattern

```python
# apps/production/services/usecases/cloturer_campagne.py
from django.db import transaction

@transaction.atomic
def cloturer_campagne(campagne_id: int, user) -> Result:
    """Use case: orchestrates business logic."""
    campagne = Campagne.objects.select_for_update().get(id=campagne_id)
    # Delegate to domain services, persist changes
    return Result(campagne=campagne, bilan=bilan)
```

| Layer | Purpose | I/O |
|-------|---------|-----|
| `usecases/` | Orchestration | Yes |
| `domain/` | Pure business rules | No |
| `integrations/` | External APIs | Yes |
| `etl/` | Data pipelines | Yes |

## Models & ORM

### Base Model

```python
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
```

### N+1 Prevention (Critical)

```python
# BAD - N+1 queries
for lot in Lot.objects.all():
    print(lot.campagne.nom)  # 1 query per lot!

# GOOD - select_related for FK/OneToOne
lots = Lot.objects.select_related('campagne', 'operateur')

# GOOD - prefetch_related for M2M/Reverse FK
campagnes = Campagne.objects.prefetch_related('lots')
```

→ See `${CLAUDE_PLUGIN_ROOT}/skills/stack/python-django/references/models-orm.md` for QuerySets, bulk operations, constraints

## Django REST Framework

### Read/Write Serializers

```python
class LotReadSerializer(serializers.ModelSerializer):
    campagne = CampagneSerializer(read_only=True)

class LotWriteSerializer(serializers.ModelSerializer):
    campagne_id = serializers.PrimaryKeyRelatedField(
        queryset=Campagne.objects.all(), source='campagne'
    )

class LotViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return LotWriteSerializer
        return LotReadSerializer
```

→ See `${CLAUDE_PLUGIN_ROOT}/skills/stack/python-django/references/api-drf.md` for filters, permissions, authentication

## Testing

```python
# pytest + factory_boy
@pytest.mark.django_db
class TestCloturerCampagne:
    def test_success(self, user, campagne):
        result = cloturer_campagne(campagne.id, user)
        assert result.campagne.status == 'TERMINE'
```

→ See `${CLAUDE_PLUGIN_ROOT}/skills/stack/python-django/references/testing.md` for fixtures, API tests, coverage

## Commands

```bash
# Development
python manage.py runserver
python manage.py makemigrations && python manage.py migrate

# Testing
pytest --cov=apps --cov-fail-under=70

# Quality
ruff check apps/
black apps/

# Production
python manage.py check --deploy
python manage.py collectstatic --noinput
```

## Quick Reference

| Task | Pattern |
|------|---------|
| Business logic | `services/usecases/` |
| Pure calculations | `services/domain/` |
| External API | `services/integrations/` |
| FK access | `select_related()` |
| M2M/Reverse FK | `prefetch_related()` |
| Bulk insert | `bulk_create(batch_size=1000)` |
| Read API | `*ReadSerializer` |
| Write API | `*WriteSerializer` |
| Async task | Celery task → service |
| Settings | `env('VAR')` from environment |

## Common Patterns

| Pattern | Example |
|---------|---------|
| Thin views | View calls service, returns response |
| Fat services | Business logic in services, not models |
| Atomic transactions | `@transaction.atomic` on use cases |
| Custom QuerySet | `Lot.objects.actifs().avec_relations()` |
| API versioning | `/api/v1/`, `/api/v2/` |
| Environment settings | `base.py` + `{dev,test,prod}.py` |
| Domain permissions | `apps/<app>/permissions.py` |
| Test factories | `factory_boy` + `conftest.py` |

## Anti-patterns

| Anti-pattern | Why Avoid | Alternative |
|--------------|-----------|-------------|
| Logic in views | Hard to test, violates SRP | Services |
| Logic in models | Coupling, testing issues | Domain services |
| N+1 queries | Performance disaster | `select/prefetch_related` |
| `FloatField` for money | Precision loss | `DecimalField` |
| Hardcoded secrets | Security risk | `env('SECRET')` |
| `DEBUG=True` in prod | Security risk | `check --deploy` |
| Heavy work in signals | Hard to debug | Celery tasks |
| `*` imports | Namespace pollution | Explicit imports |
| No `related_name` | Unclear reverse relations | Always specify |
| Test without `@pytest.mark.django_db` | No database | Add marker |

→ See `${CLAUDE_PLUGIN_ROOT}/skills/stack/python-django/references/production.md` for security, logging, deployment
