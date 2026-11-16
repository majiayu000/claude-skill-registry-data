---
name: python-style
description: Use when choosing a type annotation, deciding what shape a record takes as it crosses a boundary, or asking whether a comment belongs here. Owns the 3.13 house interpreter floor for a new deployable project and a distributed package's floor being its consumers', `X | None` over `Optional`, the ban on `from __future__ import annotations`, immutable collection types, when a type error may be silenced inline, the rule that a fixed-shape record is a declared type rather than a bare `dict` or tuple, which builtin represents an exact decimal quantity, an instant and an identifier, and a closed set of constants as an `Enum`. What to log and which scope logs it is `python-logging`; whether a constrained scalar also earns a named type of its own belongs to the architecture family; the error classes themselves are `exception-catalog`.
---

# Python Style

Project-wide rules that are stricter than CPython's defaults and hold **whatever the architecture is** —
a hexagonal app, a flat-layered worker, or a standalone script. Two subjects: what the types look like,
and where a comment is warranted.

## When to use vs. neighbours

- Writing or changing any annotation, or any comment → this skill.
- Any log call, event name or logging configuration → `python-logging`.
- One class per module, `__all__`, the `__init__.py` re-export contract, import forms →
  `python-packaging`.
- Deriving a concrete class or module name → `naming`; deriving a concrete artifact *path* in a
  hexagonal project → `hex-conventions`, in the `pyhouse-hex` plugin.
- The exception classes themselves → `exception-catalog`.
- Where a module lives and what may import it → `hex-architecture` (in the `pyhouse-hex` plugin) or
  `flat-layered` (in `pyhouse-flat`), whichever style the project uses.
- The shape of a specific artifact → its own skill. This skill is consulted **alongside** them.

## Typing

### `X | None`, not `Optional[X]`

```python
# yes
name: str | None = None


def find(id: UUID) -> Foo | None: ...


# no
from typing import Optional

name: Optional[str] = None
```

PEP 604 union syntax is the default. `Union[A, B]` is equally banned — write `A | B`. This holds
everywhere, validation models included.

### Never `from __future__ import annotations`

Do not add this import to any module. Projects in this style rely on **runtime annotation
introspection** — the validation library, dependency-injection providers, dataclass `__post_init__`
checks, ORM/Core column inference. Stringified annotations break those tools silently, and the failure
shows up as a mis-parsed field rather than an error. Modern runtimes give PEP 604 syntax without it.

If a third-party tool tells you to add it, the fix is to change the annotation, not to silence the
runtime.

**A self-referential annotation is written as a string literal.** A class that annotates with its own
name — `def satisfies(self, required: "Foo") -> bool` inside `class Foo`, a factory classmethod annotated
`-> "Foo"`, a node whose field is `parent: "Foo | None"` — quotes that one annotation. The name is not
bound until the class statement finishes, so an unquoted reference raises `NameError` at
class-definition time, and the future import that would have deferred it is banned above. Quote only the
self-reference; every other annotation stays bare, so runtime introspection keeps working everywhere it
matters.

### The interpreter floor

**The house floor is Python 3.13.** It is a choice this style makes, not a requirement the templates
impose: one floor across every new project means every reader meets one set of forms. The catalogue's
templates are written against it and use the newer forms freely — `enum.StrEnum`, `datetime.UTC`,
PEP 695 `type` aliases and generic syntax, `AsyncGenerator[None]` with its defaulted send type — but
none of them needs 3.13 itself; they type-check and lint clean against 3.12 as well.

**The house floor applies to a new project. An existing project below it is not a violation.** It keeps
the floor it has, and the catalogue's rules apply to it unchanged. The templates type-check and lint
from 3.12 up; a project below 3.12 adapts the few newer forms they use — PEP 695 `type` aliases and
generic syntax (`def f[T](…)`) become `TypeAlias` and `TypeVar`, and below 3.11 `enum.StrEnum` and
`datetime.UTC` become their older spellings — and keeps everything else as written. **A floor is raised
deliberately, never lowered.** Raising it is a decision — reaching the house floor, a library whose own
minimum sits higher, or a form the project wants from a newer interpreter — taken once, for the whole
project, as its own change, never in half the code.

