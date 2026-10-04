---
name: db-design
description: Deep database design workflow—entities and relationships, keys and constraints, normalization vs denormalization, indexing strategy, integrity, and operational concerns. Use when designing OLTP schemas or reviewing greenfield data models.
---

# DB Design

Good OLTP design balances integrity, write paths, query patterns, and evolution—not “third normal form everywhere.”

## When to Offer This Workflow

**Trigger conditions:**

- Greenfield service schema or major new domain
- Performance or integrity issues from ad-hoc tables
- Multi-tenant isolation questions

**Initial offer:**

Use **six stages**: (1) domain & access patterns, (2) entities & relationships, (3) keys & constraints, (4) normalization trade-offs, (5) indexing & performance, (6) operations & evolution). Confirm RDBMS and scale expectations.

---

## Stage 1: Domain & Access Patterns

**Goal:** List critical queries and writes: QPS, joins, filters, hot rows.

**Exit condition:** Top access paths ranked by business importance.

---

## Stage 2: Entities & Relationships

**Goal:** ER model; cardinality; optional vs required relationships.

### Practices

- Clear table names; avoid opaque “data” blobs unless documented

---

## Stage 3: Keys & Constraints

**Goal:** Primary keys (surrogate vs natural); foreign keys with explicit ON DELETE policy; unique constraints for business rules.

### Multi-tenant

- `tenant_id` on rows that need isolation; composite keys or indexes as appropriate

---

## Stage 4: Normalization Trade-offs

**Goal:** Normalize to reduce update anomalies; denormalize read hotspots with documented trade-offs.

---

## Stage 5: Indexing & Performance

**Goal:** Indexes serve real queries; watch write amplification and index bloat.

---

## Stage 6: Operations & Evolution

**Goal:** Migration strategy (expand/contract); backup/restore; PII columns flagged.

---

## Final Review Checklist

- [ ] Access patterns drive schema
- [ ] Keys, FKs, and constraints explicit
- [ ] Multi-tenant isolation if applicable
- [ ] Normalization decisions justified
- [ ] Index plan aligned with queries
- [ ] Migration and ops considerations noted

## Tips for Effective Guidance

- NULL semantics and defaults matter for bugs and migrations.
- Pair with **db-migrate** for online schema changes.

## Handling Deviations

- Document stores: embed vs reference with consistency story.
