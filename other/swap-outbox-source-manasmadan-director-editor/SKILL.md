---
name: swap-outbox-source
description: Replace the outbox relay's polling with change data capture (logical replication, Debezium). Use when the user decides outbox polling load or event latency needs it, or asks about CDC for domain events. Not for debugging; when something fails, use the debug skill.
disable-model-invocation: true
---

# Swap the outbox source

There is no interface for this yet: the replaceable unit is the relay itself,
`OutboxRelay` in `apps/worker/src/outbox/relay.service.ts`, which feeds the `EventBus`.

- **Today:** each pass claims unpublished rows from every `<schema>.outbox_event` listed
  in `apps/worker/src/outbox/sources.ts` with `FOR UPDATE SKIP LOCKED`, publishes them,
  and stamps `published_at`. It wakes on `NOTIFY` (a direct connection) and polls as a
  fallback. Any number of worker replicas can run it.
- **Env:** `WORKER_DATABASE_DIRECT_URL` (LISTEN), `RELAY_BATCH_SIZE`,
  `RELAY_POLL_INTERVAL_MS` (`apps/worker/src/env.ts`).

## Swap

1. A CDC reader (a logical replication slot on the outbox tables, or Debezium) that
   hands each committed row to `EventBus.publish` as an `EventEnvelope` (same parsing
   as the relay: unknown event names are passed through, not dropped).
2. Replace `OutboxRelay` in `apps/worker/src/outbox/outbox.module.ts` with it. `emitEvent`,
   the outbox tables and every consumer stay as they are.
3. Retention: the `outbox-retention` maintenance job purges rows by `published_at`, so
   the reader must still stamp it, or retention must change to match.
4. Replication needs a role with `REPLICATION` and a slot per environment: a migration
   can't grant that; it's `infra/postgres/init` locally and OpenTofu or CloudNativePG in
   clusters. An abandoned slot holds WAL forever: monitor it.

## Tests

The `outbox relay` tests in `apps/worker/test/worker.integration.test.ts` (delivery,
crash and redelivery, several relays at once) must pass unchanged against the new source.

## Finish

1. The verify skill.
2. Ask the `reviewer` agent to review the change, and the `security-reviewer` agent: a
   new implementation brings its own credentials and sends data somewhere new. If you
   wrote a migration, the `migration-reviewer` agent too.
3. Update the seam's row in the README's "Scaling path" table if what's "Now" changed.
