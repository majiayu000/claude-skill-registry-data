---
name: django-import-enforcer
description: Automatically validate and fix Django import patterns to use absolute modular imports with aliases. Use when writing imports, creating new Python files, modifying existing files, or seeing import statements in code.
---

# Import Convention Enforcer

Enforces absolute modular import conventions for Django projects.

## Activation Triggers

This skill activates when:
- Writing or modifying Python files
- Creating models, services, views, or serializers
- Mentioning "import", "add", "create", or "refactor"
- Reviewing or fixing code

## Django Import Pattern (MANDATORY)

### ✅ CORRECT Pattern
```python
# Absolute modular imports with app-prefixed aliases
import users.models as _users_models
import users.services as _users_services
import users.serializers as _users_serializers
import core.utils as _core_utils

# Usage - clear which app each import is from
user = _users_models.User.objects.get(id=user_id)
result = _users_services.UserService.create_user(data)
serializer = _users_serializers.UserSerializer(user)
token = _core_utils.generate_token()
```

### Pattern Rule
```
import {app}.{module} as _{app}_{module}
```

### ❌ WRONG Patterns
```python
# Relative imports - NEVER USE
from .models import User
from ..services import UserService

# Direct class imports - NEVER USE
from users.models import User
from users.services import UserService

# Relative module imports - NEVER USE
import .models as models
from . import models
```

## Validation Process

### Step 1: Detect Import Violations

Scan Python code for:

**Violation Type 1: Relative imports**
```python
from .models import User          # ❌
from ..services import UserService  # ❌
```

**Violation Type 2: Direct class imports**
```python
from users.models import User     # ❌
```

**Violation Type 3: Missing alias**
```python
import users.models               # ❌ (no alias)
```

### Step 2: Auto-Fix Violations

**Before (Violation):**
```python
from .models import User, Profile
from users.services import UserService
```

**After (Corrected):**
```python
import users.models as _users_models
import users.services as _users_services

# Update usage
user = _users_models.User.objects.get(...)
profile = _users_models.Profile.objects.get(...)
result = _users_services.UserService.create_user(...)
```

### Step 3: Explain the Fix

Report to developer:
> **Import Pattern Violation Fixed**
>
> Changed relative/direct imports to absolute modular imports with app-prefixed aliases:
> - `from .models import User` → `import users.models as _users_models`
> - Usage: `user = _users_models.User.objects.get(...)`
>
> **Why**: Absolute imports with aliases:
> - ✅ Clear module boundaries
> - ✅ Easier to refactor
> - ✅ No circular dependency issues
> - ✅ Consistent across entire codebase

### Step 4: Verify All Imports

Check the entire file to ensure ALL imports follow the pattern:

```python
import uuid
import users.models as _users_models          # ✅
import users.services as _users_services      # ✅
import features.auth.models as _auth_models   # ✅
from rest_framework import serializers        # ✅ Third-party is fine
from django.db import models                  # ✅ Django imports are fine
```

## Common Scenarios

### Creating New Model File

**User writes:**
```python
# users/models.py
from django.db import models
from .base import BaseModel  # ❌ WRONG
```

**Auto-fix to:**
```python
# users/models.py
from django.db import models
import users.models.base as _users_base  # ✅ CORRECT

class User(_users_base.BaseModel):
    pass
```

### Creating New Service

**User writes:**
```python
# users/services.py
from .models import User  # ❌ WRONG
from .serializers import UserSerializer  # ❌ WRONG
```

**Auto-fix to:**
```python
# users/services.py
import users.models as _users_models  # ✅ CORRECT
import users.serializers as _users_serializers  # ✅ CORRECT

class UserService:
    def create_user(self, data):
        user = _users_models.User.objects.create(**data)
        serializer = _users_serializers.UserSerializer(user)
        return serializer.data
```

### Cross-App Imports

**User writes:**
```python
# orders/services.py
from users.models import User  # ❌ WRONG
from products.models import Product  # ❌ WRONG
```

**Auto-fix to:**
```python
# orders/services.py
import users.models as _user_models  # ✅ CORRECT
import products.models as _product_models  # ✅ CORRECT

class OrderService:
    def create_order(self, user_id, product_id):
        user = _user_models.User.objects.get(id=user_id)
        product = _product_models.Product.objects.get(id=product_id)
```

## Barrel Exports (Optional)

For cleaner imports, suggest barrel exports in `__init__.py`:

```python
# users/models/__init__.py
from users.models.user import User
from users.models.profile import Profile

__all__ = ['User', 'Profile']
```

Then allow:
```python
import users.models as _users_models

user = _users_models.User.objects.get(...)  # Clean!
```

## Success Criteria

✅ All Python files use absolute modular imports with aliases
✅ Zero relative imports in codebase
✅ Zero direct class imports from same project
✅ Consistent `_alias` naming pattern
✅ Developers understand WHY (explained every time)

## Behavior

**Proactive enforcement:**
- Check imports without being asked
- Fix violations immediately
- Explain why the pattern is required
- Update all related usage in the file

**Never:**
- Require explicit "check imports" request
- Wait for code review
- Just warn without fixing
