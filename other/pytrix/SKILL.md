---
name: pytrix
description: "Knowledge base from \"Python Tricks: The Book\" by Dan Bader. Use when applying Bader's idioms for assertions, decorators, closures, namedtuples, comprehensions, generators, iterators, dict tricks, data-structure choice, and Pythonic style — while coding Python, studying the book, or referencing its concepts."
allowed-tools:
  - Read
  - Grep
argument-hint: [topic, idiom name, or chapter number]
---

# Python Tricks: The Book
**Author**: Dan Bader | **Pages**: ~297 | **Chapters**: 8 | **Generated**: 2026-06-07

## How to Use This Skill

- **Without arguments** — load core idioms below for reference.
- **With a topic** — ask about `decorators`, `namedtuples`, `generators`, `dict merge`, etc.; I find and read the relevant chapter.
- **With a chapter** — ask for `ch06`; I load that specific chapter file.
- **Browse** — ask "what chapters do you have?" for the full index.

When you ask about a topic not in Core Idioms below, I read the relevant chapter file before answering.

---

## Core Idioms & Mental Models

**Assertions are self-checks, not validation (Ch 2).** `assert cond, msg` declares impossible conditions (bugs). Never validate data or guard auth with them — they vanish under `-O`. Never put a tuple in an assert (always truthy).

**Trailing commas everywhere (Ch 2).** End every line in multi-line list/dict/set literals with a comma — clean diffs, no accidental string-concat bugs.

**`with` + context managers for resources (Ch 2).** Implement `__enter__`/`__exit__` or `@contextlib.contextmanager`; guarantees cleanup via `try/finally`.

**Underscores (Ch 2).** `_var` = internal hint (convention); `__var` = real name mangling (`_Class__var`); `__var__` = reserved; `_` = throwaway / last REPL result.

**String formatting rule of thumb (Ch 2).** User-supplied → Template Strings (safe). Else → f-strings (3.6+) or `str.format()`.

**Functions are first-class (Ch 3).** Assign, store, pass, return them. Closures capture enclosing scope — the basis of factories and decorators.

**Decorators = `callable -> callable` (Ch 3).** `@deco` is sugar for `f = deco(f)`; stacking applies bottom-to-top; **always** `@functools.wraps(func)` to preserve metadata. Use for logging/timing/auth/caching.

**`*args`/`**kwargs` collect; `*`/`**` unpack (Ch 3).** In a def they gather (tuple/dict); at a call they spread an iterable/dict.

**Lambdas sparingly (Ch 3).** Fine as a one-off `key=` func; for anything complex use a named function or comprehension.

**`is` vs `==` (Ch 4).** Identity vs equality. Use `is` only for `None`/singletons.

**Always add `__repr__` (Ch 4).** Unambiguous, dev-facing, ideally re-creatable: `f'{self.__class__.__name__}({self.x!r})'`. `__str__` (readable) falls back to it.

**Custom exception hierarchies (Ch 4).** Derive from `Exception`/built-ins; give a module a base error so callers catch the family with one `except`.

**Shallow vs deep copy (Ch 4).** `list(x)`/`copy.copy` shares children; `copy.deepcopy` is fully independent.

**ABCs enforce interfaces at instantiation (Ch 4).** `ABCMeta` + `@abstractmethod` beats `NotImplementedError`.

**Method types (Ch 4).** instance (`self`), `@classmethod` (`cls`, alt constructors/factories), `@staticmethod` (neither, namespaced).

**Class vs instance variables (Ch 4).** Class vars are shared; assigning `self.x` to a class-var name silently shadows it — a classic counter bug (`self.__class__.x += 1`).

**Pick the right data structure (Ch 5).** `dict` (O(1)); `deque` for stacks/queues; `namedtuple`/`typing.NamedTuple` for records; `Counter` for multisets; `frozenset` as keys; `queue.PriorityQueue`/`heapq` for priority. Start with `list`, specialize later.

