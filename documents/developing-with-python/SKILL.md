---
name: developing-with-python
description: Python 3.11+ development with type hints, async patterns, FastAPI, and pytest
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Python Development Skill

Production-grade Python development following strict quality standards.
Prefer security and correctness over convenience and performance.

## Scope

Python code using PEP 257 docstrings. Typical library or service modules.
Testing is covered in the pytest skill.

## Primary Deliverables

- Source code with full type hints
- Clear, concise docstrings for all non-trivial modules, classes, functions
- Minimal runtime dependencies with version pins
- Example configuration and usage documentation

## Definition of Done

- All rules in this skill are followed
- All code is type-annotated and passes static checks
- No secrets or credentials embedded
- Logging used appropriately; no print calls for diagnostics
- Clear README section or usage docstring included

## Global Constraints

- Follow PEP 8
- Keep line length under 79 characters
- Use descriptive names
- Modular design with Single Responsibility Principle (SRP)
- Prefer dependency injection; avoid globals
- Validate and sanitize all external inputs
- Use logging, not print, for diagnostics
- Use generators/iterators when memory efficiency matters
- Cache expensive/pure functions appropriately
- Pin dependency versions and use environment variables for config

## Prohibited Patterns

- Bare `except` or catching `Exception` without re-raising or handling
- Silent failures or swallowed exceptions
- `print` for operational logging
- Hardcoded secrets, tokens, or credentials
- Global mutable state for cross-module coordination
- Circular imports (restructure or inject dependencies instead)

---

## Structure and Organization

Break code into small, reusable units (functions/classes).
Each module/class/function should have a single clear purpose (SRP).
Design for loose coupling; inject collaborators instead of importing
deep implementation details.

---

## Type Hints

Fully annotate public APIs and internal functions.
Use `Optional`, `Union`, `TypedDict`, `Protocol`, and generics
as appropriate.

```python
from __future__ import annotations

from typing import TypeVar, Generic, Protocol, Iterator

T = TypeVar('T')


class Sink(Protocol):
    """Protocol for item consumers."""

    def write(self, item: tuple[int, str]) -> None:
        """Write a single item."""
        ...


def process(
    lines: Iterator[str],
    sink: Sink,
) -> int:
    """Process lines and write to sink.

    Args:
        lines: Input line iterator.
        sink: Destination for processed items.

    Returns:
        Number of items processed.
    """
    count = 0
    for line in lines:
        # Processing logic here
        count += 1
    return count
```

---

## Docstrings (PEP 257)

Every non-trivial module, class, and function has a docstring.
First line: short imperative summary. Then a blank line.
Include Args, Returns, Raises, and Examples when useful.

```python
def normalize_token(token: str) -> str:
    """Normalize a single token to lowercase.

    Strips whitespace and converts to lowercase. Empty tokens
    after stripping raise ValueError.

    Args:
        token: Raw token string.

    Returns:
        Normalized lowercase token.

    Raises:
        TypeError: If token is not a string.
        ValueError: If token is empty after stripping.

    Examples:
        >>> normalize_token("  Hello  ")
        'hello'
        >>> normalize_token("")
        Traceback (most recent call last):
            ...
        ValueError: token cannot be empty
    """
    if not isinstance(token, str):
        raise TypeError("token must be str")
    t = token.strip()
    if not t:
        raise ValueError("token cannot be empty")
    return t.lower()
```

---

## Error Handling and Logging

Catch specific exceptions; attach context and re-raise when needed.
Prefer `raise ... from e` to maintain traceback.
Use `logging.getLogger(__name__)`; choose appropriate levels.

```python
import logging
from typing import Iterable, Iterator

logger = logging.getLogger(__name__)


class ParseError(ValueError):
    """Raised when input lines are malformed."""

    pass


def parse_lines(
    lines: Iterable[str],
) -> Iterator[tuple[int, str]]:
    """Parse input lines of the form 'id,value'.

    Emits pairs (id, normalized_value). Lines with leading/trailing
    spaces are tolerated. Empty lines are skipped.

    Args:
        lines: Iterable of CSV-like strings.

    Yields:
        Tuples of (int id, normalized str value).

    Raises:
        ParseError: When a non-empty line is malformed.
    """
    for raw in lines:
        if raw is None:
            raise TypeError("lines must contain str items")
        s = raw.strip()
        if not s:
            continue
        try:
            left, right = s.split(",", 1)
            ident = int(left.strip())
            value = right.strip().lower()
            yield ident, value
        except (ValueError, TypeError) as e:
            logger.debug("Failed to parse line %r: %s", raw, e)
            raise ParseError(f"Malformed line: {raw!r}") from e
```

