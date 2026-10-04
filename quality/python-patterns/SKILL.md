---
name: python-patterns
description: Provides idiomatic modern Python (3.11+) patterns covering type hints, dataclasses and pydantic at boundaries, pathlib, context managers, generators, async basics, explicit error handling, and a uv/ruff/pytest project layout. Use when writing, reviewing, or refactoring Python code or setting up a Python project.
---

# Python Patterns

Readable, explicit, typed. These patterns target Python 3.11 or newer with `uv` for
environments, `ruff` for lint and format, and `pytest` for tests.

## When to use

- Writing new Python modules, packages, scripts, or services.
- Reviewing Python diffs for idiom, typing, and error handling.
- Setting up or modernising a Python project's tooling.

## Core principles

- **Readability over cleverness.** Names say what things hold; comprehension over a three-line loop, a function over a three-clause comprehension.
- **Explicit over implicit.** No import-time side effects, no hidden global configuration.
- **EAFP where the exception is the normal control flow** (`try: d[key] except KeyError`), LBYL where a check is cheaper and clearer (`if path.exists()` before a destructive operation).
- **Immutability by default.** Frozen dataclasses, tuples, and new objects returned from functions; mutate in place only when the API is designed for it.

## Typing

Annotate every function signature. Use built-in generics and the union operator.

```python
from collections.abc import Iterable, Iterator, Callable, Sequence
from typing import Protocol, TypeVar, TypeAlias, Self

def first(items: Sequence[T]) -> T | None:
    return items[0] if items else None

JSON: TypeAlias = dict[str, "JSON"] | list["JSON"] | str | int | float | bool | None

class Renderable(Protocol):
    def render(self) -> str: ...

def render_all(items: Iterable[Renderable]) -> str:
    return "\n".join(item.render() for item in items)
```

- Prefer `collections.abc` types (`Iterable`, `Mapping`, `Sequence`) for parameters and concrete types (`list`, `dict`) for return values.
- `Protocol` for structural typing instead of abstract base classes when callers just need a shape.
- `Self` for fluent methods; `Literal[...]` for closed string sets; `TypedDict` for dict-shaped external payloads you do not control.
- Run `pyright` or `mypy --strict` in CI. Untyped third-party libraries get a `py.typed` stub or a narrow `cast` at the import boundary, not `Any` spreading through the codebase.

## Data at the boundaries

Two tools, two jobs:

- **`dataclass`** for internal data you construct yourself. Frozen unless mutation is the point; `slots=True` when you create many.
- **`pydantic.BaseModel`** at system boundaries: request bodies, config files, API responses, message payloads. It validates and coerces once, on the way in, then the rest of the code trusts the types.

```python
from dataclasses import dataclass, field
from datetime import datetime, UTC
from pydantic import BaseModel, Field, field_validator

@dataclass(frozen=True, slots=True)
class Money:
    amount_minor: int
    currency: str

    def add(self, other: "Money") -> "Money":
        if other.currency != self.currency:
            raise ValueError(f"currency mismatch: {self.currency} vs {other.currency}")
        return Money(self.amount_minor + other.amount_minor, self.currency)

class CreateOrder(BaseModel):
    customer_id: str = Field(min_length=1)
    items: list[str] = Field(min_length=1)
    note: str | None = None

    @field_validator("items")
    @classmethod
    def no_duplicates(cls, items: list[str]) -> list[str]:
        if len(set(items)) != len(items):
            raise ValueError("duplicate items")
        return items

class Settings(BaseModel):
    database_url: str
    log_level: str = "INFO"
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
```

Parse external input into a model at the edge (`CreateOrder.model_validate(payload)`); raise a
clear error there. Never pass raw `dict[str, Any]` deeper than the boundary. `NamedTuple` remains
fine for tiny immutable records like coordinates.

## Paths and files

`pathlib` everywhere; `os.path` string juggling is legacy.

```python
from pathlib import Path

CONFIG_DIR = Path.home() / ".myapp"

def load_config(path: Path = CONFIG_DIR / "config.toml") -> Settings:
    if not path.is_file():
        raise ConfigError(f"config not found: {path}")
    return Settings.model_validate(tomllib.loads(path.read_text(encoding="utf-8")))

for source in Path("data").glob("*.csv"):
    target = source.with_suffix(".parquet")
```

Always pass `encoding="utf-8"` when reading or writing text. Use `Path.resolve()` and check
`is_relative_to()` before writing to a path derived from user input.

## Context managers

Anything that acquires must release, and `with` is how Python says so.

```python
from contextlib import contextmanager
import time

@contextmanager
def timed(label: str) -> Iterator[None]:
    start = time.perf_counter()
    try:
        yield
    finally:
        logger.info("%s took %.3fs", label, time.perf_counter() - start)

class Transaction:
    def __init__(self, conn: Connection) -> None:
        self._conn = conn

    def __enter__(self) -> Self:
        self._conn.begin()
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        if exc_type is None:
            self._conn.commit()
        else:
            self._conn.rollback()
        return False  # never swallow the exception
```

Use `contextlib.ExitStack` when the number of resources is dynamic. Return `False` from `__exit__`
unless suppressing is the whole point.

## Iteration and generators

```python
# Generator: lazy, constant memory
def read_records(path: Path) -> Iterator[Record]:
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            yield Record.parse(line.rstrip("\n"))

total = sum(r.amount for r in read_records(path))       # generator expression, no list

# Comprehension for simple transforms; a named function once it needs two conditions
active_emails = [u.email for u in users if u.is_active]
```

