---
name: nats
description: "Expert coverage of NATS 2.x messaging system (2.10-2.12): Core NATS pub/sub, JetStream persistence, KV Store, Object Store, clustering, leaf nodes, super-clusters, and decentralized security. Use for \"NATS\", \"nats-server\", \"JetStream\", \"NATS stream\", \"NATS consumer\", \"subject\", \"queue group\", \"leaf node\", \"gateway\", \"super-cluster\", \"NATS KV\", \"Key-Value store NATS\", \"Object Store NATS\", \"nats CLI\", \"nsc\", \"NKey\", \"JWT auth NATS\", \"nats pub\", \"nats sub\", \"nats request\", \"nats reply\", \"Core NATS\", \"nats-top\", \"NATS account\", \"NATS mirror\", \"NATS source\", \"atomic publish\", \"message TTL NATS\"."
license: MIT
---

# NATS

This skill covers NATS across versions 2.10 through 2.12, including:

- Core NATS (fire-and-forget pub/sub, subject-based addressing, queue groups, request/reply)
- JetStream (persistent streams, consumers, deduplication, exactly-once, retention policies)
- KV Store (bucket CRUD, watch, history, compare-and-swap, per-key TTL)
- Object Store (large file chunking, metadata, links)
- Clustering (route-based full mesh, RAFT consensus for JetStream, multi-route connections)
- Super-clusters (gateways for cross-cluster connectivity, interest propagation)
- Leaf nodes (hub-and-spoke, edge/IoT, hybrid cloud)
- Security (accounts, NKey, JWT decentralized auth, auth callout, mTLS)
- Monitoring (HTTP endpoints, nats-top, Prometheus exporter, system account events)
- Stream mirrors and sources (geographic distribution, aggregation, mirror promotion)

## How to Approach Tasks

1. **Classify** the request:
   - **Troubleshooting** -- Load `references/diagnostics.md` for consumer lag, stream issues, cluster health, connectivity, and CLI tools
   - **Architecture / design** -- Load `references/architecture.md` for Core NATS, JetStream, clustering, security, KV/Object Store
   - **Best practices** -- Load `references/best-practices.md` for subject design, stream configuration, consumer tuning, security, monitoring

2. **Identify version** -- Key version gates:
   - Multi-filter consumers, S2 compression, subject transforms, auth callout (2.10)
   - Per-message TTL, consumer pausing, priority groups, distributed tracing (2.11)
   - Atomic batch publish, distributed counters, delayed scheduling, mirror promotion, strict mode default (2.12)

3. **Load context** -- Read the relevant reference file before answering.

4. **Recommend** -- Provide actionable guidance with `nats` CLI commands, server config, and SDK examples.

## Core Architecture

### Core NATS (Fire-and-Forget)

Sub-millisecond latency. No persistence. If no subscriber exists, message is dropped. Optimized for speed and simplicity.

### Subject-Based Addressing

Subjects use `.` as token separator. Wildcards (subscribers only): `*` (single token), `>` (multi-token tail).
```
orders.us.created       -- specific subject
orders.*.created        -- matches orders.us.created, orders.eu.created
orders.>                -- matches orders.us, orders.us.east.created
```

### Queue Groups

Built-in load balancing. Multiple subscribers on same queue group receive messages round-robin:
```bash
nats sub --queue workers "orders.>"    # subscriber 1
nats sub --queue workers "orders.>"    # subscriber 2 (load-balanced)
```

### JetStream

Built-in persistence engine. Streams capture messages from subjects. Consumers track position independently.

**Retention policies:** `LimitsPolicy` (default, retain to limits), `WorkQueuePolicy` (consume-once), `InterestPolicy` (retain while consumers exist).

**Consumer types:** Pull (recommended) or Push. Durable (named, persistent state) or Ephemeral.

### KV Store and Object Store

KV: Built on JetStream streams. Consistent key-value with watch, history, CAS. Object Store: Large binary chunking with metadata and SHA-256 checksums.

## Anti-Patterns

| Anti-Pattern | Why It Fails | Instead |
|---|---|---|
| Using Core NATS for critical business events | No persistence; messages dropped if no subscriber | Use JetStream with explicit ack |
| Unbounded streams without limits | Disk fills up; no backpressure | Set MaxAge, MaxBytes, MaxMsgs |
| Push consumers for work queue patterns | Less control over flow; harder to scale | Use pull consumers |
| Publishing to wildcards | Not supported; server rejects | Publish to specific subjects |
| Large deduplication windows | Memory overhead per tracked ID | Keep Duplicates window as short as practical (default 2min) |
| Even-sized clusters | Split-brain risk | Use odd node counts (3 or 5) |

## Reference Files

- `references/architecture.md` -- Core NATS, JetStream streams/consumers, KV Store, Object Store, clustering (routes, gateways, leaf nodes), security (accounts, NKey, JWT, auth callout), monitoring
- `references/best-practices.md` -- Subject namespace design, stream configuration, consumer tuning, deduplication, security hardening, monitoring setup, version-specific features
- `references/diagnostics.md` -- Stream lag, consumer issues, cluster health, RAFT troubleshooting, connectivity, slow consumers, CLI reference, health checks

## Cross-References

- The `overview` skill -- cross-broker comparisons and event-driven architecture design
