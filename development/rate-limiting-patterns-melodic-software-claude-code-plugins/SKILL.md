---
name: rate-limiting-patterns
description: Use when implementing rate limiting, throttling, or API quotas. Covers algorithms like token bucket and sliding window, plus distributed rate limiting patterns.
allowed-tools: Read, Glob, Grep
---

# Rate Limiting Patterns

Patterns for protecting APIs and services through rate limiting, throttling, and quota management.

## When to Use This Skill

- Implementing API rate limiting
- Choosing rate limiting algorithms
- Designing distributed rate limiting
- Setting up quota management
- Protecting against abuse

## Why Rate Limiting

```text
Protection against:
- DDoS attacks
- Brute force attempts
- Resource exhaustion
- Cost overruns (cloud APIs)
- Cascading failures

Business benefits:
- Fair resource allocation
- Predictable performance
- Cost control
- SLA enforcement
```

## Rate Limiting Algorithms

### Token Bucket

**Concept:** Tokens added at fixed rate, requests consume tokens

```text
Configuration:
- Bucket size (max tokens): 100
- Refill rate: 10 tokens/second

Behavior:
┌─────────────────────────┐
│ Bucket (capacity: 100)  │
│ ████████████░░░░░░░░░░  │ 60 tokens available
└─────────────────────────┘
        ↑           ↓
   10 tokens/s   Request takes 1 token

Allows bursts up to bucket size, then rate-limited.
```

**Characteristics:**

- Allows controlled bursts
- Simple to implement
- Memory efficient
- Most common algorithm

**Implementation sketch:**

```text
token_bucket:
  tokens = min(tokens + (now - last_update) * rate, capacity)
  if tokens >= cost:
    tokens -= cost
    return ALLOW
  return DENY
```

### Leaky Bucket

**Concept:** Requests queue and process at fixed rate

```text
┌─────────────────────────┐
│ Queue (capacity: 100)   │
│ ██████████████████████  │ Requests waiting
└──────────┬──────────────┘
           │
           ▼ Process at fixed rate (10/sec)
       [Processing]

Smooths traffic to constant rate.
```

**Characteristics:**

- Smooth output rate
- No bursts allowed
- Requests may queue
- Good for downstream protection

### Fixed Window

**Concept:** Count requests in fixed time windows

```text
Window: 1 minute, Limit: 100 requests

|-------- Window 1 --------|-------- Window 2 --------|
   95 requests                  ? requests
   [Allow]                      [Reset to 0]

Problem: Boundary burst
End of window 1: 100 requests
Start of window 2: 100 requests
= 200 requests in ~1 second span
```

**Characteristics:**

- Simple to implement
- Memory efficient
- Boundary burst problem
- Good for simple use cases

### Sliding Window Log

**Concept:** Track timestamp of each request

```text
Window: 1 minute, Limit: 100

Requests: [t-55s, t-50s, t-45s, ..., t-5s, t-2s, now]
Count all requests in [now - 60s, now]

No boundary burst problem, but memory intensive.
```

**Characteristics:**

- Precise limiting
- No boundary issues
- Memory intensive (stores all timestamps)
- Good for strict limits

### Sliding Window Counter

**Concept:** Weighted average of current and previous windows

```text
Previous window: 80 requests
Current window: 30 requests (40% through window)

Weighted count = 80 * 0.6 + 30 = 78
Limit: 100
Result: ALLOW (78 < 100)
```

**Characteristics:**

- Approximation (usually good enough)
- Memory efficient
- Smooths boundary issues
- Best balance for most cases

## Algorithm Selection Guide

| Algorithm | Burst Handling | Memory | Precision | Use Case |
| --------- | -------------- | ------ | --------- | -------- |
| Token Bucket | Allows bursts | Low | Good | General API limiting |
| Leaky Bucket | No bursts | Low | Good | Smooth rate enforcement |
| Fixed Window | Boundary burst | Very Low | Poor | Simple limits |
| Sliding Log | No bursts | High | Exact | Strict compliance |
| Sliding Counter | Minimal burst | Low | Good | Best general choice |

