---
name: replay-events
description: Rebuild the graph or re-process archived events with just replay — re-produces events from the S3 archive back onto the Kafka bus (disaster recovery, schema change, retro trips).
---
# Replay events

The graph is a disposable projection; the S3 archive is the permanent record.
`just replay` lists every `events/**/event.json` in the archive bucket, validates
each envelope, and re-produces the in-scope events to `wos.events.v1` in `seq`
(receipt-ULID) order — the same order the bus originally saw.

## Read first
- services/graph-writer/README.md — "Replay: rebuilding the graph" (why `--reset` is required for a rebuild, and the every-consumer caveat).
- tools/README.md — "replay" section for full flag semantics and env vars.

## Commands
```bash
just replay --dry-run                       # print first 10 in-scope envelopes + count, touch nothing
just replay --trip <tripId>                 # one trip only (exact match)
just replay --since 2026-07-01T00:00:00Z    # createdAt filter; combinable with --trip
just replay --trip <tripId> --reset         # clear graphedAt markers first → writer reprocesses
```
Env: `WOS_ARCHIVE_BUCKET`, `WOS_KAFKA_BROKERS`, `WOS_KAFKA_API_KEY`, `WOS_KAFKA_API_SECRET`; `WOS_LEDGER_TABLE` for `--reset`. AWS credentials for account 458443189947.

## Gotchas
- Without `--reset`, the graph-writer's `graphedAt` short-circuit skips every already-graphed event — a plain replay only fills gaps.
- Replays hit ALL consumers: no consumer reads the `wos-replay: true` header. The archiver overwrites identical keys and the live-publisher regenerates identical pages (both harmless), but with `--reset` any `@bot` event re-produces its bot job, and a re-run job can add a duplicate card to the phone's inbox.
- "Rebuild" means idempotent re-MERGE (Cypher's create-or-match) through the normal writer — never drop-and-recreate.
- Stays (Flink-derived dwell events) are derived, not archived: to regenerate them, replay while the Flink job is running (`just live-up`, replay, wait, `just live-down`); deterministic stay ids keep it idempotent.
- The full path is unit-tested but has never been needed in production.
