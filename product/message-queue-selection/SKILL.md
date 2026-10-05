---
name: message-queue-selection
description: "Messaging systems fall into three fundamental shapes, and most bad choices come"
---

# Message Queue Selection (Verbose)

## Core Patterns

### Three Shapes: Work Queue, Pub/Sub, Log

Messaging systems fall into three fundamental shapes, and most bad choices come
from reaching for a familiar product before deciding which shape the problem needs.

**Work queue.** A message is delivered to exactly one consumer from a pool, and
once acknowledged it is deleted. This is the shape for distributing work: many
identical workers pull tasks, each task handled once. Adding workers increases
throughput. Managed examples include SQS and Cloud Tasks. The defining questions it
answers well: "spread these jobs across a fleet, each done once."

**Pub/sub (fan-out).** A message published to a topic is delivered to *every*
subscriber, and is then gone. This is the shape for broadcasting an event to
several independent consumers that each need their own copy — one order-placed
event driving billing, inventory, and email simultaneously. Managed examples
include SNS and Pub/Sub topics. Note that each subscriber typically has its own
backing queue; the fan-out is the point.

**Log.** An append-only, ordered sequence that consumers read by tracking an
**offset**. The defining difference from the other two: a message is **retained**
after being read, for a configured window, and can be re-read. This enables replay
(reprocess history after a bug fix), multiple independent consumer groups each at
their own position, and event-sourcing designs. Kafka and Kinesis are the canonical
examples. A log is the right shape whenever "who consumed it and when" must be
decoupled from "how long the data lives."

Two questions usually settle the choice: *one consumer or many independent
consumers?* (queue vs pub/sub or log) and *consumed-and-deleted or
retained-and-replayable?* (queue/pub-sub vs log). A log can emulate the others, but
carries operational weight you should not pay unless you need retention or replay;
conversely, using pub/sub where you actually needed to replay history is a
correctness gap you discover during your first incident.

### Delivery Guarantees: At-Least-Once Is the Reality

There are three delivery semantics in theory:

- **At-most-once** — never redelivers; may lose messages. Fine only for data where
  a gap is acceptable (some metrics/telemetry).
- **At-least-once** — guarantees delivery by redelivering when an acknowledgement
  is lost; therefore *may deliver duplicates*.
- **Exactly-once** — each message effects the system once and only once.

In a distributed system, at-least-once is what you actually get, and the reason is
fundamental: for a broker to guarantee a message is not lost, it must redeliver
when it does not receive an ack — and an ack can be lost even after the consumer
successfully processed the message. The broker cannot distinguish "consumer never
got it" from "consumer got it, processed it, and the ack vanished," so it
redelivers. The duplicate is not a bug; it is the price of not losing messages.

"Exactly-once" features exist, but they are narrow: they typically cover a specific
producer-to-broker-to-consumer path within one system's own transactional
boundary, and they do **not** extend to the side effects your consumer performs —
charging a card, sending an email, calling a third party. The moment your handler
touches anything outside that boundary, exactly-once evaporates.

The correct engineering response is to **assume at-least-once and make consumers
idempotent**, so that processing the same message twice produces the same result as
processing it once. This is the single most important discipline in messaging, and
it is covered in depth in `idempotency-patterns` — typically a deduplication key
persisted transactionally with the effect, or naturally idempotent operations
(upserts, set-to-value rather than increment).

### Ordering: Buy It Only Where Needed

Strict, global ordering is expensive: it forces messages through a single
serialized path, which caps throughput and prevents parallel consumption. Teams
often request "ordered delivery" reflexively and pay this cost for a guarantee they
did not need.

The key realization is that most ordering requirements are **per-key**, not global.
You need events for a single account, or a single order, to be processed in order —
but events for *different* accounts have no ordering relationship and can safely run
in parallel. Both major mechanisms exploit this:

- FIFO queues with a **message group id**: order is preserved within a group,
  groups run independently.
- Logs with a **partition key**: order is preserved within a partition (all
  messages for a key land in one partition), partitions are consumed in parallel.