## Distributed Rate Limiting

### Challenge

```text
Single node: Simple in-memory counter
Multiple nodes: Need coordination

Without coordination:
Node 1: 50 requests (under 100 limit)
Node 2: 50 requests (under 100 limit)
Node 3: 50 requests (under 100 limit)
Total: 150 requests (over 100 limit!)
```

### Pattern 1: Centralized (Redis)

```text
┌─────────┐     ┌─────────┐     ┌─────────┐
│ Node 1  │     │ Node 2  │     │ Node 3  │
└────┬────┘     └────┬────┘     └────┬────┘
     │               │               │
     └───────────────┼───────────────┘
                     │
              ┌──────▼──────┐
              │    Redis    │
              │ (counters)  │
              └─────────────┘

Pros: Accurate, consistent
Cons: Redis dependency, latency, single point of failure
```

### Pattern 2: Local + Sync

```text
Each node gets fraction of limit:
- 3 nodes, 100 limit → 33 per node

Periodically sync to rebalance unused capacity.

Pros: Low latency, resilient
Cons: Less precise, sync complexity
```

### Pattern 3: Sticky Sessions

```text
Route same client to same node (by IP, API key, etc.)

Pros: Simple, no coordination needed
Cons: Uneven load, failover complexity
```

### Redis Implementation

```text
Token Bucket with Redis:

EVALSHA token_bucket_script 1 {key}
  {capacity} {refill_rate} {tokens_requested}

Script:
1. Get current tokens and timestamp
2. Calculate tokens to add since last request
3. If enough tokens, decrement and allow
4. Return tokens remaining
```

## Rate Limit Headers

Standard headers to communicate limits to clients:

```text
HTTP/1.1 200 OK
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1640000000
Retry-After: 30  (when rate limited)

Or draft standard:
RateLimit-Limit: 100
RateLimit-Remaining: 45
RateLimit-Reset: 30
```

## Rate Limit Response

```text
HTTP/1.1 429 Too Many Requests
Content-Type: application/json
Retry-After: 30

{
  "error": {
    "code": "RATE_LIMITED",
    "message": "Rate limit exceeded",
    "retry_after": 30,
    "limit": 100,
    "window": "1m"
  }
}
```

## Multi-Tier Rate Limiting

```text
Apply limits at multiple levels:

Level 1: Global (protect infrastructure)
  - 10,000 req/sec across all clients

Level 2: Per-tenant (fair allocation)
  - 1,000 req/min per organization

Level 3: Per-user (prevent abuse)
  - 100 req/min per user

Level 4: Per-endpoint (protect expensive operations)
  - 10 req/min for /export endpoint
```

## Quota Management

### Quota vs Rate Limit

```text
Rate Limit: Requests per time window (burst protection)
  - 100 requests/minute

Quota: Total allocation over period (budget)
  - 10,000 API calls/month
```

### Quota Tracking

```text
Track usage:
- Per API key
- Per endpoint
- Per operation type

Alert thresholds:
- 80% usage: Warning notification
- 100% usage: Hard block or overage charges
```

## Best Practices

### Graceful Degradation

```text
Instead of hard block:
1. Reduce quality (lower resolution, fewer results)
2. Queue requests (process later)
3. Serve cached responses
4. Allow burst with penalty (slower recovery)
```

### Client-Side Handling

```text
Implement exponential backoff:
1. Receive 429
2. Wait Retry-After (or 1s)
3. Retry
4. If 429 again, wait 2s
5. Continue doubling up to max (e.g., 60s)
```

### Testing Rate Limits

```text
Test scenarios:
- Burst traffic
- Sustained high traffic
- Clock skew (distributed systems)
- Recovery after limit
- Multiple client types
```

## Related Skills

- `api-design-fundamentals` - API design patterns
- `idempotency-patterns` - Safe retries
- `quality-attributes-taxonomy` - Performance attributes
