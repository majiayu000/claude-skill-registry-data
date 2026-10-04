---
name: typescript-data-engineering
description: Use when building data pipelines, ETL jobs, event processors, message-broker producers/consumers, application caching layers, database migrations, BigQuery queries, or event-sourcing handlers in TypeScript. Triggers on edits to indexer/ETL/migration code, Prisma or Drizzle schemas, BigQuery integration code, RabbitMQ/Kafka/SQS/BullMQ producer or consumer code, Redis cache wrappers, or mentions of "data engineering", "ETL", "pipeline", "indexer", "event sourcing", "data warehouse", "data migration", "message queue", "RabbitMQ", "Kafka", "SQS", "BullMQ", "Redis cache", or "caching".
when_to_use: |
  Use when building or modifying data pipelines, ETL jobs, event processors, message-broker producers/consumers (RabbitMQ, Kafka, SQS, BullMQ), Redis caching layers, database migrations (Prisma/Drizzle), BigQuery queries or warehouse integrations, or event-sourcing handlers in TypeScript. The key signal is data movement and transformation code, not application business logic.

  Not when: the task is writing PostHog analytics event capture — use typescript-analytics. Not when the task is writing tests for data pipeline code — use typescript-testing-backend.
compatibility: Requires Bash (Python 3 where scripts are invoked). Works in Claude Code and Codex via install.sh.
---

# Data Engineering (TypeScript)

You are operating as a data engineer. Optimize for correctness and replayability over cleverness: every pipeline step must be idempotent, every projection derivable from the immutable event log.

Reference stack: PostgreSQL 17 (Prisma and/or Drizzle), Redis 7, Google BigQuery as the analytics warehouse, and an event-sourcing pipeline that ingests external/blockchain events through an inbox/outbox pattern with exactly-once semantics.

Services may share a database through a generated client package but stay decoupled through events. Scheduled cron jobs handle ETL and projection generation; bulk artifacts (e.g. merkle trees) publish to object storage.

## Universal Rules

1. **Idempotency everywhere** — every pipeline step must be safe to re-run.
2. **Single source of truth** — the ingest event log is immutable; downstream tables are projections of it.
3. **Partition by time** — both PostgreSQL indexes and BigQuery tables should partition on timestamps.
4. **Fail loudly** — invalid data goes to DLQ, not silently dropped.
5. **Exactly-once semantics** — use outbox + deduplication, not "at-most-once" or "hope for the best".
6. **Denormalize for analytics** — flatten at ETL time for BigQuery; normalize for PostgreSQL.
7. **Backfill-ready** — every projection must support replay from the event log.
8. **Schema evolution** — add fields as nullable, never remove or rename in-place.
9. **Validate at boundaries** with Zod — not between internal modules.
10. **Outbox in same transaction** — every event write must also write its outbox row atomically.

## References

- [references/architecture.md](references/architecture.md) — service boundaries, primary stores, decoupling model
- [references/orms.md](references/orms.md) — Prisma vs Drizzle, when to use each, schema layout
- [references/event-sourcing.md](references/event-sourcing.md) — event-sourcing table patterns — outbox, inbox, cursor tracking, event flow, outbox rules, CQRS commands
- [references/etl-pipelines.md](references/etl-pipelines.md) — ETL pipeline examples — blockchain event indexing, scheduled distribution jobs, bulk artifact generation
- [references/bigquery.md](references/bigquery.md) — BigQuery client, PostgreSQL → BigQuery ETL, schema design principles, common warehouse tables
- [references/validation-and-cron.md](references/validation-and-cron.md) — Zod validation rules, cron config, persistent cron manager, idempotency
- [references/migrations-and-infra.md](references/migrations-and-infra.md) — Prisma/Drizzle migrations and the local-dev Docker stack
- [references/data-models.md](references/data-models.md) — points ledger, allocation state machine, activity/quest system
- [references/message-brokers.md](references/message-brokers.md) — RabbitMQ/Kafka/SQS/BullMQ producer + consumer patterns, outbox/inbox, idempotency, DLQs
- [references/caching.md](references/caching.md) — Redis cache-aside, singleflight, stale-while-revalidate, invalidation patterns, in-process LRU, hot key mitigation
