---
name: dataclass-patterns
description: Dataclass patterns including frozen dataclasses, slots, immutability, and value objects. Activated when designing data classes or value types.
---

# Dataclass patterns

## Purpose

Guide for designing dataclasses including frozen (immutable) dataclasses, slots optimization, validation, and value object patterns.

## When to use

This skill activates when:

- Creating data classes
- Designing immutable value objects
- Optimizing memory usage with slots
- Implementing validation in dataclasses
- Using dataclass features like field factories

## Core patterns

### Frozen immutable dataclass

```python
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Point:
    """Immutable point with memory-efficient slots."""
    x: float
    y: float

# Usage
p = Point(1.0, 2.0)
# p.x = 3.0  # Raises FrozenInstanceError
```

### With validation

```python
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class PositivePoint:
    """Point with validation."""
    x: float
    y: float

    def __post_init__(self) -> None:
        if self.x < 0 or self.y < 0:
            raise ValueError(f"Coordinates must be positive: ({self.x}, {self.y})")
```

### With field defaults

```python
from dataclasses import dataclass, field

@dataclass(frozen=True, slots=True)
class Config:
    """Configuration with defaults."""
    name: str
    enabled: bool = True
    options: tuple[str, ...] = field(default_factory=tuple)
    metadata: dict[str, str] = field(default_factory=dict)
```

## Slots optimization

### Why use slots

```python
# Without slots: each instance has __dict__ for attributes
@dataclass
class RegularPoint:
    x: float
    y: float
# 120+ bytes per instance

# With slots: fixed attribute storage
@dataclass(slots=True)
class SlottedPoint:
    x: float
    y: float
# ~50 bytes per instance
```

### Slots with inheritance

```python
@dataclass(slots=True)
class Base:
    x: int

@dataclass(slots=True)
class Derived(Base):
    y: int
    # Python 3.10+ handles slots inheritance correctly
```

## Immutability patterns

### Frozen with copy modification

```python
from dataclasses import dataclass, replace

@dataclass(frozen=True, slots=True)
class User:
    id: int
    name: str
    active: bool

# Modify by creating new instance
user = User(id=1, name="Alice", active=True)
updated = replace(user, active=False)

assert user.active is True
assert updated.active is False
```

### Deeply immutable

```python
from dataclasses import dataclass, field

@dataclass(frozen=True, slots=True)
class ImmutableConfig:
    """Deeply immutable config using tuples instead of lists."""
    name: str
    options: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def from_list(cls, name: str, options: list[str]) -> 'ImmutableConfig':
        """Create from list, converting to tuple."""
        return cls(name=name, options=tuple(options))
```

## Field patterns

### Field with factory

```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass(frozen=True, slots=True)
class Event:
    name: str
    timestamp: datetime = field(default_factory=datetime.now)
    tags: frozenset[str] = field(default_factory=frozenset)
```

### Field with metadata

```python
from dataclasses import dataclass, field

@dataclass(frozen=True, slots=True)
class FormField:
    name: str
    value: str = ""
    required: bool = field(default=False, metadata={'form': 'checkbox'})
    max_length: int = field(default=100, metadata={'form': 'hidden'})
```

### Exclude from repr/compare

```python
from dataclasses import dataclass, field

@dataclass(frozen=True, slots=True)
class CachedResult:
    key: str
    value: str
    # Cache metadata not part of equality or repr
    _cache_time: float = field(repr=False, compare=False, default=0.0)
```

## Validation patterns

### Post-init validation

```python
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Range:
    start: int
    end: int

    def __post_init__(self) -> None:
        if self.start > self.end:
            raise ValueError(f"start ({self.start}) must be <= end ({self.end})")
```

### Factory method validation

```python
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Email:
    """Validated email address."""
    address: str

    def __post_init__(self) -> None:
        if '@' not in self.address:
            raise ValueError(f"Invalid email: {self.address}")

    @classmethod
    def parse(cls, value: str) -> 'Email':
        """Parse and validate email string."""
        return cls(address=value.strip().lower())
```

## Comparison and ordering

### Custom ordering

```python
from dataclasses import dataclass
from functools import total_ordering

@total_ordering
@dataclass(frozen=True, slots=True, eq=True)
class Version:
    major: int
    minor: int
    patch: int

    def __lt__(self, other: 'Version') -> bool:
        return (self.major, self.minor, self.patch) < (other.major, other.minor, other.patch)
```

### Hash for use in sets/dicts

```python
@dataclass(frozen=True, slots=True)
class HashableItem:
    """Frozen dataclass is automatically hashable."""
    id: str
    name: str

# Can be used in sets and as dict keys
items = {HashableItem("1", "a"), HashableItem("2", "b")}
lookup = {HashableItem("1", "a"): "value"}
```

## Pattern: Value object

```python
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Money:
    """Immutable value object representing money."""
    amount: int  # In cents to avoid float issues
    currency: str

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValueError("Amount cannot be negative")
        if len(self.currency) != 3:
            raise ValueError("Currency must be 3-letter code")

    def add(self, other: 'Money') -> 'Money':
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")
        return Money(self.amount + other.amount, self.currency)

    def __str__(self) -> str:
        return f"{self.amount / 100:.2f} {self.currency}"
```

## Checklist

- [ ] Use `frozen=True` for immutable data
- [ ] Use `slots=True` for memory efficiency
- [ ] Validation in `__post_init__` or factory methods
- [ ] Use `tuple`/`frozenset` for immutable collections
- [ ] Use `replace()` for modifications
- [ ] Document invariants

---

**Additional resources:**

- [dataclasses documentation](https://docs.python.org/3/library/dataclasses.html)
