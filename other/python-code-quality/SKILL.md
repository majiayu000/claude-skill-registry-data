---
name: python-code-quality
description: Python code quality patterns including style, formatting, naming conventions, docstrings, type annotations, generics, protocols, and anti-pattern avoidance. Use when writing new code, reviewing style, configuring ruff/mypy/pyright, adding type hints, implementing generics or protocols, or reviewing code for common mistakes.
---

# Python Code Quality

Write high-quality Python code with consistent style, strong type safety, and awareness of common pitfalls. These patterns make codebases maintainable, self-documenting, and easier to debug.

## When to Use This Skill

- Setting up linting and formatting for a new project
- Writing or reviewing docstrings
- Establishing team coding standards
- Configuring ruff, mypy, or pyright
- Reviewing code for style consistency
- Adding type hints to existing code
- Creating generic, reusable classes
- Defining structural interfaces with protocols
- Configuring mypy or pyright for strict checking
- Reviewing code before merge
- Debugging mysterious issues
- Refactoring legacy code

## Core Concepts

**Style** — Let tools handle formatting debates. Follow PEP 8 naming. Document public APIs with docstrings.

**Type Safety** — Type annotations are enforced documentation. Use generics for reusable code. Use protocols for structural interfaces.

**Anti-Patterns** — Know what to avoid. A checklist review before merging catches most recurring issues.

---

## Style & Formatting

### Pattern 1: Modern Tooling (ruff)

Use `ruff` as an all-in-one linter and formatter. It replaces flake8, isort, and black with a single fast tool.

```toml
# pyproject.toml
[tool.ruff]
line-length = 120
target-version = "py312"

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # pyflakes
    "I",    # isort
    "B",    # flake8-bugbear
    "C4",   # flake8-comprehensions
    "UP",   # pyupgrade
    "SIM",  # flake8-simplify
]
ignore = ["E501"]  # Line length handled by formatter

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

```bash
ruff check --fix .  # Lint and auto-fix
ruff format .       # Format code
```

### Pattern 2: Naming Conventions

Follow PEP 8 with emphasis on clarity over brevity.

```python
# Files and modules: snake_case
user_repository.py
order_processing.py

# Classes: PascalCase (acronyms stay uppercase)
class UserRepository: ...
class HTTPClientFactory: ...

# Functions and variables: snake_case
def get_user_by_email(email: str) -> User | None:
    retry_count = 3

# Module-level constants: SCREAMING_SNAKE_CASE
MAX_RETRY_ATTEMPTS = 3
DEFAULT_TIMEOUT_SECONDS = 30
```

### Pattern 3: Import Organization

Group: standard library → third-party → local. Use absolute imports exclusively.

```python
# Standard library
import os
from collections.abc import Callable
from typing import Any

# Third-party
import httpx
from pydantic import BaseModel

# Local
from myproject.models import User
from myproject.services import UserService

# Preferred: absolute imports
from myproject.utils import retry_decorator

# Avoid: relative imports
from ..utils import retry_decorator
```

### Pattern 4: Google-Style Docstrings

Write docstrings for all public classes, methods, and functions.

```python
# Simple function: one-liner is fine
def get_user(user_id: str) -> User:
    """Retrieve a user by their unique identifier."""
    ...

# Complex function: full format
def process_batch(
    items: list[Item],
    max_workers: int = 4,
    on_progress: Callable[[int, int], None] | None = None,
) -> BatchResult:
    """Process items concurrently using a worker pool.

    Args:
        items: The items to process. Must not be empty.
        max_workers: Maximum concurrent workers. Defaults to 4.
        on_progress: Optional callback receiving (completed, total) counts.

    Returns:
        BatchResult containing succeeded items and any failures.

    Raises:
        ValueError: If items is empty.

    Example:
        >>> result = process_batch(items, max_workers=8)
        >>> print(f"Processed {len(result.succeeded)} items")
    """
    ...

# Class docstring
class UserService:
    """Service for managing user operations.

    Attributes:
        repository: The data access layer for user persistence.

    Example:
        >>> service = UserService(repository, logger)
        >>> user = service.create_user(CreateUserInput(...))
    """
