---
name: hex-domain-model
description: Use when creating or changing a domain entity, value object, enum or filter record — stdlib dataclasses, `__post_init__` invariants, identity versus value equality, when a bare primitive carrying a constraint, a unit or a rule must become a value object instead, and the tunable variant of a value object for an environment-sourced threshold (max rows, retention days), which is neither a service nor a settings class. A rule needing another aggregate's state is `hex-domain-service`; the wire model is `hex-restapi-schema`.
paths: ["**/domain/**"]
---

# Hex — Domain Model

The four data shapes of the domain layer. They share one substrate — stdlib only, no third-party
imports — and a change that adds a capability usually adds several of them together,
which is why they live in one place.

## When to use vs. neighbours

Which of this skill's shapes a thing is → Choosing a shape, at the head of Rules. Outside it:

- The interface a repository or a capability must satisfy → `hex-domain-ports`.
- A rule needing another aggregate's state, or a domain capability → `hex-domain-service`.
- The single error catalog → `exception-catalog`.
- A DTO crossing the application boundary → `hex-application`. A filter record may be reused there; the query DTO wraps it, plus the caller's scope where the caller is authenticated.
- The request or response model on the wire → `hex-restapi-schema`; a domain type is never serialized straight out.
- Persistence of any of these → `hex-persistence` (a relational store) or `hex-store-repository` (a client-style store).
- The settings class the tunable variant's values come from → `python-settings`; the lifetime rules its provider follows → `hex-wiring`; the provider itself is shown beside the template.
- Testing an invariant, identity equality or the pinned enum member set → `hex-test-domain`.
- What the class and its module are called → `naming`; one class per module and the re-export → `python-packaging`.

## Template(s) — stdlib dataclasses and enums

### Entity

```python
from dataclasses import dataclass
from uuid import UUID

from ..exceptions import ValidationError

__all__ = ["Foo"]


@dataclass
class Foo:
    id: UUID
    name: str
    note: str | None = None

    def __post_init__(self) -> None:
        if not self.name:
            raise ValidationError("name must be non-empty", {"field": "name"})

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Foo):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
```

Every other aggregate — `Bar`, or `Baz` in `hex-store-repository`'s key-value example — has this same
form with its own fields, in its own subdomain package. `note` exists to show an optional field — one a
partial update may leave or set, and a store round trip carries as `None`; an entity with no
such field has none.

### Value object — standard case (value equality across all fields)

```python
from dataclasses import dataclass

from ..exceptions import ValidationError

__all__ = ["FooQuota"]


@dataclass(frozen=True)
class FooQuota:
    field_a: str
    field_b: int

    def __post_init__(self) -> None:
        if self.field_b < 0:
            raise ValidationError("field_b must be non-negative", {"field": "field_b"})
```

The `@dataclass(frozen=True)`-generated `__eq__` / `__hash__` compare all fields. Do not override them
in the standard case.

When a value object stores both a raw input and a normalized form — an email as typed and its
lowercased form — it overrides `__eq__` and `__hash__` to compare the normalized field only; otherwise
two semantically equal values compare unequal.

### Value object — tunable variant (configuration the domain consumes)

A value object can serve as the domain-shaped view of an environment-tunable threshold (max upload
size, max page size, retention days). The form is identical — frozen dataclass, primitive fields, no
methods. For the file and class names, see `naming`.

```python
from dataclasses import dataclass

__all__ = ["FooRetentionTunable"]


@dataclass(frozen=True)
class FooRetentionTunable:
    retention_days: int
```

No field carries a default: the value is the deployment's, and a default here would turn a missing
setting into a silent wrong answer (`python-settings` rule 5).

Distinguishing characteristics:

- Sourced from a settings class at the composition root — a provider of its own reads each field off
  the settings object and passes it. The binding, an add-on to `hex-wiring`'s base composition root, is
  process-lifetime; `FooSettings` stands for whichever settings class declares the field
  (`python-settings`), bound in `SettingsProvider` like any other:

```python
class FoosProvider(Provider):
    @provide(scope=Scope.APP)
    def foo_retention_tunable(self, settings: FooSettings) -> FooRetentionTunable:
        return FooRetentionTunable(retention_days=settings.foo_retention_days)
```

- Injected into domain services and application handlers, never into entities. Entities do not read
  tunables; services do.
