---
name: api-and-system-design
version: 1.0.0
author: Param
description: Enforces REST API design, distributed systems patterns, database design, and event-driven architecture at principal-engineer level.
applies-to: .py, .yaml, .yml, OpenAPI specs, SQL schema files, Terraform configs, API design documents, microservice implementations
---

## Intent

This skill ensures that every API and distributed system designed or implemented in this session follows the discipline of a principal engineer: correct HTTP semantics, versioned from day one, with explicit auth on every endpoint, validated inputs at every boundary, and the distributed systems patterns (idempotency, retries, circuit breakers, timeouts) that separate toy implementations from production-grade services. It prevents the class of failures that only appear at scale — N+1 queries, missing pagination, unversioned APIs that can never be changed, and external service calls that bring down the whole system when they time out. Loading this skill means no API ships without an OpenAPI spec, no external call ships without a timeout, and no message consumer ships without idempotency.

See also: [`software-architecture/SKILL.md`](../software-architecture/SKILL.md) for project structure and error handling, [`python-excellence/SKILL.md`](../python-excellence/SKILL.md) for Pydantic schema patterns, [`mlops-and-infra/SKILL.md`](../mlops-and-infra/SKILL.md) for ML serving APIs.

---

## 1. REST API Design

**Resources are nouns, never verbs.** The HTTP method is the verb.

```
# WRONG — verb in URL
GET  /getUser/123
POST /createOrder
POST /deleteAccount/456

# CORRECT — noun resources, method is the verb
GET    /users/123
POST   /orders
DELETE /accounts/456
```

**Use correct HTTP methods with their correct semantics:**
- `GET`: Read a resource; must be idempotent and safe (no side effects)
- `POST`: Create a new resource or trigger a non-idempotent action
- `PUT`: Replace a resource entirely (full update); must be idempotent
- `PATCH`: Partial update; update only specified fields
- `DELETE`: Remove a resource; must be idempotent

**Use correct HTTP status codes. Never return 200 for an error.**

| Situation | Status Code |
|-----------|-------------|
| Successful GET, PATCH, DELETE | 200 OK |
| Successful POST (resource created) | 201 Created + `Location` header |
| Successful POST with no response body | 204 No Content |
| Client sent invalid data | 400 Bad Request |
| Missing or invalid authentication | 401 Unauthorized |
| Valid auth but insufficient permission | 403 Forbidden |
| Resource not found | 404 Not Found |
| Conflict (duplicate, version mismatch) | 409 Conflict |
| Validation error (semantic, not syntax) | 422 Unprocessable Entity |
| Rate limit exceeded | 429 Too Many Requests |
| Server error | 500 Internal Server Error |
| Downstream service unavailable | 503 Service Unavailable |

**Always paginate collection endpoints.** Never return an unbounded list.

For standard datasets: use offset-based pagination with explicit defaults:
```
GET /orders?page=1&page_size=50
```

For large or real-time datasets: use cursor-based pagination:
```
GET /events?cursor=eyJpZCI6MTIzfQ&limit=100
```

Always include pagination metadata in the response:
```json
{
  "data": [...],
  "pagination": {
    "cursor": "eyJpZCI6MTIzfQ==",
    "has_next": true,
    "total": 4823
  }
}
```

**Always version APIs from day one.** Version in the URL path (`/v1/`, `/v2/`). Header-based versioning is acceptable but harder to test and debug.

```
/v1/users/{id}
/v2/users/{id}
```

**Every endpoint must have an OpenAPI/Swagger spec.** Generate it from code (FastAPI does this automatically). Never maintain a separate spec manually — it will drift.

---

## 2. Request and Response Design

**Use Pydantic models for all request bodies and response schemas.** Every endpoint has a typed input model and a typed output model.

```python
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID

class CreateOrderRequest(BaseModel):
    user_id: UUID
    items: list[OrderItem] = Field(min_length=1, max_length=100)
    delivery_address: Address
    idempotency_key: str = Field(min_length=16, max_length=64)

    model_config = ConfigDict(str_strip_whitespace=True)

class OrderResponse(BaseModel):
    order_id: UUID
    status: OrderStatus
    total_amount: Decimal
    created_at: datetime
    estimated_delivery: date

    model_config = ConfigDict(from_attributes=True)
```

**Validate all inputs at the API boundary.** Downstream services and business logic must never receive unvalidated data.

**Consistent error response format across all endpoints:**

```json
{
  "error": {
    "code": "INSUFFICIENT_FUNDS",
    "message": "Account balance $12.50 is insufficient for transaction amount $50.00.",
    "details": {
      "account_id": "acc_abc123",
      "available_balance": 12.50,
      "required_amount": 50.00
    },
    "request_id": "req_xyz789"
  }
}
```

**Response envelopes for list endpoints:**
```json
{
  "data": [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"}
  ],
  "pagination": {
    "cursor": "eyJpZCI6Mn0=",
    "has_next": true,
    "total": 1547
  },
  "meta": {
    "request_id": "req_abc123",
    "generated_at": "2024-01-15T10:30:00Z"
  }
}
```

