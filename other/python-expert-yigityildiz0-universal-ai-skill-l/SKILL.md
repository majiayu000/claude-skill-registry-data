---
name: python-expert
description: Deep Python expertise for production systems. Use when writing Python code, implementing async patterns, designing class hierarchies, handling exceptions.
---

# Python Expert

Specialized expertise in Python programming, providing deep guidance on type annotations and static analysis, exception handling idioms, async/await concurrency, data modeling with dataclasses and Pydantic, testing with pytest, performance optimization, and modern packaging with pyproject.toml.

## When to Use This Skill

Use this skill for:

- Adding type annotations and configuring mypy strict mode
- Designing custom exception hierarchies and error chains
- Implementing async/await patterns with asyncio
- Modeling data with dataclasses and Pydantic
- Writing pytest test suites with fixtures and parametrize
- Profiling and optimizing Python performance
- Setting up Python project structure and packaging

**Trigger phrases**: "python", "asyncio", "pydantic", "pytest", "mypy", "type hints", "dataclass", "python packaging", "python performance"

## What This Skill Does

Provides Python expertise including:

- **Type System**: Annotations, generics, protocols, mypy strict
- **Error Handling**: Custom exceptions, error chains, context managers
- **Async/Await**: asyncio event loop, task groups, async generators
- **Data Modeling**: dataclasses, Pydantic BaseModel, validation
- **Testing**: pytest fixtures, parametrize, monkeypatch, coverage
- **Performance**: Profiling, generators, slots, caching, comprehensions
- **Packaging**: pyproject.toml, src layout, virtual environments

## Instructions

### Step 1: Master Type Annotations and mypy-Strict Patterns

**Enable Postponed Evaluation and Modern Syntax**:

```python
from __future__ import annotations

from typing import TypeVar, Generic, Protocol

# X | Y union syntax (works at runtime with __future__ annotations)
def fetch_user(user_id: int) -> User | None:
    """Return user or None if not found."""
    row = db.query("SELECT * FROM users WHERE id = %s", (user_id,))
    if row is None:
        return None
    return User.from_row(row)

# Avoid Optional[X] and Union[X, Y] in new code
# Bad:  Optional[str]
# Good: str | None
def parse_header(raw: str) -> str | None:
    parts = raw.split(":", maxsplit=1)
    return parts[1].strip() if len(parts) == 2 else None
```

**TypeVar and Generic Containers**:

```python
from typing import TypeVar, Generic

T = TypeVar("T")

class Stack(Generic[T]):
    """Type-safe generic stack."""

    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self) -> T:
        if not self._items:
            raise IndexError("peek at empty stack")
        return self._items[-1]

    def __len__(self) -> int:
        return len(self._items)

# Usage: mypy enforces type consistency
stack: Stack[int] = Stack()
stack.push(42)
stack.push("oops")  # mypy error: Argument 1 has incompatible type "str"
```

**Protocol for Structural Subtyping**:

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Serializable(Protocol):
    def to_dict(self) -> dict[str, object]: ...

class User:
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    def to_dict(self) -> dict[str, object]:
        return {"name": self.name, "age": self.age}

# User satisfies Serializable without inheriting from it
def serialize(obj: Serializable) -> str:
    import json
    return json.dumps(obj.to_dict())

# Runtime check also works
assert isinstance(User("Alice", 30), Serializable)
```

**mypy Strict Configuration** (pyproject.toml):

```toml
[tool.mypy]
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_any_generics = true
check_untyped_defs = true
```

### Step 2: Handle Exceptions Idiomatically

**Custom Exception Hierarchy**:

```python
class AppError(Exception):
    """Base exception for the application."""

    def __init__(self, message: str, code: str = "UNKNOWN") -> None:
        super().__init__(message)
        self.code = code

