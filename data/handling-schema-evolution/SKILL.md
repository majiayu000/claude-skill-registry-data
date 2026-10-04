---
name: handling-schema-evolution
description: Evolve data schemas safely over time — backward/forward compatibility, additive vs breaking changes, column adds/renames/type changes, and evolution in Avro, Parquet, Iceberg, Delta, and warehouse tables. Use when changing a table or event schema, adding or renaming columns, changing types, or preventing a schema change from breaking readers or pipelines.
---

# Handling Schema Evolution

## When to use

- Changing a table, file, or event schema that others read.
- Adding, renaming, dropping, or retyping columns.
- Choosing a compatibility mode for Avro/Iceberg/Delta/Parquet.
- Do NOT use for cross-team producer interfaces (use `designing-data-contracts`).

## Compatibility model

- **Backward compatible** — new readers can read old data (safe to add optional
  fields with defaults). Most warehouse evolution targets this.
- **Forward compatible** — old readers can read new data (they ignore new fields).
- **Full** — both. Aim for backward-compatible-by-default.

## Workflow

```
- [ ] Classify the change: additive (safe) or breaking
- [ ] Prefer additive: add nullable/defaulted columns
- [ ] For renames/type changes, add-new + backfill + dual-write, then deprecate
- [ ] Enable the format's schema evolution settings deliberately
- [ ] Communicate + version breaking changes
```

1. **Classify.** Additive (new optional column) is safe. Rename, drop, type
   narrowing, or nullability tightening are breaking.
2. **Prefer additive.** Add a nullable/defaulted column instead of mutating an
   existing one.
3. **Migrate breaking changes in steps**: add the new column, backfill it,
   dual-write old+new, switch readers, then drop the old column later.
4. **Configure the format** — evolution is opt-in and format-specific (below).
5. **Version + announce** anything breaking.

## Patterns

**Additive, backward-compatible column:**

```sql
ALTER TABLE fct_orders ADD COLUMN discount_amount NUMERIC DEFAULT 0;  -- readers unaffected
```

**Rename without breaking readers** — add the new name, backfill, dual-write, then
deprecate the old column across a release window (never rename in place on a table
others read).

**Format-specific evolution:**

- **Avro** — use a schema registry with `BACKWARD` compatibility; add fields with
  defaults, never remove required fields.
- **Delta** — `mergeSchema` on write for additive columns; explicit `ALTER TABLE`
  otherwise. Column mapping enables safe renames/drops.
- **Iceberg** — full schema evolution by column ID: add/drop/rename/reorder
  without rewriting data.
- **Parquet (raw)** — no built-in evolution; a table format (Delta/Iceberg/Hudi)
  or explicit reconciliation on read is required.

## Common pitfalls

- **Renaming/dropping a column in place** on a shared table — breaks every reader
  immediately; use add-new + deprecate.
- **Narrowing a type** (int→smallint, widening→tightening) — overflows/truncation;
  only widen.
- **Positional schema assumptions** — code that reads by column order breaks on
  reorder; read by name/ID.
- **Blind `mergeSchema` everywhere** — silently absorbs typos as new columns; use
  it intentionally and monitor for drift.
- **No backfill for a new non-null column** — old rows violate the constraint; add
  as nullable/defaulted, backfill, then tighten.
- **Breaking change with no version or notice** — coordinate through a contract and
  a deprecation window.
