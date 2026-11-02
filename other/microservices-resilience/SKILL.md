---
name: microservices-resilience
description: Distributed systems resilience patterns, circuit breakers, bulkheads, rate limiting, and exponential backoff with jitter. Use when designing fault-tolerant microservices, integrating third-party APIs, preventing cascading service failures, or handling transient network errors.
allowed-tools: Read, Write, Edit, Glob, Grep
version: 1.0
category: backend-api-design
---

# Microservices Resilience

> **Circuit Breakers, Bulkheads, Exponential Backoff & Fault-Tolerant Distributed Systems**

---

## 🏗️ Core Principles

| Principle | Rule |
|-----------|------|
| **Fail Fast with Circuit Breakers** | When a downstream dependency fails repeatedly, trip the circuit to `OPEN` immediately to prevent thread starvation and cascading failures. |
| **Exponential Backoff with Full Jitter** | Never retry on fixed intervals (causes thundering herd). Calculate retry delay as $t = \text{random}(0, \min(\text{cap}, \text{base} \times 2^{\text{attempt}}))$. |
| **Bulkhead Isolation** | Isolate critical resources (connection pools, worker threads) into separate pools so failure in one integration cannot exhaust entire system capacity. |
| **Idempotency Keys** | All state-modifying requests (payments, order placement) must accept and enforce an `Idempotency-Key` header stored with atomic lock semantics. |
| **Timeout Budgeting** | Pass request deadlines down the call graph (distributed context propagation). If a request timeout is 2 seconds, do not allow downstream calls to wait 5 seconds. |

---

## 📋 Resilient Retry with Jitter Pattern (TypeScript)

```typescript
export async function retryWithBackoff<T>(
  operation: () => Promise<T>,
  options: {
    maxRetries?: number;
    baseDelayMs?: number;
    maxDelayMs?: number;
  } = {}
): Promise<T> {
  const { maxRetries = 3, baseDelayMs = 100, maxDelayMs = 2000 } = options;

  let attempt = 0;
  while (true) {
    try {
      return await operation();
    } catch (error: any) {
      attempt++;
      if (attempt > maxRetries || !isTransientError(error)) {
        throw error;
      }

      // Exponential backoff with Full Jitter
      const exponentialDelay = Math.min(maxDelayMs, baseDelayMs * Math.pow(2, attempt));
      const jitteredDelay = Math.floor(Math.random() * exponentialDelay);

      console.warn(`Transient failure on attempt ${attempt}. Retrying in ${jitteredDelay}ms...`);
      await new Promise((resolve) => setTimeout(resolve, jitteredDelay));
    }
  }
}

function isTransientError(error: any): boolean {
  // Retry 502/503/504 and network disconnects; never retry 400/401/403/422
  const status = error.statusCode || error.status;
  return status === 429 || (status >= 500 && status <= 504) || error.code === 'ECONNRESET';
}
```

---

## ❌ Anti-Patterns

- ❌ Unbounded retries without maximum count or timeouts.
- ❌ Retrying non-idempotent mutations without idempotency keys (risks duplicate charges).
- ❌ Tight coupling without fallback responses or cached degraded states.