class NotFoundError(AppError):
    """Raised when a resource is not found."""

    def __init__(self, resource: str, identifier: object) -> None:
        super().__init__(
            f"{resource} with id {identifier!r} not found",
            code="NOT_FOUND",
        )
        self.resource = resource
        self.identifier = identifier

class ValidationError(AppError):
    """Raised when input validation fails."""

    def __init__(self, field: str, reason: str) -> None:
        super().__init__(
            f"Validation failed for {field!r}: {reason}",
            code="VALIDATION_ERROR",
        )
        self.field = field
        self.reason = reason
```

**Error Chaining with raise-from**:

```python
import logging

logger = logging.getLogger(__name__)

def load_config(path: str) -> dict[str, object]:
    try:
        with open(path) as f:
            import json
            return json.load(f)
    except FileNotFoundError as exc:
        raise AppError(f"Config file missing: {path}") from exc
    except json.JSONDecodeError as exc:
        raise AppError(f"Invalid JSON in {path}: line {exc.lineno}") from exc

# The original exception is preserved in __cause__
# Tracebacks show: "The above exception was the direct cause of..."
```

**Context Managers for Resource Cleanup**:

```python
from contextlib import contextmanager
from typing import Iterator

@contextmanager
def temporary_directory(prefix: str = "tmp") -> Iterator[str]:
    """Create a temp directory and clean it up on exit."""
    import tempfile
    import shutil

    path = tempfile.mkdtemp(prefix=prefix)
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)

# Usage
with temporary_directory("build_") as build_dir:
    compile_assets(build_dir)
    # Directory is cleaned up even if an exception occurs

# Class-based context manager for database transactions
class Transaction:
    def __init__(self, conn: Connection) -> None:
        self._conn = conn

    def __enter__(self) -> Transaction:
        self._conn.begin()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object,
    ) -> bool:
        if exc_type is not None:
            self._conn.rollback()
            logger.error("Transaction rolled back: %s", exc_val)
            return False  # Re-raise the exception
        self._conn.commit()
        return False
```

### Step 3: Implement Async/Await Patterns

**Basic asyncio Patterns**:

```python
import asyncio

async def fetch_url(session: aiohttp.ClientSession, url: str) -> str:
    """Fetch a single URL with timeout."""
    async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as resp:
        resp.raise_for_status()
        return await resp.text()

async def fetch_all(urls: list[str]) -> list[str]:
    """Fetch multiple URLs concurrently."""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        return await asyncio.gather(*tasks, return_exceptions=False)

# Entry point
async def main() -> None:
    urls = [
        "https://api.example.com/users",
        "https://api.example.com/orders",
        "https://api.example.com/products",
    ]
    results = await fetch_all(urls)
    for url, body in zip(urls, results):
        print(f"{url}: {len(body)} bytes")

asyncio.run(main())
```

**Task Groups (Python 3.11+)**:

```python
async def process_batch(items: list[Item]) -> list[Result]:
    """Process items concurrently with structured cancellation."""
    results: list[Result] = []

    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(process_item(item)) for item in items]

    # All tasks completed successfully if we reach here.
    # If any task raises, the group cancels all remaining tasks
    # and raises an ExceptionGroup.
    results = [task.result() for task in tasks]
    return results
```

**Async Context Managers and Generators**:

```python
from contextlib import asynccontextmanager
from typing import AsyncIterator

@asynccontextmanager
async def managed_connection(dsn: str) -> AsyncIterator[Connection]:
    """Acquire a database connection and release it on exit."""
    conn = await asyncpg.connect(dsn)
    try:
        yield conn
    finally:
        await conn.close()

# Async generator for streaming results
async def stream_rows(query: str) -> AsyncIterator[dict[str, object]]:
    """Yield rows one at a time without loading all into memory."""
    async with managed_connection(DATABASE_URL) as conn:
        async with conn.transaction():
            async for record in conn.cursor(query):
                yield dict(record)

