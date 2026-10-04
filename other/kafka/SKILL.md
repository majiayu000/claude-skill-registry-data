---
name: kafka
description: "Expert skill for Apache Kafka as a streaming ETL/data-integration platform across all versions (3.9-4.2): broker architecture, KRaft consensus, producer/consumer patterns, Kafka Connect, Kafka Streams, exactly-once semantics, and operational troubleshooting. WHEN: \"Kafka\", \"Kafka broker\", \"Kafka topic\", \"Kafka partition\", \"Kafka producer\", \"Kafka consumer\", \"consumer group\", \"consumer lag\", \"Kafka Connect\", \"Kafka Streams\", \"KRaft\", \"ZooKeeper migration\", \"exactly-once\", \"Schema Registry\", \"Avro\", \"Protobuf\", \"MirrorMaker\", \"kafka-console-consumer\", \"kafka-topics.sh\", \"rebalancing\", \"ISR\", \"under-replicated partitions\", \"tiered storage\", \"Share Groups\". Do NOT use for Kafka as general-purpose pub/sub messaging infrastructure (queue design, broker sizing for app messaging, comparing Kafka to RabbitMQ/SQS/Pulsar) -- that's the `kafka` skill in the messaging plugin."
license: MIT
---

# Apache Kafka

This skill covers Apache Kafka across all supported versions (3.9 through 4.2). It provides deep knowledge of:

- Broker architecture, topics, partitions, segments, and replication (ISR, high watermark, leader election)
- KRaft consensus (metadata quorum, controller nodes, dynamic quorums) and ZooKeeper migration
- Producer internals (batching, compression, idempotence, transactions)
- Consumer internals (consumer groups, offset management, rebalancing protocols, static membership)
- Kafka Connect (source/sink connectors, converters, SMTs, DLQ, distributed mode)
- Kafka Streams (topology, state stores, windowing, joins, exactly-once processing)
- Schema Registry (Avro, Protobuf, JSON Schema, compatibility modes, evolution strategies)
- Exactly-once semantics (idempotent producer + transactional producer + read_committed consumer)
- Storage (log segments, retention, compaction, tiered storage)
- Security (SASL, mTLS, ACLs, encryption in transit)
- Multi-datacenter replication (MirrorMaker 2, topologies, offset translation)
- Monitoring (JMX metrics, consumer lag, broker health) and operational troubleshooting

When a question is version-specific, read the appropriate version reference below. When the version is unknown, provide general guidance and note where behavior differs across versions.

## When to Use This Skill's General Guidance vs. Version References

**Use the general guidance in this file** for general Kafka architecture, producer/consumer patterns, Connect pipelines, Streams design, troubleshooting, and best practices that apply across versions.

**Read a version reference** when the question involves version-specific features, migration between specific versions, or behavior that changed in a particular release:
- `references/versions/3.9.md` -- Last ZooKeeper version, tiered storage GA, KRaft migration prep
- `references/versions/4.0.md` -- ZooKeeper removed, KIP-848 GA, Share Groups EA, Java 17 requirement
- `references/versions/4.1.md` -- Share Groups preview, Streams rebalance, OAuth, ELR default
- `references/versions/4.2.md` -- Share Groups GA, Streams DLQ, CLI standardization (current)

## How to Approach Tasks

1. **Classify** the request:
   - **Troubleshooting** -- Load `references/diagnostics.md` for consumer lag, rebalancing storms, under-replicated partitions, performance bottlenecks, and CLI tool usage
   - **Architecture / design** -- Load `references/architecture.md` for broker internals, replication, KRaft, Connect, Streams, Schema Registry, storage, and EOS mechanics
   - **Best practices** -- Load `references/best-practices.md` for topic design, producer/consumer tuning, exactly-once patterns, schema evolution, security, monitoring, and multi-DC
   - **Version migration** -- Route to the appropriate version agent and load `references/architecture.md` for KRaft migration details

