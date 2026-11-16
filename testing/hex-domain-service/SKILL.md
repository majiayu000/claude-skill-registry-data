---
name: hex-domain-service
description: Use when a domain rule needs state one entity cannot see — a cross-aggregate check, a uniqueness check, does the referenced Bar exist — producing one stateless domain service (`FooUniquenessService`) with injected protocols and `assert_*`, `is_*` or verb methods. Not an entity invariant and not a tunable threshold, both `hex-domain-model`; orchestrating a use case is `hex-application`.
paths: ["**/domain/**"]
---

# Hex — Domain Service

Produces one domain service: a stateless class that orchestrates a domain rule using injected protocols. Domain services live next to the aggregate they primarily concern. See `naming` for identifiers.

## When to use vs. neighbours

- Rule enforceable from one entity's own fields → not a service; use `__post_init__` on the entity (see `hex-domain-model`).
- Rule needs to query other aggregates or a domain capability → this skill.
- Rule is a numeric or boolean threshold (max rows, retention days, quotas) → not a service; model it as the tunable value object in `hex-domain-model`.
- Orchestrating a use case across multiple aggregates → that is a command or query handler, not a service (see `hex-application`).
- The `IFooRepository` or `ICan<Verb>` protocols this service takes in its constructor → `hex-domain-ports`.
- The exception an `assert_*` method raises → `exception-catalog`.
- Binding the service (per-operation) so handlers receive it → `hex-wiring`.
- Testing it with stdlib, `pytest` and the domain package alone → `hex-test-domain`.
- What the service, its methods and its module are called → `naming`.

## Template — stdlib only, collaborators injected as domain ports

```python
from ..exceptions import FooConflictError
from .i_foo_repository import IFooRepository

__all__ = ["FooUniquenessService"]


class FooUniquenessService:
    def __init__(self, repository: IFooRepository) -> None:
        self._repository = repository

    async def assert_name_available(self, name: str) -> None:
        if await self._repository.get_by_name(name) is not None:
            raise FooConflictError("foo name already exists", {"field": "name"})
```

**A service exists because it has collaborators.** Injected protocols on `__init__`, async methods
that touch them — the form above. A pure transformation with nothing to inject (`normalize_*`,
`derive_*`) is not a class at all: a class whose constructor holds no state is a module function
(`python-packaging`), so it is a module-level function in the aggregate's package, or a value object's
own construction (`hex-domain-model`). Nothing binds it in the composition root, because there is nothing
to construct; only when a third-party library does the work does it become a sync capability port
(`hex-domain-ports`).

## Rules

Path: `src/myapp/domain/foos/<class_snake>.py`. Follow `naming` for file and class names.

1. **A domain service is behaviour, not a record.** It holds collaborators, not fields, so it carries no
   data-class decorator and no generated equality or ordering — two services built from the same
   collaborators are not interchangeable values, and comparing them is meaningless.
2. **The constructor takes only domain protocols, other domain services, or value objects.** Never a
   concrete adapter, and never a settings object: a configured number reaches the domain wrapped in a
   tunable value object, so the domain never learns where configuration came from.
3. **Collaborators are private and set once.** Each is stored on a private attribute in the constructor;
   no public attribute, no assignment outside it. A service a caller can re-point is a service whose
   behaviour cannot be read off its construction site. Names follow `naming`.
4. **A method name states what happens on failure** — `assert_*` raises, `is_*`/`has_*`/`can_*` returns
   a boolean, a bare verb computes. The three are not interchangeable and `naming` owns the rule and its
   reason; it applies here because a policy's whole public surface is these methods.
5. **Async if and only if the method reaches IO through an injected protocol.** A pure helper method
   stays sync, so a sync signature is a standing claim that the call performs no IO.
6. **Failures raise a catalogue exception** — `exception-catalog`.
7. **No state beyond the constructor collaborators.** No cache, no counter, no mutable attribute: one
   instance serves every call made through it, so anything it remembers leaks from one call into the
   next.
8. **No transport, persistence or framework code.** The only IO is through the injected protocols, which
   is what lets the service run against hand-written stubs with no infrastructure present. Access the
   service needs to a store or a vendor is added as a method on the domain protocol it already depends
   on, never reached through a session, driver or client.
9. **A uniqueness rule this service asserts is not a guarantee.** A check that reads and then writes
   admits the second concurrent writer — nothing between the read and the write stops it. So the
   `assert_*` method goes in paired with a unique constraint on the same key in the store — the
   template's `name`, held by `uq_foos_name` — which is what actually holds the rule
   (`hex-persistence`). The repository translates that constraint's rejection
   into **the same catalogue class this service raises** — `FooConflictError` here, not the generic
   `ConflictError` — so the caller sees one error, one `code`, whichever side refused (`exception-catalog`
   owns the class). What the service contributes is the earlier refusal with a legible message, not the
   guarantee.

### What a domain service is not

- Not an application handler — services don't know commands, queries, or transactions.
- Not a single-entity validator — that's `__post_init__`.
- Not a dumping ground for unrelated helpers.

## Inlined typing / import rules

See `python-style` and `python-packaging`.

- Stdlib only plus relative domain imports. No third-party. No `from __future__ import annotations`.
- `X | None`. Full annotations on `__init__`, every method, and every parameter.
- No comments unless a non-obvious *why*; one short line max.

## Package wiring

Follow `python-packaging` for module registration and `hex-architecture` for placement. The DI provider that constructs this service is the responsibility of `hex-wiring`, not this skill.

## Hard stops

- The service accumulates methods for rules that do not share a subject — past about four or five → stop, use `coupling`; one service holds one cohesive rule set, and the count is the symptom, not the rule.
- The rule is checkable from one entity's own fields, or is a tunable threshold → stop, use `hex-domain-model`.
- Asked to orchestrate a use case — load, mutate, save across aggregates → stop, that is a handler; use `hex-application`.
