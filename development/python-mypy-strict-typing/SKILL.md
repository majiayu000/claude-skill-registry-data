---
name: python-mypy-strict-typing
description: >
  Use this when designing the signature of a new public Python function or
  class, reviewing code that uses bare dict / list / Optional / Union / Any,
  weighing a # type: ignore against fixing the underlying issue, or shipping
  a new package that consumers will type-check. Covers PEP 484 / 563 / 604 /
  655 / 673 / 695 syntax, full annotations on every public symbol, X | None
  and X | Y shorthand, parametrized collection types, Self for fluent
  builders and factories, Protocol (with @runtime_checkable) over ABC, the
  py.typed PEP 561 marker, assert isinstance over cast, scoped # type:
  ignore[code] with rationale, TypedDict + Required / NotRequired for kwargs,
  Generic[T] vs PEP 695 type-parameter syntax, @overload, Literal, Final, and
  avoiding Any in favor of object + narrowing.
  Triggers: mypy, --strict, type:, typing, Protocol, ABC, TypeVar, Optional, Union, Self, py.typed, TypedDict, cast, type: ignore, overload.
cross_language_ok: true
---

# python-mypy-strict-typing (v1.0.0)

## Rationale

`mypy --strict` is the Python pack's static-typing gate (`python.json:toolchain.vet`). Every line of public SDK code must type-check under strict mode. Strict mode is not optional polish — it catches the same class of bugs Go's `go vet` + interface-conformance assertions catch. SDK consumers running their own `mypy --strict` pull our `py.typed` marker and inherit our types; if our types are loose or wrong, every consumer pays for it.

This skill is cited by `code-reviewer-python` (PEP 484+), `documentation-agent-python` (signature-derived docstrings), `refactoring-agent-python` (type-aware refactors), `sdk-api-ergonomics-devil-python` (E-12 pyright friendliness), `sdk-convention-devil-python` (C-3 py.typed, C-6 type system), and `sdk-packaging-devil-python` (P-6 py.typed).

## Activation signals

- Designing a new public function or class — every signature gets full annotations.
- Code review surfaces `dict` / `list` without parametrization.
- Code review surfaces `Optional[X]` or `Union[X, Y]` instead of shorthand.
- mypy reports an error you're tempted to silence with `# type: ignore`.
- Designing a generic protocol / ABC.
- New module — does it need `from __future__ import annotations`?
- New package — does it have `py.typed`?

## Core rules

### Rule 1 — Full annotations on every public symbol

```python
# WRONG
def parse(data, opts=None):
    return ...

# RIGHT
def parse(data: bytes, opts: ParseOptions | None = None) -> Record:
    return ...
```

Every parameter typed. Every return typed. No exceptions. `mypy --strict` enforces.

For private helpers (leading underscore), strict mode still requires annotations, but the signal-to-noise tradeoff is cheap — type them. The exception is local lambdas / nested closures where inference is sufficient and explicit annotations would clutter:

```python
records.sort(key=lambda r: r.timestamp)        # inference is fine
```

### Rule 2 — Use the shorthand: `X | None`, `X | Y`

PEP 604 (3.10+) made `X | None` the canonical form. `Optional[X]` and `Union[X, Y]` are still valid but verbose.

```python
# WRONG (verbose; older idiom)
def fetch(self, url: str, timeout: Optional[float] = None) -> Union[bytes, None]:
    ...

# RIGHT
def fetch(self, url: str, timeout: float | None = None) -> bytes | None:
    ...
```

`Optional[X]` is `X | None`. `Union[A, B, C]` is `A | B | C`. Reach for the shorthand by default.

The exception: when introspecting type hints at runtime via `typing.get_type_hints` and pattern-matching on `Union`, the shorthand and `Union[...]` produce the same `UnionType`. They are interchangeable; the shorthand is preferred for readability.

### Rule 3 — Parametrize collection types

```python
# WRONG
def get_records(self) -> list:                # what's in the list?
    ...

# RIGHT
def get_records(self) -> list[Record]:
    ...

# WRONG
def get_metadata(self) -> dict:                # what type are the values?
    ...

# RIGHT
def get_metadata(self) -> dict[str, str]:
    ...
```

PEP 585 (3.9+) made `list[T]`, `dict[K, V]`, `tuple[T, ...]` legal at runtime. `from typing import List, Dict` is the pre-3.9 idiom and is now legacy — `typing.List` is deprecated in mypy. Always use the lowercase `list[T]` form.