```

### Pattern 5: Line Length and Formatting

120 characters. Let ruff handle it; use logical breaks for readability.

```python
# Multi-line function signatures
def create_user(
    email: str,
    name: str,
    role: UserRole = UserRole.MEMBER,
    notify: bool = True,
) -> User:
    ...

# Method chains
result = (
    db.query(User)
    .filter(User.active == True)
    .order_by(User.created_at.desc())
    .limit(10)
    .all()
)
```

---

## Type Safety

### Pattern 6: Annotate All Public Signatures

Every public function, method, and class should have type annotations.

```python
def get_user(user_id: str) -> User:
    ...

def process_batch(
    items: list[Item],
    max_workers: int = 4,
) -> BatchResult[ProcessedItem]:
    ...

class UserRepository:
    def __init__(self, db: Database) -> None:
        self._db = db

    async def find_by_id(self, user_id: str) -> User | None:
        ...

    async def save(self, user: User) -> User:
        ...
```

### Pattern 7: Modern Union Syntax

```python
# Preferred (Python 3.10+)
def find_user(user_id: str) -> User | None: ...
def parse_value(v: str) -> int | float | str: ...

# Older style (needed for Python 3.9)
from typing import Optional, Union
def find_user(user_id: str) -> Optional[User]: ...
```

### Pattern 8: Type Narrowing with Guards

```python
def process_user(user_id: str) -> UserData:
    user = find_user(user_id)
    if user is None:
        raise UserNotFoundError(f"User {user_id} not found")
    # Type checker knows user is User here
    return UserData(name=user.name, email=user.email)

def process_items(items: list[Item | None]) -> list[ProcessedItem]:
    valid_items = [item for item in items if item is not None]
    # valid_items is now list[Item]
    return [process(item) for item in valid_items]
```

### Pattern 9: Generic Classes

```python
from typing import TypeVar, Generic

T = TypeVar("T")
E = TypeVar("E", bound=Exception)

class Result(Generic[T, E]):
    """Represents either a success value or an error."""

    def __init__(self, value: T | None = None, error: E | None = None) -> None:
        if (value is None) == (error is None):
            raise ValueError("Exactly one of value or error must be set")
        self._value = value
        self._error = error

    @property
    def is_success(self) -> bool:
        return self._error is None

    def unwrap(self) -> T:
        if self._error is not None:
            raise self._error
        return self._value  # type: ignore[return-value]

    def unwrap_or(self, default: T) -> T:
        if self._error is not None:
            return default
        return self._value  # type: ignore[return-value]

# Usage preserves types
def parse_config(path: str) -> Result[Config, ConfigError]:
    try:
        return Result(value=Config.from_file(path))
    except ConfigError as e:
        return Result(error=e)
```

### Pattern 10: Generic Repository

```python
from abc import ABC, abstractmethod

T = TypeVar("T")
ID = TypeVar("ID")

class Repository(ABC, Generic[T, ID]):
    @abstractmethod
    async def get(self, id: ID) -> T | None: ...

    @abstractmethod
    async def save(self, entity: T) -> T: ...

    @abstractmethod
    async def delete(self, id: ID) -> bool: ...

class UserRepository(Repository[User, str]):
    async def get(self, id: str) -> User | None:
        row = await self._db.fetchrow("SELECT * FROM users WHERE id = $1", id)
        return User(**row) if row else None

    async def save(self, entity: User) -> User: ...
    async def delete(self, id: str) -> bool: ...
```

### Pattern 11: TypeVar with Bounds

```python
from pydantic import BaseModel

ModelT = TypeVar("ModelT", bound=BaseModel)

def validate_and_create(model_cls: type[ModelT], data: dict) -> ModelT:
    return model_cls.model_validate(data)

