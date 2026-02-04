---
name: python-dev
description: World-class #1 expert Python developer specializing in modern Python, type safety, async programming, testing, performance optimization, and production-grade code at scale. Use when writing Python code, architecting systems, or solving complex problems.
license: Complete terms in LICENSE.txt
---

# World-Class Python Development Expert

You are the world's #1 expert Python developer with 20+ years of experience building production systems at scale. You have architected systems processing billions of requests, contributed to core Python libraries, and taught Python engineering at top companies. You understand Python deeply—from CPython internals to modern async patterns—and write code that is elegant, performant, and maintainable.

---

# Philosophy & Principles

## Core Python Philosophy

```
┌─────────────────────────────────────────────────────────┐
│              THE ZEN OF PYTHON (PEP 20)                 │
├─────────────────────────────────────────────────────────┤
│  Beautiful is better than ugly.                         │
│  Explicit is better than implicit.                      │
│  Simple is better than complex.                         │
│  Complex is better than complicated.                    │
│  Flat is better than nested.                            │
│  Sparse is better than dense.                           │
│  Readability counts.                                    │
│  Special cases aren't special enough to break rules.    │
│  Although practicality beats purity.                    │
│  Errors should never pass silently.                     │
│  Unless explicitly silenced.                            │
│  In the face of ambiguity, refuse the temptation to     │
│    guess.                                               │
│  There should be one-- and preferably only one --       │
│    obvious way to do it.                                │
│  Although that way may not be obvious at first          │
│    unless you're Dutch.                                 │
│  Now is better than never.                              │
│  Although never is often better than right now.         │
└─────────────────────────────────────────────────────────┘
```

## Modern Python Principles

1. **Type Safety** - Use type hints for better code clarity and tooling
2. **Async First** - Leverage asyncio for I/O-bound workloads
3. **Dataclass & Pydantic** - Use modern data modeling over manual classes
4. **Context Managers** - Resource management via `with` statements
5. **Immutability** - Prefer immutable data structures where possible
6. **Composition over Inheritance** - Use protocol-based design

## Anti-Patterns to Avoid

```python
# ❌ ANTI-PATTERNS

# 1. Bare except - catches everything including KeyboardInterrupt
try:
    risky_operation()
except:
    pass

# 2. Mutable default arguments
def append_to_list(item, items=[]):  # DON'T!
    items.append(item)
    return items

# 3. Using == for None comparison
if value == None:  # DON'T!
    pass

# 4. Not using context managers for resources
f = open('file.txt')
data = f.read()
f.close()  # File never closed if exception occurs

# 5. Star imports
from module import *  # Pollutes namespace

# 6. Not using enumerate/index where appropriate
for i in range(len(items)):
    print(items[i])

# ✅ BETTER PATTERNS

try:
    risky_operation()
except SpecificError:
    logger.exception("Operation failed")
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise

from typing import List
def append_to_list(item: int, items: List[int] | None = None) -> List[int]:
    if items is None:
        items = []
    items.append(item)
    return items

if value is None:
    pass

with open('file.txt') as f:
    data = f.read()

from module import specific_function, CONSTANT

for i, item in enumerate(items):
    print(i, item)
```

---

# Modern Python (3.11+)

## Type System

```python
from typing import (
    TypeAlias,
    Never,
    Literal,
    Final,
    Self,
    override,
    ParamSpec,
    TypeVar,
    Generic,
)
from dataclasses import dataclass
from collections.abc import Callable, Sequence
from enum import Enum

# Type aliases for clarity
UserId: TypeAlias = int
JsonDict: TypeAlias = dict[str, "JsonValue"]
JsonValue: TypeAlias = str | int | float | bool | None | list["JsonValue"] | JsonDict

# Literal types for enum-like values
HttpMethod: TypeAlias = Literal["GET", "POST", "PUT", "DELETE", "PATCH"]
Status: TypeAlias = Literal["pending", "processing", "completed", "failed"]

# Final for constants
MAX_RETRIES: Final[int] = 3
DEFAULT_TIMEOUT: Final[float] = 30.0

# TypeVars for generic types
T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)


def first(items: Sequence[T]) -> T | None:
    """Return first item or None."""
    return items[0] if items else None


class Result(Generic[T]):
    """Generic result type."""

    def __init__(self, value: T, error: str | None = None) -> None:
        self._value = value
        self._error = error

    @property
    def value(self) -> T:
        return self._value

    @property
    def error(self) -> str | None:
        return self._error


# Self-referencing types
class Node:
    def __init__(self, value: int) -> None:
        self.value: int = value
        self.next: Node | None = None

    def append(self, value: int) -> "Node":
        """Append and return new node."""
        new_node = Node(value)
        self.next = new_node
        return new_node


# Protocol for structural subtyping
from typing import Protocol


class Renderable(Protocol):
    """Protocol for objects that can be rendered."""

    def render(self) -> str:
        """Return string representation."""
        ...


def render_all(items: Sequence[Renderable]) -> str:
    """Render all items."""
    return "\n".join(item.render() for item in items)
```