Use `enumerate`, `zip(strict=True)`, `itertools` (`batched`, `groupby`, `chain`) before writing
index arithmetic. Build strings with `"".join(parts)` or an f-string, never `+=` in a loop.

## Async basics

Use `asyncio` for I/O-bound concurrency (HTTP, sockets, database drivers with async support).
Use a thread pool for blocking libraries you cannot change. Use processes for CPU-bound work.

```python
import asyncio
import httpx

async def fetch_json(client: httpx.AsyncClient, url: str) -> JSON:
    response = await client.get(url, timeout=10.0)
    response.raise_for_status()
    return response.json()

async def fetch_all(urls: list[str]) -> list[JSON | BaseException]:
    async with httpx.AsyncClient() as client:
        async with asyncio.TaskGroup() as group:
            tasks = [group.create_task(fetch_json(client, url)) for url in urls]
    return [task.result() for task in tasks]

# Blocking call inside async code
data = await asyncio.to_thread(legacy_blocking_read, path)
```

Rules: never call blocking I/O or `time.sleep` inside a coroutine; bound concurrency with
`asyncio.Semaphore` when fanning out to an external service; prefer `TaskGroup` (3.11+) over
bare `gather` so failures cancel siblings and propagate as an `ExceptionGroup`; pass timeouts explicitly.

## Error handling

- Catch specific exceptions. A bare `except:` or `except Exception: pass` is a bug.
- Chain with `raise ... from e` so the original traceback survives.
- Define a small hierarchy rooted at one application exception; callers catch the root when they
  want "anything ours", the leaf when they can act on it.
- Log with `logger.exception(...)` at the level that handles the error, once. Do not log and re-raise
  at every layer.
- User-facing messages are friendly; logs carry full context.

```python
class AppError(Exception):
    """Base for all errors raised by this application."""

class ConfigError(AppError): ...
class NotFoundError(AppError): ...

def load_user(user_id: str) -> User:
    try:
        row = repo.get(user_id)
    except RepositoryError as e:
        raise AppError(f"could not load user {user_id}") from e
    if row is None:
        raise NotFoundError(f"user not found: {user_id}")
    return User.model_validate(row)
```

## Logging and configuration

- `logging.getLogger(__name__)` per module; configure handlers once at the entry point.
- Lazy formatting: `logger.info("user %s logged in", user_id)`, not an f-string, so the string
  is built only when the level is enabled.
- Configuration comes from environment variables or a file, validated into a `Settings` model at
  startup. Missing required settings fail fast with a clear message. No secrets in source.

## Project layout with uv, ruff, pytest

```
myproject/
  pyproject.toml
  uv.lock
  README.md
  src/
    mypackage/
      __init__.py
      __main__.py          # python -m mypackage
      config.py
      orders/              # organise by feature, not by layer
        __init__.py
        models.py
        service.py
        repository.py
  tests/
    conftest.py
    orders/
      test_service.py
```

```toml
[project]
name = "mypackage"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = ["pydantic>=2", "httpx>=0.27"]

[dependency-groups]
dev = ["pytest>=8", "pytest-cov", "pytest-asyncio", "ruff", "pyright"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "UP", "B", "SIM", "PTH", "RUF"]

[tool.pyright]
strict = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-q --strict-markers"
asyncio_mode = "auto"
```

Everyday commands:

```bash
uv sync                          # create .venv and install locked deps
uv add httpx                     # add a dependency and update the lock
uv add --group dev pytest-cov    # dev dependency
uv run pytest                    # run tests in the project env
uv run ruff check . --fix && uv run ruff format .
uv run pyright
uv run python -m mypackage
```

The `src/` layout guarantees tests import the installed package, not the working directory.
Ruff replaces black, isort, flake8, and pyupgrade; do not run them alongside it.

## Testing conventions

- One test module per source module, mirrored under `tests/`.
- Fixtures in `conftest.py`; prefer small factory functions over deep fixture graphs.
- `pytest.raises` with `match=` for error paths. `tmp_path` for filesystem tests. `monkeypatch`
  for environment variables.
- Parametrize instead of copy-pasting near-identical tests.
- Mock at boundaries (HTTP, clock, database) using `respx`, `freezegun`, or a fake repository
  class; do not mock your own modules.

## Anti-patterns

```python
def add(item, items=[]): ...                 # mutable default; use None and create inside
if type(obj) == list: ...                    # use isinstance
if value == None: ...                        # use `is None`
from os.path import *                        # explicit imports only
except: pass                                 # catch specific, handle or re-raise
print(f"debug {x}")                          # use logging; no print in library code
open(path).read()                            # no context manager, no encoding
results = []; for x in xs: results.append(f(x))   # [f(x) for x in xs]
```

## Review checklist

- [ ] Every public function is annotated; `Any` appears only at a justified boundary.
- [ ] External input is validated into a model at the edge.
- [ ] Files, sockets, locks, and transactions are opened with `with`.
- [ ] No bare `except`; exceptions are chained; errors are logged once.
- [ ] `pathlib` and `encoding="utf-8"` for all file access.
- [ ] Async code has no blocking calls and bounds its concurrency.
- [ ] `ruff check`, `ruff format --check`, `pyright`, and `pytest` all pass.

## Related skills

- `opm:tdd-workflow` - pytest RED/GREEN cycle with `uv run pytest`.
- `opm:verification-loop` - the uv/ruff/pytest gate sequence.

<!-- Adapted from affaan-m/ecc (MIT) -->
