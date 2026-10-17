---
name: schema-spec
description: >
  Write a data schema specification document. Use when the user says "schema spec",
  "document this schema", "schema design doc", "data model spec", "table spec",
  "field definitions", "schema contract", "data dictionary", "define these fields",
  or needs to formally document a database schema, event schema, or API payload schema
  - even if they don't explicitly say "schema spec".
---

## Overview

Based on **Fundamentals of Data Engineering** (Reis & Housley) and **Designing Data-Intensive Applications** (Kleppmann). A schema spec is the data contract between producers and consumers. Kleppmann's rule: schema changes are the most dangerous category of change in a data system - the spec exists to make schema evolution explicit and backward-compatible.

The test: can a consumer engineer write a query or build an integration using only this document, without reading source code or asking the producer team?

## Workflow

### Step 1: Write the schema header

```
Schema: [table name / event name / object name]
Domain: [which product or service owns this data]
Owner: [team]
Type: [relational table / event / API payload / Avro / Parquet / JSON]
Storage: [database name, topic name, or S3 path]
Created: [date]
Last modified: [date]
Version: [v1 / v2 / etc.]
```

### Step 2: Document each field

Use a table for readability:

| Field | Type | Nullable | Default | Description |
|-------|------|----------|---------|-------------|
| id | UUID | No | — | Unique record identifier, generated at insert |
| user_id | BIGINT | No | — | Foreign key to users.id |
| status | ENUM | No | 'pending' | Current state: pending, active, cancelled, completed |
| amount_cents | INTEGER | No | — | Transaction amount in cents. Never fractional. |
| created_at | TIMESTAMPTZ | No | NOW() | UTC timestamp of record creation |
| metadata | JSONB | Yes | NULL | Unstructured key-value pairs. Schema not enforced. |

For each field, ensure:
- **Type** is precise (INTEGER not "number", TIMESTAMPTZ not "timestamp")
- **Nullable** is explicit (yes or no, not ambiguous)
- **Description** explains business meaning, not just the field name
- **Enums** list all valid values
- **Units** are explicit (cents not dollars, seconds not "time", bytes not "size")

### Step 3: Document primary and foreign keys

```
Primary key: id (UUID)
Unique constraints: (user_id, order_id) - one record per user per order
Foreign keys:
  - user_id → users.id (CASCADE DELETE)
  - order_id → orders.id (SET NULL on delete)
Indexes:
  - (user_id, created_at DESC) — supports user activity queries
  - (status) WHERE status != 'completed' — partial index for active records
```

### Step 4: Document business rules

Rules enforced at the application or database level that don't appear in column definitions:

```
Business rules:
- amount_cents must be > 0 (enforced by CHECK constraint)
- status transitions are one-way: pending → active → completed or cancelled
- cancelled records are never deleted, only soft-deleted via status
- created_at is immutable after insert
- metadata keys must match the approved key registry (not enforced by DB - application responsibility)
```

### Step 5: Document partitioning and retention

```
Partitioning: by created_at (monthly)
Retention: 7 years (regulatory requirement - SOX compliance)
Archival policy: records older than 1 year moved to cold storage tier
PII fields: [list any fields containing personal data and their handling policy]
```

### Step 6: Document schema evolution policy

This section prevents breaking changes:

```
Evolution rules:
- Adding nullable columns: backward-compatible, no coordination required
- Adding NOT NULL columns: requires default value or migration, coordinate with consumers
- Renaming columns: never rename in place - add new column, backfill, deprecate old
- Removing columns: 90-day deprecation window, announce to consumer teams
- Type widening (INT → BIGINT): coordinate with consumers before applying
- Type narrowing: prohibited without explicit consumer sign-off

Current deprecations: [list any fields marked for removal with target date]
```

## Anti-Patterns

**1. Ambiguous types and units**
Bad: `amount FLOAT` with no description
Good: `amount_cents INTEGER NOT NULL` + "Amount in USD cents. Divide by 100 for display. Never stored as float to avoid rounding errors."

**2. Missing enum values**
Bad: `status VARCHAR` with description "the status"
Good: `status ENUM('pending','active','cancelled','completed') NOT NULL` + each value explained

**3. No evolution policy**
Bad: Schema doc with no guidance on how to make changes
Good: Explicit rules for each change category (add, rename, remove, retype) with consumer notification requirements

**4. PII undocumented**
Bad: Fields containing email, name, or location with no annotation
Good: Each PII field flagged, data classification noted (e.g., PII-direct, PII-quasi), and handling policy cited

## Quality Checklist

- [ ] Schema header complete (owner, type, storage location, version)
- [ ] Every field has type, nullability, and a business-meaning description
- [ ] Units are explicit on all numeric and timestamp fields
- [ ] All enum values are listed and explained
- [ ] Primary key, unique constraints, foreign keys, and indexes documented
- [ ] Business rules not expressible as column constraints are called out explicitly
- [ ] PII fields are flagged
- [ ] Partitioning and retention policy stated
- [ ] Schema evolution rules defined for add / rename / remove / retype operations
- [ ] Current deprecations listed
