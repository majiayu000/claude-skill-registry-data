---
name: separate-monolithic-python
description: Break large Python files (>500 LOC) into smaller, well-organized modules with proper package structure. Use when a Python file is too large, monolithic, or needs refactoring. Triggered by requests mentioning "too large", "separate", "split", "break up", or "refactor" for Python files.
---

# Separate Monolithic Python Code

Break large Python files into maintainable modules following Python best practices.

## Workflow

### Step 1: Analyze
1. Read entire file to understand structure
2. Identify components (classes, function groups, constants)
3. Count lines (>500 LOC needs separation)
4. Map dependencies (what depends on what)

### Step 2: Plan Structure
Choose a separation pattern:

**By Responsibility** (Recommended):
```
mypackage/
├── __init__.py       # Public API exports
├── models.py         # Data models/classes
├── services.py       # Business logic
├── utils.py          # Helper functions
└── constants.py      # Configuration
```

**By Feature**:
```
mypackage/
├── __init__.py
├── feature_a/
│   ├── __init__.py
│   ├── models.py
│   └── logic.py
└── feature_b/
```

**By Layer** (Domain-driven):
```
mypackage/
├── __init__.py
├── domain/          # Core models
├── application/     # Use cases
└── infrastructure/  # External deps
```

Present plan to user before proceeding.

### Step 3: Create Structure
```bash
mkdir mypackage
touch mypackage/__init__.py mypackage/models.py mypackage/services.py
```

### Step 4: Extract Code
Extract in dependency order:
1. **Constants** (no dependencies)
2. **Models** (minimal dependencies)
3. **Utilities** (depend on constants/models)
4. **Services** (depend on everything)
5. **Main** (orchestrate all)

### Step 5: Update Imports

**In new modules:**
```python
# models.py
from .constants import DEFAULT_ROLE
from .utils import validate_email
```

**In `__init__.py` (public API):**
```python
from .models import User, Product
from .services import create_user

__all__ = ['User', 'Product', 'create_user']
```

**In external files:**
```python
# Before: from monolith import User
# After:  from mypackage import User
```

### Step 6: Validate
```bash
ruff check mypackage/
mypy mypackage/
python -c "from mypackage import User"
pytest tests/
```

## Key Principles

**High Cohesion**: Keep related code together
- Group by purpose, not type
- Example: `user_service.py` not `all_services.py`

**Low Coupling**: Minimize dependencies
- Avoid circular imports
- Use dependency injection

**Single Responsibility**: One clear purpose per module

**Clear API**: Use `__init__.py` to expose public interface

## Handling Circular Dependencies

**Option 1: Move shared code**
```python
# Create shared.py for common code
```

**Option 2: TYPE_CHECKING**
```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .services import UserService  # Only for type hints
```

**Option 3: Late import**
```python
def process_user():
    from .services import create_user  # Import inside function
    create_user()
```

## File Size Guidelines

- ✅ **Ideal**: 100-300 lines
- ⚠️ **Warning**: 300-500 lines (consider splitting)
- ❌ **Too large**: >500 lines (should split)

## Quick Example

**Before** (monolith.py - 800 lines):
```python
DATABASE_URL = "sqlite:///./test.db"

class User:
    def __init__(self, name):
        self.name = name

def create_user(name):
    return User(name)

app = FastAPI()

@app.get("/users")
def get_users():
    return []
```

**After**:
```
api/
├── __init__.py
├── config.py      # DATABASE_URL
├── models.py      # User class
├── services.py    # create_user
└── routes.py      # FastAPI routes
```

## Troubleshooting

**Import errors**: Check `__init__.py` exports, verify relative imports (`.module`)

**Circular imports**: Use TYPE_CHECKING or late imports, or extract shared code

**Tests failing**: Update test imports to new package structure

For detailed examples, patterns, and troubleshooting, see [references/detailed-guide.md](references/detailed-guide.md).
