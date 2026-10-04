---
name: microservices-architect
description: >
  Design distributed systems using microservices patterns. Triggers on: microservices, service mesh, distributed systems, event-driven architecture, saga pattern, service boundaries, monolith to microservices, API gateway, message queue, eventual consistency, circuit breaker, gRPC, service decomposition. Provides ADRs, service boundary diagrams, API contracts, data flow analysis, and failure mode assessments. Remember: distributed systems are HARD. Every service boundary is a network call.
---

# Microservices Architecture Skill

## Core Philosophy

Distributed systems introduce complexity that's not worth paying unless you genuinely need it. Most teams reach for microservices too early. Start with a modular monolith. Add microservices only when:
- You have independent scaling needs per domain
- You need true deployment independence
- Your team is large enough to own separate services
- Your data access patterns don't require tight consistency

**The monolith-first argument**: A well-structured monolith is simpler, debuggable, and deployable. Graduate to microservices when pain points prove you need them—not theoretically, but in practice.

---

## 1. When to Use Microservices (and When NOT To)

### Decision Framework

| Characteristic | Monolith | Modular Monolith | Microservices |
|---|---|---|---|
| Team size | 1-5 people | 5-15 people | 15+ people, clear domains |
| Scaling needs | Uniform | Mostly uniform | Heterogeneous by domain |
| Deployment cadence | Single | Single, modular | Independent per service |
| Data consistency | Strong ACID | Mostly strong | Eventual (by necessity) |
| Operational overhead | Low | Low | High (requires observability obsession) |
| Debugging difficulty | Easy | Medium | Hard (distributed tracing required) |