2. **Identify version** -- Determine which Kafka version the user runs. Key version gates:
   - KRaft-only (4.0+), ZooKeeper still supported (3.9)
   - KIP-848 consumer protocol GA (4.0+), preview (3.9)
   - Share Groups EA (4.0), preview (4.1), GA (4.2)
   - Tiered storage GA (3.9+)
   - ELR default (4.1+)
   - Java 17 server requirement (4.0+)

3. **Load context** -- Read the relevant reference file for deep technical detail before answering.

4. **Analyze** -- Apply Kafka-specific reasoning. Consider replication factor, partition count, consumer group state, ISR health, and exactly-once requirements.

5. **Recommend** -- Provide actionable guidance with configuration examples, CLI commands, and code patterns.

6. **Verify** -- Suggest validation steps (describe topic, describe group, check metrics, test with console consumer/producer).

## Core Architecture

### How Kafka Works

```
Producer ──► Broker Cluster ──► Consumer Group
               │
        ┌──────┼──────┐
        │      │      │
     Broker  Broker  Broker
     0       1       2
        │      │      │
     ┌──┴──┐ ┌┴───┐ ┌┴───┐
     │Part │ │Part│ │Part│   Topic: orders (3 partitions, RF=3)
     │0(L) │ │1(L)│ │2(L)│   L=Leader, F=Follower
     │1(F) │ │2(F)│ │0(F)│
     │2(F) │ │0(F)│ │1(F)│
     └─────┘ └────┘ └────┘
```

**Brokers** store data on disk and serve client requests. A cluster consists of multiple brokers for load distribution and fault tolerance.

**Topics** are named, append-only, immutable logs -- the fundamental unit of organization. Producers write to topics; consumers read from topics.

**Partitions** are the unit of parallelism and ordering. Records within a partition are strictly ordered by offset. A partition key determines routing via hashing.

**Segments** are the physical storage unit. Each partition is a sequence of log segments (`.log`, `.index`, `.timeindex`). Active segment is writable; closed segments are immutable and eligible for retention or compaction.

### Replication and ISR

Each partition has a configurable number of replicas (typically 3 in production). One replica is the **leader** (handles all reads/writes); the rest are **followers** (replicate via fetch requests).

The **ISR (In-Sync Replica set)** is the subset of replicas caught up within `replica.lag.time.max.ms` (default 30s). With `acks=all`, the leader waits for all ISR members to acknowledge before confirming a write. Combined with `min.insync.replicas=2`, this ensures at least 2 replicas have the data before acknowledging.

The **high watermark** is the offset of the last record replicated to all ISR members. Consumers with `isolation.level=read_committed` only see records up to the high watermark.

### KRaft Consensus (ZooKeeper Replacement)

KRaft (Kafka Raft) replaced ZooKeeper for metadata management:
- **Controller nodes** form a quorum using an event-based Raft consensus protocol
- One controller is the **active controller** (leader); others are hot standbys
- Metadata stored in internal `__cluster_metadata` topic
- All brokers subscribe to metadata and maintain a local cache

**Benefits**: Single system (not two), faster failover (seconds vs minutes), millions of partitions per cluster (vs ~200K with ZK), single security model.

**Timeline**: KRaft production-ready in 3.3, ZooKeeper removed in 4.0. Migration path goes through 3.9 (mandatory stepping stone).

## Producer Patterns

### Batching and Compression

The producer buffers records in a `RecordAccumulator`, groups them into batches per topic-partition, and a background Sender thread transmits full batches:

| Parameter | Default | Purpose |
|-----------|---------|---------|
| `batch.size` | 16,384 (16 KB) | Maximum batch size in bytes per partition |
| `linger.ms` | 5 ms (Kafka 4.x) | Wait time for batch filling before sending |
| `buffer.memory` | 33,554,432 (32 MB) | Total memory for buffering; `send()` blocks when full |
| `compression.type` | `none` | `lz4` for speed, `zstd` for best ratio; applied per batch |

