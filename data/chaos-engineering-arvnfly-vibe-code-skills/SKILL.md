---
name: chaos-engineering
description: "Resilience engineering, fault injection testing, circuit breaker patterns, and graceful degradation protocols."
---

# Chaos Engineering & Resilience Protocol

Ensure applications survive network partitions, downstream latency spikes, and unexpected dependency failures.

---

## 1. Circuit Breaker Pattern

Wrap all external network and database calls in circuit breakers:
- **Closed**: Requests pass through normally.
- **Open**: If failure rate exceeds 50% over a 10-second window, fail immediately without touching downstream services.
- **Half-Open**: After reset timeout (e.g. 30s), allow a canary request through. If successful, resume normal traffic.

---

## 2. Fallbacks & Graceful Degradation

1. When a non-critical downstream service fails, return static cached defaults or empty arrays.
2. Never allow a secondary service failure to crash the primary user checkout or login flow.
3. Implement retry logic with exponential backoff and randomized jitter to prevent the thundering herd problem.
