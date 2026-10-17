---
name: aiwf-data-storage
description: Use for SQLite, Android Room, Postgres, pgvector, Chroma, Qdrant, Milvus, database schemas, migrations, transactions, backups, concurrency, vector collections, retention, and data-integrity work in local AI and embedded applications.
---

# AIWF Data Storage

## Core Rule

Identify the authoritative store, schema version, migration mechanism, transaction boundary, backup path, concurrency model, and recovery plan before changing persisted data. Treat vector dimensions, metrics, embedding identity, and payload schema as database contracts.

## Workflow

1. Inspect schema definitions, migrations, ORM or client versions, connection settings, indexes, constraints, tests, backups, and data volume.
2. Classify the change: additive schema, backfill, destructive migration, query/index tuning, backend switch, retention cleanup, vector-space migration, or corruption recovery.
3. Define forward migration, rollback or restore path, compatibility window, and validation query before editing.
4. Test against a copy, fixture, or disposable database. Keep production or user data untouched unless Shawn explicitly authorizes the operation.
5. Verify row or point counts, constraints, representative queries, transaction behavior, and application compatibility.

## Guardrails

- Do not drop, truncate, rewrite, vacuum, compact, or bulk-delete user data without explicit approval and a verified backup or reversible plan.
- Do not hand-edit generated Room schema files or migration history.
- Keep migrations idempotent where the framework expects it and safe under interrupted execution.
- Use transactions for multi-step invariants; do not assume a sequence of successful calls is atomic.
- Do not change vector dimension, distance metric, embedding model, normalization, or index type in place unless the backend explicitly supports a safe migration.
- Distinguish exact search from approximate search and measure recall before changing ANN settings.
- Keep credentials out of connection strings committed to source or logs.
- Add `aiwf-rag-retrieval` when the user-visible issue is retrieval quality rather than storage correctness.

## Validation

Prefer project migration and integrity checks. Verify schema version, backup readability, representative reads and writes, rollback or restore behavior, and concurrent access where relevant. Record the exact database copy or environment used.

## Primary Sources

- SQLite transactions: https://www.sqlite.org/lang_transaction.html
- Android Room: https://developer.android.com/training/data-storage/room
- pgvector: https://github.com/pgvector/pgvector
- Qdrant collections: https://qdrant.tech/documentation/manage-data/collections/