# Consuming an async generator
async def export_csv(query: str, path: str) -> int:
    count = 0
    with open(path, "w") as f:
        async for row in stream_rows(query):
            f.write(",".join(str(v) for v in row.values()) + "\n")
            count += 1
    return count
```

**Semaphore for Rate Limiting**:

```python
async def fetch_with_limit(
    urls: list[str],
    max_concurrent: int = 10,
) -> list[str]:
    """Fetch URLs with a concurrency limit."""
    semaphore = asyncio.Semaphore(max_concurrent)

    async def limited_fetch(session: aiohttp.ClientSession, url: str) -> str:
        async with semaphore:
            return await fetch_url(session, url)

    async with aiohttp.ClientSession() as session:
        tasks = [limited_fetch(session, url) for url in urls]
        return await asyncio.gather(*tasks)
```

### Step 4: Model Data with Dataclasses and Pydantic

**Dataclass Fundamentals**:

```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass(frozen=True)
class Money:
    """Immutable value object for monetary amounts."""
    amount: int  # Store as cents to avoid float issues
    currency: str = "USD"

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValueError("Amount cannot be negative")

    def __add__(self, other: Money) -> Money:
        if self.currency != other.currency:
            raise ValueError(f"Cannot add {self.currency} and {other.currency}")
        return Money(self.amount + other.amount, self.currency)

@dataclass
class Order:
    """Mutable entity with computed defaults."""
    customer_id: int
    items: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    total: Money = field(default_factory=lambda: Money(0))

    def add_item(self, name: str, price: Money) -> None:
        self.items.append(name)
        self.total = self.total + price
```

**Dataclass with Slots (Python 3.10+)**:

```python
@dataclass(slots=True)
class Point:
    """Memory-efficient dataclass using __slots__."""
    x: float
    y: float
    z: float = 0.0

    def distance_to(self, other: Point) -> float:
        return (
            (self.x - other.x) ** 2
            + (self.y - other.y) ** 2
            + (self.z - other.z) ** 2
        ) ** 0.5
```

**Pydantic BaseModel for Validation and Serialization**:

```python
from pydantic import BaseModel, Field, field_validator, model_validator

class CreateUserRequest(BaseModel):
    """Validated API request model."""
    username: str = Field(min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_]+$")
    email: str = Field(max_length=255)
    age: int = Field(ge=13, le=150)
    tags: list[str] = Field(default_factory=list, max_length=10)

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("Invalid email address")
        return v.lower()

    @model_validator(mode="after")
    def check_consistency(self) -> CreateUserRequest:
        if self.age < 18 and "admin" in self.tags:
            raise ValueError("Users under 18 cannot be admins")
        return self

# Parse and validate from dict (e.g., request.json())
user = CreateUserRequest.model_validate({"username": "alice", "email": "ALICE@example.com", "age": 25})
print(user.email)  # alice@example.com (lowercased by validator)

# Serialize to dict or JSON
user.model_dump()
user.model_dump_json()
```

**Pydantic Settings for Configuration**:

```python
from pydantic_settings import BaseSettings

class AppSettings(BaseSettings):
    """Load settings from environment variables."""
    database_url: str
    redis_url: str = "redis://localhost:6379"
    debug: bool = False
    max_connections: int = 10

    model_config = {"env_prefix": "APP_"}

# Reads APP_DATABASE_URL, APP_REDIS_URL, etc. from environment
settings = AppSettings()
```

### Step 5: Write Thorough Tests with pytest

**Basic Test Structure and Parametrize**:

```python
import pytest
from myapp.calculator import add, divide

def test_add_positive_numbers() -> None:
    assert add(2, 3) == 5

def test_divide_by_zero_raises() -> None:
    with pytest.raises(ZeroDivisionError, match="division by zero"):
        divide(10, 0)

@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (2, 3, 5),
        (-1, -1, -2),
        (0, 0, 0),
        (-1, 1, 0),
        (100, 200, 300),
    ],
    ids=["positive", "negative", "zeros", "mixed", "large"],
)
def test_add_parametrized(a: int, b: int, expected: int) -> None:
    assert add(a, b) == expected
