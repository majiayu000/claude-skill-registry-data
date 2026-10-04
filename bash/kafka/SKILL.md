---
name: kafka
description: "Configure Kafka topics and consumers, inspect partitions and offsets, and diagnose consumer-group lag."
category: devops
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["kafka", "streaming", "events", "consumer-groups", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Apache Kafka Streaming AI Skill Guide

## Overview & Engine Architecture

Kafka is a distributed commit log. Producers append records to **topics** split into **partitions**; consumers read with offsets, typically as part of a **consumer group** for parallelism. Ordering is per partition key. Agents design keys for ordering needs, monitor lag, and document delivery semantics (at-least-once vs idempotent/exactly-once setups).

```
Producers -> Kafka brokers (topics/partitions/replicas)
                 -> Consumer groups (shared partitions)
```

## When to use this skill

- Introducing event-driven integration between services
- Debugging consumer lag or rebalances
- Choosing keys, partitions, and retention
- Designing retry/DLQ patterns around consumers

## Operational directives

1. Key by entity ID when you need per-entity ordering.
2. Treat consumers as at-least-once unless idempotent processing is proven.
3. Make handlers idempotent (dedupe on event id).
4. Size partitions for throughput, not vanity; more partitions increase fanout cost.
5. Never commit offsets before side effects succeed (unless intentional).

## Topic mental model

| Concept | Meaning |
| --- | --- |
| Topic | Named stream of records |
| Partition | Ordered log segment; unit of parallelism |
| Offset | Position within a partition |
| Consumer group | Competing consumers sharing partitions |

## Producer/consumer notes (conceptual)

```text
Producer: send(topic, key=userId, value=jsonEvent)
Consumer: subscribe(topic); process; commit offsets
```

CLI examples (scripts vary by install):

```bash
kafka-topics.sh --bootstrap-server localhost:9092 --list
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic events --from-beginning
```

## Failure modes

| Symptom | Likely cause | Direction |
| --- | --- | --- |
| Growing lag | Slow consumer / blocked IO | scale consumers; optimize handler |
| Hot partition | Skewed keys | redesign key; salt carefully |
| Dup processing | rebalance + at-least-once | idempotent writes |
| Poison message | bad payload loops | DLQ + quarantine |

## Best practices

- Include schema/version fields; consider Schema Registry for Avro/Protobuf.
- Compacted topics for changelog/state projections.
- Alert on lag and ISR under-replication.
- Load-test consumers with realistic event sizes.

## Limitations

- Broker operations (disk, JVM, ISR) need platform expertise.
- Exactly-once across Kafka + external DB requires transactional design.
- Managed Kafka (MSK, Confluent Cloud) changes auth and networking.

## Related skills

- `@rabbitmq` - alternative broker for work queues
- `@opentelemetry` - tracing produce/consume spans
- `@postgresql` - projecting events into tables
