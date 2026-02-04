---
name: django-development
version: 2.0.0
description: |
  Comprehensive Django development guidelines for Pantas Green emissions tracking platform.
  Use when: writing Django models, views, serializers, migrations, ORM queries, templates, or any Python backend code.
  Triggers: django, model, view, serializer, migration, ORM, queryset, endpoint, API, DRF, emission, carbon, python backend, template, admin
---

# Django Development Guidelines

## Quick Reference

| Rule | Description |
|------|-------------|
| **TDD** | Scaffold stub → write failing test → implement |
| **ORM** | Use `select_related()` and `prefetch_related()` to avoid N+1 |
| **Decimals** | Use `DecimalField` for financial/emissions, never `FloatField` |
| **Business Logic** | Keep in models and services, not views |
| **Constants** | No hardcoded strings - use constants from `*/constants/*.py` |
| **DRY Templates** | Don't pass redundant context variables to templates |

---

## Before Coding

- **BP-1 (MUST)** Ask clarifying questions
- **BP-2 (SHOULD)** Draft and confirm approach for complex work
- **BP-3 (SHOULD)** List pros/cons if multiple approaches exist

---

## Code Organization & Structure

### Import Organization
```python
# Standard library imports
import os
from datetime import datetime

# Third-party imports
from django.db import models
from rest_framework import serializers

# Local imports
from .models import MyModel
from .constants import STATUS_PENDING
```

### Class Method Order
```python
class MyClass:
    # 1. __init__ and constructors
    def __init__(self): ...

    # 2. @classmethod methods
    @classmethod
    def create(cls): ...

    # 3. @staticmethod methods
    @staticmethod
    def validate(): ...

    # 4. @property methods
    @property
    def name(self): ...

    # 5. Public methods
    def process(self): ...

    # 6. Private methods
    def _internal(self): ...

    # 7. Magic methods
    def __str__(self): ...
```

### File Naming
- Files: `snake_case.py`
- Classes: `PascalCase`
- Functions: `snake_case`
- Constants: `UPPER_SNAKE_CASE`

### Directory Structure
```
green/
├── static/
│   ├── js/<model_name>/    # JavaScript files by model
│   └── css/<model_name>/   # CSS files by model
└── templates/
    └── <app_name>/
```

---

## Model Standards

### Base Requirements
- **Inherit from `CustomModel`** for common fields
- **Use `HistoricalRecords`** for audit trails
- **Use `DecimalField`** for financial/emissions calculations (never `FloatField`)

### Admin Registration Pattern
```python
@admin.register(MyModel)
class MyModelAdmin(GreenImportExportMixin, LocalDatetimeMixin, SimpleHistoryAdmin):
    change_list_template = 'admin/impexp_change_list.html'
    local_datetimes = ('created_at', 'updated_at')
    list_select_related = ('foreign_key_field',)  # Optimize queries

    class Meta:
        permissions = [
            ('import_mymodel', 'Can import MyModel'),
            ('export_mymodel', 'Can export MyModel'),
        ]
```

---

## Function Quality Standards

- **Readability**: Function purpose should be immediately clear
- **Low Complexity**: Minimal nesting, low cyclomatic complexity
- **Early Returns**: Exit early instead of deep nesting
- **Positive Checks**: Prefer `if is_valid` over `if not is_invalid`
- **No Unused Code**: Remove unused parameters, variables, and functions
- **Descriptive Names**: Consistent with existing codebase vocabulary

---

## Database Query Optimization

### N+1 Prevention (CRITICAL)
```python
# ❌ BAD - N+1 query problem
for order in Order.objects.all():
    print(order.customer.name)  # Queries DB for each order

# ✅ GOOD - Single query with JOIN
for order in Order.objects.select_related('customer'):
    print(order.customer.name)  # No additional queries

# ✅ GOOD - Prefetch for ManyToMany and reverse FK
orders = Order.objects.prefetch_related('items', 'tags')
```

### Bulk Operations
```python
# ❌ BAD - Multiple queries
for id in ids:
    obj = Model.objects.get(id=id)

# ✅ GOOD - Single query
objs = Model.objects.filter(id__in=ids)
```

### Circular Join Detection
```python
# ❌ BAD - Circular join pattern (A → B → A)
Model.objects.filter(related__back_to_model__field=value)

# ❌ BAD - Excessive relationship traversal
Model.objects.filter(a__b__c__d__e__field=value)

# ✅ GOOD - Direct path
Model.objects.filter(direct_field=value)
```

