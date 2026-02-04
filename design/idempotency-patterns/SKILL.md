---
name: idempotency-patterns
description: Use when designing idempotent APIs, handling retries safely, or preventing duplicate operations. Covers idempotency keys, at-most-once semantics, and duplicate prevention.
allowed-tools: Read, Glob, Grep
---

# Idempotency Patterns

Patterns for designing APIs and systems that handle retries safely without duplicate side effects.

## When to Use This Skill

- Designing APIs that handle retries safely
- Implementing idempotency keys
- Preventing duplicate operations
- Building reliable payment/order systems
- Handling network failures gracefully

## What is Idempotency?

```text
Idempotent operation: Same result regardless of how many times executed

f(x) = f(f(x)) = f(f(f(x))) = ...

Examples:
- GET /user/123      → Always returns same user (idempotent)
- DELETE /user/123   → User deleted once, subsequent calls no-op (idempotent)
- POST /orders       → Creates new order each time (NOT idempotent)
```

## Why Idempotency Matters

```text
Network reality:
Client ──request──> Server
       <──response── (lost!)

Client doesn't know if request succeeded.
Should it retry?

Without idempotency:
- Retry creates duplicate order
- Customer charged twice
- Inventory decremented twice

With idempotency:
- Retry returns same result
- No duplicate side effects
- Safe to retry
```

## HTTP Method Idempotency

| Method | Idempotent | Safe | Notes |
| ------ | ---------- | ---- | ----- |
| GET | Yes | Yes | No side effects |
| HEAD | Yes | Yes | No side effects |
| OPTIONS | Yes | Yes | No side effects |
| PUT | Yes | No | Replace entire resource |
| DELETE | Yes | No | Delete is idempotent (already deleted = no-op) |
| POST | No | No | Creates new resource |
| PATCH | Maybe | No | Depends on implementation |

## Idempotency Key Pattern

### Concept

```text
Client generates unique key, server tracks processed keys

Request 1:
POST /payments
Idempotency-Key: abc-123
{amount: 100}
→ Process payment, store result with key abc-123

Request 2 (retry):
POST /payments
Idempotency-Key: abc-123
{amount: 100}
→ Find stored result for abc-123, return same response
→ No duplicate payment
```

### Implementation

```text
Idempotency store schema:
┌──────────────────────────────────────────────────┐
│ idempotency_key │ request_hash │ response │ ttl │
├──────────────────────────────────────────────────┤
│ abc-123         │ sha256(...)  │ {...}    │ 24h │
└──────────────────────────────────────────────────┘

Flow:
1. Receive request with idempotency key
2. Check if key exists in store
3. If exists:
   a. Verify request_hash matches (same request)
   b. Return stored response
4. If not exists:
   a. Process request
   b. Store response with key
   c. Return response
```

### Key Generation

```text
Client-generated keys (recommended):
- UUID v4: 550e8400-e29b-41d4-a716-446655440000
- ULID: 01ARZ3NDEKTSV4RRFFQ69G5FAV
- Custom: {client_id}-{timestamp}-{random}

Requirements:
- Globally unique
- Unpredictable (prevent guessing)
- Client controls key
```

### Request Fingerprinting

```text
Verify retry is same request (not just same key):

request_hash = hash(
  method,
  path,
  body,
  relevant_headers
)

If idempotency_key exists but request_hash differs:
→ Return 422: "Idempotency key reused with different request"
```

## At-Most-Once vs At-Least-Once

### At-Most-Once

```text
Operation executes 0 or 1 time, never more.

Use when: Duplicate is worse than missing
- Payment processing
- Order creation
- Resource provisioning

Implementation: Idempotency keys with deduplication
```

### At-Least-Once

```text
Operation executes 1 or more times.

Use when: Missing is worse than duplicate
- Event notifications
- Log ingestion
- Analytics events

Implementation: Retry until acknowledged, handle duplicates downstream
```

### Exactly-Once (Hard)