**Pythonic loops (Ch 6).** Iterate directly; `enumerate()` for index, `dict.items()` for k/v, `range(a, n, s)` for stepped. Avoid `range(len(...))`.

**Comprehensions & generators (Ch 6).** `[expr for x in xs if cond]` is sugar for a build-up loop (also set/dict). Generators (`yield`) and genexprs `(...)` are lazy, memory-efficient iterators; chain them into pipelines. Keep nesting ≤ 1 level.

**Dict tricks (Ch 7).** `d.get(k, default)` over membership checks (EAFP); `{key: fn}.get(k, default)()` for switch/case; `sorted(items, key=...)` for custom order; `{**a, **b}` to merge (right wins). Keys identified by equality **and** hash (`True == 1 == 1.0`).

**Productivity (Ch 8).** `dir()`/`help()`/`dis.dis()` to explore from the REPL; always isolate deps in a `venv`.

---

## Chapter Index

| # | Title | Key Idioms |
|---|-------|-----------|
| [ch01](chapters/ch01-introduction.md) | Introduction | Python Trick philosophy, Pythonic |
| [ch02](chapters/ch02-cleaner-python.md) | Patterns for Cleaner Python | assertions, trailing commas, context managers, underscores, string formatting |
| [ch03](chapters/ch03-effective-functions.md) | Effective Functions | first-class functions, closures, decorators, `*args`/`**kwargs`, lambdas |
| [ch04](chapters/ch04-classes-oop.md) | Classes & OOP | `is`/`==`, `__repr__`, custom exceptions, copy, ABCs, namedtuples, method types |
| [ch05](chapters/ch05-data-structures.md) | Common Data Structures | dict/array/record/set/stack/queue/PQ choice |
| [ch06](chapters/ch06-looping-iteration.md) | Looping & Iteration | loops, comprehensions, slicing, iterator protocol, generators, chains |
| [ch07](chapters/ch07-dictionary-tricks.md) | Dictionary Tricks | `get()`, sorting, dispatch tables, merge, key identity |
| [ch08](chapters/ch08-pythonic-productivity.md) | Pythonic Productivity | `dir`/`help`, virtualenv, bytecode/`dis` |

## Topic Index

- **ABC / abstract base class** → ch04
- **argument unpacking** → ch03
- **array / bytes / bytearray** → ch05
- **assertions** → ch02
- **bytecode / dis** → ch08
- **class vs instance variables** → ch04
- **classmethod / staticmethod** → ch04
- **closures** → ch03
- **comprehensions** → ch06
- **context managers / `with`** → ch02
- **copy (shallow/deep)** → ch04
- **Counter / multiset** → ch05
- **decorators** → ch03, ch02
- **defaultdict** → ch05, ch07
- **deque / stack / queue** → ch05
- **dict default / get** → ch07
- **dict merge** → ch07
- **dict dispatch / switch-case** → ch07
- **exceptions (custom)** → ch04
- **first-class functions** → ch03, ch07
- **f-strings / string formatting** → ch02
- **functools.wraps** → ch03
- **generators / generator expressions** → ch06
- **is vs ==** → ch04
- **iterator protocol** → ch06
- **key funcs / sorting** → ch07
- **lambdas** → ch03
- **name mangling / underscores** → ch02
- **namedtuple / NamedTuple** → ch04, ch05
- **priority queue / heapq** → ch05
- **`__repr__` / `__str__`** → ch04
- **slicing** → ch06
- **`*args` / `**kwargs`** → ch03
- **virtualenv** → ch08
- **yield** → ch06
- **Zen of Python** → ch02

## Supporting Files

- [glossary.md](glossary.md) — all key terms with definitions
- [patterns.md](patterns.md) — all techniques with when/how/trade-offs
- [cheatsheet.md](cheatsheet.md) — quick-reference tables and decision guides

---

## Scope & Limits

Covers the book content only (Python 2/3-era idioms; some notes flag 3.5+/3.6+ features). For current Python versions, dataclasses, and modern typing, combine with up-to-date docs. For implementation in your codebase, pair with project-specific tooling.