**The house floor binds what the project deploys; a distributed package's floor is its consumers'.** A
service or a CLI tool runs on an interpreter the project chooses, so it takes the house floor. A library
or SDK others install runs on whatever interpreter each consumer has, so its floor is the oldest one its
consumers run — which may sit below the house floor — and it writes the few newer forms above in their
older spellings. Everything else here applies to it unchanged.

**The floor is chosen once, at setup, and written down in three settings that must stay in step:**
`requires-python` in the root `pyproject.toml` (`>=3.13`), the linter's `target-version` (`py313`), and
the type checker's `python_version` (`3.13`). All three name the **oldest** interpreter the project must
run on, never the newest one on the developer's machine — a form the linter permits because
`target-version` drifted upward is a form that fails on the deployment runtime. A member of a workspace
never restates them; the root settles them and every member inherits.

### Full coverage on every signature

Every function, method and `__init__` parameter is fully annotated, return type included. `-> None` is
required on a procedure. Lambdas inside business logic are forbidden — use a named function; a lambda in
`dataclasses.field(default_factory=...)` is fine because it carries no annotations.

This includes test code: a fixture annotates what it yields (`-> AsyncIterator[T]`), a builder annotates
its return, a parametrize hook types its argument. Type-checking `tests` at parity with `src` is only
possible because of this.

### Type suppressions

A type error is fixed, not silenced: restate the type, narrow with a runtime guard, or `cast` after a
guard the checker cannot follow. **An inline type-ignore is the last resort, where the checker is wrong
and the code cannot be restated to satisfy it** — in source and tests alike, it names the one error code
it silences and carries the reason on the same line (`# type: ignore[<code>]  # <why>`), so it stops
hiding the next error in that expression. A package that ships no type information is never silenced
inline: it gets one per-package override in the type checker's configuration (`python-toolchain`).

### `Any` only at raw external boundaries

`typing.Any` is permitted only where data has not yet been parsed:

- raw deserialized JSON before validation;
- a third-party SDK return type not yet narrowed.

Related convention: when collecting heterogeneous values, use `dict[str, object]`, not `dict[str, Any]`
— as in `context: dict[str, object]` on an exception — because `object` forces explicit narrowing at the
point of consumption.

Past the boundary — in business logic, a handler body, the body of a job — `Any` is forbidden. If a type is
hard to express, introduce a `type` alias or a small dataclass.

### A `type` alias for repeated complex types

```python
from uuid import UUID

type FooKey = tuple[UUID, int]
```

The PEP 695 `type` statement, not `typing.TypeAlias` — the statement is the form the house floor gives,
and it is evaluated lazily, so an alias may name a class defined further down. Use one whenever the same composite — a `tuple[…, …]`, a `dict[str, frozenset[UUID]]`, a callable
signature — appears in more than one signature. Place it at the top of the module owning the concept,
after imports and before classes, and re-export it via `__all__` if it crosses module boundaries. For a
module-internal one-shot type, write the type out; a premature alias hides intent.

### Immutable collections on shared value types

A type that is frozen, hashed, compared, or passed across a boundary uses **immutable** collections, so
it cannot be mutated by a holder that was only meant to read it.

| Mutable | Immutable equivalent |
|---|---|
| `list[T]` | `tuple[T, ...]` when ordered, `Sequence[T]` for a read-only view |
| `set[T]` | `frozenset[T]` |
| `dict[K, V]` | `Mapping[K, V]` for a read-only view, a frozen dataclass for a fixed-shape record |

```python
@dataclass(frozen=True)
class Foo:
    id: UUID
    tags: frozenset[str]
    items: tuple[Item, ...]
```