### Rule 4 — `Self` for fluent / factory return types

```python
# WRONG (pre-3.11 idiom)
class Builder:
    def with_x(self, x: int) -> "Builder":
        ...

# RIGHT (3.11+)
from typing import Self
class Builder:
    def with_x(self, x: int) -> Self:
        ...
```

`Self` (PEP 673) is the typed self-reference. For subclass-aware factories:

```python
class Config:
    @classmethod
    def from_url(cls, url: str) -> Self:           # subclass returns subclass
        return cls(...)
```

Without `Self`, a subclass `ProductionConfig.from_url(...)` is typed as `Config` not `ProductionConfig`.

The pre-3.11 alternative (`TypeVar('T', bound='Config')`) is verbose and now legacy. Bump `requires-python` floor and use `Self`.

### Rule 5 — Protocol over ABC for structural typing

```python
# Use Protocol for "anything quacking like this"
from typing import Protocol, runtime_checkable

@runtime_checkable
class Cache(Protocol):
    def get(self, key: str) -> bytes | None: ...
    def put(self, key: str, value: bytes) -> None: ...

# Consumer just needs to provide an object with the methods; no inheritance.
class InMemoryCache:
    def __init__(self) -> None:
        self._store: dict[str, bytes] = {}
    def get(self, key: str) -> bytes | None:
        return self._store.get(key)
    def put(self, key: str, value: bytes) -> None:
        self._store[key] = value

# No `class InMemoryCache(Cache):` needed — duck-typed.
```

Use `ABC` only when the design intent is nominal subtyping (a base class that provides shared behavior + a contract):

```python
from abc import ABC, abstractmethod

class Storage(ABC):
    """Base class for storage implementations.

    Subclasses MUST implement ``put`` and ``get``. Provides shared serialization.
    """
    def serialize(self, record: Record) -> bytes:
        return record.to_bytes()                    # shared behavior

    @abstractmethod
    def put(self, key: str, data: bytes) -> None: ...
    @abstractmethod
    def get(self, key: str) -> bytes | None: ...
```

Heuristic: if you'd write `accept this object if it implements these methods`, that's a Protocol. If you'd write `inherit from this base to share its behavior`, that's an ABC. Most public SDK contracts are Protocols.

### Rule 6 — `from __future__ import annotations` on Python ≤3.12

PEP 563 deferred evaluation of annotations. With it, annotations are stored as strings and only resolved when explicitly inspected. Benefits:
- Forward references work without quoting (`def f(x: MyClass)` even if `MyClass` is defined later in the file).
- Smaller import-time cost (no eager type construction).

```python
# Top of every typed module
from __future__ import annotations

from dataclasses import dataclass

@dataclass
class Tree:
    value: int
    left: Tree | None = None              # works; would otherwise NameError
    right: Tree | None = None
```

On Python 3.12, the future import is OPTIONAL (3.12 introduced PEP 695 type-parameter syntax which defers naturally). The Python pack default is to INCLUDE it for code that needs to work on 3.10–3.13 — its absence costs nothing on 3.12+ but its presence enables forward refs without quoting.

If your module introspects annotations at runtime (e.g., `typing.get_type_hints(cls)`), be aware that `from __future__ import annotations` means the hints are STRINGS until `get_type_hints` resolves them. Some libraries (older pydantic, attrs) had bugs with stringified annotations; modern versions handle them. Test before committing.

### Rule 7 — `py.typed` marker file

PEP 561. Create `src/<pkg>/py.typed` (empty file). Without it, `mypy --strict` consumers fall back to `Any` for every import of your package — your typing work is invisible to them.

```bash
touch src/motadatapysdk/py.typed
```

Verify the build backend includes it in the wheel. Hatchling does this automatically; setuptools needs explicit `include_package_data = true` + `MANIFEST.in` entry. `sdk-packaging-devil-python` P-6 catches the omission.

### Rule 8 — `assert isinstance` over `cast`

```python
# WRONG — silent reinterpretation; if the runtime type is wrong, you get
# a confusing AttributeError later.
from typing import cast
def fetch(self) -> Record:
    raw = self._raw_fetch()
    return cast(Record, raw)              # mypy trusts you; runtime can't.

# RIGHT — runtime + type-checker both agree
def fetch(self) -> Record:
    raw = self._raw_fetch()
    assert isinstance(raw, Record), f"expected Record, got {type(raw).__name__}"
    return raw

# RIGHT (preferred when mypy can narrow naturally) — use isinstance() check
def fetch(self) -> Record:
    raw = self._raw_fetch()
    if not isinstance(raw, Record):
        raise TypeError(f"expected Record, got {type(raw).__name__}")
    return raw                             # mypy narrows here
```