Choose your key so that everything that must be ordered shares it and everything
that doesn't spreads across keys. If you truly need no ordering, take the
unordered, higher-throughput path and gain parallelism. If you think you need
global ordering, examine whether a well-chosen key gives you the same correctness
at a fraction of the cost — it usually does.

### Dead-Letter Queues

Some messages cannot be processed: malformed payloads, references to deleted
entities, bugs that fail deterministically. Under at-least-once redelivery, such a
"poison" message retries forever. In a work queue that wastes capacity; in an
ordered partition it is worse — the poison message blocks every message behind it,
because the next one cannot be delivered until this one is acked.

A **dead-letter queue** breaks this: after a configured number of failed attempts,
the message is moved to a separate DLQ instead of being retried again. The main
pipeline keeps flowing, ordering is unblocked, and the failed message is preserved
for inspection, alerting, and manual or automated reprocessing once the cause is
fixed. A DLQ with no alerting is only half the pattern — messages arriving in the
DLQ should page someone, because a filling DLQ means something is systematically
failing.

### Backpressure

Producers can, and eventually will, produce faster than consumers consume — a
traffic spike, a slow downstream dependency, a consumer deploy gone wrong. What
happens next is a design decision, and skipping it turns a slow consumer into an
outage:

- **Scale consumers on backlog.** Autoscale the consumer fleet on queue depth or
  consumer lag, *not* on CPU — a backlogged consumer is often not CPU-bound at all
  (see `autoscaling-strategies`).
- **Slow the producers.** Apply flow control so producers block or shed load rather
  than growing an unbounded queue — pushing the backpressure toward the source.
- **Expire or shed.** For data where staleness makes messages worthless, set a TTL
  so the queue drains rather than growing without bound.

For logs specifically, backpressure has a sharp edge: retention is time-based, so
if a consumer falls further behind than the retention window, the oldest unread
messages are deleted before it reaches them — **silent data loss**. Retention must
exceed your worst-case consumer downtime, and consumer lag must be monitored
against it.

## Common Anti-Patterns

❌ **Assuming exactly-once delivery.** Duplicates are inherent to at-least-once.
✅ Design at-least-once; make consumers idempotent (`idempotency-patterns`).

❌ **Requiring global ordering by default.** Serializes the pipeline, kills
throughput.
✅ Order per key via message groups / partition keys; parallelize across keys.

❌ **No dead-letter queue.** Poison messages retry forever or block a partition.
✅ Route to a DLQ after N attempts, and alert on DLQ arrivals.

❌ **Pub/sub where replay was needed** (or a log where simple fan-out sufficed).
✅ Match the shape: retained/replayable → log; broadcast-and-forget → pub/sub.

❌ **Autoscaling consumers on CPU.** A backlogged consumer can look idle.
✅ Scale on backlog depth / consumer lag.

❌ **Unbounded, unmonitored queues.** A slow consumer silently becomes an outage.
✅ Monitor depth and lag; decide the backpressure policy explicitly.

❌ **Log retention shorter than worst-case consumer downtime.**
✅ Set retention above realistic recovery time; alert on lag approaching it.

## Message Queue Selection Checklist

- [ ] Shape chosen deliberately: work queue vs pub/sub vs log
- [ ] "One consumer or many independent consumers?" answered
- [ ] "Consumed-and-deleted or retained-and-replayable?" answered
- [ ] Consumers designed for at-least-once (idempotent handlers)
- [ ] Idempotency/dedup key defined for operations with side effects
- [ ] Ordering requirement identified as per-key or none (not global by reflex)
- [ ] Partition/group key chosen so ordered items share it
- [ ] Dead-letter queue configured with a max-attempts threshold
- [ ] Alerting on DLQ arrivals
- [ ] Consumer autoscaling driven by backlog/lag, not CPU
- [ ] Backpressure policy chosen (scale, slow producers, or expire)
- [ ] Queue depth and consumer lag monitored and alerted
- [ ] For logs: retention exceeds worst-case consumer downtime

## See Also
- `idempotency-patterns` — making at-least-once processing correct
- `microservices-communication-patterns` — synchronous vs asynchronous, and
  event-driven service design
- `autoscaling-strategies` — scaling consumers on backlog rather than CPU
