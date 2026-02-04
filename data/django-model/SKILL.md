---
name: django-model
description: >
  Creating Django models following Counterpart's patterns. Use when building new models, working
  with audit fields, implementing relationships, or using PydanticJSONEncoder. Triggers: 'create model',
  'new database table', 'audit fields', 'BaseModel inheritance', 'add foreign key', 'JSON field validation'
---

# django-model - Creating Models with Counterpart Patterns

## Overview

Django models at Counterpart follow specific patterns: all inherit from `BaseModel` with UUID primary keys
and audit timestamps, use type hints consistently, and leverage Pydantic for JSON field validation. This
skill shows exactly how to build models that follow the architecture patterns documented in CLAUDE.md,
including proper relationships, JSON fields, and testing considerations.

## When to Use This Skill

- Creating a new Django model for a database entity (applications, quotes, policies, etc.)
- Adding relationships between models (foreign keys, one-to-many, many-to-many)
- Implementing JSON fields with Pydantic validation (nested data structures)
- Working with models that need audit trail tracking (who changed what, when)
- Ensuring type safety and consistency in model definitions

**Don't use this skill for:**
- Modifying existing models where patterns already exist (just follow the established pattern)
- Simple model tweaks that don't involve new relationships
- Models in third-party packages or external integrations

## Prerequisites

Django project with Counterpart setup. Core models live in `common/models.py` and extend `BaseModel`.

**Required imports:**
```python
from django.db import models
from pydantic import BaseModel as PydanticBaseModel, Field
from common.models import BaseModel  # UUID PK + audit fields already included
from typing import Optional, List
```

**Existing patterns in codebase:**
- Look at `application/models.py`, `quote/models.py` for existing examples
- Review `common/models.py` for BaseModel definition with audit fields

## Decision Tree

**Choose your approach based on model complexity:**

1. **Simple Entity** → Basic model with standard fields
   - When: Core business object with no special requirements
   - Best for: Applications, quotes, carriers, standard lookup data
   - Example: Single table, maybe one or two foreign keys

2. **Complex Entity** → Model with JSON fields for nested data
   - When: Storing flexible, semi-structured data (config, settings, attributes)
   - Best for: Policy terms, coverage details, rating factors
   - Example: Uses Pydantic models as JSON field validators

3. **Relationship Hub** → Model connecting multiple entities
   - When: Junction/bridge model or central coordinator
   - Best for: Policy events, activity logs, carrier programs
   - Example: Multiple foreign keys with specific ordering/constraints

## Workflow

### Step 1: Define Pydantic Models for JSON Fields (if needed)

If your model has JSON fields with structured data, define Pydantic models first for validation.
This ensures type-safe serialization and validation.

```python
from pydantic import BaseModel as PydanticBaseModel, Field
from typing import Optional, List

class CoverageDetailSchema(PydanticBaseModel):
    """Pydantic model for coverage details stored as JSON."""
    coverage_type: str = Field(..., description="Type of coverage")
    limit: float = Field(..., gt=0, description="Coverage limit in dollars")
    deductible: float = Field(default=0, ge=0, description="Deductible amount")
    effective_date: str = Field(..., description="Start date in YYYY-MM-DD format")
    notes: Optional[str] = Field(default=None, max_length=500)

    class Config:
        json_schema_extra = {
            "example": {
                "coverage_type": "liability",
                "limit": 1000000,
                "deductible": 2500,
                "effective_date": "2024-01-01",
                "notes": "Standard commercial liability"
            }
        }
```

**Key parameters:**
- Use `Field()` for all fields with descriptions and constraints
- Add `json_schema_extra` with example data for API documentation
- Set `gt` (greater than), `ge` (greater than/equal), `max_length`, etc. for validation

### Step 2: Create the Model Class

Use BaseModel as parent (gets UUID PK + audit fields automatically). Add type hints to all fields.