**Never expose internal implementation details in public API responses:**
- Internal database row IDs (prefer UUIDs or slugs)
- Internal column names or schema structure
- Stack traces or internal error messages (log them; return a request_id instead)
- Internal service names or infrastructure details

---

## 3. Authentication and Authorization

**Document the auth mechanism for every endpoint.** Every endpoint in the OpenAPI spec must declare its security scheme:

```yaml
# In OpenAPI spec
/orders/{order_id}:
  get:
    security:
      - BearerAuth: []
    responses:
      401:
        description: Missing or invalid JWT token
      403:
        description: Authenticated user does not own this order
```

**Never roll your own auth.** Use JWT (RS256 or ES256 — not HS256 for multi-service environments) or OAuth2 with a proven library.

**Authorization is resource-scoped, not just session-scoped.** Checking that a user is authenticated is necessary but not sufficient. Every resource access must verify the caller has permission for that specific resource:

```python
@router.get("/orders/{order_id}")
async def get_order(
    order_id: UUID,
    current_user: AuthenticatedUser = Depends(get_current_user),
    order_service: OrderService = Depends(get_order_service),
) -> OrderResponse:
    order = order_service.get_by_id(order_id)
    if order is None:
        raise HTTPException(status_code=404)
    # Authorization check: user can only see their own orders
    if order.user_id != current_user.id and not current_user.has_role("admin"):
        raise HTTPException(status_code=403, detail={"code": "FORBIDDEN"})
    return OrderResponse.model_validate(order)
```

**Rate limiting: document expected QPS and rate limit strategy for every endpoint.** Implement at the API gateway layer. Document:
- The rate limit (e.g., 100 requests per minute per API key)
- The rate limit response (`429 Too Many Requests` with `Retry-After` header)
- The burst allowance if any

---

## 4. Distributed Systems Patterns

**Idempotency: POST endpoints that create resources must support idempotency keys.**

```python
@router.post("/orders", status_code=201)
async def create_order(
    request: CreateOrderRequest,
    order_service: OrderService = Depends(get_order_service),
) -> OrderResponse:
    # Idempotency: if this key was already processed, return the existing result.
    # This allows safe retries without duplicate order creation.
    existing = order_service.find_by_idempotency_key(request.idempotency_key)
    if existing:
        return OrderResponse.model_validate(existing)

    order = order_service.create(request)
    return OrderResponse.model_validate(order)
```

**Retry logic: always implement exponential backoff with jitter for external service calls.**

```python
import random
import time

def call_with_retry(
    func: Callable,
    *args,
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
    retryable_exceptions: tuple = (requests.Timeout, requests.ConnectionError),
) -> Any:
    """Call func with exponential backoff and jitter on retryable failures.

    Jitter prevents thundering herd: if 1000 clients hit a timeout simultaneously,
    random jitter spreads out retries so they don't all hammer the service at once.
    """
    for attempt in range(max_attempts):
        try:
            return func(*args)
        except retryable_exceptions as e:
            if attempt == max_attempts - 1:
                raise
            # Exponential backoff with full jitter
            delay = min(max_delay, base_delay * (2 ** attempt))
            jitter = random.uniform(0, delay)
            logger.warning(
                "retrying_after_failure",
                attempt=attempt + 1,
                delay_s=jitter,
                error=str(e),
            )
            time.sleep(jitter)
```

**Circuit breaker: document the fallback behavior when a downstream service is unavailable.**

```python
# Document circuit breaker config and fallback strategy
"""
Circuit Breaker: RecommendationService
========================================
Failure threshold: 5 failures in 10 seconds → circuit opens
Recovery: attempt 1 request per 30 seconds (half-open state)
Fallback: return top-k most popular items by global click rate (cached, updated hourly)
Rationale: a degraded recommendation experience is better than a 500 error.
           Popularity fallback ensures users still see relevant content.
"""
```

**Timeouts: every external call must have an explicit timeout. Never rely on default (often infinite) timeouts.**

```python
# WRONG — no timeout; will hang forever if downstream is slow
response = requests.get("https://api.example.com/data")

# CORRECT — explicit connect and read timeouts
response = requests.get(
    "https://api.example.com/data",
    timeout=(5.0, 30.0),  # (connect_timeout_s, read_timeout_s)
)

# For httpx async client
async with httpx.AsyncClient(timeout=httpx.Timeout(connect=5.0, read=30.0)) as client:
    response = await client.get("https://api.example.com/data")
```

**Distributed tracing: propagate trace IDs across service boundaries.**

```python
# Every service call must propagate the trace context
async def call_downstream_service(
    client: httpx.AsyncClient,
    endpoint: str,
    request_id: str,
) -> dict:
    return await client.get(
        endpoint,
        headers={
            "X-Request-ID": request_id,
            "X-B3-TraceId": current_trace_id(),  # Zipkin / Jaeger style
            "traceparent": current_traceparent(),  # W3C Trace Context standard
        },
    )
```