Conversion happens at the boundary: the caller converts — `tags=frozenset(payload.tags)`,
`items=tuple(item_inputs)`. A wire schema may hold `list[...]`, the validation library's natural shape;
the frozen type stores the frozen form.

Ordinary procedural code may use mutable collections **internally** — loop accumulators, row building —
but anything crossing into a frozen type is converted first.

### A record that crosses a boundary is a declared type

A value that leaves the scope that built it — returned from a client, handed to the function a job runs, passed
between packages, stored on another object — arrives somewhere that has to know its shape. A bare
`dict`, a bare tuple or a forwarded `**kwargs` does not carry that shape: the receiving side learns the
keys by reading the sender, the checker verifies nothing, and a renamed key fails at the line that
reads it rather than at the line that changed it.

**Anything with a fixed set of named fields is declared once, as a type, and passed as that type.**
The declaration is a frozen dataclass in the ordinary case — the form the table above already names for
a fixed-shape record — or the validation library's model where the same boundary is also where the data
is parsed.

| Being passed | Declare instead |
|---|---|
| a `dict` whose keys are known when the code is written | a frozen dataclass, or a validation model at a parse boundary |
| a tuple whose positions mean different things | a frozen dataclass; a `type` alias only when it is genuinely n of one thing |
| `**kwargs` forwarded and unpacked further down | named parameters, or one parameter of a declared type |

A `dict` is still the right type where the **keys are data**: a lookup keyed by id, a count per
category, a payload whose keys are not known until runtime. The rule is about a *record* — a fixed set
of named fields — not about every mapping. `dict[str, object]` for heterogeneous values, above, is that
case and is unaffected.

`TypedDict` declares the keys but leaves the object a `dict`: nothing is checked at construction, and
there is no type to hang an invariant or a method on. Use it only where a mapping's shape must be
described without changing the object — a third-party call that requires a literal `dict` — never as
the default record form. `NamedTuple` has no use here at all; a frozen dataclass gives the same
immutability without the positional half nobody wanted.

Conversion happens at the boundary, the same way the collection conversions above do: the raw form is
parsed or constructed into the declared type at the edge, and the declared type is what travels inward.

### Which builtin represents which kind of value

A scalar whose kind constrains its representation takes the type that carries the constraint, not the
one that is shortest to write:

- **An exact decimal quantity is `decimal.Decimal`** — money, a rate, anything summed, compared for
  equality, or shown to someone who will check the arithmetic. A binary float cannot represent most
  decimal fractions exactly, so the same total added in a different order is a different number and an
  equality check on it is a coin toss. A genuine measurement, carrying no exactness claim, stays a
  `float`.
- **An instant is a timezone-aware `datetime`.** A naive one carries no offset, so two of them cannot
  be compared or subtracted correctly once anything runs in a second zone, and every store it passes
  through is free to reinterpret it. A calendar day with no instant in it stays a `date`.
- **An identifier this project mints is `uuid.UUID`, not `str`.** The string form belongs at the edges
  — a log field, a path parameter, a wire model — and the conversion happens there. Inside, a swapped
  identifier is then a type error rather than a lookup that quietly returns nothing. **An identifier
  issued elsewhere** — a webhook's event id, a broker's message id, an identity provider's subject, a
  store's own sequence included — keeps its issuer's form, since nothing promises it parses as a UUID,
  and is a distinct type over that form (a `NewType` over `str` or `int`, say), never the bare builtin.

These are representation rules: they say which builtin holds the value. **Whether a constrained scalar
also earns a named type of its own** — an amount that must be non-negative, a code that must match a
pattern — is an architecture question this skill does not answer. The hexagonal family answers it with
a value object whose invariant is checked at construction (`hex-domain-model`, in the `pyhouse-hex`
plugin); a service with no domain layer checks it where the value enters and keeps the scalar.

### A closed set of named constants is an enum

