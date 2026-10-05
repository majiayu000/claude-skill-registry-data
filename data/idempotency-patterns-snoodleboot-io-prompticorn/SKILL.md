---
name: idempotency-patterns
description: "**Pattern:**"
---

# Idempotency Patterns (Verbose)

## Natural Keys (Database Level)

**Pattern:**
```sql
-- Idempotency via unique constraint
CREATE TABLE orders (
  customer_id INT,
  order_timestamp TIMESTAMP,
  amount DECIMAL,
  UNIQUE (customer_id, order_timestamp)
);

-- First attempt: Inserts
INSERT INTO orders (customer_id, order_timestamp, amount)
VALUES (123, '2026-04-10 14:30:00', 99.99);
-- Success: row inserted

-- Retry (same values): Error or replace
INSERT INTO orders (customer_id, order_timestamp, amount)
VALUES (123, '2026-04-10 14:30:00', 99.99)
ON DUPLICATE KEY UPDATE amount = 99.99;
-- Safe: row not duplicated, no error
```

## Idempotency Keys (Application Level)

**Pattern:**
```python
# Client generates unique key
idempotency_key = f"{customer_id}-{order_time}-{uuid.uuid4()[:8]}"

response = client.post('/api/orders', {
    'customer_id': customer_id,
    'amount': 99.99,
    'idempotency_key': idempotency_key
})

# Server stores key with response
# If retry with same key, return cached response
```

**Server Implementation:**
```python
@app.post('/api/orders')
def create_order(request):
    idempotency_key = request.json['idempotency_key']
    
    # Check if we've seen this key before
    cached = db.query(
        "SELECT response FROM idempotency_cache WHERE key = ?",
        idempotency_key
    )
    if cached:
        return cached.response  # Return cached response
    
    # Process order
    order = create_order_in_db(request.json)
    
    # Cache the response
    db.execute(
        "INSERT INTO idempotency_cache (key, response) VALUES (?, ?)",
        idempotency_key, json.dumps(order)
    )
    
    return order
```

## Deduplication Pattern

```python
# Track processed IDs to avoid duplicates
processed_ids = set()

for event in event_stream:
    if event.id in processed_ids:
        continue  # Skip duplicate
    
    process(event)
    processed_ids.add(event.id)
```

## State Machine Pattern

```python
class OrderStateMachine:
    VALID_TRANSITIONS = {
        'draft': ['pending'],
        'pending': ['confirmed', 'cancelled'],
        'confirmed': ['shipped'],
        'shipped': ['delivered'],
        'delivered': []
    }
    
    def transition(self, current_state, new_state):
        if new_state not in self.VALID_TRANSITIONS[current_state]:
            raise InvalidTransition()
        return new_state

# Idempotent: Transition from 'pending' to 'confirmed'
# Retry: 'pending' to 'confirmed' = same result
```

## Optimistic Locking

```sql
CREATE TABLE orders (
  order_id INT,
  status VARCHAR,
  version INT,
  ...
);

-- Only update if version hasn't changed
UPDATE orders 
SET status = 'shipped', version = version + 1
WHERE order_id = 123 AND version = 5;
-- If version != 5, 0 rows updated (detect conflict)
```

## Comparison: Which Pattern to Use

| Pattern | Pros | Cons | Use Case |
|---------|------|------|----------|
| Natural Keys | Simple, database-enforced | Need unique key | Orders, transactions |
| Idempotency Keys | HTTP-safe, user-facing | More complex | Payment API |
| Deduplication | Flexible | In-memory (memory issues) | Stream processing |
| State Machine | Prevents invalid states | More code | Order workflows |
| Optimistic Locking | Detects conflicts | Requires retry logic | Updates |
