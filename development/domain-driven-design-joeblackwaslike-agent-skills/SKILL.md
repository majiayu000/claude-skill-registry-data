---
name: domain-driven-design
description: >
  Use when modeling a business domain or structuring a backend around business rules —
  designing aggregates, entities, value objects, domain events, repositories; separating
  reads from writes (CQRS); event sourcing; bounded contexts and ubiquitous language; or
  hexagonal/clean/onion architecture. Triggers on explicit mentions of DDD, CQRS, event
  sourcing, aggregates, bounded contexts, domain modeling — AND implicitly whenever an
  agent is building a non-trivial domain with real invariants, even if the user never
  names a pattern. Teaches strategic + tactical DDD, CQRS, and event sourcing with
  framework-agnostic examples in both TypeScript and Python.
metadata:
  last_updated: "2026-06-10"
---

# Domain-Driven Design

Use this skill to model a business domain *well* — so the code reads like the business,
invariants are enforced in one place, and the architecture survives change. It covers
strategic DDD (carving the problem into bounded contexts), tactical DDD (the building
blocks you write code with), CQRS (splitting reads from writes), and event sourcing
(storing facts instead of state).

**Core principle:** the domain model is the asset. Everything else — the database, the web
framework, the message bus — is a detail that plugs into the model, never the other way
around. When persistence, transport, or framework concerns leak into your domain objects,
the model stops being able to express the business and DDD has failed.

One worked domain — **e-commerce Orders & Fulfillment** — runs through every reference file
so the pieces compose instead of floating as disconnected snippets.

## Before you reach for this: do you even need it?

DDD has a real cost. It pays off when the **domain is complex and the rules are the point**
of the software. It is overkill for a CRUD app whose hard part is the UI or the
integrations, not the business logic.

| Signal | Lean toward |
| --- | --- |
| Rich invariants, workflows, state transitions, domain experts who argue about edge cases | DDD |
| "It's just forms over data" — store it, show it, edit it | Plain CRUD / active record |
| One team, one database, simple lifecycle | Tactical DDD without bounded-context ceremony |
| Multiple teams, multiple meanings of the same word ("order" means different things to sales vs. fulfillment) | Strategic DDD — draw bounded contexts first |
| Reads and writes have wildly different shapes/scale | Add CQRS |
| You need a full audit trail, temporal queries, or "why is it in this state?" | Consider event sourcing |
| You reached for CQRS/ES because they sound rigorous | Stop — read `references/anti-patterns.md` |

If the answer is "plain CRUD," say so and stop. Misapplied DDD is worse than no DDD.

## Route First

Pick the reference that matches the task. Read the most specific one first.

| Task | Read |
| --- | --- |
| Carving the problem into bounded contexts, ubiquitous language, subdomains, context mapping, integrating with other teams/systems | `references/strategic-design.md` |
| Writing the building blocks — entities, value objects, aggregates, domain events, domain services, factories, repositories | `references/tactical-patterns.md` |
| Splitting reads from writes, command handlers, read models, projections | `references/cqrs.md` |
| Storing events as the source of truth, rebuilding state from a stream, snapshots, projections | `references/event-sourcing.md` |
| Layering the codebase — hexagonal / ports & adapters / clean / onion, where each block lives, transaction boundaries | `references/application-architecture.md` |
| A complete, copy-paste-ready bounded context in TypeScript | `references/typescript-examples.md` |
| A complete, copy-paste-ready bounded context in Python | `references/python-examples.md` |
| Recognizing and fixing DDD gone wrong — anemic models, ORM leakage, god aggregates, CQRS/ES cargo-cult | `references/anti-patterns.md` |

## The universal mental model

Hold these five ideas in your head no matter which layer you're working in:

1. **Speak the ubiquitous language.** The names in the code (`Order`, `place`, `ship`,
   `LineItem`, `Money`) are the names the business uses. If a domain expert wouldn't
   recognize a class name, it's wrong. A glossary disagreement is a modeling bug, not a
   wording nitpick.

2. **Make illegal states unrepresentable.** Push rules into types and constructors so an
   invalid object can't be built. A `Quantity` that rejects zero and negatives beats
   scattering `if qty <= 0` across the codebase. Validate at the boundary; trust within.

3. **Protect invariants inside an aggregate.** An aggregate is a consistency boundary: a
   cluster of objects that must always be valid *together*, with one entry point (the
   aggregate root). Outside code never reaches in and mutates a child directly — it calls a
   method on the root, which enforces the rule. One transaction changes one aggregate.

4. **Keep the domain pure.** Entities, value objects, and aggregates have **no** import from
   your ORM, web framework, or message broker. They don't know whether they live in
   Postgres or a JSON file. Dependencies point *inward*: infrastructure depends on the
   domain, never the reverse.

5. **Tell the rest of the system what happened, don't command it.** When something
   meaningful occurs, the aggregate records a **domain event** (`OrderShipped`). Other parts
   of the system react. This decouples the core decision ("ship the order") from its
   consequences (email the customer, decrement inventory, update the read model).

## How the layers fit (end-to-end sketch)

A single write flows like this — every block has a dedicated reference:

```
HTTP / CLI / queue            ← adapter (infrastructure)
  → validate input (Zod / Pydantic at the boundary)
  → ApplicationService.placeOrder(command)        ← use case, opens a transaction
      → repository.load(orderId)                   ← port; adapter hydrates the aggregate
      → order.addItem(...) / order.place()         ← AGGREGATE enforces invariants
      → repository.save(order)                      ← one aggregate, one transaction
      → publish(order.pullEvents())                ← domain events go out
  ← returns an id / DTO, never the aggregate itself
```

Reads skip the aggregate entirely (that's CQRS): a query goes straight to a **read model**
shaped for the screen that needs it. Writes go through the domain; reads come from
projections built off the events. See `references/cqrs.md`.

## Red flags — stop and reconsider

- "I'll just add a getter/setter for every field." → anemic model; logic is leaking out of
  the domain. See `references/anti-patterns.md`.
- "The entity extends the ORM base class." → persistence is now welded to your domain.
- "This aggregate has 14 child collections." → too big; find the real consistency
  boundaries and split. Reference other aggregates by id.
- "I'll update three aggregates in one transaction to keep them consistent." → use eventual
  consistency via domain events instead.
- "Let's use CQRS and event sourcing because it's the proper way." → justify the cost
  against the table at the top, or don't.
- "The read model and the domain model are the same class." → reads and writes have
  different shapes; conflating them is why both get awkward.

## Completion criteria

Before considering domain work done:

- The model uses the ubiquitous language; a domain expert would recognize the names.
- Invariants live inside aggregates, enforced through the root — not in services or
  controllers.
- Domain objects import nothing from infrastructure (ORM, web, broker).
- Each transaction modifies exactly one aggregate; cross-aggregate consistency is eventual.
- Value objects are immutable and self-validating; illegal states are hard to construct.
- If CQRS/ES were used, the cost was justified, not cargo-culted.
- Examples (the code you wrote) actually compile/parse — the model is the product.
