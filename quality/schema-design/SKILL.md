---
name: schema-design
description: Design data structures, invariants and migrations for an identified datastore. Triggers on "data model", "数据模型".
---

# Schema Design

## When to use

- Design data structures, invariants and migrations for an identified datastore.

**Not for:** api-design for transport; deprecation-migration for migration execution.

## Steps

1. Identify datastore, ownership, access patterns, consistency and retention; do not assume relational storage.

2. Model entities or documents, identifiers, constraints and indexes using actual datastore capabilities.

3. Evaluate deletion, concurrency, uniqueness and query cost; validate performance using real query plans or representative data.

4. Specify backfill, repeated execution, consumer impact and recovery; create a separate SCHEMA only if useful for review.

**Output:** Suggested paths, subject to [human audit](../../../references/human-audit.md): `docs/design/SCHEMA.md` if useful beyond schema source.

## Verify

- Structures fit real access patterns; integrity and migration checks are explicit and performance evidence is labelled.

## References

- [engineering-principles.md](../../../references/engineering-principles.md) — shared decision boundaries, scope and verification.
- [mermaid-diagrams.md](../../../references/mermaid-diagrams.md) — Mermaid erDiagram syntax for entity-relationship diagrams
- [human-audit.md](../../../references/human-audit.md) — document consent, readability and human review.
- [references/schema-patterns.md](references/schema-patterns.md) — normalization trade-offs, index patterns, partitioning strategies, soft-delete policies