Larger batches yield better compression and throughput. `batch.size` and `linger.ms` work together -- increase both for throughput workloads.

### Acknowledgements

- `acks=0`: Fire and forget. No durability guarantee.
- `acks=1`: Leader acknowledges after local write. Risk of loss on leader failure before replication.
- `acks=all`: Leader waits for all ISR members. Strongest durability. Use with `min.insync.replicas=2`.

### Idempotent Producer

Enabled by default (3.0+). Broker assigns a Producer ID (PID) and tracks sequence numbers per partition. Duplicate records from retries are silently rejected. Requires `acks=all`, `retries > 0`, `max.in.flight.requests.per.connection <= 5`. There is no reason to disable this -- it is free deduplication.

### Transactional Producer

Extends idempotence for atomic writes across multiple partitions:

```
producer.initTransactions();
producer.beginTransaction();
producer.send(record1);  // To partition A
producer.send(record2);  // To partition B
producer.sendOffsetsToTransaction(offsets, consumerGroupMetadata);
producer.commitTransaction();  // Atomic: all or nothing
```

Configured via `transactional.id` (must be stable and unique per producer instance). Enables exactly-once when combined with `read_committed` consumers. Uses a Transaction Coordinator broker managing the `__transaction_state` internal topic. Adds ~10-50ms overhead per transaction.

## Consumer Patterns

### Consumer Groups

A consumer group cooperatively consumes from topics. Each partition is assigned to exactly one consumer within a group. Multiple groups can independently consume the same topic. The Group Coordinator (a broker) manages membership and assignment. Coordinator determined by hashing `group.id` to a partition of `__consumer_offsets` (50 partitions by default).

### Offset Management

- Offsets committed to internal `__consumer_offsets` topic
- `enable.auto.commit=true` (default): offsets committed periodically (`auto.commit.interval.ms`, default 5s)
- Manual commit: `commitSync()` or `commitAsync()` for precise control
- `auto.offset.reset`: `latest` (default) for real-time, `earliest` for reprocessing

### Rebalancing Protocols

**Cooperative (Incremental) Rebalance** (2.4+): Only moved partitions are revoked. Unaffected consumers continue processing. Strategy: `CooperativeStickyAssignor`.

**KIP-848 New Consumer Group Protocol** (4.0 GA): Server-side partition assignment. Continuous heartbeat replaces JoinGroup/SyncGroup. Eliminates stop-the-world rebalances. Opt-in: `group.protocol=consumer`.

**Static Group Membership**: Set `group.instance.id` to a stable identifier (e.g., Kubernetes pod name). Consumer retains its assignment across restarts within `session.timeout.ms`. Prevents unnecessary rebalances in containerized environments.

### Key Consumer Timeouts

| Parameter | Default | Impact |
|-----------|---------|--------|
| `session.timeout.ms` | 45,000 | Consumer removed from group if no heartbeat within this window |
| `heartbeat.interval.ms` | 3,000 | Set to 1/3 of `session.timeout.ms` |
| `max.poll.interval.ms` | 300,000 | Consumer evicted if no `poll()` call within this window |
| `max.poll.records` | 500 | Records per `poll()` call; reduce if processing is slow |

## Kafka Connect

A framework for streaming data between Kafka and external systems without writing code:

```
External System ──► Source Connector ──► Kafka ──► Sink Connector ──► External System
                         │                              │
                    Converter (Avro)              Converter (Avro)
                    SMT chain                     SMT chain
```

- **Source connectors**: Ingest FROM external systems INTO Kafka (JDBC Source, Debezium CDC, FileStream)
- **Sink connectors**: Deliver FROM Kafka TO external systems (Elasticsearch, S3, JDBC Sink, HDFS)
- **Converters**: Serialize/deserialize between Connect's internal format and wire format (Avro, JSON, Protobuf). Decoupled from connectors -- any connector works with any converter.
- **SMTs**: Single-message transforms applied in an ordered pipeline chain (InsertField, ReplaceField, TimestampRouter, RegexRouter, Cast, Flatten)
- **Dead Letter Queue**: Failed records routed to a DLQ topic with error context in headers (sink connectors only). Config: `errors.tolerance=all`, `errors.deadletterqueue.topic.name=<topic>`

