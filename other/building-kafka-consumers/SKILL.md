---
name: building-kafka-consumers
description: Build reliable Apache Kafka consumers and producers — consumer groups and partition assignment, offset commit strategy, at-least-once vs exactly-once, idempotent/transactional producers, rebalancing, and dead-letter handling. Use when writing Kafka consumers/producers, configuring offset commits or consumer groups, tuning throughput, or handling rebalances and poison messages.
---

# Building Kafka Consumers

## When to use

- Writing or debugging Kafka consumers/producers.
- Choosing offset-commit strategy and delivery guarantees.
- Tuning consumer-group parallelism, rebalancing, or dead-letter handling.
- Do NOT use for stream processing/windowing (use `processing-streaming-data`).

## Workflow

```
- [ ] Size partitions to target parallelism (consumers <= partitions)
- [ ] Commit offsets AFTER successful processing
- [ ] Make the sink idempotent (upsert by event key)
- [ ] Handle rebalances (commit on revoke, avoid long poll gaps)
- [ ] Route poison messages to a dead-letter topic
```

1. **Partitions cap parallelism.** A consumer group scales out only up to the
   partition count; extra consumers sit idle. Choose partitions for peak throughput.
2. **Commit after processing.** Commit offsets once the work is durably done, not
   before — committing early loses messages on a crash.
3. **Idempotent sink.** At-least-once means duplicates on retry; upsert by a stable
   event key so reprocessing is harmless.
4. **Rebalances happen.** Commit on partition revoke and keep `poll()` intervals
   under `max.poll.interval.ms` so the broker doesn't evict the consumer.
5. **Poison messages** go to a dead-letter topic with the error, so one bad record
   doesn't block the partition.

## Patterns

**Manual commit after processing:**

```python
consumer = KafkaConsumer("orders", group_id="etl",
                         enable_auto_commit=False,
                         max_poll_records=500)
for msg in consumer:
    try:
        upsert(process(msg))          # idempotent by key
        consumer.commit()             # commit only after success
    except PoisonError:
        send_to_dlq(msg)
        consumer.commit()             # skip the bad record
```

**Idempotent / transactional producer** — set `enable.idempotence=true` (dedupes
retries) and use transactions for read-process-write exactly-once across topics.

**Throughput tuning** — increase `max.poll.records`, `fetch.min.bytes`, and
process in batches; keep processing fast to avoid rebalance eviction.

## Common pitfalls

- **Auto-commit + slow processing** — offsets advance before work completes; a
  crash drops messages. Prefer manual commit after processing.
- **More consumers than partitions** — the extras idle; repartition to scale.
- **Long processing between polls** — exceeds `max.poll.interval.ms` and triggers
  endless rebalances; process in bounded batches or use a background worker.
- **No dead-letter path** — one poison message blocks the whole partition.
- **Relying on exactly-once without an idempotent sink** — any at-least-once hop
  reintroduces duplicates.
