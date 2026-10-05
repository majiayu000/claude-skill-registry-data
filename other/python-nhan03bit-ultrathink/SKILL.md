---
name: python
description: Python best practices, type hints, async programming, packaging, virtual environments, and production patterns
layer: domain
category: backend
triggers:
  - "python"
  - "pip"
  - "poetry"
  - "asyncio"
  - "type hints"
  - "pydantic"
  - "python packaging"
inputs:
  - "Python application requirements"
  - "Type safety requirements"
  - "Async architecture needs"
outputs:
  - "Type-safe Python implementations"
  - "Async patterns and architectures"
  - "Packaging and deployment configurations"
linksTo:
  - fastapi
  - django
  - message-queues
  - microservices
  - postgresql
  - mongodb
  - redis
linkedFrom:
  - error-handling
  - logging
  - testing
preferredNextSkills:
  - fastapi
  - django
  - postgresql
fallbackSkills:
  - nodejs
  - golang
riskLevel: low
memoryReadPolicy: selective
memoryWritePolicy: none
sideEffects: []
---

# Python Domain Skill

## Purpose

Provide expert guidance on modern Python (3.10+) development patterns including type hints, async/await, structured concurrency, packaging, and production-grade application architecture.

## Key Patterns

### 1. Type Hints and Protocols

Always use type hints. Prefer `Protocol` over inheritance for duck typing.

```python
from typing import Protocol, runtime_checkable
from collections.abc import Sequence, Mapping, AsyncIterator

# Structural subtyping with Protocol
@runtime_checkable
class Repository(Protocol):
    async def get(self, id: str) -> dict | None: ...
    async def save(self, entity: dict) -> str: ...
    async def delete(self, id: str) -> bool: ...

# Use generics for reusable types
from typing import TypeVar, Generic

T = TypeVar("T")

class PaginatedResult(Generic[T]):
    def __init__(self, items: list[T], total: int, page: int, per_page: int) -> None:
        self.items = items
        self.total = total
        self.page = page
        self.per_page = per_page
        self.pages = (total + per_page - 1) // per_page

    @property
    def has_next(self) -> bool:
        return self.page < self.pages

# Modern union syntax (3.10+)
def process(value: str | int | None) -> str:
    match value:
        case str():
            return value.upper()
        case int():
            return str(value)
        case None:
            return ""

# TypeGuard for type narrowing
from typing import TypeGuard

def is_string_list(val: list[object]) -> TypeGuard[list[str]]:
    return all(isinstance(x, str) for x in val)
```

### 2. Async/Await and Structured Concurrency

```python
import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator

# TaskGroup for structured concurrency (Python 3.11+)
async def fetch_all_data(urls: list[str]) -> list[dict]:
    results: list[dict] = []

    async with asyncio.TaskGroup() as tg:
        for url in urls:
            tg.create_task(fetch_and_append(url, results))

    return results

# Async context managers
@asynccontextmanager
async def managed_connection(dsn: str) -> AsyncGenerator[Connection, None]:
    conn = await create_connection(dsn)
    try:
        yield conn
    finally:
        await conn.close()

# Async generators
async def stream_records(query: str) -> AsyncGenerator[dict, None]:
    async with managed_connection(DATABASE_URL) as conn:
        async for row in conn.execute_stream(query):
            yield dict(row)

# Semaphore for rate limiting
async def fetch_with_limit(urls: list[str], max_concurrent: int = 10) -> list[str]:
    semaphore = asyncio.Semaphore(max_concurrent)

    async def _fetch(url: str) -> str:
        async with semaphore:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    return await resp.text()

    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(_fetch(url)) for url in urls]

    return [t.result() for t in tasks]
```

### 3. Dataclasses and Pydantic Models

```python
from dataclasses import dataclass, field
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, model_validator

# Frozen dataclasses for value objects
@dataclass(frozen=True, slots=True)
class Money:
    amount: int  # Store in cents
    currency: str = "USD"

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError(f"Cannot add {self.currency} and {other.currency}")
        return Money(self.amount + other.amount, self.currency)

    def display(self) -> str:
        return f"${self.amount / 100:.2f} {self.currency}"

# Pydantic for validation and serialization
class CreateUserRequest(BaseModel):
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., ge=13, le=150)
    tags: list[str] = Field(default_factory=list, max_length=10)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.lower().strip()

    @model_validator(mode="after")
    def validate_model(self) -> "CreateUserRequest":
        if "admin" in self.tags and self.age < 18:
            raise ValueError("Admin users must be 18+")
        return self

    model_config = {"str_strip_whitespace": True}
```

