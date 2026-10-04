---
name: operating-postgresql-server
kind: skill
status: ready
provenance:
  principles:
  - P003
  - P008
  - P015
  - P009
  - P016
  - P017
  - P020
  - P021
  - P047
  claims:
  - C00472
  - C00476
  - C00455
  - C00456
  - C00460
  - C00461
  - C00424
  - C00439
  - C00498
  - C00499
  - C00305
  - C00306
  - C00373
  - C00565
  - C00481
  - C00491
  - C00527
  - C00529
  evidence:
  - E00134
  - E00135
  - E00127
  - E00128
  - E00131
  - E00132
  - E00123
  - E00124
  - E00142
  - E00143
  - E00098
  - E00099
  - E00118
  - E00154
  - E00137
  - E00141
  source_anchors:
  - b1c9b849675c-c0005
  - b1c9b849675c-c0004
  - b1c9b849675c-c0003
  - b1c9b849675c-c0000
  - b1c9b849675c-c0002
  authored_from_digest: 87dfac020705dfcf94852513622dc027db2d39b53c6bf2d698f8eacde61f78df
---

# Operating a PostgreSQL server

## Purpose

Design PostgreSQL operational practice — backups, roles and privileges, replication, function volatility, space reclamation, connection control, and migration.

## When to use

When planning PostgreSQL backup, security, replication, maintenance, or a migration to PostgreSQL.

## Procedure

1. Back up with pg_dump for selective day-to-day backups (compressed/TAR/directory formats enable parallel restore) and run pg_dumpall --globals-only daily to capture roles and tablespaces. (P003)
2. Manage roles with CREATE ROLE (not the deprecated CREATE USER/GROUP), keep group roles login-less, state INHERIT/NOINHERIT explicitly, and rely on SET ROLE for the never-inherited superuser rights. (P008)
3. Grant USAGE on a schema or table/function grants are inert; do not assume database ownership grants access to all objects; and consider revoking risky PUBLIC defaults (CONNECT, EXECUTE, etc.). (P015)
4. Mark function volatility correctly (IMMUTABLE/STABLE/VOLATILE) so the planner can optimize, apply STRICT cautiously (it can block index use), and prefer SQL functions for planner inlining while using PL/pgSQL when control flow or dynamic SQL is needed. (P009)
5. Plan replication for availability and read scalability with one master and read-only slaves shipping WAL; choose synchronous (waits for a slave) versus asynchronous (lower latency but possible lag/loss); use streaming/cascading to reduce coupling; and note all servers must share the same version and unlogged tables are excluded. (P016)
6. Run space-reclamation maintenance (vacuum/compaction) as an asynchronous background process and persist the free-page list so free space survives crashes and is not leaked. (P017)
7. Terminate connections sparingly: pg_cancel_backend cancels a query without dropping the connection, pg_terminate_backend kills it; clear affected connections before a backup or restore. (P020)
8. Never delete files from the data cluster folder to reclaim space: pg_log may be purged, but deleting pg_xlog's root or pg_clog destroys data and deleting archived WAL breaks point-in-time recovery and slave catch-up. (P021)
9. When migrating to PostgreSQL, rewrite non-portable SQL (LIMIT/OFFSET, Oracle (+)/dual/sysdate) and clean data-integrity violations from non-strict MySQL; use oracle_fdw/ora2pg/orafce or pg_chameleon/mysql_fdw and port stored procedures manually. (P047)

## Grounding

Distilled (no verbatim) from this package's principles (P003, P008, P015, P009, P016, P017, P020, P021, P047) and their anchored claims/evidence. Verify version-specific PostgreSQL or SQLite syntax and behaviour against current official documentation.