**Red flags for premature microservices**:
- "We want to scale independently" (you don't, yet)
- "We want to use different technologies" (this is a smell, not a feature)
- "We need faster deployment" (deploy your monolith modules independently first)
- "Different teams own different parts" (organize code, not infrastructure)

---

## 2. Service Decomposition

### Strategies

**Domain-Driven Design (DDD)**
- Identify **bounded contexts** in your domain
- Each context maps to one service boundary
- Within a context: tight coupling OK. Between contexts: explicit contracts only.
- Example: Order service, Inventory service, Billing service—not User service (cross-cutting).

**By Business Capability**
- Product Catalog, Order Management, Payments, Fulfillment
- Aligns with org structure and team ownership
- Each service owns its data and API

**By Data Ownership**
- Who owns this data at the business level?
- Avoid shared tables across services
- One service writes; others read via events or APIs

### Anti-patterns

- **Chatty services**: Designing services that require 10 calls to fulfill a request. Coalesce.
- **Shared databases**: Couples services at the data layer. Own your data.
- **God services**: 10+ responsibilities. You've just moved complexity, not reduced it.

---

## 3. Communication Patterns

### Synchronous

**REST/HTTP**
- Simple, debuggable, browser-friendly
- Tight coupling via request/response
- Use for **immediate consistency needs** (user-initiated actions)
- Timeout is your friend: always set explicit timeouts. Cascade failures otherwise.

**gRPC**
- Typed, contract-first (Protocol Buffers)
- Binary (faster, smaller payload)
- Streaming support
- Use when: high throughput, low latency, strong contracts matter
- Your FastAPI backend can call gRPC services via Python clients

### Asynchronous

**Message Queues** (RabbitMQ, Kafka, AWS SQS)
- Decouple timing of request and response
- Services don't need to know about each other
- Use for: background jobs, eventual consistency, fire-and-forget workflows
- Example: Order placed → publish OrderCreated event → Inventory service consumes and reserves stock

**Event-Driven Architecture**
- Services emit events when state changes
- Other services subscribe and react
- Single source of truth: events, not shared state
- Kafka is the golden standard (immutable log, replay-able)

**Saga Pattern** (Distributed Transactions)
- For cross-service workflows that must complete or all rollback
- Choreography: services listen and trigger each other (implicit, hard to debug)
- Orchestration: dedicated saga coordinator (explicit, easier to reason about)
- Example: CreateOrder saga → Reserve inventory → Process payment → Confirm shipment (or all rollback)
- This complexity is a smell: if you need sagas, your service boundaries are probably wrong

### Before/After Communication Patterns

**Example 1: Synchronous Chain → Async Event-Driven**

```python
# BEFORE: Synchronous chain (Order Service calls Inventory Service calls Warehouse Service)
# FastAPI Order Handler
@app.post("/api/orders")
async def create_order(req: OrderRequest):
    order = Order(user_id=req.user_id, total=req.total)
    db.save(order)

    # Direct synchronous call to Inventory Service
    inv_response = httpx.post(
        "http://inventory-service/reserve",
        json={"order_id": order.id, "items": req.items}
    )
    if not inv_response.ok:
        db.delete(order)  # Rollback
        raise Exception("Inventory unavailable")

    # Direct synchronous call to Warehouse Service
    warehouse_response = httpx.post(
        "http://warehouse-service/schedule",
        json={"order_id": order.id}
    )
    if not warehouse_response.ok:
        # Complex rollback logic...
        pass

    return {"order_id": order.id, "status": "confirmed"}
```

Problems: Tight coupling, cascading failures, complex rollback, slow response time.

```python
# AFTER: Async event-driven (Order Service publishes event, Inventory and Warehouse listen independently)
# Order Service
@app.post("/api/orders")
async def create_order(req: OrderRequest):
    order = Order(user_id=req.user_id, total=req.total, status="pending")
    db.save(order)

    # Publish event and return immediately
    event = {
        "event_type": "order.created",
        "order_id": order.id,
        "items": req.items
    }
    await kafka_producer.send("orders", json.dumps(event))

    return {"order_id": order.id, "status": "pending"}

# Inventory Service (independent consumer)
async def inventory_consumer():
    async for message in kafka_consumer.subscribe("orders"):
        event = json.loads(message.value)
        if event["event_type"] == "order.created":
            try:
                reserve_inventory(event["order_id"], event["items"])
                publish_event("inventory.reserved", order_id=event["order_id"])
            except InsufficientStock:
                publish_event("order.failed", order_id=event["order_id"], reason="no_stock")

# Warehouse Service (independent consumer)
async def warehouse_consumer():
    async for message in kafka_consumer.subscribe("orders"):
        event = json.loads(message.value)
        if event["event_type"] == "inventory.reserved":
            schedule_shipment(event["order_id"])
            publish_event("shipment.scheduled", order_id=event["order_id"])
```

Benefits: Services decouple, fast response (no waiting), independent scaling, easier recovery.

**Example 2: Shared Database → Database-per-Service**

```python
# BEFORE: Shared database (Order and Inventory services both read/write shared tables)
# Order Service: reads inventory directly
SELECT o.id, o.total, i.quantity_available
FROM orders o
JOIN inventory i ON o.product_id = i.product_id

# Inventory Service: also manages inventory table
UPDATE inventory SET quantity_available = quantity_available - 1 WHERE product_id = ?

# Problem: Race conditions, tight coupling, cascading schema changes
```

```python
# AFTER: Database-per-service (Inventory Service owns inventory data)
# Order Service: has its own schema, calls Inventory Service API
class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    product_id = Column(Integer)  # No foreign key to inventory
    quantity = Column(Integer)
    total = Column(Decimal)

# To check availability:
async def can_fulfill_order(product_id: int, quantity: int) -> bool:
    response = await httpx.get(
        f"http://inventory-service/products/{product_id}/availability",
        params={"quantity": quantity}
    )
    return response.json()["available"]

# Inventory Service: owns its database and API
class InventoryStock(Base):
    __tablename__ = "stock"
    product_id = Column(Integer, primary_key=True)
    quantity_available = Column(Integer)
    last_updated = Column(DateTime)

@app.get("/products/{product_id}/availability")
async def check_availability(product_id: int, quantity: int):
    stock = db.query(InventoryStock).filter(
        InventoryStock.product_id == product_id
    ).first()
    return {
        "product_id": product_id,
        "available": stock.quantity_available >= quantity if stock else False
    }
```

Benefits: Scaling independent, schema evolution independent, clear data ownership.

### API Gateway

- Single entry point for external clients
- Handles routing, authentication, rate limiting, response aggregation
- Anti-pattern: Making the gateway smart. Keep it dumb (routing + cross-cutting concerns only).

---

## 4. Data Management

### Database-per-Service Pattern

**Rule**: Each service owns one database. No cross-service queries.

Why?
- Service independence: deploy without coordinating migrations
- Scaling: optimize schema per service needs
- Failure isolation: one DB goes down, others unaffected

**Implementation**:
- Order Service has `orders` DB with `orders`, `order_items` tables
- Inventory Service has separate `inventory` DB with `stock`, `reservations` tables
- They communicate via APIs/events, not shared tables

### Eventual Consistency

The harsh reality of microservices: **you cannot have strong consistency across service boundaries without synchronous blocking calls** (which re-couple services).

Accept eventual consistency. Design for it:
- Order placed → Inventory increments eventually
- Display "processing" state to user during consistency window
- Implement conflict resolution (e.g., if inventory insufficient, trigger compensation)

**When you *need* strong consistency across services**: You drew the boundary wrong. Move those domains into the same service.

### Event Sourcing (Use Sparingly)

Store the immutable event log instead of current state. Reconstruct state by replaying events.

**Worth the complexity only if**:
- You need audit trails (regulatory requirement)
- You need to debug "how did we get here?" (time-travel debugging)
- You're processing high-velocity events

**Cost**: Schema migrations become event migrations. Snapshots needed to avoid replaying years of events.

For your Python/FastAPI apps, consider Kafka as an event store before building custom event sourcing.

### Shared Data Anti-patterns

- Shared database tables (couples services at data layer)
- "Read-only" cross-service queries (still couples; use events instead)
- Shared reference tables (duplicate them or use a reference service API)

---

## 5. Resilience Patterns

**Every network call can fail.** Design for it.

### Circuit Breaker
- Track failures to a dependency
- After N failures: stop calling, return cached/default response (open state)
- Periodically retry (half-open state)
- Restore when succeeds (closed state)
- Library: `pybreaker` for Python

### Bulkhead Pattern
- Isolate resources (threads, connections) per dependency
- If Service B is slow, it doesn't starve Service C
- Thread pools, connection pools with limits

### Retry with Exponential Backoff
- Transient failures (network hiccup, timeout)
- Don't retry: 4xx errors, authentication failures
- Retry: 5xx, timeouts, connection errors
- Backoff: 100ms → 200ms → 400ms (with jitter to avoid thundering herd)

### Timeout Cascades
- If you set timeout T at the gateway, and each service has timeout T, requests fail silently
- Rule: Each downstream call must have shorter timeout than the upstream caller
- Example: Client timeout 30s → Gateway timeout 28s → Service A timeout 25s → Service B timeout 20s

### Graceful Degradation
- Service down? Return partial response, cached data, or feature flag off
- Don't hard-fail the entire request

---

## 5.5 Service Architecture Health Score

When reviewing an existing microservices system, assess health across these dimensions:

```
Service Architecture Health Score
==================================

Service Independence   ████░░░░░░  [Needs Work] - services have minimal coupling
Data Ownership        ███░░░░░░░  [Critical Gap] - each service owns its data
Resilience Patterns   ██████░░░░  [Good] - circuit breakers, retries, timeouts
Observability         █████░░░░░  [Solid] - tracing, logging, metrics
Deployment Independence ██░░░░░░░░ [Critical Gap] - can deploy one service without others

Overall: [Sentence verdict. E.g., "Services are well-designed but lack observability—distributed tracing and metrics are mandatory before scaling further."]
```

### What to Check for Each Dimension

**Service Independence** — Are services loosely coupled?
- [ ] No cross-service database queries (couples data layer)
- [ ] No synchronous chains > 2 hops (one service → at most 2 others)
- [ ] No shared code libraries (except base contracts/shared types)
- [ ] Service A can be down without cascading failure

**Data Ownership** — Is data ownership clear?
- [ ] Each service has exactly one database (no shared tables)
- [ ] One service is authoritative source for each entity type
- [ ] No cross-service foreign keys (use event-driven or APIs instead)
- [ ] Read-heavy services replicate via events, not sync queries

**Resilience Patterns** — Can the system degrade gracefully?
- [ ] Circuit breakers on all synchronous calls (detect failing services)
- [ ] Timeouts set everywhere (prevent cascading timeouts)
- [ ] Retry logic with exponential backoff (transient failures)
- [ ] Bulkhead isolation (if Service B slow, doesn't starve Service C)
- [ ] Graceful degradation (service down? Return partial response, not error)

**Observability** — Can you debug a production incident in 30 minutes?
- [ ] Distributed tracing (trace single request across all services)
- [ ] Centralized logging with trace ID correlation
- [ ] Metrics on request rate, latency, error rate per service
- [ ] Circuit breaker state visible (is anything open?)
- [ ] Can you search: "trace where service=payment and latency > 5s"?

**Deployment Independence** — Can you push one service without deploying others?
- [ ] Service version changes don't require recompiling other services
- [ ] API contracts versioned (v1, v2, backward compatible)
- [ ] Database migrations per-service (no cross-service schema coordination)
- [ ] Different deployment cadences per service are supported

### Quick Assessment Template

Use this when reviewing a microservices design:

```
Service Boundaries Assessment
=============================

Services Identified:
- Order Service (owns orders, order_items tables) ✓
- Inventory Service (owns stock, reservations tables) ✓
- Payment Service (owns payment_transactions table) ✓

Cross-Service Calls:
1. Order Service → Inventory Service: /products/{id}/availability
   [Sync or Async?] Async (event-driven)
   [Timeout?] N/A for async

2. Order Service → Payment Service: /charges
   [Sync or Async?] Sync (immediate confirmation needed)
   [Timeout?] Yes, 10s, with retry (max 2x)

Data Ownership:
- Orders ← Order Service (authoritative)
- Inventory Stock ← Inventory Service (authoritative)
- Inventory reads in Order Service ← via API calls (not sync query)

Issues Found:
- CRITICAL: Order Service queries payment_transactions table directly (should call Payment API instead)
- HIGH: No circuit breaker on Order → Inventory call (payment_service down crashes orders)
- MEDIUM: Async events published but no dead letter queue (messages silently lost on error)

Recommendation:
Extract direct database query to API call. Add circuit breaker. Implement DLQ for reliability.
```

---

## 6. Service Mesh & Observability

### Observability is Non-Negotiable

You cannot run microservices without:

**Distributed Tracing** (Jaeger, Zipkin)
- Trace a single request across all services
- Identify which service is slow
- Shows network latency, service processing time, queueing

**Centralized Logging** (ELK, Datadog, Cloud Logging)
- Correlate logs across services via trace ID
- Search "all logs where service=payment-service AND status=error"

**Metrics** (Prometheus, Datadog)
- Request rate, latency, error rate per service
- Circuit breaker state, queue depth, database connections

### Service Discovery
- Services move (deployments, scaling, failures)
- You need: DNS or a registry (Consul, Kubernetes DNS)
- Client-side (smart client) vs server-side (proxy) discovery
- Kubernetes does this for you

### Health Checks & Readiness Probes
- **Liveness**: Is the service alive? If not, restart it.
- **Readiness**: Is it ready to handle traffic? (DB migrations done, connections open?)
- Load balancers check readiness before routing requests

---

## 7. Migration Patterns

### Strangler Fig Pattern (Monolith → Microservices)
- Don't rewrite. Extract incrementally.
- New feature → new service
- Old feature → routed through proxy to monolith until replaced
- Gradually strangle the monolith

Example: Monolith handles Orders. Extract Order Service:
1. Deploy Order Service alongside monolith
2. Proxy wraps monolith requests: if `/orders/*` → call Order Service, else → call monolith
3. Migrate data, test thoroughly
4. Kill monolith routing for `/orders/*`
5. Repeat for Inventory, Payments, etc.

### Anti-Corruption Layer
- Monolith and Service speak different languages (schema, terminology)
- Adapter layer translates between them
- Prevents service from knowing monolith internals

### Parallel Run / Dark Launching
- New service runs alongside old, processing same requests
- Compare results, don't return new service response to users yet
- Verify correctness before switching traffic

---

## Assessment Framework (for Reviews)

### Service Boundaries
- Does each service own its data?
- Is there a clear business reason for this boundary?
- Count the cross-service calls per request (should be < 3)

### Coupling Analysis
- Shared database tables? (Bad)
- Synchronous chains? (Reconsider boundary)
- Hard dependencies on request/response? (Are they in the same service?)

### Communication Evaluation
- Is REST used for eventual consistency? (Reconsider—use async)
- Is async used for immediate consistency? (Reconsider—use sync or move boundary)
- Are timeouts set everywhere? (Non-negotiable)

### Data Consistency Review
- How do you handle "Saga failed halfway"?
- Do you have compensating transactions?
- Is eventual consistency acceptable here?

### Failure Modes
- What happens if Service B is down? (Degraded gracefully?)
- What happens if the message queue is full? (Backpressure?)
- What happens if a network partition splits your services?

---

## Deliverables

### Design Consultations
- **ADR (Architecture Decision Record)**: Service boundaries, communication style, data strategy
- **Service boundary diagram** (text): Show services, their APIs, and data ownership
- **API contracts**: OpenAPI/gRPC schemas for service-to-service calls
- **Data flow diagram**: Show synchronous calls, events, and query paths
- **Failure mode analysis**: FMEA for critical paths (payment, order creation)

### Code Reviews
- Assess service boundaries and inter-service coupling
- Evaluate resilience (timeouts, retries, circuit breakers)
- Check observability (tracing, logging, metrics)
- Validate data consistency strategy
- Point out premature optimization (microservices where monolith sufficient)

---

## Remember

- Every service boundary is a network call. Network calls fail.
- Microservices don't solve organizational problems (communication, unclear responsibilities).
- Eventual consistency is the price of loose coupling.
- If you can't draw why a boundary exists, it's wrong.
- Observability isn't optional—it's survival.