```python
from django.db import models
from common.models import BaseModel
from django.contrib.postgres.fields import JSONField
from pydantic import PydanticEncoder

class PolicyCoverage(BaseModel):
    """Insurance policy coverage details with audit trail."""

    # Related entities - always use ForeignKey with on_delete specified
    policy = models.ForeignKey(
        'policy.Policy',
        on_delete=models.CASCADE,  # Delete coverage when policy deleted
        related_name='coverages',  # Access via policy.coverages.all()
        help_text="Parent policy for this coverage"
    )

    # Standard fields with type hints
    coverage_name: str = models.CharField(
        max_length=100,
        help_text="Human-readable coverage name"
    )

    is_active: bool = models.BooleanField(
        default=True,
        help_text="Whether this coverage is currently active"
    )

    premium_amount: float = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Premium amount in dollars"
    )

    # JSON field with Pydantic validation
    coverage_details = models.JSONField(
        default=dict,
        encoder=PydanticEncoder,
        help_text="Coverage details as validated JSON"
    )

    class Meta:
        app_label = 'policy'
        ordering = ['-created_at']  # Newest first
        indexes = [
            models.Index(fields=['policy', 'is_active']),
        ]

    def __str__(self) -> str:
        return f"{self.coverage_name} - {self.policy.policy_number}"
```

**Field guidelines:**
- Always use `help_text` for documentation
- Use `related_name` on ForeignKey for reverse queries
- Specify `on_delete=models.CASCADE` (or SET_NULL if optional) explicitly
- Use `DecimalField` for money, not `FloatField` (precision matters)
- Use `JSONField` with `encoder=PydanticEncoder` for structured data

### Step 3: Create and Run Migration

Django creates migrations automatically, but verify it looks correct.

```bash
# Generate migration
python manage.py makemigrations policy

# Review the migration file before applying
cat policy/migrations/000X_auto_YYYYMMDD_HHMM.py

# Apply migration
python manage.py migrate policy
```

**What to verify in migration:**
- Foreign key relationships have correct app labels
- Field types match your model definitions
- No accidental field removals

## Common Gotchas

### Gotcha 1: Forgetting `app_label` in Meta Class

**Symptom:** `RuntimeError: Model 'MyModel' has not been installed` or migrations fail to apply

**Cause:** Django can't find your model when `app_label` isn't specified in Meta, especially if the model file structure is unusual

**Solution:**
```python
class Meta:
    app_label = 'policy'  # Explicitly set to the app containing the model
    ordering = ['-created_at']
```

**Prevention:** Always include `app_label` in Meta. Even though it's often inferred, being explicit prevents migration headaches.

### Gotcha 2: Using `FloatField` for Money

**Symptom:** Rounding errors, precision loss ($1.23 becomes $1.2300000001234), test failures with specific amounts

**Cause:** FloatField uses IEEE floating-point which can't represent all decimal values exactly

**Solution:**
```python
# WRONG
price = models.FloatField()

# CORRECT
price = models.DecimalField(max_digits=12, decimal_places=2)  # Up to $9,999,999.99
```

**Prevention:** Use DecimalField for any financial data. The extra digits (max_digits=12) give buffer for calculations.

### Gotcha 3: Missing `on_delete` on ForeignKey

**Symptom:** `TypeError: __init__() missing 1 required positional argument: 'on_delete'` during migration

**Cause:** Django 2.0+ requires explicit behavior when referenced object is deleted

**Solution:**
```python
# WRONG - will raise error
policy = models.ForeignKey('policy.Policy')

# CORRECT - choose appropriate behavior
policy = models.ForeignKey(
    'policy.Policy',
    on_delete=models.CASCADE,  # Delete this when policy deleted
    # OR on_delete=models.SET_NULL (requires null=True)
    # OR on_delete=models.PROTECT (raise error if try to delete)
)
```

**Prevention:** Always specify `on_delete`. Use CASCADE for child entities, PROTECT for shared resources, SET_NULL for optional refs.

### Gotcha 4: Default Mutable Objects in JSONField

**Symptom:** Updating one object's JSON also updates another object's JSON field inexplicably

**Cause:** Using mutable default (list, dict) shares the same object across all model instances

**Solution:**
```python
# WRONG - all instances share same dict
details = models.JSONField(default={})

# CORRECT - callable creates new dict for each instance
details = models.JSONField(default=dict)

# CORRECT - for lists
tags = models.JSONField(default=list)
```

**Prevention:** Use callable defaults (dict, list) not literal values ({}, []).

## Examples

### Example 1: Simple Quote Entity

**Scenario:** Creating a Quote model that belongs to an Application. Needs core info and status tracking.