A fixed set of named values — a status, a kind, a mode — is an `enum.Enum`, and a `StrEnum` when its
values are strings (`class Foo(str, Enum)` below 3.11). **Never a class of bare attributes** (`class Status: ACTIVE = "active"`): nothing
stops a value outside the set, the checker cannot tell a status from any other string, and there is no
iteration over the members. This holds in every module, whatever layer it sits in.

### Protocols

- `typing.Protocol` for an interface, where the architecture calls for one at all. (A flat-layered
  service introduces one only when a second real implementation exists; the hexagonal family defines
  ports by default. Each family's own rule is in `flat-layered`, in the `pyhouse-flat` plugin, and
  `hex-domain-ports`, in `pyhouse-hex`.)
- `@runtime_checkable` **only** when `isinstance(x, IProtocol)` is genuinely needed, and never in a hot
  path: it walks the protocol's attributes on every call.
- A protocol's method signatures carry full annotations like any other function. The `...` is the
  **method body**, never a parameter default.

### Validation models

- Model field types use the same `X | None` and PEP 585 generic forms — `list[int]`, `dict[str, str]`,
  not `List[int]` / `Dict[str, str]`. The forms above hold here with no exemption.
- **A constraint is declared on the field it bounds, in the annotation**, so the accepted shape reads
  top to bottom in one pass and a generated schema can be derived from it. Not an imperative validator
  method, and not a default-carrying assignment standing in for a constraint on a field that has no
  default — a field is optional because it has a default, never because declaring the bound was
  awkward. Under the validation library this catalogue's templates bind, that is
  `Annotated[int, Field(ge=1)]` rather than `field: int = Field(default=…)`; under another, it is
  whatever that library declares beside the field.

### Collections from `collections.abc`

| Use | Not |
|---|---|
| `collections.abc.Sequence` | `typing.Sequence` |
| `collections.abc.Mapping` | `typing.Mapping` |
| `collections.abc.Iterable` | `typing.Iterable` |
| `collections.abc.AsyncIterator` | `typing.AsyncIterator` |
| `collections.abc.Callable` | `typing.Callable` |

The `typing.*` aliases have long been deprecated; `collections.abc` keeps imports consistent and avoids a
needless `typing` import.

## Comments

Default to **no comments**. Where one is warranted it is a single short line of non-obvious *why* —
never *what*, never a multi-line block. The scope of that rule is not uniform across the tree:

- **In source**: the rule as stated, unconditionally.
- **In migrations**: the same form. A revision module's docstring is not a comment, and this rule does
  not reach it.
- **In tests**: the same holds inside a test body. Additionally legal is a **multi-line section banner**
  above a group of tests, when it says *what* the group pins and *why* it is pinned that way — which
  behaviour the group stands as evidence for, that the clock is the real one and not a substituted
  double, that both routes have to be exercised. A banner that retells what the tests below it do is
  not this allowance; that is the code said twice, and it is the form that goes stale. *This allowance rests on banners
  having held so far, not on a test of failure, so it carries its withdrawal condition: if a banner is
  ever found lying or silently out of date, the allowance goes and tests fall under the source form.*
- **In every other file the project writes by hand** — `pyproject.toml`, a `Dockerfile`, a compose
  file, a CI workflow, a hook configuration, a script: the source form. A comment a tool generated
  (`alembic.ini` after `alembic init`) is not the project's writing, and this rule does not reach it.

Structural labels are not comments worth writing: no `# Arrange` / `# Act` / `# Assert`, no `# imports`,
no `# helpers`.

**A comment or a docstring names only what outlives it.** The code stays long after the work that
produced it, so a spec, a plan, a design draft, a task list — or a requirement or task number taken from
one — is not cited: such documents are rewritten as the work moves and deleted once it is over, and the
reference then points at nothing. What the reader needs from one is said in the comment's own words, or
not at all. What the repository keeps under a stable number or name may be cited — an issue in its tracker, an
entry in its decisions record, a published standard — and a document counts as kept only where the
repository says so: a spec or a plan committed beside the code is still a working one, numbered and
tracked or not. History is held to the same test by
`git-commit-message` rule 10, in the `pyhouse-git` plugin.

