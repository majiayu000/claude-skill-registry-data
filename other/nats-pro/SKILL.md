---
name: nats-pro
description: NATS guidance — subjects, JetStream persistence, consumer patterns, clustering, and lightweight messaging design.
category: development
---

## Overview

NATS is a lightweight, high-performance messaging system: a single small binary, subject-based addressing, and optional JetStream persistence that adds streams, consumers, and exactly the durability you ask for. Where Kafka is heavy infrastructure and RabbitMQ is a feature-rich broker, NATS aims to disappear — connect and send.

That simplicity is deliberate: core NATS is fire-and-forget pub/sub and request-reply; JetStream adds persistence, consumer groups, and redelivery when you need them. This skill covers subject design, choosing core vs JetStream, consumer patterns, and operating NATS clusters.

## When to use

- Adding lightweight messaging between services.
- Choosing between NATS, Kafka, RabbitMQ, or Redis pub/sub.
- Designing subject hierarchies and stream topology.
- Implementing request-reply and service discovery patterns.
- Using JetStream for persistent streams and work queues.
- Clustering NATS for HA (superclusters, leaf nodes).
- Replacing ad-hoc HTTP polling with events.

## Core concepts

- **Subjects, not queues.** Messages publish to hierarchical subjects (`orders.created.us`); subscribers use wildcards (`orders.*`, `orders.>`). Design the hierarchy early — it's your routing, filtering, and multi-tenancy scheme.
- **Core NATS: fire-and-forget.** At-most-once pub/sub with no persistence — blazing fast, zero storage. Perfect for telemetry, cache invalidation, and signals where loss is acceptable.
- **Request-reply.** Built-in pattern: publish with a reply subject, responder replies to it. With queue groups it becomes load-balanced RPC — a natural service-mesh primitive without the mesh.
- **JetStream: persistence when you need it.** Streams persist messages with retention policies; consumers track progress with acks. Same server, opt-in durability — start with core, add JetStream where loss is unacceptable.
- **Streams and retention.** Limits-based, age-based, or work-queue retention (messages removed on ack). Work-queue retention gives you a distributed work queue with redelivery built in.
- **Consumers: push vs pull.** Push consumers get messages delivered (low latency, needs flow control); pull consumers fetch batches explicitly (backpressure-friendly, better for workers). Pull consumers are the safer default for work queues.
- **Ack policies.** Explicit ack (production default), none (fire-and-forget within JetStream), all (only ack the last — for ordered streams). Ack wait + max deliveries → redelivery → dead-letter via max-deliveries handling.
- **Queue groups.** Multiple subscribers sharing a subject with a queue group name split messages among them — the NATS load-balancing primitive for both core and JetStream.
- **KeyValue and ObjectStore.** JetStream-powered KV (materialized state, watchable) and object storage (large blobs chunked into streams) — often replacing a database or S3 for operational data.
- **Clustering.** NATS clusters with full mesh + gossip; superclusters connect clusters across regions; leaf nodes attach edge workloads. Design for your failure domains — don't stretch one cluster across high-latency links.
- **Security.** Accounts (multi-tenancy with isolation), users with scoped permissions (publish/subscribe allowlists), NKeys/JWT auth, TLS. Accounts are the isolation boundary — use them.
- **No broker-side transforms.** NATS routes bytes; schemas, validation, and serialization are your application's job. Keep message formats versioned and documented.
- **Service API.** The NATS service framework adds discovery, status, and stats to request-reply services — lightweight service-mesh primitives without the mesh.
- **Message tracing.** Built-in trace context propagation for distributed tracing across subjects — wire it into your observability stack.

## Practical workflow

1. **Design subjects.** Hierarchical, dot-separated, with wildcards in mind: `svc.orders.created.v1`, `cmd.inventory.reserve`. Reserve `>` carefully — overly broad subscriptions become coupling.
   ```
   pub:  shop.orders.created.eu
   sub:  shop.orders.created.*      (per-region workers)
   sub:  shop.orders.>              (audit)
   ```
2. **Choose core vs JetStream per flow.** Telemetry/signals → core NATS. Anything needing redelivery, replay, or persistence → JetStream stream + consumer.
3. **Create streams deliberately.** Subjects captured, retention policy, storage (memory/file), replicas, max age/bytes — streams are infrastructure, declare them as config.
   ```
   nats stream add ORDERS --subjects "shop.orders.>" --retention limits --storage file --replicas 3
   ```
4. **Build pull consumers for workers.** Durable consumers, explicit ack, `max_deliveries` with dead-letter handling, ack wait tuned to processing time.
   - Fetch batches, process, ack individually; on repeated failure, let max-deliveries route to your DLQ stream.
5. **Use KeyValue for state.** Feature flags, config, materialized views — `kv.put`/`kv.get` with watchers replacing polling loops.
6. **Secure with accounts.** One account per tenant/team; scoped user permissions; NKey auth; TLS everywhere. Test permission denials — overly broad permissions are the default mistake.
7. **Handle reconnects.** NATS clients reconnect and resubscribe automatically; JetStream durable consumers resume from last ack. Design handlers idempotent anyway — redelivery happens.
8. **Operate.** Monitor stream lag (unacked/pending), consumer redelivery rates, cluster routes, and message rates; alert on growing pending counts and cluster partitions.

   ```go
   sub, _ := js.PullSubscribe("shop.orders.>", "order-workers",
       nats.AckWait(30*time.Second), nats.MaxDeliver(5))
   for {
       msgs, _ := sub.Fetch(10, nats.MaxWait(5*time.Second))
       for _, m := range msgs {
           if err := process(m); err == nil { m.Ack() } else { m.Nak() }
       }
   }
   ```

## Common pitfalls

- **Using core NATS for critical data** — no persistence means loss on restart; JetStream exists for a reason.
- **Push consumers without flow control** — fast publishers overwhelming slow consumers; prefer pull consumers for workers.
- **No max-deliveries** — poison messages redelivering forever; cap deliveries and handle the dead-letter path.
- **Overly broad wildcard subscriptions** — `>` subscribers becoming accidental coupling and performance sinks; subscribe narrowly.
- **Ignoring ack wait tuning** — too short causes duplicate processing, too long delays redelivery; match it to real processing time.
- **Single account for everything** — no isolation between teams; use accounts as the security boundary.
- **Unbounded streams** — no max bytes/age; disk exhaustion. Set limits on every stream.
- **Non-idempotent handlers** — redelivery is normal in JetStream; handlers must tolerate replays.
- **Stretching clusters across regions** — latency and partition pain; use superclusters/gateways instead.
- **No schema versioning** — bytes on the wire with no contract; version subjects or payloads and validate.
- **Forgetting replicas** — single-replica streams losing data on node failure; R=3 for anything important.
- **Treating KV as a primary database** — it's operational state, not a system of record; know its limits.
- **Push consumer for bursty workloads** — overwhelming slow subscribers; pull consumers give you backpressure.
- **Ignoring stream storage type** — memory storage losing everything on restart; file storage for anything durable.
