---
name: stream-processing
description: Use when designing real-time data processing systems, choosing stream processing frameworks, or implementing event-driven architectures. Covers Kafka, Flink, and streaming patterns.
allowed-tools: Read, Glob, Grep
---

# Stream Processing

Patterns and technologies for real-time data processing, event streaming, and stream analytics.

## When to Use This Skill

- Designing real-time data pipelines
- Choosing stream processing frameworks
- Implementing event-driven architectures
- Building real-time analytics
- Understanding streaming vs batch trade-offs

## Batch vs Streaming

### Comparison

| Aspect | Batch | Streaming |
| ------ | ----- | --------- |
| Latency | Minutes to hours | Milliseconds to seconds |
| Data | Bounded (finite) | Unbounded (infinite) |
| Processing | Process all at once | Process as it arrives |
| State | Recompute each run | Maintain continuously |
| Complexity | Lower | Higher |
| Cost | Often lower | Often higher |

### When to Use Streaming

```text
Use streaming when:
- Real-time responses required (<1 minute)
- Events need immediate action (fraud, alerts)
- Data arrives continuously
- Users expect live updates
- Time-sensitive business decisions

Use batch when:
- Daily/hourly reports sufficient
- Complex transformations needed
- Cost optimization priority
- Historical analysis
- One-time processing
```

## Stream Processing Concepts

### Event Time vs Processing Time

```text
Event Time: When event actually occurred
Processing Time: When event is processed

Example:
┌─────────────────────────────────────────────────────────┐
│ Event: Purchase at 10:00:00 (event time)                │
│ Network delay: 5 seconds                                │
│ Processing: 10:00:05 (processing time)                  │
└─────────────────────────────────────────────────────────┘

Why it matters:
- Late events need handling
- Ordering not guaranteed
- Watermarks track progress
```

### Watermarks

```text
Watermark = "All events before this time have arrived"

Event stream:
──[10:01]──[10:02]──[10:00]──[10:03]──[Watermark: 10:00]──

Allows system to:
- Know when window is complete
- Handle late events
- Balance latency vs completeness
```

### Windows

```text
Tumbling Window (fixed, non-overlapping):
|─────|─────|─────|
0     5    10    15 (seconds)

Sliding Window (fixed, overlapping):
|─────|
  |─────|
    |─────|
Size: 5s, Slide: 2s

Session Window (activity-based):
|──────|     |───────────|    |───|
User activity with gaps defines windows

Count Window:
Process every N events
```

### State Management

```text
Stateful operations require maintained state:
- Aggregations (sum, count, avg)
- Joins between streams
- Pattern detection
- Deduplication

State backends:
- In-memory (fast, limited)
- RocksDB (larger, persistent)
- External (Redis, database)
```

## Stream Processing Frameworks

### Apache Kafka Streams

```text
Characteristics:
- Library (not a cluster)
- Exactly-once semantics
- Kafka-native
- Java/Scala

Best for:
- Kafka-centric architectures
- Simpler transformations
- Microservices

Example topology:
source → filter → map → aggregate → sink
```

### Apache Flink

```text
Characteristics:
- Distributed cluster
- True streaming (not micro-batch)
- Advanced state management
- SQL support

Best for:
- Complex event processing
- Large-scale streaming
- Low-latency requirements

Example:
DataStream<Event> events = env.addSource(kafkaSource);
events
    .keyBy(e -> e.getUserId())
    .window(TumblingEventTimeWindows.of(Time.minutes(5)))
    .aggregate(new CountAggregator())
    .addSink(sink);
```

### Apache Spark Streaming

```text
Characteristics:
- Micro-batch processing
- Unified batch + streaming API
- Wide ecosystem
- Python, Scala, Java, R

Best for:
- Teams with Spark experience
- Batch + streaming unified
- Machine learning integration

Latency: Seconds (micro-batch)
```

### Kafka Streams vs Flink vs Spark

| Factor | Kafka Streams | Flink | Spark Streaming |
| ------ | ------------- | ----- | --------------- |
| Deployment | Library | Cluster | Cluster |
| Latency | Low | Lowest | Medium |
| State | Good | Excellent | Good |
| Exactly-once | Yes | Yes | Yes |
| Complexity | Low | High | Medium |
| Scaling | With Kafka | Independent | Independent |
| SQL | Limited | Yes | Yes |
| ML integration | Limited | Limited | Excellent |

## Stream Processing Patterns