**Implementation:**
```python
from django.db import models
from common.models import BaseModel

class Quote(BaseModel):
    """Insurance quote for an application."""

    application = models.ForeignKey(
        'application.Application',
        on_delete=models.CASCADE,
        related_name='quotes',
        help_text="Parent application"
    )

    quote_number: str = models.CharField(
        max_length=50,
        unique=True,
        help_text="Unique quote identifier"
    )

    base_premium: models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Base premium before adjustments"
    )

    status: str = models.CharField(
        max_length=20,
        choices=[
            ('draft', 'Draft'),
            ('pending', 'Pending Review'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='draft',
        help_text="Quote status"
    )

    expires_at = models.DateTimeField(
        help_text="When quote is no longer valid"
    )

    class Meta:
        app_label = 'quote'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['quote_number']),
            models.Index(fields=['application', 'status']),
        ]

    def __str__(self) -> str:
        return f"Quote {self.quote_number}"
```

**Result:** Model with audit trail (created_at, updated_at, id via BaseModel), status tracking, and optimized queries via indexes.

### Example 2: Policy with JSON Nested Data

**Scenario:** Storing policy with flexible coverage details that vary by program. Needs Pydantic validation.

**Implementation:**
```python
from typing import List, Optional
from pydantic import BaseModel as PydanticBaseModel, Field, validator
from django.db import models
from common.models import BaseModel
from pydantic import PydanticEncoder

# Pydantic schema for coverage data
class CoverageSchema(PydanticBaseModel):
    """Coverage details stored as JSON."""
    type: str = Field(..., description="coverage type", min_length=1)
    limit: float = Field(..., gt=0, description="coverage limit")
    deductible: float = Field(default=0, ge=0, description="deductible amount")

    @validator('limit')
    def limit_must_exceed_deductible(cls, v, values):
        if 'deductible' in values and v <= values['deductible']:
            raise ValueError('limit must exceed deductible')
        return v

class PolicySchema(PydanticBaseModel):
    """Complete policy data with coverages."""
    coverage_list: List[CoverageSchema]
    effective_date: str
    renewal_date: str

# Django model using the Pydantic schema
class Policy(BaseModel):
    """Insurance policy with validated coverage details."""

    carrier_program = models.ForeignKey(
        'carrier_program.CarrierProgram',
        on_delete=models.PROTECT,  # Don't allow deletion if policies exist
        related_name='policies',
        help_text="Carrier program this policy belongs to"
    )

    policy_number: str = models.CharField(
        max_length=100,
        unique=True,
        help_text="Policy number from carrier"
    )

    # Validated JSON field
    policy_data = models.JSONField(
        encoder=PydanticEncoder,
        help_text="Complete policy data with coverages"
    )

    class Meta:
        app_label = 'policy'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['policy_number']),
            models.Index(fields=['carrier_program', 'created_at']),
        ]

    def __str__(self) -> str:
        return self.policy_number
```

**Verification:**
```bash
# Create policy with validation
python manage.py shell
>>> from policy.models import Policy, PolicySchema
>>> policy_schema = PolicySchema(
...     coverage_list=[
...         {'type': 'liability', 'limit': 1000000, 'deductible': 5000}
...     ],
...     effective_date='2024-01-01',
...     renewal_date='2025-01-01'
... )
>>> Policy.objects.create(
...     carrier_program_id=1,
...     policy_number='POL-2024-001',
...     policy_data=policy_schema.dict()
... )
```

### Example 3: Activity Log with Multiple Relations

**Scenario:** Tracking policy activity with references to multiple entities. Needs flexible logging.

**Implementation:**
```python
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from common.models import BaseModel

class ActivityLog(BaseModel):
    """Audit log for policy and application changes."""

    # Which user made the change
    user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='activity_logs',
        help_text="User who performed the action"
    )

    # Generic relation - can log activity for any model
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        help_text="Content type of the object being logged"
    )
    object_id: str = models.UUIDField(
        help_text="ID of the object being logged"
    )
    content_object = GenericForeignKey('content_type', 'object_id')

    action: str = models.CharField(
        max_length=50,
        choices=[
            ('created', 'Created'),
            ('updated', 'Updated'),
            ('deleted', 'Deleted'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        help_text="What action was performed"
    )

    changes = models.JSONField(
        default=dict,
        help_text="Dictionary of what changed: {field_name: [old_value, new_value]}"
    )

    description: str = models.TextField(
        help_text="Human-readable description"
    )

    class Meta:
        app_label = 'policy_events'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['action', 'created_at']),
            models.Index(fields=['user', 'created_at']),
        ]

    def __str__(self) -> str:
        return f"{self.action} on {self.content_object} by {self.user}"
```

**Why this works:** Audit logs need flexibility - they log changes to different models. GenericForeignKey allows one model to reference any other model's instances.

## Anti-Patterns

### ❌ BAD: Tight Coupling to Specific Models

