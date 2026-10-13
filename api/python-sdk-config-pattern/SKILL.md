---
name: python-sdk-config-pattern
description: >
  Use this when designing a new client class, reviewing a constructor with
  more than four parameters or a **kwargs signature, finding post-construction
  mutation of Config, or evaluating Quick start ergonomics. Covers the frozen
  @dataclass(slots=True, kw_only=True) primary form, pydantic.BaseModel(frozen,
  extra="forbid") secondary form for non-trivial validation, classmethod
  factories (from_url / from_env / from_dict), __post_init__ validators that
  raise but never mutate, dataclasses.replace for variation, mutable-default
  avoidance via field(default_factory=...), and Self-typed factory returns.
  Triggers: Config, @dataclass, frozen, pydantic, BaseModel, model_config, ConfigDict, from_url, from_env, classmethod, __init__.
---

# python-sdk-config-pattern (v1.0.0)

## Rationale

Python SDK clients have at least 4 plausible constructor shapes: positional args, `**kwargs`, builder chains, and a `Config` object. Only one matches the rest of the Python pack: **a frozen `@dataclass Config` (or `pydantic.BaseModel(frozen=True)`) passed to the client's `__init__`**. Builders mask required fields, `**kwargs` defeat type-checkers, positional args break ordering when fields are added. The Config-object pattern delivers: typed self-documenting parameters, mypy-strict friendliness, immutability after construction, and a stable shape for cross-version diffing by `sdk-breaking-change-devil-python`.

This skill is cited by `conventions.yaml` (`parameter_count`, `mutable_shared_state`), `code-reviewer-python` (PEP 484 + immutability), `sdk-api-ergonomics-devil-python` (E-1 quickstart boilerplate, E-13 parameter count), `sdk-design-devil` (universal `parameter_count` rule), and `sdk-convention-devil-python` (C-4).

## Activation signals

- Designing a new client class.
- Reviewing a constructor with >4 parameters.
- TPRD §6 Config section is empty or proposes positional / kwargs shape.
- Code review surfaces post-construction mutation of Config (`config.timeout = 5`).
- Code review surfaces `def __init__(self, **kwargs):`.
- API ergonomics review flags Quick start as boilerplate-heavy.

## Convention

### Primary: frozen @dataclass

```python
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass(frozen=True, slots=True, kw_only=True)
class Config:
    """Configuration for the motadata client.

    Args:
        base_url: Endpoint base URL. Required.
        api_key: Bearer token. Required.
        timeout_s: Per-request timeout in seconds. Default 5.0.
        max_retries: Idempotent retry cap. Default 3.
        max_concurrent_publishes: Inflight publish limit. Default 16.
    """

    base_url: str
    api_key: str
    timeout_s: float = 5.0
    max_retries: int = 3
    max_concurrent_publishes: int = 16
    extra_headers: dict[str, str] = field(default_factory=dict)


class Client:
    def __init__(self, config: Config) -> None:
        self._config = config
        ...
```

Why this shape:

- `frozen=True` — Config can't be mutated after construction. Caller cannot do `config.timeout_s = 10` then wonder why the client ignored it. This matches Go pack's `Config struct` rule of "no post-construction mutation".
- `slots=True` (3.10+) — small memory win + prevents accidental attribute injection (`config.typo = 5` raises `FrozenInstanceError`).
- `kw_only=True` (3.10+) — every field is keyword-only at the call site. `Config(base_url="...", api_key="...")` is the only legal form. Adding a new field never reorders existing call-site kwargs. PEP-style; matches the rest of the Python pack.
- `field(default_factory=dict)` for mutable defaults — never `field(default={})`. Per-instance new dict; no cross-instance state leak.
- Docstring is the contract — every field documented.

### Secondary: pydantic.BaseModel (when validation logic is non-trivial)

```python
from pydantic import BaseModel, ConfigDict, Field

class Config(BaseModel):
    """Configuration for the motadata client."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    base_url: str = Field(..., pattern=r"^https?://")
    api_key: str = Field(..., min_length=8)
    timeout_s: float = Field(default=5.0, gt=0)
    max_retries: int = Field(default=3, ge=0, le=10)
    max_concurrent_publishes: int = Field(default=16, ge=1, le=1024)
```