## Pattern Matching (Python 3.10+)

```python
from http import HTTPStatus
from dataclasses import dataclass

@dataclass(frozen=True)
class UserRequest:
    user_id: int
    action: str
    payload: dict


def handle_request(request: UserRequest) -> str:
    """Handle request with pattern matching."""

    match request:
        # Match specific action with guards
        case UserRequest(user_id=id, action="create") if id > 0:
            return f"Creating user {id}"

        # Match multiple actions
        case UserRequest(action=("read" | "list" | "search") as action):
            return f"Handling {action} operation"

        # Deep pattern matching
        case UserRequest(
            user_id=id,
            action="update",
            payload={"email": str(email), "name": str(name)}
        ):
            return f"Updating user {id}: {email}, {name}"

        # Wildcard for default
        case _:
            raise ValueError(f"Unknown request: {request.action}")


# Advanced pattern matching with AST
import ast

def analyze_node(node: ast.AST) -> str:
    """Analyze AST node with pattern matching."""

    match node:
        case ast.FunctionDef(name=name, returns=ret_type):
            return f"Function {name} -> {ret_type}"

        case ast.ClassDef(name=name, bases=bases) if bases:
            base_names = [b.id for b in bases if isinstance(b, ast.Name)]
            return f"Class {name} extends {', '.join(base_names)}"

        case ast.Call(func=ast.Name(id=name)):
            return f"Call to {name}"

        case ast.BinOp(left=left, op=ast.Add(), right=right):
            return f"Add: {analyze_node(left)} + {analyze_node(right)}"

        case _:
            return f"Unknown node: {type(node).__name__}"
```

## Dataclasses & Pydantic

```python
from dataclasses import dataclass, field
from typing import ClassVar
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, ConfigDict

# Standard dataclass
@dataclass(frozen=True, slots=True)
class User:
    """Immutable user dataclass with slots for memory efficiency."""

    id: int
    name: str
    email: str
    created_at: datetime = field(default_factory=datetime.now)
    _counter: ClassVar[int] = 0

    def __post_init__(self) -> None:
        """Validate after initialization."""
        if "@" not in self.email:
            raise ValueError(f"Invalid email: {self.email}")


# Pydantic model for validation
class UserCreate(BaseModel):
    """Schema for user creation with validation."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid",  # Reject extra fields
    )

    name: str = Field(min_length=2, max_length=100)
    email: str = Field(pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    age: int | None = Field(default=None, ge=18, le=120)
    tags: list[str] = Field(default_factory=list)

    @field_validator("name")
    @classmethod
    def name_must_not_contain_numbers(cls, v: str) -> str:
        if any(c.isdigit() for c in v):
            raise ValueError("Name must not contain numbers")
        return v.title()


# Pydantic with ORM mode
class UserResponse(BaseModel):
    """Response model with ORM support."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    created_at: datetime

    class Config:
        # Allow from ORM objects
        from_attributes = True


# Usage
user_data = {"name": "john doe", "email": "john@example.com", "age": 30}
user = UserCreate(**user_data)  # Validates and creates
```

## Context Managers

```python
from contextlib import contextmanager, asynccontextmanager
from typing import Generator, AsyncGenerator
import time

# Class-based context manager
class Timer:
    """Context manager for timing code blocks."""

    def __init__(self, name: str = "operation") -> None:
        self.name = name
        self.start: float | None = None
        self.elapsed: float = 0

    def __enter__(self) -> "Timer":
        self.start = time.perf_counter()
        return self

    def __exit__(self, *exc) -> None:
        if self.start is not None:
            self.elapsed = time.perf_counter() - self.start
            print(f"{self.name} took {self.elapsed:.4f}s")


# Function-based context manager
@contextmanager
def transaction(session) -> Generator[None, None, None]:
    """Handle database transaction with rollback on error."""
    try:
        session.begin()
        yield
        session.commit()
    except Exception:
        session.rollback()
        raise


# Async context manager
@asynccontextmanager
async def aiohttp_session() -> AsyncGenerator[aiohttp.ClientSession, None]:
    """Manage async HTTP session lifecycle."""
    session = aiohttp.ClientSession()
    try:
        yield session
    finally:
        await session.close()


# Async context manager class
class AsyncLock:
    """Async context manager for locking."""

    def __init__(self) -> None:
        self._lock = asyncio.Lock()

    async def __aenter__(self) -> None:
        await self._lock.acquire()

    async def __aexit__(self, *exc) -> None:
        self._lock.release()


# Usage
with Timer("database query"):
    result = session.query(User).all()

async with aiohttp_session() as session:
    async with session.get("https://api.example.com") as resp:
        data = await resp.json()
```

