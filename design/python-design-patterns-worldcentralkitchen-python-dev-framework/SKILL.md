---
name: Python Design Patterns
description: >
  This skill should be used when the user asks about "design patterns",
  "SOLID principles", "factory pattern", "strategy pattern", "observer pattern",
  "composition vs inheritance", "Pythonic design", "singleton alternatives",
  "anti-patterns", "dependency injection", or needs guidance on applying
  Gang of Four patterns idiomatically in Python.
---

# Python Design Patterns

Pythonic adaptations of GoF patterns, SOLID principles, and anti-patterns to avoid.

> "Modern Python simply avoids the problems that the old design patterns were meant to solve."
> — Brandon Rhodes, PyCon 2025

**Prerequisites:** `from __future__ import annotations`, `collections.abc` for Callable/Iterator, `structlog` for logging.

## Pattern Decision Table

| Need | Pattern | Python Idiom |
|------|---------|--------------|
| Multiple creation strategies | Factory | Function or `@classmethod` |
| Complex object, many options | Builder | `dataclass` + `replace()` |
| Interchangeable algorithms | Strategy | Pass `Callable` |
| Event notification | Observer | Callback list |
| Lazy sequences | Iterator | Generator (`yield`) |
| Tree structures | Composite | Recursive dataclass |
| Memory optimization | Flyweight | `__slots__`, `lru_cache` |
| Interface conversion | Adapter | Wrapper class |
| Cross-cutting concerns | Decorator | `@decorator` |
| State machines | State | Dict mapping or `match` |
| Shared configuration | Global Object | Module-level instance |
| Callbacks with state | Prebound Method | `obj.method`, `partial` |
| None is valid value | Sentinel | `_MISSING = object()` |

## SOLID Quick Reference

| Principle | Violation Sign | Fix |
|-----------|----------------|-----|
| **S**ingle Responsibility | "Manager" class | Split into focused classes |
| **O**pen-Closed | `if/elif` on types | Dict of handlers + Protocol |
| **L**iskov Substitution | `NotImplementedError` | Composition over inheritance |
| **I**nterface Segregation | Unused interface methods | Small `Protocol` classes |
| **D**ependency Inversion | `self.db = PostgresDB()` | Constructor injection |

## Anti-Patterns

| Anti-Pattern | Why Bad | Pythonic Alternative |
|--------------|---------|---------------------|
| Singleton class | Modules ARE singletons | Module-level instance |
| Deep inheritance | Coupling, diamond problem | Composition + Protocol |
| Java getters/setters | Boilerplate | Direct attrs, `@property` |
| God Object | Untestable, SRP violation | Focused services |
| Method without self | Unnecessary class | Module-level function |
| Premature patterns | Over-engineering | YAGNI - add when needed |

## Key Patterns

### Factory & Strategy

```python
# Factory: function returning instance
def create_connection(db_type: str) -> Connection:
    return {"postgres": PostgresConn, "sqlite": SQLiteConn}[db_type]()

# Strategy: pass functions, not strategy objects
def calculate_total(items: list[Item], pricing: Callable[[float], float]) -> float:
    return sum(pricing(i.price) for i in items)
```

### Observer & Decorator

```python
# Observer: callback list
@dataclass
class EventEmitter:
    _listeners: dict[str, list[Callable]] = field(default_factory=dict)
    def on(self, event: str, fn: Callable) -> None:
        self._listeners.setdefault(event, []).append(fn)
    def emit(self, event: str, *args) -> None:
        for fn in self._listeners.get(event, []): fn(*args)

# Decorator: @wraps for cross-cutting concerns
def timing(func):
    @wraps(func)
    def wrapper(*a, **kw):
        start = perf_counter()
        result = func(*a, **kw)
        log.info("timing", elapsed=perf_counter() - start)
        return result
    return wrapper
```

### Global Object & Sentinel

```python
# Global Object: module-level instance (not singleton class)
_config: Config | None = None
def get_config() -> Config:
    global _config
    if _config is None: _config = Config.from_env()
    return _config

# Sentinel: distinguish None from "not provided"
_MISSING = object()
def get(key: str, default: object = _MISSING) -> object:
    if (v := cache.get(key)) is not None: return v
    if default is _MISSING: raise KeyError(key)
    return default
```

## Reference Files

| File | Content |
|------|---------|
| `references/patterns.md` | All GoF patterns with examples |
| `references/solid-anti.md` | SOLID principles + anti-patterns |
| `references/python-idioms.md` | Global Object, Prebound Method, Sentinel |

## Related

- [ADR-014](../../docs/adr/014-design-patterns-skill.md) - Design decisions
- [ADR-013](../../docs/adr/013-immutability-safety-patterns.md) - Immutability patterns