**Key indicators of problematic queries:**
- Relationship paths that go A → B → A (circular)
- More than 3-4 relationship traversals
- Complex joins when simpler alternatives exist

---

## Constants & String Literals (MANDATORY)

### Rule: No Magic Strings
String literals used **3 or more times** MUST be defined as constants.

```python
# ❌ BAD - Hardcoded strings
if material_source == 'epd':
    ...
elif material_source == 'pantas':
    ...

# ✅ GOOD - Named constants
from .constants import MATERIAL_SOURCE_EPD, MATERIAL_SOURCE_PANTAS

if material_source == MATERIAL_SOURCE_EPD:
    ...
elif material_source == MATERIAL_SOURCE_PANTAS:
    ...
```

### Constants File Pattern
```python
# app/constants.py
STATUS_PENDING = 'pending'
STATUS_COMPLETED = 'completed'
STATUS_FAILED = 'failed'

STATUS_CHOICES = [
    (STATUS_PENDING, 'Pending'),
    (STATUS_COMPLETED, 'Completed'),
    (STATUS_FAILED, 'Failed'),
]

# Usage in models
class MyModel(models.Model):
    status = models.CharField(choices=STATUS_CHOICES, default=STATUS_PENDING)
```

### Common Patterns to Avoid
| Pattern | Problem | Fix |
|---------|---------|-----|
| `== 'pending'` | Magic string | Use `STATUS_PENDING` |
| `== 'epd'` | Magic string | Use `MATERIAL_SOURCE_EPD` |
| `filter(type='scope1')` | Magic string | Use `SCOPE_1` constant |
| `choices=[('a', 'A')]` | No constants | Define choice constants |

---

## View-Template DRY (MANDATORY)

### Rule: Don't Pass Redundant Context Variables
If an object is already in context, templates can access its properties directly.

```python
# ❌ BAD - Redundant context variables
def my_view(request):
    user = request.user
    return render(request, 'template.html', {
        'user': user,
        'user_name': user.name,        # Redundant!
        'user_email': user.email,      # Redundant!
        'is_active': user.is_active,   # Redundant!
    })

# ✅ GOOD - Let template access properties
def my_view(request):
    return render(request, 'template.html', {
        'user': request.user,
    })
```

**In template:**
```django
{{ user.name }}
{{ user.email }}
{{ user.is_active }}
```

### Exceptions (NOT violations)
- **Computed values**: `"total": calculate_total(items)` ✅
- **Method calls with arguments**: `"filtered": obj.get_items(status='active')` ✅
- **Renamed for clarity**: `"current_user": request.user` when template expects specific name ✅

---

## Template Technology Consistency (MANDATORY)

### Rule: Use Django Filters, Not JavaScript
Don't duplicate Django template filter functionality in JavaScript.

| JS Pattern | Django Alternative |
|------------|-------------------|
| `new Date().toLocaleString()` | `{{ value\|date:"format" }}` |
| `toLocaleDateString()` | `{{ value\|date:"format" }}` |
| `.toLowerCase()` | `{{ value\|lower }}` |
| `.toUpperCase()` | `{{ value\|upper }}` |
| String truncation | `{{ value\|truncatechars:N }}` |
| Number formatting | `{{ value\|floatformat }}` |

### When to Use Django Filters
- Codebase already uses Django filters for same purpose
- Django handles it without JavaScript
- Reduces client-side complexity

---

## Frontend Standards

- **No Inline Styles**: Use Bootstrap classes
- **No Inline JavaScript**: Place in `green/static/js/<model_name>/`
- **Consistent Bootstrap**: Use Bootstrap framework for styling
- **Template Inheritance**: Proper Django template blocks
- **Responsive Design**: Works on mobile and desktop

---

## Exception Handling & Logging

### Exception Logging
```python
# ✅ CORRECT - exc_info=True ONLY in exception handler
try:
    result = process_data()
except Exception as e:
    logger.error(f"Processing failed: {e}", exc_info=True)

# ✅ CORRECT - No exc_info outside exception block
logger.info(f"Processing started for company {company_id}")
logger.warning(f"Missing optional field: {field_name}")

# ❌ WRONG - exc_info=True outside exception (no stack trace to capture)
logger.info(f"Processing started", exc_info=True)
```

### Log Levels
| Level | Use For |
|-------|---------|
| `ERROR` | Exceptions, failures |
| `WARNING` | Recoverable issues |
| `INFO` | Significant events |
| `DEBUG` | Diagnostic details |

