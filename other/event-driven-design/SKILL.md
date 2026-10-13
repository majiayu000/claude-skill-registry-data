---
name: event-driven-design
description: Design event-driven systems using event storming, domain events, and pub/sub patterns. Apply Martin Fowler's event patterns (event notification, event-carried state transfer, event sourcing, CQRS) to decouple services and improve system resilience.
triggers:
  - "event driven"
  - "event storming"
  - "pub sub"
  - "domain events"
  - "decouple services"
  - "async communication"
  - "event sourcing"
  - "CQRS"
audience:
  - engineer
  - manager
---

# Event-Driven Design

Design systems where components communicate through events, reducing coupling and improving resilience.

## Fowler's Four Event Patterns

Choose the right pattern before writing any code:

### 1. Event Notification
- Fires a lightweight "something happened" message; receiver fetches details if needed
- **Use when**: You want to notify downstream systems without coupling to their needs
- **Example**: `OrderPlaced { orderId: "123" }` — receiver calls back for order details
- **Trade-off**: Extra round-trip; receiver must handle stale data risk

### 2. Event-Carried State Transfer
- Event contains all data the receiver needs — no callback required
- **Use when**: Receivers need to maintain local replicas for performance/autonomy
- **Example**: `OrderPlaced { orderId, customerId, items[], total, shippingAddress }`
- **Trade-off**: Larger payloads; schema evolution is harder; data duplication

### 3. Event Sourcing
- State is derived by replaying a sequence of events; no mutable records
- **Use when**: Audit trail is critical, temporal queries needed, or undo/replay is a product feature
- **Example**: `AccountDebitedEvent`, `AccountCreditedEvent` → current balance = sum of events
- **Trade-off**: Query complexity, snapshot strategies required, steep learning curve

### 4. CQRS (Command Query Responsibility Segregation)
- Separate write model (commands → events) from read model (projections)
- **Use when**: Read and write workloads have different scaling or consistency requirements
- **Trade-off**: Eventual consistency, operational complexity

---

## Event Storming

A collaborative discovery technique for mapping domain events before writing code.

### Workshop Setup
- **Participants**: Engineers + product + domain experts (not just devs)
- **Materials**: Sticky notes (orange = domain events, blue = commands, yellow = actors/users, pink = external systems, red = hotspots/problems)
- **Time**: 2–4 hours for a bounded context

### Steps
1. **Chaotic Exploration** — Everyone adds domain events (past tense: `OrderPlaced`, `PaymentFailed`)
2. **Timeline** — Sort events left to right in temporal order
3. **Reverse Narrative** — Walk backwards: what caused this event?
4. **Commands** — Add commands (imperative: `PlaceOrder`) that trigger each event
5. **Actors** — Who/what issues the command?
6. **Aggregates** — Group related commands + events around a shared concept
7. **Hotspots** — Mark disagreements, unknowns, complexity (red stickies)
8. **Bounded Contexts** — Draw lines around cohesive groups → these become service boundaries

### Bounded Context Output Template
```
Context: [name]
Owns events: [list]
Publishes to: [other contexts]
Subscribes to: [other contexts]
Aggregate: [core entity]
Invariants: [business rules that must always hold]
```

---

## Domain Event Design

### Event Schema Checklist
- [ ] Past tense name: `OrderPlaced`, not `PlaceOrder` or `OrderEvent`
- [ ] Contains `eventId` (UUID), `occurredAt` (ISO8601), `aggregateId`
- [ ] Versioned: `"version": 1` in payload or topic name
- [ ] Idempotent consumers supported: same event processed twice = same result
- [ ] Schema registered (Avro/Protobuf/JSON Schema) — no freeform JSON blobs

### Topic/Queue Naming Convention
```
{domain}.{aggregate}.{event}
# Examples:
orders.order.placed
payments.invoice.paid
users.account.suspended
```

---

## Pub/Sub Architecture

```
Publisher (Service A)
  → emits: OrderPlaced
  → topic: orders.order.placed

Subscribers:
  → InventoryService: reserves stock
  → NotificationService: sends confirmation email
  → FraudService: evaluates for risk
  → AnalyticsService: records for reporting
```

**Key principles:**
- Publishers don't know about subscribers — zero coupling
- Each subscriber maintains its own consumer group / offset
- Dead letter queues (DLQ) for failed processing — never silently drop events
- Idempotency keys prevent duplicate processing

---

## Common Anti-Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| Event as RPC | Synchronous request disguised as event (waiting for reply) | Use gRPC/REST for synchronous calls |
| God event | One event carries everything for every consumer | Split by bounded context |
| Missing schema registry | Events change silently, consumers break | Use Avro/Protobuf + schema registry |
| No DLQ | Failed events disappear | Always configure dead letter queue |
| Choreography hell | 10 services react to each other, impossible to trace | Add orchestration layer for complex flows (Saga pattern) |
| Temporal coupling | Consumer must be up when event fires | Use durable messaging (Kafka, SQS) not in-memory buses |

---

## Decision: Choreography vs Orchestration

**Choreography** (each service reacts autonomously):
- Good for: simple flows, high decoupling, < 4 services involved
- Bad for: complex multi-step transactions, debugging, error recovery

**Orchestration** (central coordinator drives the flow):
- Good for: Saga patterns, compensating transactions, visibility
- Bad for: creates central coupling point, single point of failure

**Rule of thumb**: Start with choreography. Add an orchestrator when you can't trace a business process end-to-end.

---

## Output: Event Design Document

```markdown
## Event: [EventName]

**Domain**: [bounded context]
**Trigger**: [what command or state change causes this]
**Pattern**: [notification / state-transfer / event-sourcing]
**Schema version**: 1

### Payload
```json
{
  "eventId": "uuid",
  "occurredAt": "ISO8601",
  "aggregateId": "string",
  // domain fields
}
```

### Consumers
| Service | Why | Processing | Idempotent? |
|---|---|---|---|
| [name] | [reason] | [async/DLQ] | [yes/no] |

### Schema Evolution Strategy
[How will you add fields? What's the deprecation policy?]
```

---

## References
- Martin Fowler: [What do you mean by "Event-Driven"?](https://martinfowler.com/articles/201701-event-driven.html)
- Martin Fowler: [Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html)
- Martin Fowler: [CQRS](https://martinfowler.com/bliki/CQRS.html)
- Alberto Brandolini: [Event Storming](https://www.eventstorming.com/)
