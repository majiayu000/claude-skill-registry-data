---
name: python-patterns
description: 'Guides idiomatic Python design and resource handling. Use when refactoring Python modules, adding type hints, or choosing a concurrency model.'
---

# Python Development Patterns

Idiomatic Python patterns and best practices for building robust, efficient, and maintainable applications.

## When to Activate

- Writing new Python code
- Reviewing Python code
- Refactoring existing Python code
- Designing Python packages/modules

## Critical Rules

- Prefer EAFP (try/except) over LBYL checks.
- Annotate function signatures with type hints.
- Catch specific exceptions, never bare `except`; chain with `raise ... from e`.
- Use `with` for resource management.
- No mutable default arguments; compare to `None` with `is None`.
- No `from module import *`.
- Choose the concurrency model by workload: `asyncio`, threads for I/O, processes for CPU.

## References

Paths are relative to this SKILL.md's directory. Read only the file that matches the task. If a file cannot be read, say so.

- [references/core-idioms.md](references/core-idioms.md)
  Read when: Core Principles (readability, explicit, EAFP), Type Hints, Error Handling Patterns, Context Managers, Comprehensions and Generators.

- [references/design-and-tooling.md](references/design-and-tooling.md)
  Read when: Data Classes and Named Tuples, Decorators, Concurrency Patterns (threads, processes, asyncio), Package Organization, Memory and Performance, Python Tooling Integration.

## Quick Reference: Python Idioms

| Idiom               | Description                                     |
| ------------------- | ----------------------------------------------- |
| EAFP                | Easier to Ask Forgiveness than Permission       |
| Context managers    | Use `with` for resource management              |
| List comprehensions | For simple transformations                      |
| Generators          | For lazy evaluation and large datasets          |
| Type hints          | Annotate function signatures                    |
| Dataclasses         | For data containers with auto-generated methods |
| `__slots__`         | For memory optimization                         |
| f-strings           | For string formatting (Python 3.6+)             |
| `pathlib.Path`      | For path operations (Python 3.4+)               |
| `enumerate`         | For index-element pairs in loops                |

## Anti-Patterns to Avoid

```python
# Bad: Mutable default arguments
def append_to(item, items=[]):
    items.append(item)
    return items

# Good: Use None and create new list
def append_to(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items

# Bad: Checking type with type()
if type(obj) == list:
    process(obj)

# Good: Use isinstance
if isinstance(obj, list):
    process(obj)

# Bad: Comparing to None with ==
if value == None:
    process()

# Good: Use is
if value is None:
    process()

# Bad: from module import *
from os.path import *

# Good: Explicit imports
from os.path import join, exists

# Bad: Bare except
try:
    risky_operation()
except:
    pass

# Good: Specific exception
try:
    risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
```

**Remember**: Python code should be readable, explicit, and follow the principle of least surprise. When in doubt, prioritize clarity over cleverness.
