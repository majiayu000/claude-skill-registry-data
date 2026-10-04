---
name: processing-streaming-data
description: Build reliable streaming data pipelines with Kafka, Spark Structured Streaming, or Flink — delivery semantics (at-least-once vs exactly-once), idempotent consumers, event-time windowing and watermarks, handling late/out-of-order data, and checkpointing. Use when building or debugging streaming pipelines, configuring consumer groups, choosing delivery guarantees, or handling late events.
---

# Processing Streaming Data

## When to use

- Building or debugging Kafka / Spark Structured Streaming / Flink pipelines.
- Choosing delivery semantics and making consumers idempotent.
- Windowing on event time and handling late/out-of-order events.
- Do NOT use for batch ELT (use `building-ingestion-pipelines`).

## Workflow

```
- [ ] Choose delivery semantics; make effects idempotent regardless
- [ ] Use event time (not processing time) with watermarks
- [ ] Configure checkpointing for recovery
- [ ] Decide late-data policy (allowed lateness -> update, drop, or side output)
- [ ] Size partitions/parallelism to the throughput
```

1. **Delivery semantics.** At-least-once is the common default (duplicates
   possible on retry). Exactly-once needs transactional sinks/offsets. Either way,
   **make the downstream effect idempotent** (upsert by key) so duplicates don't
   corrupt state — this is more robust than relying on exactly-once alone.
2. **Event time + watermarks.** Window by when the event happened, not when it was
   processed; a watermark bounds how long to wait for stragglers.
3. **Checkpoint** so a failed job resumes from the last committed offset/state
   instead of reprocessing everything or losing data.
4. **Late data policy** — allowed lateness updates windows; beyond it, drop or
   route to a side output/dead-letter for reconciliation.

## Patterns

**Idempotent consumer** — key the sink write on a stable event id so replays
upsert rather than duplicate:

```python
# Structured Streaming: exactly-once-ish via idempotent upsert in foreachBatch
def upsert(batch_df, batch_id):
    (delta_table.alias("t")
       .merge(batch_df.dropDuplicates(["event_id"]).alias("s"), "t.event_id = s.event_id")
       .whenNotMatchedInsertAll().execute())

(stream.writeStream.foreachBatch(upsert)
   .option("checkpointLocation", "/chk/events").start())
```

**Event-time windowing with watermark:**

```python
(events
  .withWatermark("event_time", "10 minutes")
  .groupBy(window("event_time", "5 minutes"), "user_id")
  .count())
```

**Kafka consumer basics** — consumer group for scale-out; commit offsets **after**
processing (not before) to avoid data loss; partition count caps parallelism.

## Common pitfalls

- **Relying on exactly-once instead of idempotent sinks** — any at-least-once hop
  reintroduces duplicates; upsert by key.
- **Processing-time windows** — produce wrong results when events arrive late or
  the job lags; use event time + watermark.
- **Committing offsets before processing** — a crash then loses those messages.
- **No checkpointing** — recovery either reprocesses everything or loses state.
- **Unbounded state** (no watermark/TTL) — keyed state grows until the job OOMs.
- **Too few partitions** — caps consumer parallelism; you can't scale past
  partition count.
- **Ignoring dead-letter/late paths** — bad or very late events silently vanish.
