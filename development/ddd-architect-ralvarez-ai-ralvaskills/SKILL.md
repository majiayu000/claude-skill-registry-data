---
name: ddd-architect
version: 1.0.0
description: Domain-Driven Design — strategic-first (bounded contexts, context mapping) with aggregates, value objects, domain events, repositories. Event sourcing out of scope. Use when shaping a domain model or designing aggregate boundaries.
---

# DDD Architecture

Domain-Driven Design as practical structure, not ceremony. **Strategic decisions** (bounded contexts, integration patterns between them) carry far more weight than **tactical patterns** (entities, value objects, aggregates) — get the boundaries right and the tactics fall into place. Builds on the domain glossary captured by [grill-with-docs](../../workflows/grill-with-docs/SKILL.md). Pairs with [hexagonal-arch](../hexagonal-arch/SKILL.md) for code structure. Reference tables in [PATTERNS.md](PATTERNS.md).

## 1. Strategic DDD — bounded contexts

A **bounded context** is the scope within which a term has one unambiguous meaning. `Order` in the Ordering context isn't the same `Order` in the Fulfillment context; they share an ID but mean different things.

- **One context = one CONTEXT.md** (per [CONTEXT_FORMAT.md](../../workflows/grill-with-docs/CONTEXT_FORMAT.md)).
- **Multiple contexts in one repo = CONTEXT-MAP.md** at the root + one `CONTEXT.md` per context folder. Pattern is enforced by `grill-with-docs`; this skill consumes the artifacts.
- **A context is not a microservice.** It's a *language* boundary. One service can hold several contexts; one context can span several services (rarely a good idea).
- **A context owns its language.** When the user says "user" in Billing, that's the Billing User — even if Identity has its own User. Don't share types across contexts to "save duplication"; the meaning is different.

## 2. Context mapping — integration patterns

When two contexts must interact, name the relationship explicitly. The pattern dictates how they couple — seven patterns from Shared Kernel through Partnership, full table in [PATTERNS § 1](PATTERNS.md#1-context-mapping-patterns).

- **Default to ACL** for any external system you don't own.
- **Record relationships in `CONTEXT-MAP.md`** — one-line entries per pair.

## 3. Tactical DDD — building blocks

Tactical patterns matter, but they're load-bearing only when strategic decisions are already correct. Treat them as a toolkit, not a checklist. Comparison table in [PATTERNS § 3](PATTERNS.md#3-tactical-building-blocks).

- **Entity** — has identity (`id`); equality by ID.
- **Value Object** — no identity; immutable; equality by attributes. Reach aggressively — they catch bugs at construction.
- **Aggregate** — cluster treated as one consistency boundary; root entity enforces invariants for everything inside.
- **Repository** — collection-like abstraction; one per aggregate root.
- **Domain Service** — behavior that spans aggregates.
- **Application Service** — use-case orchestration; no domain logic.

Make value objects whenever a primitive carries hidden meaning. `string email` invites validation drift; `EmailAddress` ensures it's been validated at construction.

## 4. Aggregate sizing — small + consistency boundaries

The most common DDD mistake is aggregates that are too big.

- **An aggregate is a transaction boundary.** Whatever's inside is updated atomically; whatever's outside is eventually consistent. Bigger aggregate = more contention, more transaction conflicts.
- **Default: small.** Single entity + its value objects + a few directly-owned child entities. If you can't justify why an entity needs to be inside the aggregate, it doesn't.
- **Reference other aggregates by ID, not by object.** `Order` holds `customer_id`, not a `Customer`. Loading the related aggregate is a separate query.
- **Invariants drive the boundary.** "Order line total must equal sum of line items" → line items are inside the Order aggregate. "Order ships to one of customer's saved addresses" → no, address is referenced by ID.

## 5. Repositories

- **One per aggregate root.** `UserRepo`, `OrderRepo` — not `OrderLineRepo` (lines live inside Order).
- **Collection semantics:** `repo.find_by_id(id)`, `repo.add(aggregate)`, `repo.remove(aggregate)`. Specific queries are named methods (`active_users_signed_up_after(date)`), not a generic query DSL.
- **Return aggregates, not DTOs.** DTOs are an API-layer concern.
- **Implementation goes through [sql-architect](../../databases/sql-architect/SKILL.md)** — `psycopg + .sql` (Python) or `sqlx + //go:embed` (Go). No ORM by default; the repo *is* the abstraction over SQL, not a wrapper around an ORM.

## 6. Domain events

Domain events express *something significant happened* in the domain — `OrderPlaced`, `ShipmentDispatched`, `PaymentCaptured`.

- **Past tense.** `OrderPlaced`, not `PlaceOrder`. Events describe what already happened.
- **Immutable.** Once published, never modified.
- **Minimal payload.** IDs + the few facts subscribers genuinely need. Don't dump the entire aggregate state.
- **Published by the aggregate root**, after the transaction commits. Don't publish inside the transaction — readers will see events for state that may roll back.
- **Cross-context integration** runs on domain events: Ordering emits `OrderPlaced`; Fulfillment subscribes and reacts. Transport is usually a message bus (see [event-driven-architect](../../messaging/event-driven-architect/SKILL.md)).
- **In-process eventing** is fine for same-context reactions.

## 7. Domain vs application services

Comparison table in [PATTERNS § 2](PATTERNS.md#2-domain-service-vs-application-service).

When in doubt, **start with a method on the aggregate**. Promote to a domain service only when the behavior genuinely spans aggregates. Avoid the trap of putting *all* logic in services and leaving aggregates anemic.

## 8. Anticorruption layers (ACL)

When integrating with a legacy system, third-party API, or external vendor model:

- **Wrap the external model immediately at the boundary.** Convert their `Customer` to your domain's before any other code sees the foreign type.
- **The ACL is just a translation function** in most cases — no class hierarchy needed.
- **Validate aggressively** at the boundary. The external system isn't guaranteed to keep its contract; reject malformed data with a domain-meaningful error.
- **One ACL per external system**, lives in the infrastructure layer, called by application services.

## 9. When DDD is overkill

DDD is right when the domain is the hard part. It's wrong when the application is.

- **CRUD-only services** — login, sign-up, settings page. Just write the CRUD.
- **Throwaway prototypes** — DDD's value compounds over time.
- **Pure data pipelines** — ETL, batch jobs. The "domain" is the data shape, not behavior. Use plain functions and structs.
- **Tiny services with one context** — guidance still applies, but you may end up with one aggregate and two value objects. That's still DDD.

If the domain has 3–5 entities with genuine invariants and policies, DDD pays. If the domain is "rows in a table the user edits," it doesn't.

## 10. Cross-skill ties

- **`grill-with-docs`** captures the language → CONTEXT.md → which this skill consumes. The glossary is the input; aggregates / value objects / events use those exact terms.
- **`hexagonal-arch`** structures the *code* (domain core + ports + adapters). DDD shapes the *meaning* inside the domain core. DDD answers "what's in the domain"; hexagonal answers "where does the domain live and what touches it."
- **`sql-architect`** is how repositories are implemented (psycopg / sqlx + raw SQL, no ORM).
- **`rest-api-architect`** / framework architects are the application-service entry points. DTOs translate to / from aggregates at the boundary.
- **`improve-codebase-architecture`** benefits from DDD because the domain language gives names to good seams.