```text
Operation executes exactly 1 time.

Extremely difficult in distributed systems.
Usually achieved through:
- At-least-once delivery + idempotent processing
- Distributed transactions (2PC)
- Saga pattern with compensation
```

## Duplicate Detection Strategies

### Strategy 1: Idempotency Key Store

```text
Store: Redis or database

Key: idempotency_key
Value: {
  status: "processing" | "completed" | "failed",
  response: {...},
  created_at: timestamp,
  expires_at: timestamp
}

TTL: 24-72 hours typically
```

### Strategy 2: Natural Key Deduplication

```text
Use business identifiers:
- Order: {customer_id}-{cart_id}-{timestamp}
- Payment: {order_id}-{amount}-{currency}
- Transfer: {sender}-{receiver}-{reference}

Check if natural key exists before processing.
```

### Strategy 3: Database Constraints

```text
CREATE TABLE orders (
  id UUID PRIMARY KEY,
  idempotency_key VARCHAR(255) UNIQUE,
  ...
);

INSERT fails if idempotency_key already exists.
```

### Strategy 4: Optimistic Locking

```text
UPDATE accounts
SET balance = balance - 100, version = version + 1
WHERE id = 123 AND version = 5;

If version changed, retry with new version.
Prevents concurrent duplicate updates.
```

## Handling In-Flight Requests

```text
Problem: Request A starts, Request B (retry) arrives before A completes

Solution 1: Lock on idempotency key
- First request acquires lock
- Retry waits or returns "processing"

Solution 2: Status tracking
- Store "processing" status immediately
- Retry sees "processing", waits or returns 409

Response for in-flight:
HTTP 409 Conflict
{
  "error": "Request with this idempotency key is still processing",
  "retry_after": 5
}
```

## Idempotency in Different Contexts

### Payment APIs

```text
POST /charges
Idempotency-Key: {uuid}
{
  "amount": 1000,
  "currency": "usd",
  "source": "tok_visa"
}

Critical: Never charge twice
Store: idempotency_key → charge_id, status, response
TTL: 24-48 hours
```

### Message Queues

```text
Producer:
- Include message_id in payload
- Retry with same message_id

Consumer:
- Track processed message_ids
- Skip if already processed

Deduplication window: Based on expected retry window
```

### Database Operations

```text
Insert with idempotency:
INSERT INTO orders (id, idempotency_key, ...)
VALUES (gen_id(), 'abc-123', ...)
ON CONFLICT (idempotency_key) DO NOTHING
RETURNING *;

If conflict, fetch existing record.
```

### Event Sourcing

```text
Events naturally idempotent by sequence:
- Event ID: {aggregate_id}-{sequence_number}
- Reject if sequence already exists
- Replay is safe (events are immutable)
```

## Best Practices

### Key Storage

```text
- Use fast store (Redis) for hot path
- Persist to database for durability
- Set appropriate TTL (24-72 hours typical)
- Clean up expired keys
```

### Error Handling

```text
If processing fails:
1. Store failure response with key
2. Client retries get same error
3. Client must use NEW key to try again

This prevents infinite retry loops on bad requests.
```

### Documentation

```text
Document clearly:
- Which endpoints require idempotency keys
- Key format requirements
- TTL for stored results
- Error responses for duplicates
```

### Client Implementation

```text
1. Generate idempotency key before first attempt
2. Store key locally until confirmed success
3. Retry with SAME key on network failure
4. Generate NEW key for genuinely new requests
5. Don't reuse keys across different operations
```

## Common Pitfalls

```text
1. Storing only success responses
   → Store failures too, otherwise retry creates duplicate

2. Short TTL
   → Client might retry after TTL expires, causing duplicate

3. Not hashing request body
   → Different requests with same key processed differently

4. Race conditions on concurrent retries
   → Use locks or atomic operations

5. Not handling partial failures
   → Use sagas or compensation for multi-step operations
```

## Related Skills

- `api-design-fundamentals` - API design patterns
- `rate-limiting-patterns` - Handling retries
- `distributed-transactions` - Multi-step operations
