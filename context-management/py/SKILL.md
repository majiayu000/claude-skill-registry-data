---
name: Python
description: Write reliable Python avoiding mutable defaults, import traps, and common runtime surprises.
metadata: {"clawdbot":{"emoji":"🐍","requires":{"bins":["python3"]},"os":["linux","darwin","win32"]}}
---

## Mutable Default Arguments
- `def f(items=[])` shares list across all calls — use `items=None` then `items = items or []`
- Same for dicts, sets, any mutable — default evaluated once at definition, not per call
- Class attributes with mutables shared across instances — define in `__init__` instead

## Import Traps
- Circular imports fail silently or partially — import inside function to break cycle
- `from module import *` pollutes namespace — explicit imports always
- Relative imports require package context — `python -m package.module` not `python module.py`
- Import order matters for monkey patching — patch before target module imports patched module
- `__init__.py` runs on package import — keep it minimal

## Scope Gotchas
- `UnboundLocalError` when assigning to variable that exists in outer scope — use `nonlocal` or `global`
- List comprehension has own scope, but loop variable leaks in Python 2 — not 3
- `except Exception as e` — `e` is deleted after except block in Python 3
- Default argument values bound at definition — closure over loop variable captures final value

## String Pitfalls
- `is` vs `==`: `is` checks identity, `==` checks equality — `"a" * 100 is "a" * 100` may be False
- f-strings evaluate at runtime — `f"{obj}"` calls `__str__` each time
- `str.split()` vs `str.split(' ')` — no arg splits on any whitespace and removes empties
- Unicode normalization: `'café' != 'café'` if composed differently — use `unicodedata.normalize()`

## Iteration Traps
- Modifying list while iterating skips elements — iterate over copy: `for x in list(items):`
- Dictionary size change during iteration raises RuntimeError — copy keys: `for k in list(d.keys()):`
- Generator exhausted after one iteration — can't reuse, recreate or use `itertools.tee`
- `range()` doesn't include end — `range(5)` is 0,1,2,3,4

## Class Gotchas
- `__init__` is not constructor — `__new__` creates instance, `__init__` initializes
- Method resolution order (MRO) in multiple inheritance — use `super()` correctly or break chain
- `@property` makes attribute read-only unless you add setter
- `__slots__` breaks `__dict__` and dynamic attributes — can't add new attributes
- Mutable class attribute shared by all instances — each instance modifying same list

## Exception Handling
- Bare `except:` catches `SystemExit` and `KeyboardInterrupt` — use `except Exception:`
- `except A, B:` is syntax error in Python 3 — use `except (A, B):`
- Exception chaining: `raise NewError() from original` preserves context
- `finally` runs even on return — return in finally overrides try's return
- `else` in try/except runs only if no exception — often clearer than flag variable

## Numeric Surprises
- `0.1 + 0.2 != 0.3` — floating point, use `decimal.Decimal` for money
- Integer division: `//` always floors toward negative infinity — `-7 // 2` is -4, not -3
- `bool` is subclass of `int` — `True + True == 2`
- Large integers have no overflow — but operations get slow
- `is` fails for large integers — only small ints (-5 to 256) are cached

## File and I/O
- `open()` without context manager leaks file handles — always use `with open():`
- Default encoding is platform-dependent — always specify `encoding='utf-8'`
- `read()` loads entire file to memory — use `readline()` or iterate for large files
- Binary mode `'rb'` required for non-text — Windows line endings differ in text mode

## Concurrency
- GIL prevents true parallel Python threads — use multiprocessing for CPU-bound
- Threading still useful for I/O-bound — network, file operations release GIL
- `async/await` is not threading — single-threaded cooperative multitasking
- `multiprocessing` shares nothing by default — use Queue or Manager for communication
- Daemon threads killed abruptly on exit — may corrupt data