### 4. Error Handling

```python
from typing import TypeVar, Generic
from dataclasses import dataclass

T = TypeVar("T")
E = TypeVar("E", bound=Exception)

# Result type for explicit error handling
@dataclass(frozen=True)
class Ok(Generic[T]):
    value: T

@dataclass(frozen=True)
class Err(Generic[E]):
    error: E

type Result[T, E] = Ok[T] | Err[E]  # Python 3.12+ type alias

# Custom exception hierarchy
class AppError(Exception):
    """Base application error."""
    def __init__(self, message: str, code: str, status: int = 500) -> None:
        super().__init__(message)
        self.code = code
        self.status = status

class NotFoundError(AppError):
    def __init__(self, resource: str, id: str) -> None:
        super().__init__(
            message=f"{resource} with id '{id}' not found",
            code="NOT_FOUND",
            status=404
        )

class ValidationError(AppError):
    def __init__(self, field: str, reason: str) -> None:
        super().__init__(
            message=f"Validation failed for '{field}': {reason}",
            code="VALIDATION_ERROR",
            status=422
        )

# Context managers for resource cleanup
from contextlib import contextmanager

@contextmanager
def transaction(session):
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
```

### 5. Project Structure and Packaging

```
myproject/
├── pyproject.toml          # Single source of truth for config
├── src/
│   └── myproject/
│       ├── __init__.py
│       ├── py.typed         # PEP 561 marker
│       ├── domain/
│       │   ├── __init__.py
│       │   ├── models.py
│       │   └── services.py
│       ├── infra/
│       │   ├── __init__.py
│       │   ├── database.py
│       │   └── cache.py
│       └── api/
│           ├── __init__.py
│           ├── routes.py
│           └── middleware.py
├── tests/
│   ├── conftest.py
│   ├── unit/
│   └── integration/
└── .python-version
```

```toml
# pyproject.toml
[project]
name = "myproject"
version = "1.0.0"
requires-python = ">=3.11"
dependencies = [
    "pydantic>=2.0",
    "httpx>=0.25",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.23",
    "mypy>=1.8",
    "ruff>=0.2",
]

[tool.ruff]
target-version = "py311"
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I", "N", "UP", "B", "A", "SIM", "TCH"]

[tool.mypy]
strict = true
python_version = "3.11"

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

## Best Practices

1. **Always use `src/` layout** for packages to avoid import confusion
2. **Run `mypy --strict`** in CI -- type coverage is not optional
3. **Use `ruff`** for linting and formatting (replaces flake8, isort, black)
4. **Prefer `httpx`** over `requests` for async HTTP clients
5. **Use `slots=True`** on dataclasses for memory efficiency
6. **Use `match/case`** (3.10+) instead of long if/elif chains
7. **Prefer `pathlib.Path`** over `os.path` for file operations
8. **Use `logging.getLogger(__name__)`** -- never configure root logger in libraries
9. **Favor composition** over inheritance -- use protocols and dependency injection
10. **Use `functools.cache`** or `functools.lru_cache` for expensive pure functions

## Common Pitfalls

| Pitfall | Impact | Fix |
|---------|--------|-----|
| Mutable default arguments (`def f(x=[])`) | Shared state between calls | Use `None` default, assign inside function |
| Late binding closures in loops | All closures capture final value | Use default argument: `lambda x=x: x` |
| Blocking calls inside async functions | Event loop stalls | Use `asyncio.to_thread()` for blocking I/O |
| Bare `except:` clauses | Catches `SystemExit`, `KeyboardInterrupt` | Use `except Exception:` at minimum |
| Not using `__all__` in `__init__.py` | Uncontrolled public API | Define `__all__` in every public module |
| Ignoring `ResourceWarning` | File handle leaks | Always use `with` / context managers |
| Global mutable state | Testing nightmares, race conditions | Use dependency injection |

## Performance Tips

- Use `__slots__` on frequently instantiated classes
- Use `collections.deque` instead of `list` for queue operations
- Use `array.array` for homogeneous numeric data
- Profile with `cProfile` and `line_profiler` before optimizing
- Use `uvloop` for async applications (2-4x faster event loop)
- Consider `orjson` or `msgspec` for fast JSON serialization