**Deployment**: Use distributed mode for production (multiple workers, REST API, automatic task failover). Internal topics (`connect-offsets`, `connect-configs`, `connect-status`) should have `replication.factor=3`. Use standalone mode for development only.

## Kafka Streams Overview

A client library for stateful stream processing with no external dependencies beyond Kafka:

- **Topology**: DAG of source, stream, and sink processors
- **Two APIs**: DSL (KStream, KTable, GlobalKTable) and Processor API (low-level)
- **State stores**: Local RocksDB backed by changelog topics for fault tolerance
- **Exactly-once**: `processing.guarantee=exactly_once_v2`
- **Windowing**: Tumbling, hopping, sliding, session windows with grace periods
- **Joins**: KStream-KStream (windowed), KTable-KTable (changelog), KStream-KTable (enrichment), KStream-GlobalKTable (broadcast)

## Storage and Retention

Three cleanup policies (`cleanup.policy`) control how data is retained:

- **`delete`** (default): Old segments removed after `retention.ms` (default 7 days) or `retention.bytes`
- **`compact`**: Log compaction retains only the latest value per key. Tombstones (null value) signal deletion, retained for `delete.retention.ms` (default 24h).
- **`compact,delete`**: Both policies apply

**Tiered Storage** (GA in 3.9+, KIP-405): Offloads older segments to object storage (S3, GCS, Azure Blob). Recent data stays on local disk for low-latency tail reads. Transparent to consumers. Reduces broker storage costs and enables much longer retention.

## Schema Registry

Centralized schema management for data governance on Kafka topics:

1. Producer registers schema, gets a schema ID
2. Producer serializes data, prepends magic byte + 4-byte schema ID
3. Consumer fetches schema by ID, deserializes data
4. Schemas stored in `_schemas` topic (Kafka-backed)

**Compatibility modes** control what schema changes are allowed:
- `BACKWARD` (default): New schema can read old data. Safe: add optional fields with defaults, delete fields.
- `FORWARD`: Old schema can read new data. Safe: add fields, delete optional fields with defaults.
- `FULL`: Both backward and forward compatible.
- Add `_TRANSITIVE` suffix to check against ALL previous versions, not just the last.

**Format guidance**: Avro (most mature, binary, compact), Protobuf (strong typing, use `BACKWARD_TRANSITIVE`), JSON Schema (human-readable, less compact).

## Exactly-Once Semantics

Three cooperating mechanisms:

1. **Idempotent Producer** -- PID + sequence number deduplication (prevents duplicates from retries)
2. **Transactional Producer** -- Atomic writes across partitions + atomic offset commits
3. **Read Committed Consumers** -- `isolation.level=read_committed` ensures only committed records are visible

End-to-end flow: Consumer reads (read_committed) -> process -> transactional producer writes output + commits input offsets in a single atomic transaction. If any step fails, the entire transaction aborts and the consumer re-reads from the last committed offset.

**Kafka Streams shortcut**: Set `processing.guarantee=exactly_once_v2` -- Streams handles all three components automatically.

**Kafka-to-external patterns**: Exactly-once applies within Kafka only. For external systems, use the outbox pattern (write to external system + dedup table in one DB transaction) or idempotent writes with a deduplication key.

## Monitoring Essentials

### Critical Alerts

| What to Monitor | Alert When | Why |
|----------------|------------|-----|
| Under-replicated partitions | > 0 for > 5 min | Data durability at risk |
| Offline partitions | > 0 | Partitions unavailable for reads/writes |
| Active controller count | != 1 | Split-brain or no controller |
| Consumer group lag | Growing consistently | Consumers falling behind producers |
| ISR shrink rate | Sustained > 0 | Followers losing sync |
| Request handler idle % | < 30% | Broker I/O threads saturated |

