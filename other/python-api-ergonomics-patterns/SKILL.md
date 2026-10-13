---
name: python-api-ergonomics-patterns
description: >
  Use this for the Python-specific realization of the api-ergonomics-audit
  checklist — `async with Client(...)` quickstart, named-only constructor args,
  exception class hierarchy with discoverable subclasses, doctest-runnable
  Examples blocks, type-hinted Protocol seams, `__aexit__` shutdown semantics,
  and pyproject.toml authoring conventions.
  Triggers: async with, AsyncClient, aclose, __aenter__, __aexit__, Examples:, doctest, raise from, py.typed, PEP 561, frozen dataclass.
version: 1.0.0
last-evolved-in-run: v0.6.0-rc.0-sanitization
status: stable
tags: [python, ergonomics, sdk, api-design, async]
---

# python-api-ergonomics-patterns (v1.0.0)

## Scope

Python realization of the 8-point checklist in shared-core `api-ergonomics-audit`. The audit defines what to check; this skill defines what "good" looks like in Python.

## 5-line quickstart

```python
async with motadatapysdk.Cache(addr="localhost:6379") as cache:
    await cache.set("k", "v")
    v = await cache.get("k")
    print(v)
```

`async with` is the canonical surface for resource-owning clients — entry constructs, exit cleans up. If the quickstart exceeds 5 lines, the Config has too many required fields or the constructor isn't keyword-only.

## Doctest-runnable Examples block

PEP 257 docstring with an `Examples:` section that is also a runnable doctest:

```python
async def get(self, key: str) -> str | None:
    """Fetch a value by key.

    Returns None if the key is absent.

    Examples:
        >>> async with Cache(addr="localhost:6379") as cache:
        ...     await cache.set("greeting", "hello")
        ...     value = await cache.get("greeting")
        ...     print(value)
        hello

        >>> async with Cache(addr="localhost:6379") as cache:
        ...     missing = await cache.get("absent")
        ...     print(missing)
        None
    """
```

Wire `pytest --doctest-modules` so doctests run with the suite. For I/O-bound calls, mark with `# doctest: +SKIP` and document why; prefer fakes over skip when the example is core to the API understanding.

## Exception class hierarchy

Every failure mode is a class extending the SDK's base exception:

```python
class MotadataError(Exception):
    """Base for all SDK exceptions."""

class NetworkError(MotadataError):
    """Transient network failure — caller may retry."""

class TimeoutError(NetworkError):
    """Operation deadline exceeded."""

class AuthError(MotadataError):
    """Authentication or authorization failure — caller must re-auth."""

class KeyNotFoundError(MotadataError):
    """Sentinel for missing key. Mirrors Go SDK's ErrNil semantics."""
```

Caller pattern:

```python
try:
    v = await cache.get("k")
except KeyNotFoundError:
    return cache_miss  # discriminated by type
except NetworkError:
    return retry_with_backoff(...)
```

The exception class set is semver-public — adding is minor, removing/renaming is major. Document the hierarchy in the package's `__init__.py` docstring.

## Constructor — keyword-only, frozen Config

```python
@dataclass(frozen=True, slots=True, kw_only=True)
class CacheConfig:
    addr: str
    pool_size: int = 10
    timeout: float = 30.0

class Cache:
    def __init__(self, *, config: CacheConfig | None = None, **overrides: Any) -> None:
        self._config = config or CacheConfig(**overrides)
        # ...
```

`*` after the first arg forces keyword-only — no `Cache("localhost:6379", 10, 30)` ambiguity. `frozen=True` prevents post-construction mutation. `slots=True` slashes memory.

## Async context manager protocol

```python
class Cache:
    async def __aenter__(self) -> Self:
        await self._connect()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        """Idempotent shutdown — safe to call multiple times."""
        if self._closed:
            return
        self._closed = True
        # ordered teardown: tasks → drain → sessions
        ...
```

`aclose()` (not `close()`) is the modern convention — it signals the async semantics. Idempotency via `_closed` flag is mandatory; async-leak-detection harnesses (the `asyncio-task-tracker` fixture, `tracemalloc` snapshot diffs, `threading.enumerate` gates) will flag tasks left running after teardown.

## Type-hinted Protocol seam

Public ports use `Protocol` (PEP 544), not ABC:

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Cache(Protocol):
    async def get(self, key: str) -> str | None: ...
    async def set(self, key: str, value: str, ttl: float = 0) -> None: ...
    async def aclose(self) -> None: ...
```

Consumers can inject any object that satisfies the Protocol — no inheritance required. `mypy --strict` checks signature parity at type-check time.

## Anti-patterns

**1. String-matching error discrimination.** `if "not found" in str(exc)` — fragile to message rewording. Fix: catch the specific exception class.

**2. Bare `__init__` with positional args + `**kwargs`.** `Client(host, port, **kw)` — type-checker can't help; arg order ambiguous. Fix: keyword-only with `*` separator, plus a typed Config dataclass.

**3. Missing `py.typed` marker.** SDK ships without `py.typed`; consumers don't get type-check coverage. Add `py.typed` (PEP 561) to the package root.

**4. Non-idempotent `aclose()`.** Second call raises `RuntimeError("already closed")`. Test suites and `__aexit__` chains both call it; idempotency is mandatory.

**5. `print` for logs.** Use stdlib `logging` with structured fields. Consumers configure handlers; SDK does not own the destination.

## Severity ladder

- **BLOCKER** — sync `__init__` doing I/O, missing `aclose()`, exception class with no base, panic-equivalent on documented input
- **HIGH** — missing doctest Examples, missing exception subclass for documented failure, quickstart >5 lines, missing `py.typed`
- **MEDIUM** — sibling inconsistency (`close()` vs `aclose()`, `seconds: int` vs `timeout: float`)
- **LOW** — docstring phrasing, parameter naming, module-doc thinness

## Cross-references

- shared-core `api-ergonomics-audit` — the 8-point checklist this realizes
- `python-sdk-config-pattern` — frozen dataclass Config + keyword-only constructor
- `python-doctest-patterns` — doctest format, `+SKIP` discipline, `--doctest-modules` wiring
- `python-exception-patterns` — exception hierarchy + `raise from` chaining
- `python-mypy-strict-typing` — strict typing posture, PEP 561 marker
- `python-client-shutdown-lifecycle` — `aclose()` ordering and idempotency rules
- `sdk-semver-governance` — ergonomics-driven API rewrite triggers semver bumps
