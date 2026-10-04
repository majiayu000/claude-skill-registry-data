---
name: iceberg-lakekeeper
description: Cianfhoghlaim canonical reference for Apache Iceberg 1.4+ tables, the Iceberg REST catalog spec, and the Lakekeeper (Rust, lakekeeper.io) catalog implementation that backs `infrastructure/stacks/lakehouse`. Use when designing time-travel / hidden-partitioning / schema-evolution flows, wiring PyIceberg / DuckDB / Spark / Trino against the `lakehouse-lakekeeper:8181` REST endpoint, choosing between DuckDB ATTACH and PyIceberg for read paths, or extending the `cianfhoghlaim-pipeline` lakehouse ingestion with Iceberg features (sort orders, Z-order, V3 Variant, encryption.key-id, soft-delete, undrop, vended credentials).
---

# Iceberg + Lakekeeper (Cianfhoghlaim canonical)

## Versions (verified 2026-06-29)
- PyIceberg 0.11.1 (2026-03-03) — `pip install "pyiceberg[s3fs,pyarrow,duckdb,pyiceberg-core]"`
- Apache Iceberg Java 1.11.0 (spec latest)
- Lakekeeper v0.12.4 (2026-06-17) — `quay.io/lakekeeper/catalog:v0.12.4`
- DuckDB iceberg extension — **core** (auto-loads on first use)

## Cianfhoghlaim wiring (current)
- Catalog endpoint: `http://lakehouse-lakekeeper:8181` (lakehouse-net)
- Postgres backend (shared with DuckLake/Nimtable) at `lakehouse-postgres:5432`
- S3 backend: `http://lakehouse-garage:3900` (region `garage`)
- Warehouse: `s3://lakehouse-bucket/iceberg/`

## Two read paths, one write path
- **Read fast path** — DuckDB `ATTACH ... (TYPE iceberg, SECRET, ENDPOINT)`; supports `AT (VERSION => snap)` and `AT (TIMESTAMP => ...)` natively. No JVM. Lakekeeper is in the docs' "Iceberg REST Catalogs" list.
- **Read BAML / Arrow path** — PyIceberg 0.11.1 `load_catalog("cianfhoghlaim", type="rest", uri=...)` → returns PyArrow fragments; use this when feeding the BAML extraction pipeline.
- **Write path** — PyIceberg 0.11.1 only (DuckDB iceberg write support is still beta for v2 schema ops); commit to Lakekeeper via `/v1/transactions/commit`.

## What changed since Wave 1 (2026-06-28)
- Lakekeeper is at v0.12.4 — major v0.12.0 added V3 Variant, Idempotency Keys, Instance Admins, OPA batch opt, jemalloc, structured logs (BREAKING), Spark 4 IT.
- Env var rename: `LAKEKEEPER__OPENID_PROVIDER_URI` → `LAKEKEEPER__OPENID_PROVIDERS` (multi-IdP).
- DuckDB `iceberg` extension is now **core**; no `INSTALL/LOAD` boilerplate needed.

## Anti-patterns
- Do NOT import `pyiceberg` from a code path that already has DuckDB; the DuckDB `iceberg` extension is faster and JVM-free for read-only flows.
- Do NOT pin `treeverse/lakekeeper` anywhere — the project moved to `lakekeeper/lakekeeper`. The P1B-08 README still references the old org and needs the Phase 1B refactor to update.
- Do NOT use `unsafe_enable_version_guessing = true` in production; it may violate ACID.
- Do NOT register a `pyiceberg-core` extra for pipelines that only scan (DuckDB handles that without the Rust core).
- Do NOT skip `LAKEKEEPER__PG_ENCRYPTION_KEY` — Lakekeeper v0.12.1+ refuses to start without it.

## Sources
- PyIceberg: https://py.iceberg.apache.org/
- Lakekeeper: https://github.com/lakekeeper/lakekeeper (renamed from treeverse/lakekeeper)
- Lakekeeper image: `quay.io/lakekeeper/catalog:v0.12.4`
- See also: `.agents/skills/ducklake/SKILL.md` — DuckLake reads from the same lakehouse-net Postgres; use DuckLake for SQL-DDL-style append/merge on the same data; use Iceberg REST + PyIceberg for v2/v3 features (V3 Variant, soft-delete, undrop, vended creds, branch/tag).