### Key Tools

- `kafka-consumer-groups.sh --describe --group <id>` -- Check consumer lag per partition
- `kafka-topics.sh --describe --under-replicated-partitions` -- Find replication issues
- `kafka-metadata-quorum.sh describe --status` -- KRaft quorum health
- Prometheus + JMX Exporter + Grafana for continuous monitoring

## Security Fundamentals

- **Always use `SASL_SSL`** in production -- never `PLAINTEXT`
- **Authentication**: SASL/SCRAM-SHA-256 (username/password), mTLS (certificates), SASL/OAUTHBEARER (OAuth/OIDC, native in 4.1+)
- **Authorization**: ACLs via `kafka-acls.sh`; set `allow.everyone.if.no.acl.found=false` (deny by default)
- **Encryption**: TLS for client-broker and inter-broker traffic. At-rest encryption handled at OS/disk level.
- Use separate credentials per application. Rotate regularly.

## Anti-Patterns

| Anti-Pattern | Why It Fails | Instead |
|---|---|---|
| Using `acks=0` or `acks=1` for critical data | Data loss on broker failure | Use `acks=all` with `min.insync.replicas=2` |
| Setting `replication.factor=1` in production | No fault tolerance | Use `replication.factor=3` |
| Using underscores in topic names | Collides with metric name substitution (`.` replaced with `_`) | Use dots or hyphens |
| One giant topic for everything | No isolation, no independent scaling, no per-stream retention | One topic per event type/entity |
| More consumers than partitions (classic protocol) | Idle consumers waste resources | Match consumer count to partition count, or use Share Groups (4.2+) |
| `enable.auto.commit=true` with exactly-once | Offsets committed before processing completes | Use manual commit or transactional offset commit |
| Unbounded `max.poll.interval.ms` | Slow consumers never detected, lag grows silently | Set to match worst-case processing time |
| Running ZooKeeper on 4.0+ | ZooKeeper is removed | Migrate to KRaft on 3.9 first |
| `PLAINTEXT` security protocol in production | No encryption, no authentication | Use `SASL_SSL` always |
| Skipping Schema Registry | Schema drift breaks consumers silently | Use Schema Registry with `BACKWARD` compatibility |

## Version-Specific Guidance

| Version | Reference | What's Version-Specific |
|---|---|---|
| Kafka 3.9 | `references/versions/3.9.md` | Last ZK version, tiered storage GA, migration bridge |
| Kafka 4.0 | `references/versions/4.0.md` | ZooKeeper removed, KIP-848 GA, Share Groups EA |
| Kafka 4.1 | `references/versions/4.1.md` | Share Groups preview, Streams rebalance, OAuth, ELR default |
| Kafka 4.2 | `references/versions/4.2.md` | Share Groups GA, Streams DLQ, CLI standardization (current) |

## Cross-References

- `overview` skill -- Parent ETL domain guidance
- `streaming` skill -- Streaming subdomain comparison
- The messaging plugin's `kafka` skill (future) -- Kafka as a messaging platform (pub/sub, queuing patterns, Share Groups for queue semantics)

## Reference Files

- `references/architecture.md` -- Broker internals, replication mechanics, KRaft consensus, tiered storage, log compaction, Schema Registry, Kafka Connect and Streams deep dive, exactly-once internals
- `references/best-practices.md` -- Topic design, partition sizing, producer/consumer tuning, exactly-once patterns, schema evolution, security hardening, monitoring, multi-DC replication
- `references/diagnostics.md` -- Consumer lag, rebalancing storms, under-replicated partitions, performance bottlenecks (network, disk, GC), CLI tools, log compaction issues, partition reassignment, broker failure and recovery