Use pydantic when:
- Validation logic is non-trivial (regex match, range bounds, cross-field constraints).
- The Config is loaded from external JSON / YAML / env (pydantic-settings handles env layout natively).
- The SDK is itself pydantic-based (e.g., consumers expect `model_dump()` semantics).

Do NOT use pydantic for "I want validation" alone — `__post_init__` validators on a `@dataclass` cover most cases without the dependency. Pydantic is a runtime dep and an import-time cost; choose deliberately. `sdk-dep-vet-devil-python` will scrutinize the addition.

The `@dataclass` form remains the Python pack DEFAULT. Pydantic is the OPT-IN form. Quick start should never need pydantic to be readable.

### Convenience factories — `from_url`, `from_env`, `from_dict`

```python
@dataclass(frozen=True, slots=True, kw_only=True)
class Config:
    base_url: str
    api_key: str
    timeout_s: float = 5.0

    @classmethod
    def from_url(cls, url: str, *, api_key: str, **overrides: object) -> Config:
        """Construct from a URL with sensible defaults.

        Examples:
            >>> cfg = Config.from_url("https://api.example.com", api_key="x")
            >>> cfg.base_url
            'https://api.example.com'
        """
        return cls(base_url=url, api_key=api_key, **overrides)  # type: ignore[arg-type]

    @classmethod
    def from_env(cls, *, prefix: str = "MOTADATA_") -> Config:
        """Construct from environment variables.

        Reads ``{prefix}BASE_URL``, ``{prefix}API_KEY``, ``{prefix}TIMEOUT_S``.

        Raises:
            KeyError: If a required env var is missing.
        """
        return cls(
            base_url=os.environ[f"{prefix}BASE_URL"],
            api_key=os.environ[f"{prefix}API_KEY"],
            timeout_s=float(os.environ.get(f"{prefix}TIMEOUT_S", 5.0)),
        )
```

Convenience factories are SECONDARY constructors. The PRIMARY remains `Config(base_url=..., api_key=...)`. Factories keep callsites short for the common cases without forcing them into a builder chain.

### Validation — `__post_init__` for `@dataclass`

```python
@dataclass(frozen=True, slots=True, kw_only=True)
class Config:
    base_url: str
    timeout_s: float = 5.0

    def __post_init__(self) -> None:
        if not self.base_url.startswith(("http://", "https://")):
            raise ValueError(f"base_url must start with http(s)://, got {self.base_url!r}")
        if self.timeout_s <= 0:
            raise ValueError(f"timeout_s must be positive, got {self.timeout_s}")
```

`__post_init__` runs ONCE at construction. It can RAISE but it MUST NOT mutate fields (frozen prevents it). Validators that need to coerce or normalize must run BEFORE construction (e.g., in a classmethod factory):

```python
@classmethod
def from_url(cls, url: str, *, api_key: str) -> Config:
    return cls(base_url=url.rstrip("/"), api_key=api_key)  # normalize before frozen freezes
```

## GOOD: full example with all the right defaults

```python
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Self


@dataclass(frozen=True, slots=True, kw_only=True)
class Config:
    """Configuration for the motadata client.

    All fields are keyword-only at the call site. Mutation after construction is
    prevented by ``frozen=True``; build a new Config (e.g. via ``dataclasses.replace``)
    when you need to vary a value.

    Args:
        base_url: Endpoint base URL (must include scheme).
        api_key: Bearer token used in the ``Authorization`` header.
        timeout_s: Per-request timeout in seconds.
        max_retries: Cap on idempotent-request retries.
        max_concurrent_publishes: Maximum simultaneous in-flight publishes.
        extra_headers: Additional headers attached to every outbound request.

    Examples:
        >>> cfg = Config(base_url="https://api.example.com", api_key="secret")
        >>> cfg.timeout_s
        5.0
    """

    base_url: str
    api_key: str
    timeout_s: float = 5.0
    max_retries: int = 3
    max_concurrent_publishes: int = 16
    extra_headers: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.base_url.startswith(("http://", "https://")):
            raise ValueError(f"base_url must start with http(s)://, got {self.base_url!r}")
        if self.timeout_s <= 0:
            raise ValueError(f"timeout_s must be positive, got {self.timeout_s}")
        if self.max_retries < 0:
            raise ValueError(f"max_retries must be >= 0, got {self.max_retries}")

    @classmethod
    def from_env(cls, *, prefix: str = "MOTADATA_") -> Self:
        """Construct from ``{prefix}BASE_URL`` + ``{prefix}API_KEY`` env vars."""
        return cls(
            base_url=os.environ[f"{prefix}BASE_URL"],
            api_key=os.environ[f"{prefix}API_KEY"],
            timeout_s=float(os.environ.get(f"{prefix}TIMEOUT_S", 5.0)),
            max_retries=int(os.environ.get(f"{prefix}MAX_RETRIES", 3)),
        )


class Client:
    """Async client for the motadata API.

    Examples:
        >>> async with Client(Config(base_url="https://x", api_key="k")) as c:
        ...     await c.publish("topic", b"x")  # doctest: +SKIP
    """

    def __init__(self, config: Config) -> None:
        self._config = config
        self._session: aiohttp.ClientSession | None = None
```