---

## 5. Database Design

**Always define indexes alongside table definitions. Document the queries each index serves.**

```sql
CREATE TABLE orders (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID NOT NULL,
    status      TEXT NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    total_cents INTEGER NOT NULL
);

-- Index for: GET /users/{user_id}/orders (most common access pattern)
CREATE INDEX idx_orders_user_id ON orders(user_id);

-- Index for: background job that processes PENDING orders (ORDER BY created_at)
CREATE INDEX idx_orders_status_created ON orders(status, created_at)
    WHERE status IN ('PENDING', 'PROCESSING');

-- Index for: idempotency key lookup on POST /orders
CREATE UNIQUE INDEX idx_orders_idempotency ON orders(idempotency_key)
    WHERE idempotency_key IS NOT NULL;
```

**Always define foreign key constraints at the database level.** Application-level enforcement alone is insufficient — concurrent transactions can violate application-level checks.

```sql
ALTER TABLE orders
    ADD CONSTRAINT fk_orders_user
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT;
```

**Never use `SELECT *` in production code. Always specify the columns needed.**

```python
# WRONG — fetches all columns, including large ones (blobs, audit fields)
result = session.execute(text("SELECT * FROM orders WHERE user_id = :uid"), {"uid": user_id})

# CORRECT — fetch only what is needed
result = session.execute(
    text("SELECT id, status, total_cents, created_at FROM orders WHERE user_id = :uid"),
    {"uid": user_id},
)
```

**Transactions: always document the isolation level and the reason for the choice.**

```python
# SERIALIZABLE: required here because we read-then-write account balance.
# READ COMMITTED would allow a TOCTOU race condition where two concurrent
# withdrawals both pass the balance check before either commits.
with session.begin():
    session.execute(text("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"))
    account = session.get(Account, account_id)
    if account.balance < amount:
        raise InsufficientFundsError(...)
    account.balance -= amount
```

**Migrations: always reversible. Never destructive without a backup and rollback plan.**

```python
# Good Alembic migration pattern
def upgrade() -> None:
    # Add column with a default so existing rows are valid immediately
    op.add_column("users", sa.Column("tier", sa.String(20), nullable=False, server_default="free"))

def downgrade() -> None:
    # Always implement downgrade — if a migration has no safe downgrade, document why
    op.drop_column("users", "tier")
```

---

## 6. Message Queue and Event-Driven Architecture

**Define event schemas with versioning. Document the producer and consumer contracts.**

```python
# Event schema — versioned and self-describing
@dataclass(frozen=True)
class OrderCreatedEvent:
    """
    Producer: OrderService (order-service v1.2+)
    Consumers: InventoryService, NotificationService, AnalyticsService
    Schema version: 2 (v1 did not include `delivery_address`)
    Breaking change from v1: added required field `delivery_address`
    Migration: consumers that don't need delivery_address can ignore the field;
               v1 consumers will fail on this event — upgrade required.
    """
    event_id: UUID
    event_type: Literal["order.created"] = "order.created"
    schema_version: int = 2
    order_id: UUID
    user_id: UUID
    total_cents: int
    delivery_address: Address
    occurred_at: datetime
```

**Idempotent consumers: every consumer must handle duplicate messages gracefully.**

```python
class OrderCreatedConsumer:
    def process(self, event: OrderCreatedEvent) -> None:
        # Idempotency check: if this event_id was already processed, skip.
        # Duplicates can arrive due to: at-least-once delivery semantics,
        # producer retries on network failure, or reprocessing from DLQ.
        if self.processed_event_repo.exists(event.event_id):
            logger.info("duplicate_event_skipped", event_id=str(event.event_id))
            return

        with self.db.transaction():
            self._handle_event(event)
            self.processed_event_repo.mark_processed(event.event_id)
```

**Dead letter queues: always configured. Document the retry and DLQ strategy.**

```python
"""
Message Queue Configuration: order-events
==========================================
Retry strategy: 3 attempts with 30s, 5m, 30m delays (exponential)
Dead letter queue: order-events-dlq
DLQ alarm: alert on-call if DLQ depth > 10 messages (indicates systematic failure)
DLQ reprocessing: manual trigger via `reprocess-dlq` CLI command after root cause fix
Max retention: 7 days in DLQ; messages older than 7 days are discarded with an alarm
"""
```

**Event ordering: document whether ordering is guaranteed and how consumers handle out-of-order events.**

```python
"""
Ordering Guarantee: Partial
============================
Ordering is guaranteed within a partition key (order_id).
Events for different orders may arrive out of order.

Consumer ordering assumption: OrderShipped may arrive before OrderCreated
if messages are from different partitions (e.g., during rebalance or lag).

Consumer handling: if an OrderShipped event arrives with no corresponding
OrderCreated in the database, enqueue the event for retry in 60 seconds.
After 5 retries, send to DLQ for manual investigation.
"""
```
