---
name: Python
slug: python
version: 1.0.1
description: Write reliable Python avoiding mutable defaults, import traps, and common runtime surprises.
metadata: {"clawdbot":{"emoji":"🐍","requires":{"bins":["python3"]},"os":["linux","darwin","win32"]}}
---

## Quick Reference

| Topic | File |
|-------|------|
| Dynamic typing, type hints, duck typing | `types.md` |
| List/dict/set gotchas, comprehensions | `collections.md` |
| Args/kwargs, closures, decorators, generators | `functions.md` |
| Inheritance, descriptors, metaclasses | `classes.md` |
| GIL, threading, asyncio, multiprocessing | `concurrency.md` |
| Circular imports, packages, __init__.py | `imports.md` |
| Pytest, mocking, fixtures | `testing.md` |

## Critical Rules

- `def f(items=[])` shares list across all calls — use `items=None` then `items = items or []`
- `is` checks identity, `==` checks equality — `"a" * 100 is "a" * 100` may be False
- Modifying list while iterating skips elements — iterate over copy: `for x in list(items):`
- GIL prevents true parallel Python threads — use multiprocessing for CPU-bound
- Bare `except:` catches `SystemExit` and `KeyboardInterrupt` — use `except Exception:`
- `UnboundLocalError` when assigning to outer scope variable — use `nonlocal` or `global`
- `open()` without context manager leaks handles — always use `with open():`
- Circular imports fail silently or partially — import inside function to break cycle
- `0.1 + 0.2 != 0.3` — floating point, use `decimal.Decimal` for money
- Generator exhausted after one iteration — can't reuse, recreate or use `itertools.tee`
- Class attributes with mutables shared across instances — define in `__init__` instead
- `__init__` is not constructor — `__new__` creates instance, `__init__` initializes
- Default encoding is platform-dependent — always specify `encoding='utf-8'`
