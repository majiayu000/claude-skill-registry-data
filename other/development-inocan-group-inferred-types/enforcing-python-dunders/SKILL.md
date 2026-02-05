---
name: enforcing-python-dunders
description: >
  Ensure Python classes include appropriate, developer-friendly dunder methods—especially __repr__ and __str__.
  Use when: (1) Writing or modifying Python class definitions in .py files, (2) Refactoring existing Python classes, (3) Adding or improving __repr__, __str__, or natural arithmetic/comparison/container dunders.
  Do NOT use for: tests, fixtures, mocks, stubs, non-Python files (YAML, JSON, TOML), auto-generated code vendor libraries, or when user explicitly asks not to modify dunders.
  Ignored paths: tests/, *_test.py, test_*.py, .venv/, build/, dist/, migrations/, __init__.py.
---

# Python Dunder Method Enhancer

## Overview

This skill ensures Python classes include appropriate, developer-friendly dunder methods. It prioritizes `__repr__` and `__str__` but also adds other dunder methods when they meaningfully improve code clarity and ergonomics.

---

## Files and Directories to Ignore

This skill must NOT modify:

**Test directories:**
- `tests/`, `test/`, `__tests__/`

**Test file patterns:**
- `*_test.py`, `test_*.py`, `conftest.py`

**Virtual environments:**
- `.venv/`, `venv/`, `env/`, `.env/`

**Build artifacts and caches:**
- `build/`, `dist/`, `egg-info/`
- `.mypy_cache/`, `.pytest_cache/`, `__pycache__/`

**Auto-generated and vendor code:**
- `migrations/`, `alembic/`
- Schema files, codegen outputs
- `vendor/`, `third_party/`, `external/`

**Other:**
- `__init__.py` (unless user explicitly requests)

---

## Core Guidelines

### 1. Prioritize `__repr__` and `__str__`

- **Always implement `__repr__`**: Provide a precise, unambiguous developer-oriented representation
- **Implement `__str__`**: Provide a readable, user-friendly representation
- If only one can be implemented, implement `__repr__` and let `__str__` fall back to it unless a distinct human-friendly format is genuinely needed

**`__repr__` requirements:**
- Must be unambiguous and developer-focused
- Should ideally be valid Python that could recreate the object
- Format: `ClassName(attr1=value1, attr2=value2)`
- Use the ranking heuristics in `references/field_ranking_heuristic.md` when selecting which fields to include
- Consult the reference to distinguish between high-signal and low-signal fields
- Ensure that large business models produce concise, useful representations (2-5 high-value fields)

**`__str__` requirements:**
- User-friendly display format
- Can be less verbose than `__repr__`
- Should be meaningful to end users
- Use the ranking heuristics in `references/field_ranking_heuristic.md` when selecting which fields to include
- Start with the primary display name, add 1-2 short qualifiers
- Avoid raw IDs unless essential for user identification

### 2. Dunder Methods That Improve Intuition

#### Operator Methods
Implement only when they make objects more natural to use:
- Arithmetic: `__add__`, `__sub__`, `__mul__`, `__truediv__`, etc.
- Comparison: `__eq__`, `__lt__`, `__le__`, `__gt__`, `__ge__`

#### Container-Like Behavior
Only when the object logically represents a collection:
- `__len__`, `__getitem__`, `__setitem__`, `__delitem__`, `__iter__`, `__contains__`

#### Context Managers
Only when objects clearly manage a resource:
- `__enter__`, `__exit__`

### 3. Avoid Overuse & Complexity

Do NOT implement dunder methods that:
- Introduce surprising behavior
- Make objects harder to reason about
- Obscure real meaning or side effects

**Follow the principle of least astonishment.**

### 4. Don't Call Dunder Methods Directly

When writing code that uses objects with dunders:
- Prefer `obj + other` over `obj.__add__(other)`
- Prefer `len(obj)` over `obj.__len__()`
- Prefer `obj[key]` over `obj.__getitem__(key)`

### 5. Use `functools.total_ordering` When Appropriate

If the class implements:
- `__eq__`, AND
- Exactly ONE of: `__lt__`, `__le__`, `__gt__`, `__ge__`

Then apply the `@total_ordering` decorator to generate the rest automatically.

### 6. Document Dunder Implementations

