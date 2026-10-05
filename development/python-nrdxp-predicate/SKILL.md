---
name: python
description: |
  Idiomatic programming style, patterns, and conventions for Python development.
  Trigger when:
  - Writing, refactoring, reviewing, or debugging Python code.
  - Files matching the pattern **/*.py (including requirements.txt, pyproject.toml, setup.py) are in the workspace or referenced.
  - Tasks involve: python, pytest, pip, uv, virtualenv, flake8, black, mypy.
  - Prompt contains keywords: python, py, pep8, typing, list comprehension, decorator, generator, asyncio, yield, poetry.
---

# Python Language Idioms

Work _with_ the language. Lean into duck typing, generators, context managers, and the standard library. Write code that reads like pseudocode — if it needs a comment to explain _what_ it does, rewrite it.

---

## Core Philosophy

- **Readability is a feature** — code is read far more than it is written; optimize for the reader
- **Explicit over implicit** — no magic, no hidden state, no clever tricks
- **Flat over nested** — avoid deep indentation; early returns, guard clauses, comprehensions
- **Composition over inheritance** — functions, protocols, and dataclasses beat class hierarchies
- **Standard library first** — reach for builtins and `stdlib` before adding dependencies

---

## Formatting

Let the formatter handle it. Pick **one** formatter project-wide and enforce it in CI.

```bash
ruff check .          # Lint
ruff format .         # Format
black .               # Alternative formatter
```

### Non-Negotiables

| Rule             | Standard                                                                                  |
| :--------------- | :---------------------------------------------------------------------------------------- |
| Indentation      | 4 spaces. Tabs are prohibited.                                                            |
| Operator spacing | `x = y * 12 + 13`, not `x=y*12+13`                                                        |
| Quote style      | Pick single or double project-wide; enforce via formatter. PEP 8 is deliberately silent.  |
| Line length      | Configure in formatter (88 for `black`/`ruff`, 79 for strict PEP 8). Don't manually wrap. |
| Imports          | `isort`-ordered: stdlib → third-party → local. One import per line for `from` imports.    |

---

## Naming

### Conventions

| Scope              | Style                 | Example                                           |
| :----------------- | :-------------------- | :------------------------------------------------ |
| Modules, packages  | `snake_case`          | `crypto_key.py`, `utils/`                         |
| Functions, methods | `snake_case` (verbs)  | `get_url()`, `calculate_checksum()`               |
| Variables          | `snake_case` (nouns)  | `raw_payload`, `user_registry`                    |
| Classes            | `PascalCase`          | `HttpClient`, `TokenParser`                       |
| Constants          | `SCREAMING_SNAKE`     | `MAX_RETRIES`, `DEFAULT_TIMEOUT`                  |
| Private            | `_leading_underscore` | `_internal_cache`, `_validate()`                  |
| Name-mangled       | `__double_leading`    | `__secret` (rarely needed)                        |
| Dunder             | `__name__`            | Reserved for the language. Never invent new ones. |

### The Verb-Noun Rule

Functions are actions → verbs. Variables are data → nouns. If a function name is a noun, it's probably a property.

### Shadowing Built-ins (Prohibited)

Redefining these names breaks built-in functionality within scope and causes non-deterministic bugs:

> `id`, `type`, `len`, `range`, `list`, `dict`, `str`, `int`, `float`, `min`, `max`, `abs`, `set`, `map`, `filter`, `input`, `open`, `hash`, `format`, `next`, `iter`, `sum`, `any`, `all`, `dir`, `vars`, `help`

Use descriptive alternatives: `user_id`, `item_type`, `name_list`, `count`.

### Natural Phrasing

| ✅ Idiomatic       | ❌ Avoid           |
| :----------------- | :----------------- |
| `if x not in y`    | `if not x in y`    |
| `if x != y`        | `if not x == y`    |
| `if x is not None` | `if not x is None` |

---

## Boolean and Comparison Idioms

| Scenario    | ❌ Wrong            | ✅ Idiomatic         | Why                                                      |
| :---------- | :------------------ | :------------------- | :------------------------------------------------------- |
| Truthiness  | `if x == True:`     | `if x:`              | `if` evaluates truthiness directly                       |
| Falsiness   | `if x == False:`    | `if not x:`          | `not` is the logical inverter                            |
| None check  | `if x == None:`     | `if x is None:`      | `is` checks identity; `==` can be overridden by `__eq__` |
| Empty check | `if len(seq) == 0:` | `if not seq:`        | Empty collections are falsy                              |
| Type check  | `type(x) == int`    | `isinstance(x, int)` | Respects inheritance                                     |

---

## Data Modeling

### When to Use What

| Type                      | Use When                       | Key Trait                                       |
| :------------------------ | :----------------------------- | :---------------------------------------------- |
| `@dataclass`              | Mutable data with behavior     | Auto-generates `__init__`, `__repr__`, `__eq__` |
| `@dataclass(frozen=True)` | Immutable value objects        | Hashable, safe as dict keys                     |
| `NamedTuple`              | Lightweight immutable records  | Tuple-compatible, unpacking works               |
| `TypedDict`               | Typed dict shapes (JSON, APIs) | Runtime is still a plain `dict`                 |
| Plain `dict`              | Dynamic/unknown keys           | No structure guarantees                         |

```python
from dataclasses import dataclass, field

@dataclass(frozen=True, slots=True)
class Token:
    kind: str
    value: str
    line: int = 0
```

### `__slots__`

Use `slots=True` on dataclasses (3.10+) or define `__slots__` manually. It prevents dynamic attribute creation, reduces memory, and speeds up attribute access:

```python
# ✅ With slots — fixed attributes, lower memory
@dataclass(slots=True)
class Point:
    x: float
    y: float

# ❌ Without slots — __dict__ per instance, allows typos like p.z = 3
```

---

## Functions

### Arguments and Returns

```python
# ✅ Type-annotated at boundaries
def parse_config(raw: str, *, strict: bool = False) -> Config:
    ...

# ✅ Keyword-only after * — prevents positional misuse
def connect(host: str, port: int, *, timeout: float = 30.0) -> Connection:
    ...
```

- Use `*` to force keyword-only arguments when order could be confused
- Use `/` (3.8+) for positional-only when the parameter name is an implementation detail
- Return `None` explicitly when a function can return `None` — don't rely on implicit fallthrough

### Default Mutable Arguments (Critical)

```python
# ❌ DANGEROUS — shared across all calls
def append_to(item, target=[]):
    target.append(item)
    return target

# ✅ Sentinel pattern
def append_to(item, target: list | None = None):
    if target is None:
        target = []
    target.append(item)
    return target
```

### Properties

Use `@property` for computed attributes. Use `@cached_property` (3.8+) when the result is expensive and stable:

```python
class Circle:
    def __init__(self, radius: float):
        self.radius = radius

    @property
    def area(self) -> float:
        return math.pi * self.radius ** 2
```

---

## Iterators and Comprehensions

### Comprehensions

Prefer comprehensions for simple transforms. Use explicit loops when the logic needs `if/else` branching or side effects:

```python
# ✅ Clear — single transform + filter
names = [u.name for u in users if u.is_active]

# ✅ Dict comprehension
lookup = {u.id: u for u in users}

# ✅ Set comprehension
unique_tags = {tag for post in posts for tag in post.tags}

# ❌ Nested comprehension that requires mental parsing
result = [f(x) for x in [g(y) for y in items if h(y)] if p(x)]
# → Use intermediate variables or a generator pipeline instead
```

### Generators

Use generators for lazy evaluation over large or infinite sequences. They consume `O(1)` memory:

```python
# ✅ Generator expression — lazy, memory-efficient
total = sum(order.amount for order in orders)

# ✅ Generator function — for complex logic
def read_chunks(path: str, size: int = 8192):
    with open(path, 'rb') as f:
        while chunk := f.read(size):
            yield chunk
```

### `itertools`

Reach for `itertools` before rolling your own iteration logic:

| Function          | Purpose                         |
| :---------------- | :------------------------------ |
| `chain`           | Concatenate iterables           |
| `islice`          | Slice without materializing     |
| `groupby`         | Group sorted items by key       |
| `product`         | Cartesian product               |
| `starmap`         | `map()` with argument unpacking |
| `batched` (3.12+) | Fixed-size chunks               |

---

## Context Managers

Use `with` for any resource that needs cleanup — files, locks, connections, transactions:

```python
# ✅ Automatic cleanup
with open('data.json') as f:
    data = json.load(f)

# ✅ Multiple resources
with open('in.txt') as src, open('out.txt', 'w') as dst:
    dst.write(src.read())
```

### Writing Context Managers

For simple cases, use `contextlib.contextmanager`:

```python
from contextlib import contextmanager

@contextmanager
def temporary_directory():
    path = tempfile.mkdtemp()
    try:
        yield path
    finally:
        shutil.rmtree(path)
```

For classes, implement `__enter__` and `__exit__`. For async resources, use `async with` and `__aenter__` / `__aexit__`.

---

## Async Patterns

### `async`/`await`

Prefer `async`/`await` for I/O-bound concurrency:

```python
import asyncio

async def fetch_user(session: aiohttp.ClientSession, uid: str) -> User:
    async with session.get(f'/api/users/{uid}') as resp:
        resp.raise_for_status()
        return User(**(await resp.json()))
```

### Concurrent Operations

| Pattern                     | Behavior                             | Use When                |
| :-------------------------- | :----------------------------------- | :---------------------- |
| `asyncio.gather(*coros)`    | Runs concurrently, fails fast        | All must succeed        |
| `asyncio.TaskGroup` (3.11+) | Structured concurrency, auto-cancel  | Prefer over `gather`    |
| `asyncio.to_thread(fn)`     | Offloads blocking I/O to thread pool | Wrapping sync libraries |

### Rules

- **Never mix `asyncio.run()` with a running loop** — it raises `RuntimeError`
- **Never call blocking I/O in an async function** without `to_thread` — it blocks the entire loop
- **Use `async for`** for async iteration and **`async with`** for async context managers
- **Cancellation:** Handle `asyncio.CancelledError` explicitly when cleanup is needed

---

## Structural Pattern Matching (3.10+)

`match`/`case` is a structural destructuring tool, not a switch statement. It combines type checking, attribute extraction, and branching in one expression:

```python
match command:
    case {"action": "move", "direction": str(d)}:
        move(d)
    case {"action": "quit"}:
        sys.exit(0)
    case Point(x=0, y=y):
        print(f"On y-axis at {y}")
    case [first, *rest] if len(rest) > 2:
        process_batch(first, rest)
    case _:
        raise ValueError(f"Unknown command: {command}")
```

### Key Facts

| Fact           | Detail                                                               |
| :------------- | :------------------------------------------------------------------- |
| Single subject | `match` targets exactly one variable — no scattered conditions       |
| Destructuring  | Sequences, mappings, and class attributes are unpacked declaratively |
| Guards         | `case X if condition:` for fine-grained filtering                    |
| Wildcard `_`   | Can appear multiple times in one pattern (unlike assignment)         |
| Class matching | Uses `__match_args__` or `@dataclass` for positional patterns        |

> [!WARNING]
> **Strings are NOT sequences in `match`/`case`.** Unlike standard unpacking, `case [x, y]` will never match a two-character string. This is intentional — it prevents a class of bugs where strings are accidentally iterated as character arrays.

---

## Type System

Python's type system is gradual — annotations are optional but invaluable for static analysis. The runtime remains dynamic; types don't enforce anything at execution time.

### Annotation Rules

- **Annotate function signatures** — parameters and return types
- **Let inference handle locals** — don't annotate obvious assignments
- **Use modern syntax** — `int | str` not `Union[int, str]`, `str | None` not `Optional[str]` (3.10+)

### Key Constructs

| Construct                           | Use                                                                                 |
| :---------------------------------- | :---------------------------------------------------------------------------------- |
| `type Vector = list[float]` (3.12+) | Type alias — equivalent name for a type                                             |
| `NewType('UserId', int)`            | Distinct subtype — a raw `int` won't satisfy `UserId`                               |
| `Protocol`                          | Structural subtyping ("static duck typing")                                         |
| `@runtime_checkable`                | Enables `isinstance` checks against a `Protocol`                                    |
| `TypeIs` (3.13+)                    | Preferred over `TypeGuard` — supports intersection narrowing and negative narrowing |
| `TypeGuard`                         | Older narrowing — only narrows in the positive branch                               |

### `Any` vs `object`

`Any` disables type checking. `object` is type-safe — it requires narrowing before use. Prefer `object` when you mean "anything" but still want the checker engaged.

### The `TYPE_CHECKING` Pattern

Avoid import cycles by guarding type-only imports:

```python
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from expensive_module import HeavyType

def process(item: HeavyType) -> None:
    ...
```

---

## String Handling

### f-strings (Default)

f-strings are the standard for string interpolation. They are fast, readable, and support format specs:

```python
name = "world"
print(f"Hello, {name!r}")       # repr
print(f"Pi is {math.pi:.4f}")   # format spec
print(f"{value:>10,}")          # right-aligned with comma separator
```

### Template Strings (3.14+)

T-strings (`t"..."`) produce a `Template` object instead of a `str`, enabling handler-based interpolation. Use them when interpolating untrusted input — f-strings evaluate eagerly and cannot be intercepted:

```python
from string.templatelib import Template, Interpolation

def sanitized_sql(template: Template) -> tuple[str, tuple]:
    parts, params = [], []
    for item in template:
        if isinstance(item, str):
            parts.append(item)
        elif isinstance(item, Interpolation):
            parts.append("?")
            params.append(item.value)
    return "".join(parts), tuple(params)

query, params = sanitized_sql(t"SELECT * FROM users WHERE id = {user_input}")
```

### Legacy

- `str.format()` — use only when format spec is dynamic (known at runtime, not write-time)
- `%` formatting — legacy only. Do not use in new code.

---

## Error Handling

### Specific Exceptions

Catch specific exceptions. Never use bare `except:` or `except Exception: pass`:

```python
# ✅ Specific, with context
try:
    config = load_config(path)
except FileNotFoundError:
    raise ConfigError(f"Config not found: {path}") from None
except json.JSONDecodeError as e:
    raise ConfigError(f"Malformed config at {path}: {e}") from e

# ❌ Silent swallow — hides every possible failure
try:
    config = load_config(path)
except:
    pass
```

### Exception Chaining

Use `from` to preserve the causal chain. Use `from None` to intentionally suppress it:

```python
# Chain — preserves original traceback
raise AppError("operation failed") from original_error

# Suppress — when the original is noise for the caller
raise AppError("not found") from None
```

### Custom Exceptions

Define domain-specific exceptions. Keep hierarchies shallow:

```python
class AppError(Exception):
    """Base for application errors."""

class ValidationError(AppError):
    def __init__(self, field: str, message: str):
        self.field = field
        super().__init__(f"{field}: {message}")
```

---

## Anti-Patterns

| Anti-Pattern             | Description                                          | Remedy                                         |
| :----------------------- | :--------------------------------------------------- | :--------------------------------------------- |
| **Mutable default args** | `def f(x=[]):` — shared across calls                 | Use `None` sentinel                            |
| **Bare `except`**        | `except:` catches `SystemExit`, `KeyboardInterrupt`  | Catch specific types                           |
| **Shadowing builtins**   | `list = [1, 2, 3]`                                   | Use descriptive names                          |
| **God class**            | Monolithic class with 20+ methods                    | Decompose into functions and smaller classes   |
| **Stringly typed**       | Using strings where enums or types belong            | `enum.Enum`, `NewType`, `Literal`              |
| **Deep nesting**         | 4+ levels of indentation                             | Early returns, guard clauses, helper functions |
| **`import *`**           | Pollutes namespace, breaks tooling                   | Explicit named imports                         |
| **Type: ignore spam**    | Silencing every type error                           | Fix the types or narrow properly               |
| **Overusing classes**    | Classes with no state (just methods)                 | Use plain functions                            |
| **`isinstance` chains**  | Long `if isinstance(x, A) ... elif isinstance(x, B)` | `match`/`case` or dispatch                     |

---

## Tooling

```bash
ruff check . --fix    # Lint + autofix
ruff format .         # Format
mypy .                # Type check (strict)
pyright .             # Alternative type checker
pytest                # Run tests
pytest --cov          # Coverage
uv run ...            # Fast dependency management and execution
```

---

## Quick Reference

- **4-space indent** — never tabs, never 2-space
- **`snake_case`** — functions, variables, modules
- **`PascalCase`** — classes only
- **`if x is None`** — not `== None`
- **`if not seq`** — not `len(seq) == 0`
- **`@dataclass`** — not manual `__init__`
- **`with`** — for any resource needing cleanup
- **Comprehensions** — for simple transforms, loops for complex logic
- **Generators** — for lazy iteration over large data
- **f-strings** — default interpolation; T-strings for untrusted input
- **`int | str`** — not `Union[int, str]` (3.10+)
- **`*` separator** — force keyword-only args when order is ambiguous
- **Never shadow builtins** — `id`, `type`, `list`, `dict`, etc.
- **Never `except: pass`** — catch specific, handle or propagate

> These idioms refine but are subordinate to the [Code-Edit Constraints](../../ambient.md#code-edit-constraints).