```

**Fixtures and conftest.py**:

```python
# conftest.py
import pytest
from myapp.database import Database

@pytest.fixture
def db(tmp_path: object) -> Database:
    """Create a fresh test database for each test."""
    db = Database(f"sqlite:///{tmp_path}/test.db")
    db.create_tables()
    yield db
    db.close()

@pytest.fixture
def sample_user(db: Database) -> User:
    """Insert and return a sample user."""
    return db.create_user(name="Alice", email="alice@example.com")

# test_users.py
def test_user_creation(db: Database) -> None:
    user = db.create_user(name="Bob", email="bob@example.com")
    assert user.name == "Bob"
    assert user.id is not None

def test_user_lookup(db: Database, sample_user: User) -> None:
    found = db.get_user(sample_user.id)
    assert found is not None
    assert found.email == "alice@example.com"
```

**Monkeypatch for Isolation**:

```python
def test_config_reads_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_DATABASE_URL", "sqlite:///test.db")
    monkeypatch.setenv("APP_DEBUG", "true")

    settings = AppSettings()
    assert settings.database_url == "sqlite:///test.db"
    assert settings.debug is True

def test_fetch_retries_on_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    call_count = 0

    def mock_get(url: str, timeout: int = 30) -> object:
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ConnectionError("network error")
        return MockResponse(status_code=200, body="ok")

    monkeypatch.setattr("myapp.client.requests.get", mock_get)

    result = fetch_with_retry("https://api.example.com/data")
    assert result == "ok"
    assert call_count == 3
```

**Async Test Support**:

```python
import pytest

@pytest.mark.asyncio
async def test_async_fetch() -> None:
    async with aiohttp.ClientSession() as session:
        result = await fetch_url(session, "https://httpbin.org/get")
        assert len(result) > 0

# pytest.ini or pyproject.toml:
# [tool.pytest.ini_options]
# asyncio_mode = "auto"
```

**Coverage Configuration** (pyproject.toml):

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--strict-markers -q"

[tool.coverage.run]
source = ["src"]
branch = true

[tool.coverage.report]
fail_under = 80
show_missing = true
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "if __name__",
]
```

### Step 6: Optimize Performance

**Profiling Before Optimizing**:

```python
import cProfile
import pstats

def profile_function(func, *args, **kwargs):
    """Profile a function and print the top 20 calls by cumulative time."""
    profiler = cProfile.Profile()
    profiler.enable()
    result = func(*args, **kwargs)
    profiler.disable()

    stats = pstats.Stats(profiler)
    stats.sort_stats("cumulative")
    stats.print_stats(20)
    return result

# Or use the decorator approach
# python -m cProfile -s cumulative myapp/main.py
```

**Generators for Memory Efficiency**:

```python
# Bad: loads everything into memory
def read_all_lines(path: str) -> list[str]:
    with open(path) as f:
        return f.readlines()  # Entire file in memory

# Good: yields one line at a time
def read_lines(path: str) -> Iterator[str]:
    with open(path) as f:
        for line in f:
            yield line.strip()

# Generator expression (lazy evaluation)
total = sum(len(line) for line in read_lines("large_file.txt"))

# itertools for composable lazy pipelines
import itertools

def process_large_dataset(path: str) -> Iterator[dict[str, str]]:
    lines = read_lines(path)
    non_empty = (line for line in lines if line)
    batches = itertools.batched(non_empty, 1000)  # Python 3.12+
    for batch in batches:
        yield from process_batch(batch)
```

**Slots for Memory-Efficient Classes**:

```python
class HeavyObject:
    """Default: uses __dict__ for attribute storage."""
    def __init__(self, x: int, y: int, z: int) -> None:
        self.x = x
        self.y = y
        self.z = z

class LightObject:
    """Slots: fixed attribute set, ~40% less memory per instance."""
    __slots__ = ("x", "y", "z")

    def __init__(self, x: int, y: int, z: int) -> None:
        self.x = x
        self.y = y
        self.z = z

# Memory comparison (approximate):
# HeavyObject: ~152 bytes per instance
# LightObject: ~88 bytes per instance
```

**Caching with lru_cache and cache**:

```python
from functools import lru_cache, cache

@lru_cache(maxsize=256)
def fibonacci(n: int) -> int:
    """Memoized Fibonacci: O(n) instead of O(2^n)."""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Unbounded cache (Python 3.9+)
@cache
def expensive_lookup(key: str) -> dict[str, object]:
    return database.query(key)

# Cache with TTL using third-party library
from cachetools import TTLCache

api_cache: TTLCache[str, dict[str, object]] = TTLCache(maxsize=1000, ttl=300)
```

**Comprehensions Over Loops**:

```python
# List comprehension (faster than append loop)
squares = [x * x for x in range(1000)]

# Dict comprehension
index = {user.id: user for user in users}

# Set comprehension for deduplication
unique_domains = {email.split("@")[1] for email in emails}

# Conditional comprehension
active_users = [u for u in users if u.is_active and u.last_login is not None]

# Avoid nested comprehensions beyond 2 levels; use a function instead
# Bad:
matrix = [[row[i] for row in data] for i in range(cols)]
# Better:
def transpose(data: list[list[int]]) -> list[list[int]]:
    return [list(col) for col in zip(*data)]
```

### Step 7: Structure Projects and Packaging

**Modern pyproject.toml Configuration**:

```toml
[project]
name = "myapp"
version = "1.2.0"
description = "A production application"
requires-python = ">=3.11"
license = {text = "MIT"}
dependencies = [
    "pydantic>=2.0,<3.0",
    "httpx>=0.25",
    "asyncpg>=0.29",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-cov>=5.0",
    "pytest-asyncio>=0.23",
    "mypy>=1.8",
    "ruff>=0.3",
]

[project.scripts]
myapp = "myapp.cli:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "UP", "B", "SIM", "TCH"]
```

**src Layout (Recommended)**:

```
myapp/
  pyproject.toml
  src/
    myapp/
      __init__.py
      cli.py
      config.py
      models/
        __init__.py
        user.py
      services/
        __init__.py
        auth.py
      utils/
        __init__.py
        logging.py
  tests/
    unit/
      test_models.py
      test_services.py
    integration/
      test_database.py
    conftest.py
```

**Virtual Environment Management with uv**:

```bash
# Create virtual environment
uv venv

# Install project with dev dependencies
uv pip install -e ".[dev]"

# Add a new dependency
uv pip install httpx

# Sync from lock file (reproducible installs)
uv pip sync requirements.lock

# Generate lock file
uv pip compile pyproject.toml -o requirements.lock
```

**Package Entry Points and CLI**:

```python
# src/myapp/cli.py
from __future__ import annotations

import argparse
import sys

def main(argv: list[str] | None = None) -> int:
    """Application entry point."""
    parser = argparse.ArgumentParser(description="My Application")
    parser.add_argument("--config", default="config.toml", help="Config file path")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    subparsers = parser.add_subparsers(dest="command", required=True)

    serve_parser = subparsers.add_parser("serve", help="Start the server")
    serve_parser.add_argument("--port", type=int, default=8080)

    migrate_parser = subparsers.add_parser("migrate", help="Run database migrations")
    migrate_parser.add_argument("--dry-run", action="store_true")

    args = parser.parse_args(argv)

    if args.command == "serve":
        return run_server(args.port, args.config)
    elif args.command == "migrate":
        return run_migrations(args.config, dry_run=args.dry_run)

    return 0

if __name__ == "__main__":
    sys.exit(main())
```

## Best Practices