Every implemented dunder method must include:
- A concise docstring describing expectations
- Any edge-case behavior
- The reasoning when overriding default semantics

---

## Forbidden Dunder Methods

**NEVER implement these methods.** They control Python internals, object lifecycle, memory, class creation, async protocol machinery, pickling machinery, or interpreter-level behaviors.

### Absolutely Forbidden
- `__new__`
- `__init_subclass__`
- `__class_getitem__`
- `__getnewargs__`
- `__getnewargs_ex__`
- `__getstate__`
- `__setstate__`
- `__reduce__`
- `__reduce_ex__`
- `__del__`
- `__prepare__`
- `__mro_entries__`

### Async Protocol (Forbidden)
- `__await__`
- `__aiter__`
- `__anext__`
- `__aenter__`
- `__aexit__`

### Descriptor Protocol (Forbidden)
- `__get__`
- `__set__`
- `__delete__`
- `__set_name__`

### Attribute Interception (Forbidden)
- `__getattr__`
- `__getattribute__`
- `__setattr__`
- `__delattr__`
- `__dir__`

### Hashing & Identity (Forbidden)
- `__hash__`
- `__bool__` (too easy to misuse)

---

## Additional Python Guidelines

### Type Hints Mandatory
All dunder methods must include explicit type hints.

### Prefer Immutability When Possible
Favour `frozen=True` dataclasses when mutation isn't required.

### Use `@dataclass` When Appropriate
Let dataclasses supply basic dunder `__init__`/`__eq__`/`__repr__` unless custom behavior is needed.

### Dataclass Conversion Rules

**Do NOT automatically convert an existing non-dataclass into a dataclass.**

Only convert to `@dataclass` when ALL of these are true:
- The class is clearly a simple value object (fields only, no custom lifecycle)
- There is no inheritance, dynamic attributes, or metaclass use
- The user isn't relying on a custom `__init__` that would be overwritten
- The class has no `__slots__` definition
- There are no class-level validators or complex `__post_init__` requirements

**When in doubt, leave the class as-is and add dunder methods manually.**

For new classes, prefer `@dataclass` when:
- The class is explicitly a value object, AND
- It only stores attributes without complex lifecycle or invariants, AND
- No inheritance or dynamic attributes are involved

### `__slots__` Rules
Never add `__slots__` automatically.

Only add `__slots__` when:
- The user explicitly requests it, AND
- The class restricts attributes intentionally

### Truthiness and Hashing

**`__bool__` rules:**
- Do NOT implement `__bool__` unless the class has a single, obvious boolean meaning (e.g., success/failure wrapper, empty/non-empty collection)
- Never infer truthiness from length, internal state, or "seems falsy" heuristics
- When in doubt, omit it entirely—let Python's default behavior apply

**`__hash__` rules:**
- Never implement `__hash__` for mutable classes
- If it's not clearly immutable (e.g., `frozen=True` dataclass, all attributes are read-only), assume it is mutable and leave `__hash__` alone
- If you implement `__eq__` without `__hash__`, Python automatically sets `__hash__ = None` (unhashable)—this is usually correct for mutable objects

### Copy/Clone Behavior
Do not implement `__copy__` or `__deepcopy__` unless:
- The class manages external resources, OR
- The user explicitly requests custom clone semantics

### No Side Effects in Representation Methods
`__repr__` and `__str__` must:
- Never mutate state
- Never perform I/O
- Never log
- Never compute expensive derived values

### Use `__post_init__` for Validation
Validate invariants early and clearly in dataclasses.

---

## Subclassing Rules

When adding or modifying dunder methods on a subclass of a widely used class (standard library or popular third-party), be **extra conservative**:

### 1. Default: Inherit, Don't Override
If the parent class already defines a dunder method, do NOT override it unless:
- There is a clear, domain-specific need, AND
- The new behavior remains compatible with the parent's documented expectations

### 2. Don't Change Core Operation Meanings
Never change the fundamental semantics of:
- Equality and ordering: `__eq__`, `__lt__`, etc.
- Hashing and identity: `__hash__`, `__bool__`
- Container behavior: `__len__`, `__getitem__`, `__contains__`, `__iter__`