### Logging Levels

- **DEBUG**: Diagnostic details
- **INFO**: High-level milestones
- **WARNING**: Recoverable issues
- **ERROR/CRITICAL**: Failures

---

## Security and Reliability

Read secrets/config via environment variables (optionally via dotenv).
Validate and sanitize all external inputs; fail fast with clear errors.

```python
import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Application configuration from environment."""

    batch_size: int
    log_level: str

    @staticmethod
    def from_env() -> Settings:
        """Load settings from environment variables.

        Returns:
            Populated Settings instance.

        Raises:
            ValueError: If BATCH_SIZE is not a valid integer.
        """
        raw_bs = os.getenv("BATCH_SIZE", "100")
        try:
            bs = int(raw_bs)
        except ValueError as e:
            raise ValueError(
                "BATCH_SIZE must be an integer"
            ) from e
        level = os.getenv("LOG_LEVEL", "INFO").upper()
        return Settings(batch_size=bs, log_level=level)
```

**.env.example**:
```
BATCH_SIZE=100
LOG_LEVEL=INFO
```

---

## Performance and Scalability

Use generators/iterators for streaming data.
Avoid unnecessary copies; short-circuit early.
Use `functools.lru_cache` for pure, expensive computations.

```python
from functools import lru_cache


@lru_cache(maxsize=512)
def expensive_computation(value: str) -> str:
    """Compute result with memoization.

    Results are cached for repeated calls with the same value.

    Args:
        value: Input to process.

    Returns:
        Computed result.
    """
    # Expensive processing here
    return value.upper()
```

---

## Dependency Injection Over Globals

Avoid circular imports by injecting dependencies.

```python
from typing import Protocol, Iterable


class Sink(Protocol):
    """Protocol for output destinations."""

    def write(self, item: tuple[int, str]) -> None:
        """Write item to destination."""
        ...


def process(lines: Iterable[str], sink: Sink) -> int:
    """Process lines and write parsed items to sink.

    Args:
        lines: Input lines to process.
        sink: Destination for output.

    Returns:
        Number of successfully processed items.
    """
    from .parser import parse_lines  # local import avoids cycles

    count = 0
    for item in parse_lines(lines):
        sink.write(item)
        count += 1
    return count
```

---

## Dependencies and Environment

Pin versions in `requirements.txt` (e.g., `package==X.Y.Z`).
Keep dependencies minimal; justify each addition.
Provide `.env.example` listing required env vars.

```
# requirements.txt
pydantic==2.5.0
python-dotenv==1.0.0
```

---

## Bad Patterns and Corrections

### No type hints

```python
# Bad
def f(x): return x + 1

# Good
def f(x: int) -> int:
    return x + 1
```

### Bare except

```python
# Bad
try:
    risky_operation()
except:
    pass

# Good
try:
    risky_operation()
except ValueError as e:
    raise CustomError("Operation failed") from e
```

### Print for diagnostics

```python
# Bad
print("failed")

# Good
logger.error("Operation failed: %s", err)
```

### Hardcoded secret

```python
# Bad
API_KEY = "sk-live-..."

# Good
API_KEY = os.getenv("API_KEY")
# Document in .env.example
```

### Global mutable state

```python
# Bad
CACHE = {}

# Good
@lru_cache(maxsize=256)
def cached_lookup(key: str) -> str:
    ...
```

### Unvalidated input

```python
# Bad
int(os.getenv("BATCH_SIZE"))

# Good
raw = os.getenv("BATCH_SIZE", "100")
try:
    batch_size = int(raw)
except ValueError as e:
    raise ValueError("BATCH_SIZE must be integer") from e
```

---

## Self-Check Before Finalizing

- [ ] All public functions/classes fully type-annotated?
- [ ] All non-trivial functions/classes/modules have PEP 257 docstrings?
- [ ] Errors specific, with helpful messages, no bare except?
- [ ] Logging used instead of print for diagnostics?
- [ ] Inputs validated and sanitized?
- [ ] Dependencies pinned and minimal?
- [ ] Secrets/config from environment, documented in .env.example?
- [ ] Code modular, SRP-compliant, free of circular imports?
- [ ] Generators/caching used where appropriate?
- [ ] Line length <= 79 chars and naming descriptive?

If any answer is no, revise the code until all criteria are satisfied.