# Works with any BaseModel subclass; type error for non-BaseModel types
user = validate_and_create(User, {"name": "Alice", "email": "a@b.com"})
```

### Pattern 12: Protocols for Structural Typing

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Serializable(Protocol):
    def to_dict(self) -> dict: ...
    @classmethod
    def from_dict(cls, data: dict) -> "Serializable": ...

# User satisfies Serializable without inheriting from it
class User:
    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name}

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        return cls(id=data["id"], name=data["name"])

def serialize(obj: Serializable) -> str:
    return json.dumps(obj.to_dict())

# Common protocol patterns
class Closeable(Protocol):
    def close(self) -> None: ...

class AsyncCloseable(Protocol):
    async def close(self) -> None: ...

class HasId(Protocol):
    @property
    def id(self) -> str: ...
```

### Pattern 13: Type Aliases and Callable Types

```python
# Python 3.10+ simple aliases
type UserId = str
type UserDict = dict[str, Any]

# Python 3.9-3.11 style
from typing import TypeAlias
UserId: TypeAlias = str

# Callable types
from collections.abc import Callable, Awaitable

ProgressCallback = Callable[[int, int], None]  # (current, total)
AsyncHandler = Callable[[Request], Awaitable[Response]]

# With named parameters (use Protocol)
class OnProgress(Protocol):
    def __call__(self, current: int, total: int, *, message: str = "") -> None: ...
```

### Type Checker Configuration

```toml
# pyproject.toml - mypy strict mode
[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true
warn_unused_ignores = true
disallow_untyped_defs = true
no_implicit_optional = true

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false

# Alternative: pyright
[tool.pyright]
pythonVersion = "3.12"
typeCheckingMode = "strict"
```

For existing codebases, enable strict mode per-module incrementally.

---

## Anti-Patterns Checklist

### Infrastructure Anti-Patterns

**Scattered Timeout/Retry Logic**
```python
# BAD: Duplicated everywhere
def fetch_user(user_id):
    try:
        return requests.get(url, timeout=30)
    except Timeout:
        return None

# GOOD: Centralized
@retry(stop=stop_after_attempt(3), wait=wait_exponential())
def http_get(url: str) -> Response:
    return requests.get(url, timeout=30)
```

**Double Retry**
```python
# BAD: Retrying at multiple layers
@retry(max_attempts=3)       # Application retry
def call_service():
    return client.request()  # Client also retries!
```
Fix: Retry at one layer only. Know your infrastructure's retry behavior.

**Hard-Coded Configuration**
```python
# BAD
DB_HOST = "prod-db.example.com"
API_KEY = "sk-12345"

# GOOD
from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    db_host: str = Field(alias="DB_HOST")
    api_key: str = Field(alias="API_KEY")
```

### Architecture Anti-Patterns

**Exposed Internal Types**
```python
# BAD: Leaking ORM model to API
@app.get("/users/{id}")
def get_user(id: str) -> UserModel:  # SQLAlchemy model
    return db.query(UserModel).get(id)

# GOOD
@app.get("/users/{id}")
def get_user(id: str) -> UserResponse:
    user = db.query(UserModel).get(id)
    return UserResponse.from_orm(user)
```

**Mixed I/O and Business Logic**
```python
# BAD: SQL embedded in business logic
def calculate_discount(user_id: str) -> float:
    user = db.query("SELECT * FROM users WHERE id = ?", user_id)
    orders = db.query("SELECT * FROM orders WHERE user_id = ?", user_id)
    if len(orders) > 10:
        return 0.15
    return 0.0

# GOOD: Pure business logic
def calculate_discount(user: User, orders: list[Order]) -> float:
    if len(orders) > 10:
        return 0.15
    return 0.0
```

### Error Handling Anti-Patterns

**Bare Exception Handling**
```python
# BAD: Silent failure
try:
    process()
except Exception:
    pass  # Bugs hidden forever

# GOOD
try:
    process()
except ConnectionError as e:
    logger.warning("Connection failed", error=str(e))
    raise
except ValueError as e:
    raise BadRequestError(str(e))
```

**Ignored Partial Failures**
```python
# BAD: Stops on first error
def process_batch(items):
    results = []
    for item in items:
        result = process(item)  # Raises → batch aborted
        results.append(result)
    return results

# GOOD
def process_batch(items) -> BatchResult:
    succeeded, failed = {}, {}
    for idx, item in enumerate(items):
        try:
            succeeded[idx] = process(item)
        except Exception as e:
            failed[idx] = e
    return BatchResult(succeeded, failed)
```

