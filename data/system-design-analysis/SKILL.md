---
name: system-design-analysis
description: |
  Analyze, review, and provide recommendations for distributed system designs. Use when:
  (1) Reviewing existing system architectures for gaps or improvements,
  (2) Analyzing system designs for scalability, reliability, or performance issues,
  (3) Providing recommendations on load balancing, caching, databases, sharding, replication, messaging, rate limiting, authentication, resilience, or monitoring,
  (4) Assessing trade-offs in system design decisions,
  (5) Creating system design review documents with gaps and recommendations.
  Triggers: "review my system design", "analyze this architecture", "what are the gaps", "system design recommendations", "scalability review", "reliability analysis".
---

# System Design Analysis

Analyze distributed system designs for scalability, reliability, performance, and security. Produce structured review documents with gaps and actionable recommendations.

## Core Principle

System design is about trade-offs, not perfect answers. Every recommendation must consider context: access patterns, scale requirements, consistency needs, and operational constraints.

## Workflow

### Phase 1: Information Gathering

Ask focused questions to understand the system. Prioritize these areas:

1. **Functional scope**: What does the system do? Core operations?
2. **Scale**: Expected QPS, data volume, user count?
3. **Access patterns**: Read-heavy vs write-heavy? Hot spots?
4. **Consistency requirements**: Strong vs eventual? Where?
5. **Availability targets**: SLA requirements? Acceptable downtime?
6. **Current architecture**: Existing components, databases, services?
7. **Known pain points**: What's broken or struggling today?

Limit to 3-5 questions per message. Make reasonable assumptions when information is missing—document assumptions explicitly.

### Phase 2: Topic Analysis

Based on gathered information, analyze relevant system design topics. Load reference files as needed:

| Topic | Reference File | When to Load |
|-------|----------------|--------------|
| Load balancing | [load-balancing.md](references/load-balancing.md) | Traffic distribution, L4/L7 decisions |
| Caching | [caching.md](references/caching.md) | Latency optimization, read scaling |
| Databases | [databases.md](references/databases.md) | Data modeling, SQL vs NoSQL choices |
| CAP & Consistency | [cap-consistency.md](references/cap-consistency.md) | Consistency model decisions |
| Sharding | [sharding-partitioning.md](references/sharding-partitioning.md) | Write/storage scaling |
| Replication | [replication.md](references/replication.md) | Availability, read scaling |
| Message queues | [message-queues.md](references/message-queues.md) | Async processing, decoupling |
| Rate limiting | [rate-limiting.md](references/rate-limiting.md) | Traffic protection, abuse prevention |
| Auth | [auth.md](references/auth.md) | Security, identity management |
| Resilience | [resilience-patterns.md](references/resilience-patterns.md) | Failure handling, fault tolerance |
| Monitoring | [monitoring-observability.md](references/monitoring-observability.md) | Observability, debugging |

Load only topics relevant to the specific system under review.

### Phase 3: Document Generation

Produce a structured analysis document with these sections:

```
# System Design Analysis: [System Name]

## 1. Abstract
Brief summary of the system and analysis scope (2-3 paragraphs).

## 2. Requirements

### 2.1 Stated Requirements
Requirements explicitly provided by user.

### 2.2 Assumed Requirements
Reasonable assumptions with rationale. Format:
- **Assumption**: [what was assumed]
- **Rationale**: [why this is reasonable]

## 3. Current System Review
Analysis of existing architecture against requirements. Organize by topic area.

## 4. Gaps
Identified issues, risks, or missing capabilities. Prioritize by impact:
- **Critical**: System failures, data loss risks
- **High**: Performance bottlenecks, scalability limits
- **Medium**: Operational inefficiencies, maintainability issues
- **Low**: Nice-to-have improvements

## 5. Recommendations
Actionable improvements with:
- **Problem addressed**: Which gap(s) this solves
- **Recommendation**: Specific technical approach
- **Example**: Concrete implementation guidance
- **Trade-offs**: What you gain vs what you sacrifice
- **Impact**: Expected improvement if implemented
```

## Analysis Checklist

For each relevant topic, evaluate:

**Load Balancing**
- [ ] Algorithm appropriate for workload (round robin, least connections, consistent hashing)?
- [ ] L4 vs L7 appropriate for use case?
- [ ] LB itself highly available?
- [ ] Health checks configured?

**Caching**
- [ ] Cache strategy defined (cache-aside, write-through)?
- [ ] Eviction policy appropriate (LRU, TTL)?
- [ ] Cache invalidation strategy?
- [ ] Hot key and cache stampede handling?

**Databases**
- [ ] Data model matches access patterns?
- [ ] Indexes support critical queries?
- [ ] Read-heavy vs write-heavy considered?
- [ ] Appropriate SQL vs NoSQL choice?

**CAP & Consistency**
- [ ] Consistency model matches business requirements?
- [ ] Trade-offs between C and A explicit?
- [ ] Read-your-writes where needed?

**Sharding**
- [ ] Shard key distributes load evenly?
- [ ] Hot partitions addressed?
- [ ] Cross-shard operations minimized?

**Replication**
- [ ] Sync vs async replication appropriate?
- [ ] Replica lag acceptable?
- [ ] Leader election mechanism defined?
- [ ] Split-brain prevention?

**Message Queues**
- [ ] Delivery guarantees appropriate?
- [ ] Consumer idempotency?
- [ ] Dead-letter queue for failures?
- [ ] Backpressure handling?

**Rate Limiting**
- [ ] Algorithm chosen (token bucket recommended)?
- [ ] Limits appropriate for different tiers?
- [ ] Distributed enforcement for multi-node?
- [ ] Graceful handling of limit breaches?

**Authentication & Authorization**
- [ ] AuthN mechanism appropriate (JWT, sessions)?
- [ ] Token lifecycle managed (expiry, refresh)?
- [ ] AuthZ model defined (RBAC, ABAC)?
- [ ] Service-to-service auth?

**Resilience**
- [ ] Timeouts on all external calls?
- [ ] Retry strategy with backoff?
- [ ] Circuit breakers for unstable dependencies?
- [ ] Graceful degradation paths?

**Monitoring**
- [ ] Golden signals tracked (latency, traffic, errors, saturation)?
- [ ] Distributed tracing for request flows?
- [ ] Structured logging?
- [ ] Alerts tied to SLOs, not raw metrics?

## Common Anti-Patterns to Flag

- **No caching strategy**: "Just add Redis" without invalidation plan
- **Wrong database choice**: Forcing SQL for graph data or NoSQL for transactions
- **Ignoring partition tolerance**: Designing as if network never fails
- **Naive sharding**: Choosing shard key without considering access patterns
- **Synchronous everything**: No async processing for non-critical paths
- **Alert fatigue**: Alerting on every error instead of user impact
- **Missing rate limiting**: No protection against traffic spikes
- **Stateless assumption violations**: Session stickiness breaking horizontal scaling
