---
name: model-entity-validator
description: This skill should be used when the user asks to "create a model", "add a Django model", "create database table", "add entity", "define schema", or when writing class definitions inheriting from models.Model. Validates BaseModel inheritance pattern.
---

# Model/Entity Validator

Enforces the BaseModel inheritance pattern (UUID primary keys, audit timestamps, soft deletes) for all Django models.

## Activation Triggers

This skill activates when:
- Creating new model files
- Modifying existing models
- Mentioning "model", "database", "schema", "table"
- Writing class inheriting from `models.Model`
- Running migrations
- Discussing data structure

## Core Principle: BaseModel Inheritance

**NEVER repeat UUID/timestamp fields.** All models inherit from BaseModel.

```python
# ❌ WRONG - Repeating fields
class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    email = models.EmailField()

# ✅ CORRECT - Inherit from BaseModel
import core.models as _core_models

class User(_core_models.BaseModel):
    email = models.EmailField(unique=True)
```

## Validation Process

### Step 1: Check if BaseModel Exists

Before any action, check if the project has a BaseModel:

```python
# Search for BaseModel in (in order):
# 1. core/models.py
# 2. shared/models.py
# 3. common/models.py
# 4. {app}/base.py
```

**If BaseModel found:** Suggest inheritance (Step 2a)
**If BaseModel NOT found:** Create BaseModel first (Step 2b)

### Step 2a: BaseModel Exists - Suggest Inheritance

When seeing:
```python
class Product(models.Model):
    name = models.CharField(max_length=255)
```

Fix to:
```python
import core.models as _core_models

class Product(_core_models.BaseModel):
    """Product model - inherits id, timestamps, soft delete from BaseModel."""

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'products'
```

### Step 2b: BaseModel NOT Found - Create It First

If no BaseModel exists, create it:

```python
# core/models.py
import uuid
from django.db import models

class BaseModel(models.Model):
    """
    Abstract base model providing:
    - UUID primary key
    - Automatic timestamps (created_at, updated_at)
    - Soft delete support (is_deleted)

    All models MUST inherit from this class.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def soft_delete(self) -> None:
        """Soft delete the record."""
        self.is_deleted = True
        self.save(update_fields=['is_deleted', 'updated_at'])

    def restore(self) -> None:
        """Restore a soft-deleted record."""
        self.is_deleted = False
        self.save(update_fields=['is_deleted', 'updated_at'])


class ActiveManager(models.Manager):
    """Manager that excludes soft-deleted records."""

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)
```

Report to developer:
> **BaseModel Created**
>
> Created `core/models.py` with BaseModel. All models should now inherit from it:
> ```python
> import core.models as _core_models
>
> class YourModel(_core_models.BaseModel):
>     # Your fields here - DO NOT add id, created_at, updated_at, is_deleted
> ```

### Step 3: Detect Duplicate Fields

If seeing a model with explicit id/timestamp fields that inherits from BaseModel:

```python
# ❌ WRONG - Duplicate fields
class User(_core_models.BaseModel):
    id = models.UUIDField(...)  # Already in BaseModel!
    created_at = models.DateTimeField(...)  # Already in BaseModel!
    email = models.EmailField()
```

Remove them:
```python
# ✅ CORRECT - Only custom fields
class User(_core_models.BaseModel):
    email = models.EmailField(unique=True)
```

### Step 4: Validate Indexes

Check if appropriate indexes exist:

```python
class Product(_core_models.BaseModel):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'products'
        indexes = [
            models.Index(fields=['sku']),  # Suggest for unique lookups
            models.Index(fields=['name']),  # Suggest for search
        ]
```

## Complete Model Examples

### Standard Model

```python
# products/models.py
from django.db import models
import core.models as _core_models

class Product(_core_models.BaseModel):
    """Product model."""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=100, unique=True, db_index=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'products'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['is_active', 'is_deleted']),
        ]

    def __str__(self):
        return self.name
```

### User Model (with AbstractUser)

```python
# users/models.py
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Custom User model with UUID and timestamps.

    Note: For User, override AbstractUser directly since it has its own
    ID handling. Add the standard fields manually.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users'
```

### Through Model (Many-to-Many)

```python
# users/models.py
import core.models as _core_models

class UserOrganization(_core_models.BaseModel):
    """Through model for user-organization relationship."""

    user = models.ForeignKey('User', on_delete=models.CASCADE)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)
    role = models.CharField(max_length=50)

    class Meta:
        db_table = 'user_organizations'
        unique_together = [['user', 'organization']]
```

## Custom Managers

BaseModel provides soft delete. Add a custom manager for convenience:

```python
import core.models as _core_models

class Product(_core_models.BaseModel):
    name = models.CharField(max_length=255)

    objects = models.Manager()  # All records
    active = _core_models.ActiveManager()  # Excludes soft-deleted

# Usage
Product.active.all()  # Only non-deleted
Product.objects.all()  # All including deleted
```

## Validation Checklist

When reviewing a model, check:

1. ✅ Inherits from `BaseModel` (or has explicit required fields for special cases)
2. ✅ Does NOT duplicate fields from BaseModel
3. ✅ Uses absolute import: `import core.models as _core_models`
4. ✅ Has appropriate `db_table` name (singular or plural, snake_case)
5. ✅ Has indexes on frequently queried fields
6. ✅ Foreign keys have `on_delete` specified
7. ✅ Has docstring explaining the model
8. ✅ Has `__str__` method for admin display

## Behavior

**Proactive enforcement:**
- Check if BaseModel exists FIRST
- Suggest inheritance instead of field duplication
- Remove duplicate fields automatically
- Create BaseModel if missing
- Explain WHY inheritance is better

**Never:**
- Add duplicate id/timestamp fields to models
- Let developers repeat base fields
- Ignore existing BaseModel in the project