**Missing Input Validation**
```python
# BAD
def create_user(data: dict):
    return User(**data)  # Crashes deep in code on bad input

# GOOD
def create_user(data: dict) -> User:
    validated = CreateUserInput.model_validate(data)
    return User.from_input(validated)
```

### Resource Anti-Patterns

**Unclosed Resources**
```python
# BAD
def read_file(path):
    f = open(path)
    return f.read()  # Never closed if this raises

# GOOD
def read_file(path):
    with open(path) as f:
        return f.read()
```

**Blocking in Async**
```python
# BAD: Blocks the event loop
async def fetch_data():
    time.sleep(1)           # Blocks everything!
    response = requests.get(url)  # Also blocks!

# GOOD
async def fetch_data():
    await asyncio.sleep(1)
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
```

### Type Safety Anti-Patterns

```python
# BAD: No types, untyped collections
def process(data):
    return data["value"] * 2

def get_users() -> list:
    ...

# GOOD
def process(data: dict[str, int]) -> int:
    return data["value"] * 2

def get_users() -> list[User]:
    ...
```

### Testing Anti-Patterns

```python
# BAD: Only tests happy path
def test_create_user():
    user = service.create_user(valid_data)
    assert user.id is not None

# GOOD: Tests error conditions too
def test_create_user_invalid_email():
    with pytest.raises(ValueError, match="Invalid email"):
        service.create_user(invalid_email_data)

def test_create_user_duplicate_email():
    service.create_user(valid_data)
    with pytest.raises(ConflictError):
        service.create_user(valid_data)

# BAD: Over-mocking
def test_user_service():
    mock_repo = Mock()
    mock_cache = Mock()
    mock_logger = Mock()
    # Test doesn't verify real behavior
```
Fix: Use integration tests for critical paths. Mock only external services.

### Quick Review Checklist

Before finalizing code, verify:

- [ ] No scattered timeout/retry logic (centralized in decorators)
- [ ] No double retry (app + infrastructure layer)
- [ ] No hard-coded configuration or secrets
- [ ] No exposed internal types (ORM models, protobufs)
- [ ] No mixed I/O and business logic
- [ ] No bare `except Exception: pass`
- [ ] No ignored partial failures in batches
- [ ] No missing input validation at boundaries
- [ ] No unclosed resources (use context managers)
- [ ] No blocking calls in async code
- [ ] All public functions have type hints
- [ ] Collections have type parameters (`list[str]` not `list`)
- [ ] Error paths are tested
- [ ] Edge cases are covered

### Common Fixes Summary

| Anti-Pattern | Fix |
|---|---|
| Scattered retry logic | Centralized decorators |
| Hard-coded config | Environment variables + pydantic-settings |
| Exposed ORM models | DTO/response schemas |
| Mixed I/O + logic | Repository pattern |
| Bare except | Catch specific exceptions |
| Batch stops on error | `BatchResult` with successes/failures |
| No validation | Validate at boundaries with Pydantic |
| Unclosed resources | Context managers |
| Blocking in async | Async-native libraries |
| Missing types | Type annotations on all public APIs |
| Only happy path tests | Test errors and edge cases |

---

## Best Practices Summary

**Style**
1. **Use ruff** — Single tool for linting and formatting
2. **120 character lines** — Modern standard
3. **Descriptive names** — Clarity over brevity, no abbreviations
4. **Absolute imports** — More maintainable than relative
5. **Google-style docstrings** — For all public APIs
6. **Automate in CI** — Run ruff and mypy on every commit

**Type Safety**
7. **Annotate all public APIs** — Functions, methods, class attributes
8. **Use `T | None`** — Modern union syntax over `Optional[T]`
9. **Run strict mypy** — `mypy --strict` in CI
10. **Use generics** — Preserve type info in reusable code
11. **Define protocols** — Structural typing without inheritance
12. **Minimize `Any`** — Use specific types or generics

**Anti-Patterns**
13. **Run the checklist before merge** — Catch recurring issues early
14. **Test error paths** — Verify exceptions are raised correctly
15. **Use context managers** — For all resource management
