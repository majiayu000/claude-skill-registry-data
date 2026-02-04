---
name: queue-observability
description: "Monitor message queues, job processing, and detect backpressure"
triggers:
  - "queue metrics"
  - "Kafka monitoring"
  - "message queue observability"
  - "consumer lag"
priority: 2
---

# Queue Observability

Queues decouple systems but hide problems. Track depth, processing time, and lag.

## Key Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `queue.messages.published` | Counter | Messages sent |
| `queue.messages.consumed` | Counter | Messages processed |
| `queue.process.duration` | Histogram | Processing time |
| `queue.process.errors` | Counter | Processing failures |
| `queue.depth` | Gauge | Pending messages |
| `queue.consumer.lag` | Gauge | Behind by N messages |

## Span Attributes

| Attribute | Example | Required |
|-----------|---------|----------|
| `messaging.system` | kafka, rabbitmq | Yes |
| `messaging.destination` | orders, notifications | Yes |
| `messaging.operation` | publish, process | Yes |
| `job.type` | send_email | Recommended |

## Producer Pattern

```
Before: Start span (kind=PRODUCER), inject trace context into headers, start timer
After:  Record duration, increment published, record errors, end span
```

## Consumer Pattern

```
On receive: Extract trace context, start span (kind=CONSUMER), start timer
After:      Record duration, increment consumed, record errors, end span
```

## Issues to Detect

| Issue | Detection | Cause |
|-------|-----------|-------|
| **Growing depth** | queue.depth increasing | Consumer too slow |
| **Consumer lag** | lag > 0 and increasing | Crashed consumer, slow processing |
| **High error rate** | errors/consumed > 5% | Bad messages, downstream issues |

## Anti-Patterns

- **No trace context in messages** → Traces break at queue boundary
- **No DLQ monitoring** → Poison messages go unnoticed
- **Missing depth alerts** → Backpressure surprises

## References

- `references/platforms/{platform}/worker.md`
- `references/patterns/retry-backoff.md`
