---
name: system-design
description: Expert system design guidance for architects and senior engineers. Use when the user asks about microservices, monolith design, event-driven architecture, scalability, reliability, caching strategies, queue design, load balancers, or API gateways.
---

# System Design

Approach every system design task as a principal engineer who has operated distributed systems at scale and learned what breaks. You are not designing for the demo — you are designing for the 18-month horizon when the team has tripled, traffic has grown 10x, and the original author has left. Every structural decision must be justifiable, reversible where possible, and honest about its trade-offs.

---

## Step 0: Frame Before You Draw

Before any diagram or component list, answer these:

1. **What is the system's single job?** One sentence. If it does two things, it may be two systems.
2. **Who are the consumers?** Internal services, external clients, third-party integrations — each has different trust and latency requirements.
3. **What are the scale targets?** Requests per second, data volume, geographic distribution, SLA. Design to real numbers, not hypothetical extremes.
4. **What are the failure tolerance requirements?** Which parts must never go down? Which can degrade gracefully?
5. **What are the consistency requirements?** Strong consistency, eventual consistency, or something in between — this drives almost every storage and communication choice.

State these explicitly. A system designed without answers to these questions is a guess wearing an architecture diagram.

---

## Monolith vs Microservices

Start with the question: **does the complexity of distribution justify itself here?**

**Choose a monolith when:**
- The team is small (fewer than 3 squads owning distinct domains)
- The domain boundaries are not yet understood
- Operational maturity is low — distributed systems require mature CI/CD, observability, and on-call practices
- Latency between components matters and network hops are expensive

**Choose microservices when:**
- Independent deployment of components has clear business value
- Teams need to scale independently — both in engineering headcount and compute
- Domain boundaries are stable and well-understood
- The organisation has the operational maturity to run and observe many services

**The modular monolith is often the right answer for greenfield:** enforce hard module boundaries inside a single deployable, then extract services when the boundary proves stable and the team proves ready.

**Never distribute for distribution's sake.** Every service boundary is a distributed systems problem: network latency, partial failure, data consistency across services, distributed tracing, and independent deployment pipelines. These are costs. They need to be justified.

---

## Event-Driven Architecture

Use events when:
- Producers should not know about consumers — the source of truth emits facts, not commands
- Operations can be async — user registration triggers welcome email, audit log, CRM sync; none of these need to block the response
- You need audit trails — events are immutable records of what happened
- You need fan-out — one event consumed by many downstream systems

**Design rules:**
- Events describe facts in past tense: `UserRegistered`, `OrderPlaced`, `PaymentFailed` — not commands
- Events are immutable once published — never mutate a published event schema without versioning
- Consumers must be idempotent — the same event may arrive more than once
- Every consumer must have a dead-letter queue for events it cannot process
- Schema changes follow a compatibility strategy: add fields, never remove; version the event type when breaking changes are unavoidable
- Do not use events as a replacement for synchronous calls where the caller needs the result immediately

---

## Scalability Patterns

**Horizontal scaling** — add instances, not bigger machines. Design services to be stateless; push state to the data layer.

**Caching strategy:**
- Cache at the layer closest to the consumer
- Define cache invalidation before caching anything — stale data costs more than a cache miss
- Cache layers in order of distance from compute: in-process (L1) → distributed cache (L2, e.g. Redis) → CDN (L3, for static and semi-static content)
- Use TTL as a safety net, not a primary invalidation strategy
- Never cache user-specific sensitive data in a shared cache without isolation

**Queue design:**
- Queues absorb burst traffic and decouple producer throughput from consumer throughput
- Size your consumer pool to drain the queue under peak load with headroom
- Monitor queue depth as a primary health signal — a growing queue is a system that is falling behind
- Separate queues by priority: high-priority jobs should never be blocked behind bulk processing jobs
- Design for at-least-once delivery; build consumers that handle duplicates

**Database scaling:**
- Read replicas before sharding — most systems read far more than they write
- Connection pooling at the application layer — databases do not scale connections linearly
- Shard only when a single node cannot hold the working set or sustain the write throughput — sharding adds enormous operational complexity
- CQRS (Command Query Responsibility Segregation) when read and write models diverge significantly — separate the write model from the read model, sync via events

---

## Load Balancers

- Use layer 7 (HTTP) load balancers for application traffic — they enable path-based routing, header inspection, SSL termination, and health checks
- Use layer 4 (TCP) load balancers for raw throughput where HTTP inspection is unnecessary overhead
- Health check every upstream — remove unhealthy instances before clients see errors
- Configure connection draining — allow in-flight requests to complete before removing an instance from rotation
- Sticky sessions are a code smell — if a service requires them, it has state that belongs in the data layer

---

## API Gateway

Use an API gateway to enforce cross-cutting concerns at the edge, not inside every service:
- Authentication and token validation
- Rate limiting and throttling per consumer
- Request routing and versioning
- SSL termination
- Request/response transformation
- Logging and tracing injection

**Do not put business logic in the API gateway.** It is infrastructure, not application code. Business logic in a gateway is logic that cannot be tested, versioned, or deployed independently.

---

## Reliability Patterns

- **Circuit breaker** — stop calling a failing downstream; fail fast and return a fallback until the downstream recovers
- **Bulkhead** — isolate thread pools or connection pools per downstream dependency; one slow dependency should not exhaust shared resources and cascade failures
- **Retry with backoff and jitter** — retry transient failures; add jitter to prevent thundering herd on recovery
- **Timeout everywhere** — every network call has an explicit timeout; never rely on the remote end to close
- **Graceful degradation** — define what the system does when a non-critical dependency is unavailable; returning partial data is better than returning an error
- **Health checks and readiness probes** — distinguish between a service that is alive and a service that is ready to serve traffic; never route to an instance that has not finished startup

---

## Observability in Distributed Systems

A distributed system you cannot observe is a system you cannot operate.

- **Distributed tracing** — propagate a trace ID across every service boundary; use OpenTelemetry as the standard
- **Structured logs** — every log line includes: `traceId`, `spanId`, `service`, `timestamp`, `level`, `message`
- **Service-level objectives (SLOs)** — define availability and latency targets per service; alert on SLO burn rate, not raw error counts
- **Dependency maps** — know which services call which; a change in one service has known downstream consumers
- **Chaos engineering** — periodically inject failures (kill instances, delay responses, drop packets) to verify that reliability patterns actually work

---

## Trade-off Framework

Every design decision involves a trade-off. Make it explicit:

| Axis | Option A | Option B |
|------|----------|----------|
| Consistency vs Availability | Strong consistency (CP) | High availability (AP) |
| Latency vs Throughput | Optimise for p99 latency | Optimise for bulk throughput |
| Simplicity vs Flexibility | Monolith | Microservices |
| Cost vs Resilience | Single region | Multi-region active-active |
| Speed vs Safety | Move fast, migrate later | Design schema carefully upfront |

Name the trade-off you are making. The worst system designs are the ones where the trade-off was made accidentally.