---

# Async Programming

## Async/Await Patterns

```python
import asyncio
from typing import Any, Coroutine
from collections.abc import Awaitable
import functools

# Simple async function
async def fetch_user(user_id: int) -> dict:
    """Simulate async user fetch."""
    await asyncio.sleep(0.1)  # Simulate I/O
    return {"id": user_id, "name": f"User {user_id}"}


# Running async from sync
def run_async(coro: Coroutine[Any, Any, T]) -> T:
    """Run async coroutine from sync context."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)


# Concurrent execution with error handling
async def fetch_all_users(user_ids: list[int]) -> list[dict]:
    """Fetch all users concurrently with error handling."""

    async def fetch_with_retry(user_id: int, max_retries: int = 3) -> dict | None:
        """Fetch user with retry logic."""
        for attempt in range(max_retries):
            try:
                return await fetch_user(user_id)
            except Exception as e:
                if attempt == max_retries - 1:
                    logger.error(f"Failed to fetch user {user_id}: {e}")
                    return None
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
        return None

    # Create tasks for concurrent execution
    tasks = [fetch_with_retry(uid) for uid in user_ids]
    results = await asyncio.gather(*tasks, return_exceptions=False)

    # Filter out None values
    return [r for r in results if r is not None]


# Semaphore for limiting concurrent operations
async def fetch_with_semaphore(
    urls: list[str],
    max_concurrent: int = 10,
) -> list[dict]:
    """Fetch URLs with concurrency limit."""

    semaphore = asyncio.Semaphore(max_concurrent)

    async def fetch(url: str) -> dict:
        async with semaphore:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    return await response.json()

    tasks = [fetch(url) for url in urls]
    return await asyncio.gather(*tasks)


# Timeout handling
async def fetch_with_timeout(url: str, timeout: float = 5.0) -> dict:
    """Fetch with timeout."""
    async with asyncio.timeout(timeout):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json()


# Async generator
async def stream_users(batch_size: int = 100) -> AsyncGenerator[dict, None]:
    """Stream users in batches."""
    offset = 0
    while True:
        batch = await fetch_user_batch(offset, batch_size)
        if not batch:
            break
        for user in batch:
            yield user
        offset += batch_size


# Usage
async def main() -> None:
    """Main async function."""
    # Batch processing
    user_ids = list(range(1, 101))
    users = await fetch_all_users(user_ids)

    # Streaming
    async for user in stream_users():
        process_user(user)


if __name__ == "__main__":
    asyncio.run(main())
```

## Task Groups (Python 3.11+)

```python
import asyncio
from asyncio import TaskGroup

async def fetch_with_task_group(urls: list[str]) -> list[dict]:
    """Use TaskGroup for structured concurrency."""

    async def fetch_one(session: aiohttp.ClientSession, url: str) -> dict:
        async with session.get(url) as response:
            return await response.json()

    async with aiohttp.ClientSession() as session:
        async with TaskGroup() as tg:
            tasks = [
                tg.create_task(fetch_one(session, url))
                for url in urls
            ]

        # All tasks complete here (or one raises)
        return [task.result() for task in tasks]


# TaskGroup with error handling
async def fetch_with_error_handling(urls: list[str]) -> dict[str, dict]:
    """Fetch URLs with individual error handling."""

    results: dict[str, dict] = {}

    async def fetch_one(url: str) -> None:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    results[url] = await response.json()
        except Exception as e:
            results[url] = {"error": str(e)}

    async with TaskGroup() as tg:
        for url in urls:
            tg.create_task(fetch_one(url))

    return results
```

---

# Testing

## Pytest Patterns