- Every value-object rule still applies: frozen, no methods, primitive or VO fields only. Which
  builtin each primitive field takes — an exact decimal quantity, an instant with an offset, an
  identifier — is `python-style`'s.

Use this variant only when the value carries no domain meaning beyond "this is a knob to turn". If it
participates in the ubiquitous language — a `FooTotal`, a `RetentionWindow` with behaviour — it is an
ordinary value object.

### Enum — `StrEnum` (the default, for string-valued sets)

```python
from enum import StrEnum

__all__ = ["FooStatus"]


class FooStatus(StrEnum):
    ALPHA = "ALPHA"
    BETA = "BETA"
```

An enum may carry a pure method over its own values — ordering, ranking, membership — with no IO and
no other aggregate; the rank-ordered `Role` in `hex-restapi-auth` is the worked one, its self-reference
quoted because the catalogue bans `from __future__ import annotations`.

A set whose values are genuinely numeric is a plain `Enum` of the same form (`python-style` rule 12).

### Filter sort enum

`domain/foos/foo_sort.py`, beside the filter that imports it (`hex-conventions`). One member per ordering
the list read offers, each naming a column and a direction; the repository maps every member to its
ordered column (`hex-persistence`).

```python
from enum import StrEnum

__all__ = ["FooSort"]


class FooSort(StrEnum):
    CREATED_AT_DESC = "created_at_desc"
    CREATED_AT_ASC = "created_at_asc"
    NAME_ASC = "name_asc"
```

### Filter record

```python
from dataclasses import dataclass

from .foo_sort import FooSort

__all__ = ["FooListFilter"]


@dataclass(frozen=True)
class FooListFilter:
    name: str | None = None
    sort: FooSort = FooSort.CREATED_AT_DESC
    limit: int = 50
    offset: int = 0
```

## Rules

### Choosing a shape

Inside this skill, pick by what the thing *is*:

- A thing with a UUID and a lifecycle → **Entity**.
- An immutable type defined by its content, or a primitive that carries a constraint, a unit or a rule → **Value object**.
- A closed set of named values → **Enum**. A set whose values are loaded at runtime, from
  configuration or a store, is not closed → a **Value object**, with a lookup repository behind a port
  (`hex-domain-ports`).
- A read-side parameter bag passed to a repository `list`/`count` → **Filter record**.
- An environment-tunable threshold the domain consumes (max rows, retention days, quotas) → the **tunable
  variant** of a value object, not a service and not a settings class.

A predicate over a field carried by **both** the entity and a read-model of the same aggregate is a
**module-level function in the aggregate's package**, taking the field values as parameters — never the
same method written once per type, which drifts, nor a shared base, which the entity and value-object
rules forbid.

### Entity

1. **An entity is mutable and stays mutable** — a plain `@dataclass`, never frozen. An entity has a
   lifecycle; freezing it forces every state change through a copy, and the copy is a different object to
   everything holding the old one.
2. **Identity equality is mandatory.** Two entities are equal when their `id` is equal and for no other
   reason, and the hash agrees. Field-wise equality makes a loaded row and the same row after an edit two
   different foos, so a set or a dict keyed by entity silently grows duplicates.
3. **Invariants are checked at construction, in one place** — `__post_init__` under the dataclass
   substrate — one raise per rule, using `exception-catalog` for the error class. A rule enforced at the
   call site instead is a rule the next call site forgets; omit the hook entirely when there are no
   invariants.
4. **Cross-aggregate rules do not go here.** Uniqueness, authorization, "does referenced X exist" → a
   domain service (`hex-domain-service`). Tunable thresholds → the tunable variant above. An entity only
   checks invariants it can see from its own fields.
5. **No inheritance.** No base classes, no `ABC`. Compose by holding other domain objects.
6. **Row timestamps are never entity fields.** `created_at` / `updated_at` are a DB-managed table
   convention. A read that needs them returns a read-model DTO projected from the row.

### Value object

1. **A primitive carrying a constraint, a unit or a rule is a value object, not a bare field.** The
   test is whether the value can be wrong on its own terms: a string that must match a form, a number
   that must stay in a range or is denominated in something, a pair of values only meaningful together.
   Left bare, the check lives at whichever call site remembered it, and the next one does not — which
   is the same failure the entity's `__post_init__` rule exists to prevent, one level down. Give it a
   type and check it once, at construction.
   A primitive with nothing but its builtin type behind it stays a primitive: an opaque identifier, a
   free-text note, a count that is simply a count. Wrapping those buys a name and pays for it in
   conversions at every boundary. Which builtin a scalar takes in the first place — an exact decimal
   quantity, an instant with an offset — is `python-style`'s.