```python
# This model is tightly coupled - hard to reuse, test, or extend
class RatingFactor(BaseModel):
    application = models.ForeignKey('application.Application', on_delete=models.CASCADE)
    quote = models.ForeignKey('quote.Quote', on_delete=models.CASCADE)
    policy = models.ForeignKey('policy.Policy', on_delete=models.CASCADE)

    def get_related_entity(self):
        if self.application_id:
            return self.application
        # ... many conditionals
```

**Why it fails:**
- Each new entity type requires schema migration
- Model becomes a dumping ground for relationships
- Testing requires setting up multiple related objects
- Queries are inefficient with many nullable ForeignKeys

### ✅ GOOD: Use Generic Relations for Flexibility

```python
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class RatingFactor(BaseModel):
    """Rating factor - can apply to any entity type."""

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        help_text="Type of entity this rating applies to"
    )
    object_id: str = models.UUIDField()
    content_object = GenericForeignKey('content_type', 'object_id')

    factor_code: str = models.CharField(max_length=50)
    value = models.DecimalField(max_digits=5, decimal_places=2)
```

**Why it works:**
- Single model works with any entity type
- No schema changes when adding new entity types
- Cleaner queries: `RatingFactor.objects.filter(content_type=app_ct, object_id=id)`
- Easier to test with mock objects

---

### ❌ BAD: Storing Complex Business Logic in Model Fields

```python
class Policy(BaseModel):
    # Mixing data storage with business logic
    policy_number: str = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        # Complex side effects on every save
        self.policy_number = self.generate_policy_number_with_validation()
        self.update_rating()
        self.sync_with_salesforce()
        super().save(*args, **kwargs)
```

**Why it fails:**
- Model.save() becomes a dumping ground for side effects
- Impossible to update fields without triggering full flow
- Celery tasks can't reuse logic (they call save())
- Tests require mocking everything

### ✅ GOOD: Keep Models Simple, Use Service Layer

```python
# model.py - just data storage
class Policy(BaseModel):
    policy_number: str = models.CharField(max_length=100)
    status: str = models.CharField(max_length=20)

# services.py - business logic
class PolicyService:
    @staticmethod
    def create_policy(carrier_program, application_data) -> Policy:
        policy_number = PolicyService.generate_policy_number(carrier_program)
        policy = Policy.objects.create(
            policy_number=policy_number,
            status='draft'
        )
        return policy

    @staticmethod
    def approve_policy(policy: Policy) -> None:
        policy.status = 'approved'
        policy.save(update_fields=['status'])  # Only update status
        # Trigger async tasks if needed
        sync_with_salesforce_task.delay(policy.id)
```

**Why it works:**
- Models stay simple and testable
- Business logic reusable from tasks, APIs, tests
- Explicit dependencies - easier to mock
- Clear separation of concerns

---

### ❌ BAD: Not Indexing Query Paths

```python
class Policy(BaseModel):
    policy_number: str = models.CharField(max_length=100)
    status: str = models.CharField(max_length=20)
    carrier_program = models.ForeignKey('carrier_program.CarrierProgram', on_delete=models.CASCADE)

    class Meta:
        app_label = 'policy'
        # No indexes - queries will be slow as data grows
```

### ✅ GOOD: Index Based on Query Patterns

```python
class Policy(BaseModel):
    policy_number: str = models.CharField(max_length=100)
    status: str = models.CharField(max_length=20)
    carrier_program = models.ForeignKey('carrier_program.CarrierProgram', on_delete=models.CASCADE)

    class Meta:
        app_label = 'policy'
        indexes = [
            models.Index(fields=['policy_number']),  # Frequent exact lookups
            models.Index(fields=['carrier_program', 'status']),  # Filter by program+status
            models.Index(fields=['status', 'created_at']),  # Status + recency queries
        ]
        # If querying by combinations: add compound indexes
```

**Why it works:**
- Queries with indexed fields return in milliseconds
- Without indexes, table scans slow as data grows
- Think about actual query patterns in code, then index them

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `django.core.exceptions.FieldError: Local field 'field_name' in class 'ModelName' clashes with field of the same name from base class` | Field defined in both BaseModel and your model | Remove field - BaseModel already has id, created_at, updated_at |
| `psycopg2.errors.UndefinedColumn: column "tablename"."fieldname" does not exist` | Field added to model but migration not applied | Run `python manage.py migrate appname` |
| `TypeError: <class 'MyModel'> is not JSON serializable` | Model instance in JSONField without encoder | Add `encoder=PydanticEncoder` to JSONField |
| `ValueError: null=True and blank=True` | Setting null=True without considering semantics | null=True for DB-level NULL; blank=True for forms; use both only when optional |