### Filtering

```text
Input: All events
Output: Events matching criteria

Example: Only process events where amount > 1000
```

### Mapping/Transformation

```text
Input: Event type A
Output: Event type B

Example: Enrich order events with customer data
```

### Aggregation

```text
Input: Multiple events
Output: Single aggregated result

Examples:
- Count events per window
- Sum amounts per user
- Average latency per endpoint
```

### Join Patterns

```text
Stream-Stream Join:
┌─────────────┐     ┌─────────────┐
│   Orders    │ ──► │    Join     │
└─────────────┘     │ (by order_id│
┌─────────────┐     │  in window) │
│  Shipments  │ ──► │             │
└─────────────┘     └─────────────┘

Stream-Table Join (Enrichment):
┌─────────────┐     ┌─────────────┐
│   Events    │ ──► │    Join     │
└─────────────┘     │ (lookup by  │
┌─────────────┐     │  customer)  │
│  Customer   │ ──► │             │
│   Table     │     └─────────────┘
└─────────────┘
```

### Deduplication

```text
Problem: Duplicate events from at-least-once delivery

Solution:
1. Track seen IDs in state (with TTL)
2. If seen, drop
3. If new, process and store ID

State: {event_id: timestamp}
TTL: Based on expected duplicate window
```

## Event Delivery Guarantees

### At-Most-Once

```text
May lose events, never duplicates
Process → Commit → (if fail, event lost)

Use when: Loss acceptable, simplicity preferred
```

### At-Least-Once

```text
Never loses, may have duplicates
Commit → Process → (if fail, reprocess)

Use when: No loss acceptable, handle duplicates downstream
```

### Exactly-Once

```text
Never loses, never duplicates
Requires:
- Idempotent operations, OR
- Transactional processing

How it works:
1. Read from source transactionally
2. Process and update state
3. Write output and commit together

Flink: Checkpointing + two-phase commit
Kafka Streams: Transactional producer + EOS
```

## Late Event Handling

### Strategies

```text
1. Drop late events
   Simple, may lose data

2. Allow late events (allowed lateness)
   Process if within lateness threshold

3. Side output late events
   Main stream processes on-time
   Side stream handles late separately

4. Reprocess historical
   Batch job fixes late data impact
```

### Watermark Strategies

```text
Bounded Out-of-Orderness:
watermark = max_event_time - max_lateness

Example:
max_event_time = 10:00:00
max_lateness = 5 seconds
watermark = 09:59:55

Events before 09:59:55 considered complete
```

## Scalability Patterns

### Partitioning

```text
Partition by key for parallel processing:

┌─────────────────────────────────────────────────────┐
│ Kafka Topic (3 partitions)                          │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────────┐│
│ │ Partition 0 │ │ Partition 1 │ │ Partition 2     ││
│ │ user_a, b   │ │ user_c, d   │ │ user_e, f       ││
│ └─────────────┘ └─────────────┘ └─────────────────┘│
└─────────────────────────────────────────────────────┘
         │               │               │
         ▼               ▼               ▼
    ┌─────────┐    ┌─────────┐    ┌─────────┐
    │Worker 0 │    │Worker 1 │    │Worker 2 │
    └─────────┘    └─────────┘    └─────────┘
```

### Backpressure

```text
When downstream can't keep up:

1. Buffer (risk: OOM)
2. Drop (risk: data loss)
3. Backpressure (slow down source)

Flink: Backpressure propagates automatically
Kafka: Consumer lag indicates backpressure
```

## Monitoring Streaming Applications

### Key Metrics

```text
Throughput:
- Events per second
- Bytes per second

Latency:
- Processing latency
- End-to-end latency

Health:
- Consumer lag
- Checkpoint duration
- Backpressure rate
- Error rate
```

### Consumer Lag

```text
Lag = Latest offset - Consumer offset

High lag indicates:
- Processing too slow
- Need more parallelism
- Downstream bottleneck

Monitor: Set alerting thresholds
```

## Best Practices

```text
1. Design for exactly-once when needed
2. Handle late events explicitly
3. Use event time, not processing time
4. Monitor consumer lag closely
5. Plan for state recovery
6. Test with realistic data volumes
7. Implement backpressure handling
8. Keep processing idempotent when possible
```

## Related Skills

- `message-queues` - Messaging patterns
- `data-architecture` - Data platform design
- `etl-elt-patterns` - Data pipeline patterns