`cast` is the last resort. Most legitimate uses of `cast` are when interfacing with `**kwargs` or third-party untyped libraries.

### Rule 9 — `# type: ignore` discipline

```python
# WRONG — opaque suppression
result = legacy_call(x)  # type: ignore

# RIGHT — pin the specific check + leave a note
result = legacy_call(x)  # type: ignore[no-untyped-call]  # legacy_lib lacks stubs (issue #42)
```

`# type: ignore` without `[error-code]` silences EVERY check on that line. Always pin the code (mypy reports it as `[no-untyped-call]`, `[arg-type]`, etc.). Always leave a comment explaining why — a year from now you (or a teammate) will need to reassess.

For libraries lacking stubs: prefer `pip install types-<name>` (PEP 561 stub package) over `# type: ignore`. Modern Python ecosystem has stubs for most popular libraries.

### Rule 10 — `TypedDict` for kwargs schemas

```python
from typing import TypedDict, Required, NotRequired

class PublishOptions(TypedDict):
    timeout_s: Required[float]                     # must be present
    headers: NotRequired[dict[str, str]]           # optional
    correlation_id: NotRequired[str]

async def publish(self, topic: str, payload: bytes, **opts: PublishOptions) -> None:
    ...

# Consumer
await client.publish("t", b"x", timeout_s=5.0, headers={"X": "y"})
```

`Required` / `NotRequired` (PEP 655, 3.11+) replace the older `total=False` and individual marking. Use TypedDict whenever the kwargs have a known schema; never type kwargs as `**kwargs: Any`.

### Rule 11 — `Generic[T]` + PEP 695 type parameter syntax

```python
# Pre-3.12 (PEP 484)
from typing import Generic, TypeVar
T = TypeVar("T")
class Container(Generic[T]):
    def __init__(self, value: T) -> None:
        self._value = value
    def get(self) -> T:
        return self._value

# Python 3.12+ (PEP 695)
class Container[T]:
    def __init__(self, value: T) -> None:
        self._value = value
    def get(self) -> T:
        return self._value
```

PEP 695 syntax is cleaner and is the Python pack default for new code on 3.12+. The TypeVar form is still legal and may be needed when targeting older Python; the Python pack's `requires-python = ">=3.12"` makes PEP 695 the standard.

For bounds (`T must be a Comparable`):

```python
# Pre-3.12
T = TypeVar("T", bound="Comparable")
class Sorted(Generic[T]): ...

# 3.12+
class Sorted[T: Comparable]: ...
```

### Rule 12 — `@overload` for polymorphic signatures

```python
from typing import overload

@overload
def get(self, key: str) -> bytes: ...
@overload
def get(self, key: str, default: T) -> bytes | T: ...

def get(self, key: str, default: object = _MISSING) -> object:
    if default is _MISSING:
        if key not in self._store:
            raise KeyError(key)
        return self._store[key]
    return self._store.get(key, default)
```

Overloads are TYPE-checker hints; only the final unstubbed signature carries the runtime body. mypy / pyright pick the right overload at each call site.

### Rule 13 — `Literal` for enumerable string parameters

```python
from typing import Literal

def set_mode(self, mode: Literal["read", "write", "append"]) -> None:
    ...
```

`Literal` is more precise than `str` AND more lightweight than an `Enum` for small fixed sets. Reserve `Enum` for cases where the caller benefits from accessing values by attribute (`Mode.READ`) or where the values carry behavior beyond their string form.

### Rule 14 — `Final` for module-level constants

```python
from typing import Final

DEFAULT_TIMEOUT_S: Final = 5.0                     # mypy enforces no reassignment
MAX_PAYLOAD_BYTES: Final[int] = 1024 * 1024
```

`Final` makes the constant truly constant for the type-checker. Reassignment in any module that imports it is a mypy error.

### Rule 15 — Avoid `Any`

`Any` opts out of type-checking. Every `Any` is a leak in your strict-mode net.

```python
# WRONG
def parse(data: Any) -> Record: ...

# Better — `object` (every Python value, but caller can't use it without narrowing)
def parse(data: object) -> Record:
    if not isinstance(data, (bytes, str, dict)):
        raise TypeError("...")
    ...

# Best — be specific
def parse(data: bytes | str | dict[str, object]) -> Record: ...
```