A template's optional-line marker — `# only with …`, `# only where …` — is addressed to whoever copies
the template, not to the project's reader: the line it marks is kept or dropped, and the marker itself
never lands in the project's file.

## Rules

1. Apply the union, generic and runtime-annotation forms in **Typing**, including validation models:
   `X | None` and `A | B`, never `Optional` or `Union`; never `from __future__ import annotations`,
   whose stringified annotations break runtime introspection silently; and a class's reference to its
   own name inside its body as the one quoted annotation.
2. Check complete signature coverage in source and tests — fixtures, builders and test helpers
   included; use named functions for business logic, and no untyped `*args` or `**kwargs` there — a
   declared type is missing.
3. **Settle the interpreter floor once, at setup — for a new project at the house floor of 3.13 or
   above** — and keep `requires-python`, the linter's `target-version` and the type checker's
   `python_version` naming that same oldest supported interpreter. An existing project below the house
   floor keeps its floor; a floor is raised deliberately, never lowered. The house floor binds a
   deployable; a distributed package's floor is the oldest interpreter its consumers run.
4. Restrict `Any` to the two raw-boundary cases; use the documented heterogeneous-value and repeated-type
   forms after parsing.
5. Check shared value types against the immutable-collection table and convert at their boundary.
6. **A record crossing a boundary is a declared type, not a bare `dict`, tuple or forwarded
   `**kwargs`.** A fixed set of named fields is declared once and passed as that type; a mapping whose
   keys are data stays a mapping. `TypedDict` describes a shape without creating a type and is for the
   case that must stay a `dict`; `NamedTuple` is not used.
7. **A scalar takes the builtin that carries its kind** — an exact decimal quantity, an instant with an
   offset, an identifier this project mints as a `UUID` and one issued elsewhere as a distinct type over
   its issuer's form — and converts to a string form only at the edge that needs one. Whether it also earns a named type of its own is the architecture family's question, not this
   skill's.
8. Apply **Protocols** only where the architecture calls for an interface; reserve runtime checking for
   the documented need.
9. Check validation constraints and abstract collection imports against their dedicated typing sections.
10. **A comment is a single short line of non-obvious *why*** — never *what*, never a structural label
    (`# Arrange`, `# helpers`) — applied by location under **Comments**, preserving its
    revision-docstring and test-banner allowances and their stated limits; a test banner says what the
    group pins, never what the tests do. A comment or a docstring names only what outlives it — never a
    spec, a plan or a number taken from one, numbered and tracked or not — under the same section. The
    rule holds in every file the project writes by hand, configuration and scripts included, and never
    reaches a comment a tool generated.
11. **A type error is fixed, not silenced; an inline type-ignore is the last resort, names its error
    code and gives its reason**, and a missing stub is silenced only by a per-package configuration
    override. `cast` narrows only after a runtime guard the checker cannot follow; it never silences
    an error.
12. **A closed set of named constants is an `Enum` — a `StrEnum` for string values (`class Foo(str, Enum)` below 3.11) — never a class of bare
    attributes**, in any module.

## Hard stops

- Writing a log call, an event name or logging configuration → stop, use `python-logging`.
- Asked about one class per module, `__all__`, the `__init__.py` re-exports or an import form → stop,
  use `python-packaging`.
- Choosing what a class, module or variable is called → stop, use `naming`.
- Defining an exception class → stop, use `exception-catalog`.
- Writing the linter's or type checker's configuration → stop, use `python-toolchain`; this skill
  settles the floor it names.
- Asked whether a constrained scalar earns a named type of its own in a hexagonal service → stop, use
  `hex-domain-model`, in the `pyhouse-hex` plugin.
