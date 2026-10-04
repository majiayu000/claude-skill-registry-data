---
name: rabbitmq
description: "Configure RabbitMQ exchanges, queues, bindings, acknowledgements, dead-letter routing, and consumer processing."
category: devops
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["rabbitmq", "amqp", "messaging", "queues", "dlq", "quorum-queues"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# RabbitMQ Messaging AI Skill Guide

## Overview

RabbitMQ is a message broker that routes messages from **producers** through **exchanges** to **queues** via **bindings**, consumed by workers over AMQP 0-9-1 (or other protocols). Reliability depends on acknowledgements, durable definitions, and poison-message handling (DLX/DLQ). Agents should prefer **quorum queues** for mirrored durability in modern clusters and avoid unbounded queues without consumers.

```
Producer --> Exchange --binding--> Queue --> Consumer
                 |                    |
                 |                    +--> nack/requeue or DLX
                 +--> fanout/topic/direct/headers
```

## When to use

- Designing async workflows (jobs, events, fan-out)
- Configuring DLX/DLQ and retry policies
- Debugging consumer backlog, connection flaps, or unacked message buildup
- Migrating classic mirrored queues to quorum queues

## Operational directives

1. Declare durable exchanges/queues; publish `delivery_mode=2` for persistent messages when required.
2. Consumers must ACK only after successful side effects (or use outbox patterns).
3. Bound retries - use DLX after N failures; never infinite requeue loops.
4. Prefer quorum queues for HA data queues on RabbitMQ 3.8+.
5. Set per-queue limits / alarms; alert on ready messages and consumer count.

## Concrete examples

### Topology (topic + DLQ)

```bash
rabbitmqadmin declare exchange name=events type=topic durable=true
rabbitmqadmin declare exchange name=events.dlx type=fanout durable=true

rabbitmqadmin declare queue name=orders.created durable=true \
  arguments='{"x-queue-type":"quorum","x-dead-letter-exchange":"events.dlx"}'
rabbitmqadmin declare queue name=orders.created.dlq durable=true \
  arguments='{"x-queue-type":"quorum"}'

rabbitmqadmin declare binding source=events destination=orders.created routing_key=orders.created
rabbitmqadmin declare binding source=events.dlx destination=orders.created.dlq
```

### Publish / consume sketch (conceptual AMQP)

```text
publish: exchange=events, routing_key=orders.created, persistent=true
consume: prefetch=10, manual ack
on success -> basic.ack
on retryable fail -> basic.nack requeue=true (with retry counter header)
on poison -> basic.nack requeue=false  # routes to DLX
```

### Operator CLI

```bash
rabbitmq-diagnostics status
rabbitmqctl list_queues name messages messages_ready messages_unacknowledged consumers
rabbitmqctl list_connections
rabbitmqctl cluster_status
```

## Failure matrix

| Symptom | Cause | Fix |
| :--- | :--- | :--- |
| Growing `messages_ready` | Slow/no consumers | Scale consumers; fix crashes |
| Growing unacked | Prefetch too high / stuck handlers | Lower prefetch; fix processing |
| Memory alarm | Queue backlog | Stop publishers; drain; add capacity |
| Duplicate processing | At-least-once + crash after side effect | Idempotent consumers |

## Best practices

1. Use correlation IDs and structured payloads (JSON schema version field).
2. Separate transient task queues from long-retention event streams (or use a log system).
3. Enable TLS and fine-grained users/vhosts per app.
4. Export definitions (`rabbitmqctl export_definitions`) into Git for disaster recovery.

## Limitations

- RabbitMQ is not a full event log like Kafka; replay/retention models differ.
- Classic mirrored queues are legacy - plan quorum migration.
- Exactly-once across systems is not free; design for idempotency.

## Related skills

- `opentelemetry` - trace produce/consume with messaging semantics
- `docker` - local broker via Compose for dev
- `consul` / `kubernetes` - discovery and deployment substrates
- `makefile-automation` - `make mq-declare` topology targets