Legitimate `Any` uses: when implementing typed wrappers around untyped libraries (and the wrapper's signature is the strongly-typed surface). Even then, prefer `object` + narrowing.

## pyproject.toml — mypy strict configuration

```toml
[tool.mypy]
python_version = "3.12"
strict = true
warn_unused_ignores = true                # surface stale # type: ignore comments
warn_return_any = true
warn_unreachable = true
disallow_untyped_decorators = true
no_implicit_optional = true                # X = None requires X: T | None
exclude = ["build/", "dist/"]

# For specific submodules with known stub gaps:
[[tool.mypy.overrides]]
module = ["legacy_untyped_lib.*"]
ignore_missing_imports = true              # explicit allowlist; not blanket

# Per-package strict:
[[tool.mypy.overrides]]
module = "motadatapysdk.*"
disallow_any_explicit = true               # no Any in your own code
```

`warn_unused_ignores = true` is critical — it tells you when a `# type: ignore` was needed last year but isn't anymore (the upstream library shipped stubs).

## GOOD: full module example

```python
# src/motadatapysdk/cache.py
"""In-memory cache with size bound."""
from __future__ import annotations

from typing import Final, Generic, Protocol, Self, TypeVar, runtime_checkable

T = TypeVar("T")

DEFAULT_MAX_SIZE: Final = 1024


@runtime_checkable
class CacheProtocol(Protocol[T]):
    """Structural protocol for a key→value cache."""

    def get(self, key: str) -> T | None: ...
    def put(self, key: str, value: T) -> None: ...
    def size(self) -> int: ...


class Cache(Generic[T]):
    """Bounded in-memory cache.

    Args:
        max_size: Maximum entries; oldest evicted on overflow.

    Examples:
        >>> cache: Cache[bytes] = Cache(max_size=10)
        >>> cache.put("k", b"v")
        >>> cache.get("k")
        b'v'
    """

    def __init__(self, *, max_size: int = DEFAULT_MAX_SIZE) -> None:
        self._max_size = max_size
        self._store: dict[str, T] = {}

    def get(self, key: str) -> T | None:
        return self._store.get(key)

    def put(self, key: str, value: T) -> None:
        if len(self._store) >= self._max_size and key not in self._store:
            self._store.pop(next(iter(self._store)))     # FIFO eviction
        self._store[key] = value

    def size(self) -> int:
        return len(self._store)

    @classmethod
    def empty(cls) -> Self:
        return cls()
```

Demonstrates: `from __future__`, `Final`, `Generic[T]` + TypeVar, `Protocol[T]` with `runtime_checkable`, `Self` factory, `T | None` shorthand, `dict[str, T]` parametrization, kw-only via `*`, full annotations, no `Any`.

## BAD anti-patterns

```python
# 1. Missing annotations
def parse(data, opts=None):
    return ...

# 2. Optional / Union (verbose)
def fetch(url: str) -> Optional[bytes]:
    ...

# 3. Bare collection types
def records() -> list:
    ...

# 4. cast over isinstance
return cast(Record, raw_data)

# 5. Unscoped # type: ignore
result = thing()  # type: ignore

# 6. Any everywhere
def process(data: Any) -> Any: ...

# 7. Old TypeVar form on 3.12+
T = TypeVar("T")
class Box(Generic[T]): ...                  # use class Box[T] instead

# 8. Missing py.typed
# (no marker file → consumers see Any)

# 9. ABC where Protocol fits
class Cache(ABC):                           # nominal subtyping needed?
    @abstractmethod
    def get(self, key: str) -> bytes: ...   # caller has to inherit; Protocol better

# 10. **kwargs: Any
def publish(self, topic: str, **opts: Any) -> None: ...
# Use TypedDict.
```

## Cross-references

- `python-sdk-config-pattern` — `Config` as `@dataclass` typed shape.
- `python-asyncio-patterns` — async signatures (`AsyncIterator`, `Coroutine`).
- `python-pytest-patterns` — `pytest.MonkeyPatch`, `pytest.LogCaptureFixture` typed fixtures.
- `python-doctest-patterns` — type-checked Examples in docstrings.
- `python-exception-patterns` — typed `__init__` on exception subclasses.
- `sdk-convention-devil-python` C-3 (py.typed) + C-6 (type system) — design-rule enforcement.
- `sdk-packaging-devil-python` P-6 — wheel-side py.typed verification.