Note: `Self` (3.11+) on the classmethod return; never use `"Config"` string-quoted return type — that's the pre-3.11 idiom.

## BAD anti-patterns

```python
# 1. **kwargs constructor — defeats type-checker
class Client:
    def __init__(self, **kwargs: object) -> None:
        self.timeout = kwargs.get("timeout", 5)
        self.api_key = kwargs.get("api_key")     # what happens if missing?

# 2. Long positional list
class Client:
    def __init__(self, base_url, api_key, timeout=5, retries=3, pool=16, headers=None):
        ...                                        # too many positional; reorder = break

# 3. Builder chain (Java-isms)
client = ClientBuilder().with_base_url(...).with_api_key(...).build()
# Pythonic Config-object is shorter and type-checks better.

# 4. Mutable default
@dataclass
class Config:
    extra_headers: dict[str, str] = {}            # SHARED across instances
# Use field(default_factory=dict).

# 5. Non-frozen with post-construction mutation
@dataclass
class Config:
    timeout: float = 5.0
# allows config.timeout = 10 — caller can flip values silently after Client took ownership.

# 6. __post_init__ that mutates
@dataclass(frozen=True)
class Config:
    base_url: str
    def __post_init__(self) -> None:
        self.base_url = self.base_url.rstrip("/")  # FrozenInstanceError
# normalize before freeze (in a classmethod factory) or use object.__setattr__
# (the latter is correct but smelly; prefer the former).

# 7. Pydantic when @dataclass would do
class Config(BaseModel):
    base_url: str
    api_key: str
# Adds runtime dep, import-time cost, and serialization machinery you don't need
# for a 5-field config. Use @dataclass.

# 8. Allow extra fields
class Config(BaseModel):
    model_config = ConfigDict(extra="allow")     # config.typo = 5 silently accepted
# extra="forbid" is the SDK default.
```

## Cross-version evolution — `dataclasses.replace`

When the user wants to vary one field, build a new Config:

```python
from dataclasses import replace

base = Config(base_url="https://x", api_key="k")
test = replace(base, timeout_s=30.0)             # new instance; original unchanged
```

Document this pattern in the Config docstring's `Examples:` block — first-time consumers don't always know `replace` exists.

## Compatibility table

| Python ver | Form | Notes |
|------------|------|-------|
| 3.12 | `@dataclass(frozen=True, slots=True, kw_only=True)` | Default — all flags supported |
| 3.10–3.11 | Same | All flags supported (3.10 added `slots`, `kw_only`) |
| ≤3.9 | Cannot ship; pack requires 3.12+ |  |

`requires-python = ">=3.12"` is the Python pack default; this skill assumes it. Older targets are out of scope.

## Cross-references

- `python-mypy-strict-typing` — Config field annotations and `Self` for factory return.
- `python-asyncio-patterns` — `async with Client(config)` lifecycle uses Config.
- `python-exception-patterns` — `__post_init__` raises `ValueError` (or SDK's `ConfigError` if defined).
- `python-doctest-patterns` — the `Examples:` block in Config docstring.
- `conventions.yaml` `parameter_count`, `mutable_shared_state`, `mutable_default_argument` — design-rule enforcement at D3.