### 3. `__repr__` and `__str__` on Subclasses
It is usually safe to provide a more informative `__repr__`/`__str__` on a subclass, as long as:
- They remain truthful and unambiguous
- They do not hide important information already shown by the parent
- They do not rely on side effects or heavy computation
- Prefer to call `super().__repr__()` or `super().__str__()` and extend/augment the result

### 4. Always Call `super()` When Overriding
If the subclass overrides a dunder that the parent already uses internally:
- Call `super()` when appropriate
- Preserve any pre-/post-conditions the base class expects

### 5. No New "Fake" Container or Context Behavior
Do NOT add container dunders or context manager dunders to a subclass unless the parent class already has that role.

### 6. Check Documentation Before Changing
For classes from the standard library or well-known packages (`dict`, `list`, `Path`, `BaseModel`, `DataFrame`, etc.), treat their dunder behavior as part of a public contract.

### 7. When Unsure
If the correct behavior for a dunder on a subclass is unclear or potentially surprising:
- Avoid adding or modifying that dunder
- Leave a comment suggesting human review

---

## Expected Output

When this skill makes changes, it should prefer:

1. **A unified diff patch (git-style)** when editing files in place, OR
2. **A rewritten class definition** with improved dunder methods, if the user is working in a single file snippet.

Avoid long narrative explanations unless explicitly requested by the user. Comments in code are acceptable when rationale is non-obvious.

**Do NOT:**
- Explain what dunder methods are
- Provide tutorial-style commentary
- Ask clarifying questions unless genuinely ambiguous

**Do:**
- Make the edit directly
- Add brief inline comments only where behavior is surprising or non-obvious
- Use type hints and docstrings as the primary documentation

### When No Changes Are Needed

If a class already follows these dunder method guidelines, the skill should:
- Make no edits
- Return a brief confirmation (e.g., "Class already has appropriate dunder methods")
- Or output an empty diff

**Do not rewrite existing correct code.** Do not make style-only edits, reformat methods, or add unnecessary improvements when the class is already "good enough."

---

## Examples (See `references/`)

**Read these files before implementing dunder methods:**

| File | Purpose |
|------|---------|
| `references/examples/good_example.py` | Ideal classes with well-designed dunder methods. Pattern-match from these. |
| `references/examples/bad_example.py` | Anti-patterns to avoid. Check your work against these. |
| `references/examples/subclass_example.py` | How to handle subclasses of common library types (`dict`, `Path`, etc.). |
| `references/dunder_cheatsheet.md` | Quick reference for which dunders to implement, avoid, and how to reason about them. |
| `references/field_ranking_heuristic.md` | Guidelines for selecting high-value fields to include in `__repr__` and `__str__`. |

**When implementing dunders, open the relevant example file first.**

---

### Field Ranking Reference

This skill uses an additional bundled reference document:

- `references/field_ranking_heuristic.md`

This reference describes the domain-agnostic field ranking rules used when selecting which attributes to include in generated `__repr__` and `__str__` methods.

When deciding which fields to display:
- Consult the reference file's priority ranking
- Favor identifiers, human-readable names, and canonical external handles
- Avoid printing large text fields, noisy metadata, or large collections
- Prefer short summaries for complex fields

The logic in this skill should defer to that reference whenever choosing or ranking fields for representations.

---

## Quick Decision Tree

```
Is this Python source code (not tests/mocks/stubs)?
├─ No → Do NOT activate
└─ Yes → Continue
         │
         Does the class already have __repr__?
         ├─ No → Add __repr__ with type hints and docstring
         └─ Yes → Check if it follows best practices
                  │
                  Should this class support comparison?
                  ├─ Yes → Add __eq__ and one comparison op + @total_ordering
                  └─ No → Skip comparison dunders
                          │
                          Is this class container-like?
                          ├─ Yes → Consider __len__, __getitem__, __iter__
                          └─ No → Do NOT add container dunders
                                  │
                                  Does this class manage resources?
                                  ├─ Yes → Consider __enter__, __exit__
                                  └─ No → Do NOT add context manager dunders
```

---

## Summary

When invoked, this skill should:

1. Inspect Python class definitions
2. Add beneficial dunder methods (`__repr__`, `__str__`, and others when appropriate)
3. Avoid touching or generating forbidden dunder methods
4. Improve clarity and Pythonic ergonomics
5. Modify only Python source code—not tests
6. Produce clean, idiomatic, documented results
