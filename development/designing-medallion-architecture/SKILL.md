---
name: designing-medallion-architecture
description: Structure a lakehouse with the medallion architecture — bronze (raw), silver (cleaned/conformed), and gold (business/aggregated) layers — with clear responsibilities, idempotent layer transitions, and where to put quality checks and modeling. Use when organizing a data lakehouse, defining bronze/silver/gold layers, deciding what logic belongs in each layer, or refactoring a flat pipeline into layers.
---

# Designing Medallion Architecture

## When to use

- Organizing a lakehouse (Databricks/Iceberg/Delta) into layered zones.
- Deciding what transformation belongs in bronze vs silver vs gold.
- Refactoring a flat, hard-to-debug pipeline into clear layers.
- Do NOT use for dimensional modeling details (use `modeling-dimensional-data`).

## The three layers

- **Bronze (raw)** — ingested data as-is, append-only, with load metadata
  (source, ingest time, file). Immutable; enables replay without re-pulling.
- **Silver (cleaned/conformed)** — deduplicated, typed, validated, joined into
  conformed entities. The trustworthy, queryable base.
- **Gold (business)** — aggregated marts, metrics, and dimensional models serving
  BI/ML.

## Workflow

```
- [ ] Land raw immutably in bronze with lineage metadata
- [ ] Clean/dedupe/validate into silver; enforce schema + quality here
- [ ] Model + aggregate into gold for consumers
- [ ] Make each layer transition idempotent (overwrite/upsert by key)
- [ ] Keep heavy business logic in gold, not bronze
```

1. **Bronze = capture, not transform.** Store raw exactly as received so you can
   reprocess when logic changes. No business rules here.
2. **Silver = trust.** Deduplicate, cast types, apply data contracts and quality
   checks, and conform entities. Most `implementing-data-quality-checks` gates live
   here.
3. **Gold = serve.** Build dimensional models and aggregates
   (`modeling-dimensional-data`) for dashboards and features.
4. **Idempotent transitions.** Each layer overwrites/upserts its partition by key,
   so replays and backfills are safe (`writing-idempotent-transformations`).

## Patterns

**Layer responsibilities at a glance:**

| Layer  | Write mode             | Contains                  | Quality gate         |
| ------ | ---------------------- | ------------------------- | -------------------- |
| Bronze | append + metadata      | raw source records        | schema capture only  |
| Silver | MERGE/overwrite by key | typed, deduped, conformed | blocking checks      |
| Gold   | overwrite by partition | marts, metrics, features  | business-rule checks |

**Replay-friendly flow** — because bronze is immutable, fixing a silver/gold bug
means re-deriving from bronze, not re-ingesting the source.

## Common pitfalls

- **Business logic in bronze** — couples capture to logic; a rule change forces
  re-ingestion. Keep bronze raw.
- **Skipping silver** — pushing raw straight to marts spreads dirty data and
  duplicates quality logic across gold models.
- **Non-idempotent layer writes** — replays duplicate; overwrite/upsert by key.
- **No metadata in bronze** — lineage and debugging break; record source + ingest
  time + file.
- **Over-layering** — for a tiny pipeline, three heavyweight layers add ceremony;
  scale the rigor to the data's importance.
- **Gold reading bronze directly** — bypasses cleaning/conforming; gold should
  build on silver.