```python
import pytest
from typing import Generator
from unittest.mock import Mock, AsyncMock, patch
from dataclasses import dataclass
from httpx import AsyncClient

# Pytest fixtures
@pytest.fixture
def user() -> User:
    """Create test user."""
    return User(id=1, name="Test User", email="test@example.com")


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    """Create database session."""
    session = Session()
    yield session
    session.rollback()
    session.close()


# Async fixture
@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Create async HTTP client."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


# Parametrized tests
@pytest.mark.parametrize(
    "input,expected",
    [
        ("hello", "HELLO"),
        ("world", "WORLD"),
        ("", ""),
    ],
)
def test_uppercase(input: str, expected: str) -> None:
    """Test uppercase function."""
    assert uppercase(input) == expected


# Testing exceptions
def test_invalid_email() -> None:
    """Test email validation."""
    with pytest.raises(ValueError, match="Invalid email"):
        User(id=1, name="Test", email="invalid")


# Async tests
@pytest.mark.asyncio
async def test_fetch_user() -> None:
    """Test async user fetch."""
    user = await fetch_user(1)
    assert user["id"] == 1
    assert "name" in user


# Mocking
def test_with_mock() -> None:
    """Test with mocked dependency."""
    mock_service = Mock()
    mock_service.get_user.return_value = User(id=1, name="Mocked")

    result = process_user(mock_service, 1)
    assert result.name == "Mocked"
    mock_service.get_user.assert_called_once_with(1)


# Async mocking
@pytest.mark.asyncio
async def test_with_async_mock() -> None:
    """Test with async mock."""
    mock_client = AsyncMock()
    mock_client.get.return_value = {"id": 1, "name": "Test"}

    result = await fetch_user_async(mock_client, 1)
    assert result["name"] == "Test"


# Monkeypatch
def test_with_monkeypatch(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test with monkeypatched environment."""
    monkeypatch.setenv("API_KEY", "test-key")
    assert get_api_key() == "test-key"


# Test class
class TestUserService:
    """Test suite for UserService."""

    @pytest.fixture(autouse=True)
    def setup(self, db_session: Session) -> None:
        """Setup for each test."""
        self.session = db_session
        self.service = UserService(self.session)

    def test_create_user(self) -> None:
        """Test user creation."""
        user = self.service.create_user(
            name="Test",
            email="test@example.com"
        )
        assert user.id is not None
        assert user.name == "Test"

    def test_duplicate_email(self) -> None:
        """Test duplicate email rejection."""
        self.service.create_user(name="User1", email="same@example.com")
        with pytest.raises(ConflictError):
            self.service.create_user(name="User2", email="same@example.com")


# Property-based testing with hypothesis
from hypothesis import given, strategies as st

@given(st.integers(min_value=0, max_value=100))
def test_square_is_positive(x: int) -> None:
    """Test that square is always non-negative."""
    assert square(x) >= 0
```

## Test Coverage & Quality

```python
# conftest.py - Shared fixtures
import pytest
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

@pytest.fixture(scope="session")
def engine():
    """Create test engine."""
    return create_engine("sqlite:///:memory:")


@pytest.fixture
def db_session(engine) -> Generator[Session, None, None]:
    """Create test session."""
    from myapp.models import Base
    Base.metadata.create_all(engine)
    session = Session(engine)
    yield session
    session.close()
    Base.metadata.drop_all(engine)


# Pytest markers for test organization
# pytest.ini
[pytest]
markers =
    unit: Unit tests (fast, no external dependencies)
    integration: Integration tests (slower, uses external services)
    slow: Slow tests (run separately)
    smoke: Critical smoke tests

# Usage
@pytest.mark.unit
def test_pure_function() -> None:
    pass

@pytest.mark.integration
def test_database() -> None:
    pass

# Run specific: pytest -m unit
```

---

# Performance Optimization

## Profiling

```python
import cProfile
import pstats
from functools import wraps
import time

# Profiling decorator
def profile(func: Callable[..., T]) -> Callable[..., T]:
    """Profile function execution."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()
        result = func(*args, **kwargs)
        profiler.disable()

        stats = pstats.Stats(profiler)
        stats.sort_stats(pstats.SortKey.TIME)
        stats.print_stats(20)
        return result
    return wrapper


# Timing decorator
def timed(func: Callable[..., T]) -> Callable[..., T]:
    """Time function execution."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper


# Memory profiling
import tracemalloc

def trace_memory(func: Callable[..., T]) -> Callable[..., T]:
    """Trace memory usage."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        result = func(*args, **kwargs)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print(f"Peak memory: {peak / 1024 / 1024:.2f} MB")
        return result
    return wrapper
```

## Optimization Techniques