**Debug mode for migrations:**
```bash
# See SQL being executed
python manage.py migrate appname --verbosity=3

# Dry run - see what would happen
python manage.py migrate appname --plan
```

## Performance Considerations

**Scale factors:**
- Compound indexes are critical - single-column indexes don't help composite queries
- JSONField queries without proper indexing scan entire column
- ForeignKey relationships without `select_related()` cause N+1 queries
- Generic relations can't be indexed as efficiently - only use when necessary

**Optimization tips:**
- **Add compound indexes for common query patterns:** `models.Index(fields=['program_id', 'status'])` for queries filtering both fields
- **Use `select_related()` in queries:** `Policy.objects.select_related('carrier_program')` reduces queries from N+1 to 1
- **Use `only()` for large models:** `Policy.objects.only('id', 'policy_number')` avoids loading unnecessary columns
- **Batch operations with `bulk_create()`:** For >100 creates, use `Model.objects.bulk_create(instances)` instead of loop

**Benchmarks (typical PostgreSQL on modern hardware):**
```bash
# Single row by indexed field: ~1-2ms
SELECT * FROM policy WHERE policy_number = 'POL-2024-001';

# Filter by two indexed fields: ~2-3ms
SELECT * FROM policy WHERE carrier_program_id = 1 AND status = 'approved';

# Unindexed scan of 100k rows: ~50-100ms (slow!)
SELECT * FROM policy WHERE notes LIKE '%term%';  # No index, full table scan
```

## Advanced Usage

### Advanced Technique 1: Using Q Objects for Complex Queries

When you need complex filtering logic in the model or service layer:

```python
from django.db.models import Q
from common.models import BaseModel

class Quote(BaseModel):
    """Quote model for querying multiple conditions."""

# Query using Q objects for OR/AND logic
quotes = Quote.objects.filter(
    Q(status='approved') | Q(expires_at__gte=now)  # Approved OR not expired
)

# Complex: approved quotes from specific programs
from datetime import datetime
quotes = Quote.objects.filter(
    (Q(status='approved') | Q(status='pending')) &
    Q(application__carrier_program__in=[1, 2, 3]) &
    Q(created_at__gte=datetime(2024, 1, 1))
)
```

**When to use:** Complex filtering that's hard to express with simple `.filter()` calls. Easier to test logic when extracted into service methods.

### Advanced Technique 2: Custom Managers for Common Queries

Define custom managers to encapsulate frequent query patterns:

```python
from django.db import models
from common.models import BaseModel

class ApprovedPoliciesManager(models.Manager):
    """Manager for approved policies - encapsulates common filtering."""

    def get_queryset(self):
        return super().get_queryset().filter(status='approved')

    def by_carrier(self, carrier_id):
        return self.filter(carrier_program_id=carrier_id)

class Policy(BaseModel):
    """Policy model with custom manager."""

    status: str = models.CharField(max_length=20)
    carrier_program = models.ForeignKey('carrier_program.CarrierProgram', on_delete=models.PROTECT)

    # Add custom manager
    approved = ApprovedPoliciesManager()

# Usage - much cleaner
approved_policies = Policy.approved.by_carrier(1)  # Already filtered to approved
```

**When to use:** Queries used in multiple places or complex filtering logic. Makes code more readable and DRY.

## Integration with Other Tools

**Works well with:**
- `pytest` fixtures: Use model factories in test conftest.py for creating test instances
- Django REST framework serializers: Serialize model instances to JSON for APIs
- Celery tasks: Reference model IDs in tasks, instantiate in task handlers
- Django admin: Automatically register models for admin interface management

**Testing notes:**
- Use pytest-django for model testing
- Mock external API calls in service layer tests
- Use factory_boy for generating test instances with realistic data

## Related Skills

- `django-service-layer` - Use for business logic around model creation/updates
- `django-migrations` - Use when modifying existing models or dealing with complex migrations
- `django-api-design` - Use when exposing models through REST endpoints

## Maintenance Notes

**Last updated:** October 2024

**Known issues:**
- UUID primary keys require PostgreSQL or explicit UUID support in other databases
- SimpleHistory package may conflict with custom save() methods

**Tested with:**
- Django 4.2+
- Python 3.9+
- PostgreSQL 13+
- Pydantic 2.x