- **Type everything** - Run mypy strict in CI; zero type errors is the target
- **Raise specific exceptions** - Never raise bare Exception; define a project hierarchy
- **Use context managers** - For any resource that needs cleanup (files, connections, locks)
- **Prefer composition** - Inherit only from abstract base classes or Protocol
- **Immutable by default** - Use frozen dataclasses and tuples unless mutation is required
- **Profile first** - Measure before optimizing; use cProfile or py-spy
- **Test at boundaries** - Mock external services, not internal functions
- **Pin dependencies** - Exact versions in production; ranges only in library pyproject.toml

## Common Patterns

### Pattern 1: Repository Pattern with Protocol

```python
from __future__ import annotations

from typing import Protocol

class UserRepository(Protocol):
    def get(self, user_id: int) -> User | None: ...
    def save(self, user: User) -> User: ...
    def delete(self, user_id: int) -> bool: ...

class PostgresUserRepository:
    def __init__(self, conn: asyncpg.Connection) -> None:
        self._conn = conn

    async def get(self, user_id: int) -> User | None:
        row = await self._conn.fetchrow(
            "SELECT * FROM users WHERE id = $1", user_id
        )
        return User(**dict(row)) if row else None

    async def save(self, user: User) -> User:
        row = await self._conn.fetchrow(
            "INSERT INTO users (name, email) VALUES ($1, $2) RETURNING *",
            user.name,
            user.email,
        )
        return User(**dict(row))

    async def delete(self, user_id: int) -> bool:
        result = await self._conn.execute(
            "DELETE FROM users WHERE id = $1", user_id
        )
        return result == "DELETE 1"

class InMemoryUserRepository:
    """Test double that satisfies the same Protocol."""

    def __init__(self) -> None:
        self._store: dict[int, User] = {}
        self._next_id = 1

    def get(self, user_id: int) -> User | None:
        return self._store.get(user_id)

    def save(self, user: User) -> User:
        user.id = self._next_id
        self._store[self._next_id] = user
        self._next_id += 1
        return user

    def delete(self, user_id: int) -> bool:
        return self._store.pop(user_id, None) is not None
```

### Pattern 2: Retry with Exponential Backoff

```python
from __future__ import annotations

import asyncio
import logging
from typing import TypeVar

T = TypeVar("T")
logger = logging.getLogger(__name__)

async def retry(
    func,
    *args,
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
    retryable: tuple[type[Exception], ...] = (ConnectionError, TimeoutError),
) -> T:
    """Retry an async callable with exponential backoff."""
    last_exc: Exception | None = None

    for attempt in range(1, max_attempts + 1):
        try:
            return await func(*args)
        except retryable as exc:
            last_exc = exc
            if attempt == max_attempts:
                break
            delay = min(base_delay * (2 ** (attempt - 1)), max_delay)
            logger.warning(
                "Attempt %d/%d failed (%s), retrying in %.1fs",
                attempt,
                max_attempts,
                exc,
                delay,
            )
            await asyncio.sleep(delay)

    raise last_exc  # type: ignore[misc]

# Usage
result = await retry(fetch_url, session, url, max_attempts=5)
```

## Quality Checklist

- [ ] All functions have type annotations (parameters and return)
- [ ] mypy strict passes with zero errors
- [ ] Custom exceptions inherit from a project base class
- [ ] Context managers used for resource cleanup
- [ ] Async code uses TaskGroup or gather for concurrency
- [ ] Pydantic models validate all external input
- [ ] pytest coverage at or above 80%
- [ ] No mutable default arguments in function signatures
- [ ] ruff check and ruff format pass
- [ ] pyproject.toml defines all project metadata

## Related Skills

- `performance-testing` - Python profiling and benchmarks
- `cicd-architect` - Python CI/CD pipelines
- `code-quality` - Python code standards
- `api-designer` - FastAPI and async web services

---

**Version**: 1.0.0
**Last Updated**: March 2026
**Based on**: awesome-codex-subagents python-pro patterns

### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets are not met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
