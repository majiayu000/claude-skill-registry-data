---
name: nats
description: "Configure NATS messaging and JetStream persistence; manage pub/sub subjects, consumer groups, key-value buckets, and distributed clustering."
category: devops
risk: safe
source: self
source_type: self
date_added: "2026-09-13"
tags: ["nats", "jetstream", "messaging", "pubsub", "microservices", "event-driven", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# NATS & JetStream Distributed Messaging AI Skill Guide

## Overview & Engine Architecture

NATS is a cloud-native, high-performance messaging system designed for microservices, edge devices, and event-driven architectures. While **Core NATS** provides lightweight, in-memory, at-most-once publish-subscribe and request-reply routing, **NATS JetStream** adds distributed persistence, at-least-once delivery, exactly-once message deduplication, time-ordered streams, key-value (KV) stores, and object stores built upon a distributed Raft consensus layer.

Claude operates as a Principal Messaging Architect and Cloud Infrastructure Engineer, specializing in **JetStream stream topologies**, **subject namespace design**, **durable pull consumers**, **message deduplication windows**, and **fault-tolerant multi-cluster superclusters**.

### NATS Core & JetStream Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 NATS & JetStream Topology                   │
│                                                             │
│  Publishers (Microservices / Edge Devices / Webhooks)       │
│  └── Subjects: `orders.us.created`, `telemetry.sensors.temp`│
│                                                             │
│  NATS Server Cluster (Raft-replicated Metadata & JetStream) │
│  ├── In-Memory Core NATS (Microsecond Latency Routing)      │
│  ├── JetStream Stream Storage (File/Memory with Retention)  │
│  │   ├── Retention Policies: Limits, WorkQueue, Interest    │
│  │   └── Deduplication Engine (`Nats-Msg-Id` Window)        │
│  └── Distributed KV & Object Stores                         │
│                                                             │
│  Consumers (Pull / Push Consumer Groups)                    │
│  ├── Durable Pull Consumers (Batch Fetch, Explicit Ack)     │
│  └── Ephemeral Observers & Real-Time Monitoring             │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **Hierarchical Subject Namespaces**: Segment subjects cleanly using dot tokens (`app.region.resource.action`). Use `*` for single-token wildcards and `>` for trailing multi-token wildcards. Never use broad wildcards like `>` in high-throughput JetStream streams without specific subject filters.
2. **Exactly-Once Delivery via Deduplication**: In payment and order pipelines, always attach the `Nats-Msg-Id` header to published messages and configure the stream's `duplicate_window` (e.g., `2m` or `10m`) to prevent duplicate writes during network retries.
3. **Prefer Durable Pull Consumers**: In production microservices, use durable pull consumers over push consumers to allow consumers to control their own batch sizes (`fetch()`) and prevent slow-consumer buffer overflow drops.
4. **Explicit Acknowledgments**: Always configure `AckPolicy: AckExplicit`. Acknowledge messages only after business logic has safely completed (`msg.ack()`), or call `msg.nak()` with backoff when temporary downstream failures occur.

---

## Production Node.js / TypeScript Automation: JetStream Stream & Pull Consumer

### 1. JetStream Stream Setup & Publishing (`src/nats_producer.ts`)

```typescript
import { connect, JSONCodec, headers } from "nats";

interface OrderEvent {
  orderId: string;
  customerId: string;
  total: number;
}

async function produceOrder() {
  const nc = await connect({ servers: ["nats://127.0.0.1:4222"] });
  const js = nc.jetstream();
  const jsm = await nc.jetstreamManager();
  const codec = JSONCodec<OrderEvent>();

  // Ensure Stream exists with limits and deduplication window
  await jsm.streams.add({
    name: "ORDERS",
    subjects: ["orders.*"],
    retention: "limits" as any,
    max_bytes: 1024 * 1024 * 1024, // 1 GB
    max_age: 7 * 24 * 60 * 60 * 1e9, // 7 days in nanoseconds
    duplicate_window: 120 * 1e9, // 2 minutes deduplication
  });

  const order: OrderEvent = { orderId: "ord-1042", customerId: "cust-9", total: 249.99 };
  const hdrs = headers();
  hdrs.append("Nats-Msg-Id", `order-${order.orderId}`); // Idempotent key

  const pubAck = await js.publish("orders.created", codec.encode(order), { headers: hdrs });
  console.log(`Published order ${order.orderId} to stream ${pubAck.stream} at seq ${pubAck.seq}`);

  await nc.drain();
}

produceOrder().catch(console.error);
```

### 2. Resilient Durable Pull Consumer (`src/nats_consumer.ts`)

```typescript
import { connect, JSONCodec, ackDelay } from "nats";

async function consumeOrders() {
  const nc = await connect({ servers: ["nats://127.0.0.1:4222"] });
  const js = nc.jetstream();
  const codec = JSONCodec();

  // Create or bind durable pull consumer
  const consumer = await js.consumers.get("ORDERS", "order-worker-group");
  console.log("Connected to consumer: order-worker-group");

  const messages = await consumer.consume({ max_messages: 10 });
  for await (const msg of messages) {
    try {
      const data = codec.decode(msg.data);
      console.log(`Processing message seq: ${msg.seq}`, data);

      // Simulate business logic
      msg.ack();
    } catch (err) {
      console.error(`Error processing seq ${msg.seq}, sending NAK:`, err);
      msg.nak(ackDelay(2000)); // retry in 2 seconds
    }
  }
}

consumeOrders().catch(console.error);
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **`nats: Slow Consumer Detected` error** | Consumer process cannot process messages as fast as they arrive on an in-memory push subject. | 1. Migrate workload to a **JetStream Durable Pull Consumer**.<br>2. Increase consumer worker concurrency.<br>3. Tune client buffer sizes (`max_pending`). |
| **`ErrNoStorage` or `Maximum Stream Storage Exceeded`** | Stream exceeded `max_bytes` or underlying disk partition is full. | 1. Inspect stream status via `nats stream info ORDERS`.<br>2. Lower stream retention TTL (`max_age`) or change retention to `workqueue` if messages are consumed once.<br>3. Expand disk volume. |
| **Duplicate processing of messages across restarts** | Consumer is using `AckNone` or failed to call `msg.ack()` before `ack_wait` timeout expired. | 1. Ensure `AckPolicy` is set to `AckExplicit`.<br>2. Tune `ack_wait` to exceed the maximum expected activity execution time.<br>3. Verify consumer uses consistent durable names. |
| **Cluster leader election failure in JetStream** | Network partition or insufficient nodes to achieve Raft quorum (need $(N/2)+1$). | 1. Check `nats server report jetstream`.<br>2. Ensure cluster has at least 3 nodes with odd-numbered sizing.<br>3. Verify network connectivity on port 6222. |

---

## Command Line Syntax & Operational Recipes

```bash
# 1. Start NATS server with JetStream enabled
nats-server -js -sd /var/lib/nats/storage -p 4222

# 2. Inspect active streams and storage statistics
nats stream ls
nats stream info ORDERS

# 3. Create a Key-Value bucket with 30-day TTL
nats kv add app-config --history 5 --ttl 30d

# 4. Monitor real-time message flow across all subjects
nats sub ">"
```

---

## Agent Operational Directive

> **MANDATORY**: For any financial, inventory, or transactional workflows, always enforce `duplicate_window` on streams and send deterministic `Nats-Msg-Id` headers to eliminate duplicate execution under network retries.