### Context in Logs
Include relevant IDs: `user_id`, `file_id`, `company_id`

**Never log:** passwords, tokens, sensitive PII

---

## Testing Standards

### Organization
- Tests in `tests/` directory within each app
- Unit tests: `SimpleTestCase` (no DB)
- Integration tests: `TestCase` (with DB)

### Database Mocking
```python
# ✅ Unit tests use Mock, no real DB
from unittest.mock import Mock, patch

class MyTestCase(SimpleTestCase):
    @patch('myapp.services.Model.objects.get')
    def test_something(self, mock_get):
        mock_get.return_value = Mock(name='Test')
        ...
```

### Test Data
```python
# ❌ BAD - Meaningless test data
user = User(name='foo', age=42)

# ✅ GOOD - Realistic test data
user = User(name='John Smith', age=35)
```

### Assertions
```python
# ❌ WEAK - Ambiguous assertion
self.assertGreaterEqual(count, 0)

# ✅ STRONG - Specific assertion
self.assertEqual(count, 5)
```

---

## Domain-Specific: Emissions

- **Precision**: Maintain accuracy in carbon calculations
- **Unit Consistency**: Consistent units throughout
- **Financial Fields**: Always use `DecimalField`
- **Audit Trails**: Track all calculation changes
- **Validation**: Validate emission factors and data sources

---

## Performance & Security

### Performance
- Test query count for performance-critical code
- Consider memory usage in data processing
- Use Dramatiq for long-running operations

### Security
- Never log sensitive information
- Validate file types and sizes for uploads
- Use Django ORM (avoid raw SQL)

---

## Quality Gates

| Gate | Command/Requirement |
|------|---------------------|
| **G-1** | `ruff check` passes |
| **G-2** | `mypy` passes |
| **G-3** | `python manage.py test` passes |

---

## Code Review Checklist

Before submitting code for review, verify:

### Code Quality
- [ ] Import organization correct (stdlib → third-party → local)
- [ ] Class method order follows convention
- [ ] No unused imports, variables, or functions
- [ ] Early return pattern used (no deep nesting)

### Database
- [ ] N+1 queries prevented with `select_related`/`prefetch_related`
- [ ] No circular join patterns
- [ ] Bulk operations used where appropriate

### Constants (MANDATORY)
- [ ] No hardcoded strings used 3+ times
- [ ] Existing constants reused from `*/constants/*.py`
- [ ] New constants created for repeated domain-specific strings

### View-Template DRY (MANDATORY)
- [ ] No redundant context variables in `render()` calls
- [ ] Templates access object properties directly

### Template Technology (MANDATORY)
- [ ] No JavaScript duplicating Django filter functionality
- [ ] Consistent with existing codebase patterns

### Testing
- [ ] Unit tests use Mock (no DB access)
- [ ] Realistic test data (not "foo" or 42)
- [ ] Strong assertions (assertEqual vs assertGreaterEqual)

### Logging
- [ ] `exc_info=True` only in exception handlers
- [ ] No sensitive data in logs
- [ ] Includes relevant context IDs

---

## Summary of Coding Rules

| Rule | Level | Description |
|------|-------|-------------|
| BP-1 | MUST | Ask clarifying questions |
| BP-2 | SHOULD | Confirm approach for complex work |
| BP-3 | SHOULD | List pros/cons for multiple approaches |
| C-1 | MUST | Follow TDD workflow |
| C-2 | MUST | Use existing domain vocabulary |
| C-3 | SHOULD | Use Django class-based views |
| C-4 | SHOULD | Prefer simple, composable functions |
| C-6 | MUST | Follow import conventions and PEP 8 |
| C-10 | MUST | Use constants for repeated strings |
| C-11 | MUST | No local imports inside functions |
| D-1 | MUST | Avoid N+1 queries |
| D-2 | SHOULD | Use transactions for atomic operations |
| D-3 | MUST | Create migrations for model changes |
| D-4 | SHOULD | Use Decimal for financial/emissions |
| T-1 | MUST | Tests in `tests/` directory |
| T-3 | MUST | Separate unit from integration tests |
| T-7 | MUST | Realistic test data |
| L-1 | MUST | `exc_info=True` in exception handlers |
| L-4 | MUST | No sensitive data in logs |
| G-1 | MUST | `ruff check` passes |
| G-2 | MUST | `mypy` passes |
| G-3 | MUST | Django tests pass |

---

*Version: 2.0.0 - Enhanced with lessons from django-reviewer agent*
