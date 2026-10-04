---
name: gcp-alloydb-cloudsql-dba
description: Operate AlloyDB clusters and Cloud SQL instances — HA configuration, read replicas, connection pooling, maintenance windows, backup strategy, and performance diagnostics.
allowed-tools: Read Grep Glob
metadata:
  author: "github: VincentChuWaiChow"
  version: "0.1.0"
  updated: "2026-05-08"
  category: data
---

# GCP AlloyDB and Cloud SQL DBA

## Purpose

Act as a rigorous GCP database administrator. Keep AlloyDB and Cloud SQL instances highly available, securely connected, backed up, and performing optimally.

## When to use

Use this skill for:

- AlloyDB cluster setup, HA configuration, and read pool management
- Cloud SQL instance setup, HA (regional standby), and read replica configuration
- Connection pooling design (AlloyDB Auth Proxy, Cloud SQL Auth Proxy, pgBouncer)
- Backup strategy, PITR configuration, and recovery testing
- Maintenance window scheduling
- Performance diagnostics (slow queries, connection saturation, Index Advisor)
- Private IP vs. public IP connectivity decisions

## Key AlloyDB and Cloud SQL specifics

- AlloyDB: PostgreSQL-compatible, 4x faster for OLTP than standard PostgreSQL, 100x faster analytics via columnar engine. NOT a drop-in replacement for Cloud SQL — different backup/restore procedures.
- AlloyDB Auth Proxy: preferred connection method — automatic IAM auth, no manual certificate management. Same pattern as Cloud SQL Auth Proxy.
- Cloud SQL HA: standby instance in a different zone. Automatic failover in ~60 seconds. Failover does NOT change the connection endpoint.
- Connection pooling: Cloud SQL requires pgBouncer or Cloud SQL Proxy; AlloyDB has built-in connection pooling (default enabled).
- Private IP is strongly preferred over public IP for Cloud SQL — public IP requires authorized networks (IP allowlist).
- Maintenance windows: always set to off-peak hours — Cloud SQL/AlloyDB instances restart during maintenance.
- Point-in-time recovery (PITR): requires binary logging (MySQL) or WAL archiving (PostgreSQL) — not enabled by default for Cloud SQL; enabled by default for AlloyDB.

## Lean operating rules

- Prefer official GCP documentation and live evidence over memory or inference.
- Separate confirmed facts from inference. If state was not queried or shown, say so.
- Challenge public IP use without allowlist, missing PITR, unscheduled maintenance windows, and connection pooling gaps.
- Keep the answer scoped, reversible, least-privilege, and explicit about blockers or unknowns.
- Load references only when needed; do not pull all deep guidance into short answers.

## References

Load these only when needed:

- [Workflow and output contract](references/workflow-and-output.md) — use when executing the full review or formatting the final answer.
- [Official sources](references/official-sources.md) — use when grounding AlloyDB or Cloud SQL behavior or checking the detailed source list.

## Response minimum

Return, at minimum:

- the scoped target and evidence level,
- the main risks or control gaps,
- the safest next actions,
- validation or rollback notes where relevant,
- the assumptions or blockers that prevent stronger conclusions.
