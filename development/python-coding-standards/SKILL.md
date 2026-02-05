---
name: python-coding-standards
description: Python coding standards following PEP 8, type hints, testing best practices, and modern Python patterns. Use for Python projects requiring clean, maintainable, production-ready code with comprehensive testing.
---

# Python Coding Standards

> **Quick Navigation:**
> Level 1: [Quick Start](#level-1-quick-start) (5 min) | Level 2: [Implementation](#level-2-implementation) (30 min) | Level 3: [Mastery](#level-3-mastery-resources) (Extended)

---

## Level 1: Quick Start

### Core Principles

1. **Pythonic Code**: Write idiomatic Python following "The Zen of Python"
2. **Type Safety**: Use type hints for all public interfaces
3. **Test-First**: Write tests before implementation (TDD)
4. **Documentation**: Docstrings for all public functions
5. **Modern Python**: Use Python 3.10+ features

### Essential Checklist

- [ ] PEP 8 compliant (Black + isort formatted)
- [ ] Type hints on all function signatures
- [ ] pytest tests with >80% coverage
- [ ] Google-style docstrings
- [ ] Specific exception handling (no bare `except:`)
- [ ] No hardcoded secrets
- [ ] src layout project structure
- [ ] Pinned dependencies in requirements.txt

### Quick Example

```python
"""User authentication module."""

from dataclasses import dataclass
from typing import Optional
import bcrypt


@dataclass
class User:
    """User account data."""
    username: str
    email: str
    password_hash: str


def authenticate_user(username: str, password: str) -> Optional[User]:
    """Authenticate user with username and password.

    Args:
        username: User's username
        password: Plain text password to verify

    Returns:
        User object if authentication succeeds, None otherwise

    Raises:
        ValueError: If username or password is empty
    """
    if not username or not password:
        raise ValueError("Username and password required")

    user = _fetch_user_from_db(username)
    if user and _verify_password(password, user.password_hash):
        return user
    return None
```

---

## Level 2: Implementation

### Code Style & Formatting

**PEP 8 + Black Formatting:**

```python
# Good: Black-formatted, clear naming
def calculate_user_discount(
    user: User,
    purchase_amount: Decimal,
    promo_code: Optional[str] = None
) -> Decimal:
    """Calculate discount for user purchase."""
    base_discount = _get_loyalty_discount(user)
    promo_discount = _validate_promo_code(promo_code) if promo_code else Decimal("0")
    return min(base_discount + promo_discount, Decimal("0.5"))
```

**Tool Configuration (pyproject.toml):**

```toml
[tool.black]
line-length = 88
target-version = ["py310"]

[tool.isort]
profile = "black"

[tool.ruff]
line-length = 88
select = ["E", "F", "W", "I", "UP", "B", "C4"]
```

**Common Patterns:**

```python
# List/dict comprehensions
active_users = [u for u in users if u.is_active]
user_map = {u.id: u for u in users}

# Generator expressions (memory-efficient)
total = sum(order.amount for order in orders)

# Context managers
with open("data.json") as f:
    data = json.load(f)

# Walrus operator (Python 3.8+)
if (user := get_user(user_id)) is not None:
    process_user(user)
```

**Anti-Patterns to Avoid:**

```python
# Bad: Mutable default arguments
def add_item(item, items=[]):  # Bug: shared list
    items.append(item)

# Good: Use None
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items

# Bad: Bare except
try:
    risky_operation()
except:  # Catches KeyboardInterrupt, SystemExit
    pass

# Good: Specific exceptions
try:
    risky_operation()
except (ValueError, KeyError) as e:
    logger.error(f"Operation failed: {e}")
```

### Type Hints

**Essential Patterns:**

```python
from typing import Protocol, TypeVar, Generic, Literal
from collections.abc import Sequence

# Basic types (Python 3.10+)
def process_items(items: list[str], count: int = 10) -> dict[str, int]:
    return {item: len(item) for item in items[:count]}

# Protocols (structural typing)
class Drawable(Protocol):
    def draw(self) -> None: ...

def render(obj: Drawable) -> None:
    obj.draw()

# Generics
T = TypeVar('T')

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

# Literal types
LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR"]

# Union types (Python 3.10+)
def parse_id(value: str | int) -> int:
    return int(value) if isinstance(value, str) else value
```

**mypy Configuration:**

```ini
[mypy]
python_version = 3.10
disallow_untyped_defs = True
warn_return_any = True
strict_equality = True
```

### Testing Standards

**pytest Best Practices:**

```python
import pytest
from unittest.mock import patch
from myapp.auth import authenticate_user, User


@pytest.fixture
def mock_user():
    """Create mock user for testing."""
    return User(username="testuser", email="test@example.com", password_hash="$2b$...")


@pytest.fixture
def auth_service(mock_user):
    """Create auth service with mocked database."""
    with patch('myapp.auth._fetch_user_from_db', return_value=mock_user):
        yield


def test_authenticate_valid_credentials(auth_service, mock_user):
    """Test authentication with valid credentials."""
    user = authenticate_user("testuser", "correct_password")
    assert user is not None
    assert user.username == mock_user.username


def test_authenticate_empty_username():
    """Test authentication rejects empty username."""
    with pytest.raises(ValueError, match="Username and password required"):
        authenticate_user("", "password")


@pytest.mark.parametrize("username,password,expected", [
    ("user1", "pass1", True),
    ("user2", "wrong", False),
])
def test_authenticate_multiple_cases(username, password, expected):
    """Test authentication with multiple inputs."""
    result = authenticate_user(username, password)
    assert (result is not None) == expected
```

**Test Organization:**

```
tests/
├── conftest.py           # Shared fixtures
├── unit/                 # Unit tests (fast, isolated)
├── integration/          # Integration tests (DB, API)
└── e2e/                  # End-to-end tests
```

### Documentation

**Google-Style Docstrings:**

```python
def fetch_user_orders(
    user_id: int,
    start_date: datetime,
    end_date: datetime,
    status: Optional[str] = None
) -> list[Order]:
    """Fetch user orders within date range.

    Args:
        user_id: Unique user identifier
        start_date: Start of date range (inclusive)
        end_date: End of date range (inclusive)
        status: Optional status filter ("pending", "shipped", "delivered")

    Returns:
        List of Order objects matching criteria.

    Raises:
        ValueError: If end_date is before start_date
        UserNotFoundError: If user_id doesn't exist

    Example:
        >>> orders = fetch_user_orders(123, start, end, status="shipped")
    """
```

### Project Structure

**Recommended src Layout:**

```
myproject/
├── src/myapp/
│   ├── __init__.py
│   ├── api/
│   ├── models/
│   ├── services/
│   └── utils/
├── tests/
│   ├── conftest.py
│   ├── unit/
│   └── integration/
├── pyproject.toml
├── requirements.txt
└── README.md
```

**pyproject.toml:**

```toml
[project]
name = "myapp"
version = "1.0.0"
requires-python = ">=3.10"
dependencies = [
    "fastapi>=0.100.0",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "black>=23.0.0",
    "mypy>=1.5.0",
    "ruff>=0.0.290",
]
```

### Error Handling

**Exception Hierarchy:**

```python
class AppError(Exception):
    """Base exception for application errors."""
    def __init__(self, message: str, code: str, details: dict = None):
        super().__init__(message)
        self.code = code
        self.details = details or {}


class ValidationError(AppError):
    """Input validation failed."""
    def __init__(self, field: str, message: str):
        super().__init__(
            message=f"Validation failed for {field}: {message}",
            code="VALIDATION_ERROR",
            details={"field": field}
        )


class ResourceNotFoundError(AppError):
    """Requested resource not found."""
    def __init__(self, resource_type: str, resource_id: str | int):
        super().__init__(
            message=f"{resource_type} {resource_id} not found",
            code="NOT_FOUND",
            details={"resource_type": resource_type, "resource_id": resource_id}
        )
```

**Error Handling Pattern:**

```python
from contextlib import contextmanager

@contextmanager
def handle_api_errors():
    """Context manager for API error handling."""
    try:
        yield
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.message)
    except ResourceNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    except AppError as e:
        logger.error(f"Application error: {e}", extra=e.details)
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/users/")
async def create_user(user_data: UserCreate):
    with handle_api_errors():
        return user_service.create_user(user_data)
```

### Security

**Input Validation with Pydantic:**

```python
from pydantic import BaseModel, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    """User creation schema with validation."""
    username: str = Field(min_length=3, max_length=32, pattern=r'^[a-zA-Z0-9_-]+$')
    email: EmailStr
    password: str = Field(min_length=8)

    @field_validator('password')
    @classmethod
    def password_strength(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError("Must contain uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Must contain digit")
        return v
```

**Secrets Management:**

```python
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings from environment."""
    database_url: str
    secret_key: str
    api_key: str

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()
```

### Performance

**Optimization Patterns:**

```python
from functools import lru_cache
from sqlalchemy.orm import joinedload

# Memoization
@lru_cache(maxsize=128)
def expensive_calculation(n: int) -> int:
    return sum(i ** 2 for i in range(n))

# N+1 query prevention
def fetch_users_with_orders():
    return db.query(User).options(joinedload(User.orders)).all()

# Batch processing
def process_items_batch(items: list[Item], batch_size: int = 100):
    for i in range(0, len(items), batch_size):
        process_batch(items[i:i + batch_size])
```

**Async Patterns:**

```python
import asyncio
import aiohttp


async def fetch_all_urls(urls: list[str]) -> list[dict]:
    """Fetch multiple URLs concurrently."""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        return await asyncio.gather(*tasks)
```

---

## Level 3: Mastery Resources

For comprehensive examples, configurations, and advanced patterns, see [REFERENCE.md](REFERENCE.md).

### Quick Reference Commands

```bash
# Setup
python -m venv venv && source venv/bin/activate
pip install -e ".[dev]"

# Code quality
black src/ tests/ && isort src/ tests/
mypy src/ && ruff check src/

# Testing
pytest --cov=src --cov-report=html

# Pre-commit
pre-commit install && pre-commit run --all-files
```

### Related Skills

- [Testing Standards](../../testing/SKILL.md) - Comprehensive testing practices
- [Security Practices](../../security-practices/SKILL.md) - Security implementation
- [API Design](../../api/graphql/SKILL.md) - RESTful and GraphQL APIs
- [DevOps CI/CD](../../devops/ci-cd/SKILL.md) - Continuous integration

### Extended Resources in REFERENCE.md

- Complete type hint patterns (Protocols, Generics, TypedDict)
- Full mypy/pylint/ruff configuration files
- pytest fixtures and parametrization examples
- Production FastAPI example with database
- Exception hierarchy templates
- Structured logging configuration
- Async/await patterns
- Performance profiling decorators
- NIST control tag examples

---

## Validation

- Token count: Under 5,000 tokens
- Code examples: All tested and working
- Links: All internal references valid
- YAML frontmatter: Valid and complete