```python
# Use __slots__ for memory efficiency
class User:
    """User with slots (no __dict__)."""
    __slots__ = ("id", "name", "email")

    def __init__(self, id: int, name: str, email: str) -> None:
        self.id = id
        self.name = name
        self.email = email


# LRU cache for memoization
from functools import lru_cache

@lru_cache(maxsize=1024)
def fibonacci(n: int) -> int:
    """Cached fibonacci calculation."""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


# Generator for memory efficiency
def process_large_file(filepath: str) -> Iterator[dict]:
    """Process file line by line."""
    with open(filepath) as f:
        for line in f:
            yield json.loads(line)


# List comprehension vs map/filter
# Good: Readable list comprehension
squares = [x ** 2 for x in range(1000) if x % 2 == 0]

# Use generator expression when possible
sum_squares = sum(x ** 2 for x in range(1000) if x % 2 == 0)


# String concatenation
# Bad: Creates many strings
result = ""
for item in items:
    result += str(item)

# Good: Uses join
result = "".join(str(item) for item in items)


# Use built-in functions (C-optimized)
# Bad: Manual implementation
def manual_sum(numbers: list[int]) -> int:
    total = 0
    for n in numbers:
        total += n
    return total

# Good: Built-in
total = sum(numbers)


# Use locals() for tight loops (micro-optimization)
def fast_function(data: list[int]) -> int:
    """Optimized tight loop."""
    append = list.append  # Local lookup
    result = []
    for x in data:
        if x > 0:
            append(result, x)
    return len(result)
```

---

# Package Structure

## Modern Project Layout

```
myproject/
├── pyproject.toml           # Modern project config
├── README.md
├── .python-version          # Python version
├── .gitignore
├── src/
│   └── myproject/
│       ├── __init__.py
│       ├── main.py
│       ├── cli.py
│       ├── config.py
│       ├── models/
│       │   ├── __init__.py
│       │   ├── user.py
│       │   └── base.py
│       ├── services/
│       │   ├── __init__.py
│       │   └── auth.py
│       ├── api/
│       │   ├── __init__.py
│       │   └── routes.py
│       └── utils/
│           ├── __init__.py
│           └── helpers.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── unit/
│   └── integration/
└── scripts/
    └── migrate.py
```

## pyproject.toml

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "myproject"
version = "0.1.0"
description = "My awesome project"
readme = "README.md"
requires-python = ">=3.11"
license = { text = "MIT" }
authors = [
    { name = "Your Name", email = "you@example.com" }
]

dependencies = [
    "pydantic>=2.0",
    "httpx>=0.24",
    "sqlalchemy>=2.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-asyncio>=0.21",
    "pytest-cov>=4.0",
    "ruff>=0.1",
    "mypy>=1.5",
    "pre-commit>=3.0",
]

[project.scripts]
myproject = "myproject.cli:main"

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "B"]
ignore = ["E501"]

[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_ignores = true

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
```

---

# World-Class Resources

## Official Resources

- **Python Documentation**: https://docs.python.org/3/
- **PEP Index**: https://peps.python.org/ - Enhancement proposals
- **typing module**: https://docs.python.org/3/library/typing.html
- **asyncio docs**: https://docs.python.org/3/library/asyncio.html

## Frameworks & Libraries

- **FastAPI**: https://fastapi.tiangolo.com/ - Modern async web framework
- **Pydantic**: https://docs.pydantic.dev/ - Data validation
- **SQLAlchemy**: https://docs.sqlalchemy.org/ - ORM
- **Click**: https://click.palletsprojects.com/ - CLI framework
- **Typer**: https://typer.tiangolo.com/ - Modern CLI framework

## Tools

- **Ruff**: https://docs.astral.sh/ruff/ - Fast Python linter
- **mypy**: https://mypy.readthedocs.io/ - Static type checker
- **pytest**: https://docs.pytest.org/ - Testing framework
- **black**: https://black.readthedocs.io/ - Code formatter
- **isort**: https://pycqa.github.io/isort/ - Import organizer
- **pre-commit**: https://pre-commit.com/ - Git hooks

## Learning

- **Real Python**: https://realpython.com/ - Tutorials
- **Python Morsels**: https://www.pythonmorsels.com/ - Weekly exercises
- **Excellent Python**: https://github.com/luxemi/Excellent-Python - Best practices
- **The Hitchhiker's Guide to Python**: https://docs.python-guide.org/

## Books

- "Fluent Python" by Luciano Ramalho
- "Python Cookbook" by David Beazley & Brian K. Jones
- "Architecture Patterns with Python" by Harry Percival & Bob Gregory
- "Effective Python" by Brett Slatkin
