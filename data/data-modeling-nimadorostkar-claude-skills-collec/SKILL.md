---
name: data-modeling
description: Use when designing a schema. Covers normalization and when to break it, choosing keys, modeling time and history, soft deletes, multi-tenancy, and schema decisions that are expensive to reverse.
metadata:
  category: data
  version: 1.0.0
  tags: [schema, normalization, keys, multi-tenancy, migrations]
---

# Data Modeling

## Purpose

Design a schema that supports the queries you need and the changes you will want. Schema mistakes are the most expensive category of technical debt because the data outlives every application that touched it.

## When to Use

- Designing a new schema or a significant new table.
- Adding multi-tenancy to an existing model.
- Modeling history, versioning, or audit requirements.
- Reviewing a schema before it becomes hard to change.

## Capabilities

- Normalization, and deliberate denormalization.
- Key selection: natural, surrogate, UUID, ULID.
- Temporal modeling: valid time, transaction time, event history.
- Multi-tenancy strategies and their isolation guarantees.
- Constraint design: the invariants the database should enforce.

## Inputs

- The domain entities and the relationships between them.
- The queries the schema must serve, and their frequency.
- Retention, audit, and compliance requirements.

## Outputs

- A schema with enforced constraints and appropriate keys.
- A documented tenancy and soft-delete strategy.
- A migration path from the current schema, if there is one.

## Workflow

1. **Normalize first** — Third normal form as the default. Denormalize only where a measured query cost justifies it, and record the decision.
2. **Choose keys deliberately** — A surrogate key (UUID/ULID) is stable and safe to expose. A natural key is meaningful and changes when the business changes its mind. Prefer surrogates for identity, and enforce natural uniqueness with a constraint.
3. **Enforce invariants in the database** — Foreign keys, unique constraints, check constraints, not-null. Application-level validation does not survive a concurrent request, a background job, or a psql session.
4. **Model time explicitly** — If history matters, do not overwrite. Append versions or events. `updated_at` tells you when, not what it was before.
5. **Decide tenancy up front** — Shared table with a tenant column, schema per tenant, or database per tenant. Migrating between these later is a project, not a task.
6. **Plan the migration** — Every schema change on a large table needs a plan that does not lock it.

## Best Practices

- A soft delete (`deleted_at`) makes every query wrong by default: any query that forgets the filter returns deleted rows. If you use it, enforce it with a view or a row-level policy, not with discipline.
- Sequential integer IDs leak business information (your order count) and are enumerable. ULIDs are sortable, unique, and safe to expose.
- Storing money as a float is a defect. Use an integer of minor units, or `numeric` — never `float` or `double`.
- Store timestamps in UTC, in a timestamp-with-timezone column. Store the user's timezone separately if you need to render local time.
- A nullable foreign key with a nullable meaning ("null means unassigned, or means deleted, or means legacy") is three columns pretending to be one.
- The `EAV` pattern (entity-attribute-value) makes every query hard and every constraint impossible. Use JSONB for genuinely dynamic attributes instead.

## Examples

**History as an append-only fact, rather than an overwritten field:**

```sql
-- Overwriting loses the answer to "what was the price when they ordered?"
-- forever, and that question will be asked.
CREATE TABLE product_prices (
  id           uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  product_id   uuid NOT NULL REFERENCES products(id),
  amount_cents bigint NOT NULL CHECK (amount_cents >= 0),
  currency     char(3) NOT NULL,
  valid_from   timestamptz NOT NULL,
  valid_to     timestamptz,                       -- NULL = currently in effect

  -- No two price rows for the same product may overlap in time.
  EXCLUDE USING gist (
    product_id WITH =,
    tstzrange(valid_from, valid_to) WITH &&
  )
);

-- The price at any point in time is now a query, not an archaeology project.
SELECT amount_cents FROM product_prices
WHERE product_id = $1
  AND tstzrange(valid_from, valid_to) @> $2::timestamptz;
```

**Multi-tenancy that the database enforces, not the application:**

```sql
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON orders
  USING (tenant_id = current_setting('app.tenant_id')::uuid);
```

A forgotten `WHERE tenant_id = ...` in application code is now not a data breach. Relying on every query in the codebase to remember the filter, forever, is not a strategy.

## Notes

- The exclusion constraint above is enforced by the database, so overlapping price periods cannot exist even under concurrent writes. Application-level checks for this are subject to a race that will eventually happen.
- Row-level security has a real performance cost and must be tested. It is still cheaper than a cross-tenant data leak.
- Adding a column is easy; changing a column's type or removing it is not. Think hardest about the columns you are most confident about.
