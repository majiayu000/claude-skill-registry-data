---
name: thalarch-kotlin-jpa
description: "Kotlin-specific JPA/Hibernate persistence engineering for entities, repositories, relationships, fetch plans, transactions, equality/identity, uniqueness constraints, optimistic locking, and N+1 or LazyInitialization diagnostics."
license: Apache-2.0
metadata:
  upstream: https://github.com/Kotlin/kotlin-agent-skills/tree/main/skills/kotlin-backend-jpa-entity-mapping
  upstream-author: JetBrains
  modification-notice: Modified for Thalarch; see THIRD_PARTY_NOTICES.md.
---

# Thalarch Kotlin JPA

Kotlin and ORM semantics interact in ways that generic Java/JPA advice can miss. Treat entity
identity, proxying, nullability, generated IDs, lazy associations, equality and serialization as
one contract.

If the current host exposes the official Kotlin/JetBrains
`kotlin-backend-jpa-entity-mapping` skill and the task matches it, prefer loading that skill for
platform-specific guidance. This Thalarch skill remains the scope/evidence/verification envelope.

## 1. Prove the persistence stack

Before editing, confirm from build files and imports:

- Kotlin version and compiler plugins;
- JPA package (`javax.persistence` vs `jakarta.persistence`);
- ORM/framework and version (Hibernate/Spring Data/etc.);
- no-arg/all-open/JPA plugins or equivalent proxy support;
- database/migration stack;
- serialization/API mapping conventions;
- project entity equality/ID conventions.

Do not impose a new entity style if the repository already has a deliberate, working convention.

## 2. Entity identity is the primary invariant

For every entity define explicitly:

- what identifies a persisted instance;
- what identifies an unsaved instance;
- whether equality is ID-based, business-key-based, or intentionally reference-based;
- whether hash code stays safe when persistence state changes;
- how proxies/subclasses interact with equality;
- whether lazy state can be touched by `equals`, `hashCode`, `toString`, logging or serialization.

Do not use Kotlin `data class` for a JPA entity by default. Generated all-property equality,
`copy()`, destructuring and mutable ORM state often create the wrong semantics. If a project uses
data-class entities intentionally, verify the exact equality/proxy/lifecycle contract before
changing it.

Generated database IDs should model the actual unsaved state; do not invent sentinel values such
as `0` unless the repository/database contract deliberately uses them.

## 3. Nullability and construction

Kotlin non-null types must reflect what is true across the complete ORM lifecycle, not merely the
database schema.

Check:

- constructor requirements;
- proxy/no-arg construction;
- generated ID lifecycle;
- ORM-populated fields;
- nullable DB columns;
- framework reflection/serialization behavior;
- `lateinit` usage and access-before-initialization risk.

A non-null database column does not automatically prove the field is non-null during every entity
construction/hydration phase.

## 4. Relationships and fetch plans

Default assumptions are not evidence. Inspect actual queries/logs/tests when fetch behavior matters.

For associations review:

- owning vs inverse side;
- bidirectional graph synchronization;
- cascade semantics;
- orphan removal lifecycle;
- collection type and equality requirements;
- pagination combined with collection fetches;
- DTO projection vs entity loading;
- serialization/logging accidentally touching lazy state;
- transaction boundary around lazy access.

Do not “fix” lazy-loading symptoms by making everything eager.

For N+1 claims, show the query pattern before and after when practical.

## 5. Uniqueness and idempotency

Application-level duplicate checks are useful for clean errors but are not sufficient for
concurrent correctness.

When a uniqueness/idempotency invariant belongs in the database:

- enforce it with a real unique constraint/index appropriate to the schema;
- optionally add the application pre-check for user-facing error quality;
- handle the race where two requests pass the pre-check concurrently;
- verify transaction/error translation behavior.

## 6. Transactions and concurrency

Inspect the real framework interception model and version.

Check:

- transaction scope;
- proxy/self-invocation traps;
- read-modify-write races;
- lost updates;
- `@Version`/optimistic locking where appropriate;
- bulk update/delete behavior that bypasses managed state/callbacks;
- retry semantics and idempotency.

Do not add retries around transactional writes without proving repeated execution is safe.

## 7. DTO/entity boundary

Do not expose persistence entities directly through external APIs by default. Preserve the
repository's existing boundary, and when a task crosses transport/persistence layers explicitly
review:

- lazy state exposure;
- recursive relationships;
- JSON field stability;
- entity mutation by deserialization;
- versioned API compatibility;
- domain/transport validation.

## 8. Verification

Use evidence at the layer where the risk lives:

- compile affected Kotlin/JVM target;
- focused entity/repository tests;
- real database/ORM integration tests for query/transaction/constraint semantics;
- SQL/query-count evidence for N+1/fetch claims;
- concurrent test for uniqueness/lost-update bugs when practical;
- migration/schema validation when annotations imply schema changes.

A mocked repository test cannot prove ORM identity, SQL, transaction or constraint behavior.

## Completion report

State:

- persistence stack/version evidence;
- identity/equality strategy reviewed;
- fetch/transaction/schema changes;
- queries/integration checks run;
- remaining production-scale assumptions marked `UNVERIFIED`.