2. **A value object is immutable** — a frozen dataclass. An invariant checked at construction stops
   holding the moment a field can be reassigned, and a mutable value cannot safely be shared or used as a
   key.
3. **No identity field.** No `id: UUID`. If one is called for, this is an entity.
4. **Value equality.** Use the dataclass-generated equality. Override `__eq__` / `__hash__` only for the
   normalized-form escape hatch.
5. **Invariants in `__post_init__`.** Use `exception-catalog` for the error shape. Omit the method
   when there are none.
6. **No inheritance.** Compose, do not inherit.
7. **No cross-aggregate logic.** Anything needing another aggregate's state is a domain service.

### Enum

1. **A member's value is the value that leaves the process**; whether the set is a `StrEnum` or a plain
   `Enum` is `python-style` rule 12. Never an integer enum for codes that are really strings — the
   mismatch surfaces in the database and on the wire, not here.
2. **Member names follow `naming`.** For a `StrEnum` the value is usually identical to the
   name; do not invent lowercased values unless the wire format requires them.
3. **Module boundaries follow `python-packaging`; module names follow `naming`.**
4. **Methods only when pure.** Anything touching another aggregate, IO or external state is not an enum
   method. Methods receive `self` and other enum values only.
5. **No custom base class.** Inherit from `StrEnum` or `Enum` directly; no "abstract enum" hierarchies.
6. **No constants pretending to be enums** (`python-style`).

### Filter record

1. **Frozen dataclass, value equality.** Generated `__eq__` / `__hash__` — never override.
2. **A collection-valued filter field defaults to an empty immutable collection, never to a mutable
   one** — see `python-style` for the collection types. A mutable default would be one object every
   filter in the process shares and can change; an immutable default — `frozenset()` — cannot change,
   so it is safe to share.
3. **Absence of a constraint is expressed as `None`**, never a sentinel value such as `""` or `-1`,
   which the adapter cannot distinguish from a caller who meant it. Annotation forms follow
   `python-style`.
4. **Sort is an enum reference**, never a bare string. See `python-packaging` for its module.
5. **One pagination shape, explicitly.** Either `limit: int` + `offset: int`, both defaulted, or
   `cursor: str | None`. Never both. If it is not stated which, ask. **The default page size is the
   project's decision, not the catalogue's** — pick one bound, state it once, and keep every filter in
   the service on it.
6. **No methods.** A filter record is a passive data bag. Anything computed — translating a sort key to
   a SQL column, say — belongs in the repository adapter.
7. **No business invariants.** A repository receives whatever the caller passed; range and authorization
   checks live in the query handler. Default to no `__post_init__` at all.

## Inlined typing / import rules

These hold for all four shapes; the full rules are `python-style` and `python-packaging`.

- **Stdlib only**, plus relative domain imports. No third-party libraries — no Pydantic, no SQLAlchemy.
  The usable set is `dataclasses`, `datetime`, `decimal`, `enum`, `uuid`, `collections.abc`, `typing`;
  an enum module normally needs only `enum`.
- **No `from __future__ import annotations`**, anywhere in the project.
- `X | None`, never `Optional[X]`. Collection fields are `frozenset[T]` / `tuple[T, ...]`, never `set` /
  `list`.
- **Full annotations** on every field and every method signature, including `-> None` on
  `__post_init__`.
- Default to no comments. Add one only when the *why* is non-obvious, one short line — never a
  multi-paragraph docstring.

## Package wiring

Follow `hex-architecture` for file placement and `python-packaging` for module exports, package re-exports,
and imports, including the module-level predicate function above.

## Hard stops

- Asked for behaviour that needs another aggregate's state → stop, use `hex-domain-service`.
- Asked for repository methods or persistence on any of these → stop, use `hex-domain-ports` for the interface and `hex-persistence` for the adapter.
- Asked for a filter-record method that translates the filter to SQL → stop, use `hex-persistence`.
- A filter record is asked to validate cross-aggregate state, or to range-check its own fields → stop, use `hex-application`.
- Asked for enum values persisted to a SQL column → stop, use `hex-persistence` for the column type and its mapping; the enum still belongs here.
