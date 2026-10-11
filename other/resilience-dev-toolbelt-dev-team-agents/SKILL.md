---
name: resilience
description: Resilience — circuit breaker, retry, bulkhead, health checks.
---

## Patterns Reference

| Pattern | Problem Solved | When to Use |
|---------|---------------|------------|
| Circuit Breaker | Prevents cascading failures to a degraded dependency | Any synchronous external call |
| Retry + Exponential Backoff | Recovers from transient failures automatically | Idempotent operations, network timeouts, 5xx errors |
| Bulkhead | Isolates resource pools so one slow dependency doesn't block others | Services with multiple downstream dependencies |
| Timeout | Prevents indefinite blocking on slow responses | Every network boundary |
| Fallback | Provides a degraded but functional response on failure | Non-critical dependencies (recommendations, ads, enrichment) |
| Rate Limiter | Protects services from traffic spikes and abuse | Inbound API endpoints, outbound third-party calls |
| HTTP Connection Pooling | Reuses TCP/TLS connections instead of paying handshake cost per call | Any outbound HTTP client making repeated calls to the same host |

## Circuit Breaker

States and transitions:

```
CLOSED → (N consecutive failures) → OPEN → (probe timeout) → HALF-OPEN → (probe succeeds) → CLOSED
                                                                         → (probe fails)    → OPEN
```

- **CLOSED:** requests pass through; failure counter increments on error
- **OPEN:** requests fail immediately with a fallback; no calls to the downstream
- **HALF-OPEN:** one probe request is allowed through to test recovery

Rules:
- Open after N failures within a rolling time window (e.g., 5 failures in 30s)
- Never open on client errors (4xx) — those are the caller's fault, not the downstream's
- Set the probe timeout long enough for the downstream to recover (e.g., 30s – 60s)
- Emit metrics on state transitions; alert on circuit opening

## Retry Policy

- Max **3 retries** (4 total attempts) for most cases
- **Exponential backoff with jitter:**

```
attempt 1 delay: 100ms + rand(0–50ms)
attempt 2 delay: 200ms + rand(0–100ms)
attempt 3 delay: 400ms + rand(0–200ms)
```

- Retry only transient failures: 5xx responses, network timeouts, connection resets
- Do NOT retry: 4xx errors (except 429 with `Retry-After`), validation failures, business logic errors
- Ensure the operation is idempotent before retrying — use idempotency keys for non-idempotent operations
- Combine with circuit breaker: stop retrying when the circuit is open

## Timeout

- Set a timeout at **every** network boundary — database, HTTP call, message broker, internal RPC
- Client-side timeout must be **shorter** than server-side timeout:
  - If the client times out first and retries, the server may process the original request twice
  - Rule of thumb: client timeout = 80–90% of the server's configured processing timeout
- Use separate timeouts for connection establishment and total response time
- Log timeout events with the full call target and duration for observability

## Bulkhead

- Assign a **separate thread pool or connection pool** to each critical downstream dependency
- One pool exhaustion must not prevent calls to other dependencies
- Size pools independently based on expected concurrency and dependency SLA:

```
billing-service pool:    max 20 threads, queue 50
inventory-service pool:  max 10 threads, queue 20
notification-service pool: max 5 threads, queue 10
```

- Reject requests with a clear error (503 + explanation) when the pool is saturated — never silently queue indefinitely
- Monitor pool saturation as a leading indicator of downstream degradation

## Fallback

- Always provide an explicit fallback — never return a silent empty response on failure
- Fallback options in priority order:
  1. Return a cached (possibly stale) result
  2. Return a safe default value (empty list, zero, placeholder)
  3. Return a degraded response (feature disabled message)
  4. Return a clear error to the caller with enough context to retry later
- Never swallow exceptions silently — log the original error even when serving a fallback
- Mark fallback responses in the payload or headers so callers can distinguish real from degraded data

## HTTP Client Connection Pooling

Establishing a TCP connection (plus TLS handshake over HTTPS) is expensive relative to the request itself. A pooled HTTP client keeps connections open and reuses them across calls to the same host instead of opening a fresh one every time. This is a client-side concern — separate from the server-side pooling covered under Bulkhead above, and from database connection pooling (see `skills/integrations/database-production/SKILL.md`).

**Use when:**
- The service makes repeated outbound calls to the same host (internal microservice, third-party API, webhook target)
- Call volume is high enough that per-request handshake latency shows up in p95/p99
- The downstream supports HTTP keep-alive (virtually all modern HTTP/1.1+ and HTTP/2 servers do)

**Skip or scope narrowly when:**
- The call is a true one-off (cold start, cron job hitting a host once) — pooling adds idle-connection overhead with no reuse benefit
- The target host rotates behind short-lived DNS (e.g. some load balancers) — see DNS caching pitfall below

**Every HTTP client library exposes some form of this — names vary by stack, but the concepts don't:**

| Concept | What it controls | Typical failure mode if misconfigured |
|---|---|---|
| Max connections per host | Ceiling on concurrent open connections to one downstream | Too low → requests queue/block waiting for a free connection under load; too high → downstream gets overwhelmed or hits its own connection limits |
| Max idle connections | How many idle (kept-alive) connections stay open for reuse | Too low → connections keep getting closed and reopened, losing the reuse benefit; too high → resource waste, may exhaust downstream connection limits |
| Idle timeout | How long an unused connection stays open before being closed | Too short → connections churn like no pooling was configured; too long → stale connections get used and fail (see below), or resources leak |
| Connection timeout | Max time to wait establishing a new connection | Too long → slow failure detection, threads/goroutines pile up waiting; too short → false failures under normal network jitter |

**Common pitfalls:**
- **Stale connection reuse**: a pooled connection can be silently closed by the server or an intermediate proxy/load balancer while idle. Configure the client to validate or retry-once-on-connection-reset rather than surfacing it as a hard failure to the caller.
- **DNS caching mismatch**: a pooled connection binds to a resolved IP. If the client also caches DNS aggressively, it can keep talking to a decommissioned backend after a deploy or failover. Keep idle timeout shorter than the downstream's DNS TTL when the target is behind a rotating load balancer.
- **One pool per downstream, not one global pool**: mirror the Bulkhead pattern — size the pool for each downstream independently based on its expected concurrency and latency profile, so one saturated dependency doesn't starve connections meant for another.
- **Missing pooling entirely**: the default HTTP client in many languages does *not* pool by default, or pools with a very small ceiling (e.g. 1–2 connections per host) — verify the actual default before assuming reuse is happening.

Consult your stack's HTTP client documentation for the exact parameter names (e.g. `MaxIdleConnsPerHost`, `maxConnections`, `pool_maxsize`, `maxSockets`) — the concepts above map onto all of them.

## Rate Limiting

| Algorithm | Behavior | Best For |
|-----------|----------|---------|
| Token Bucket | Smooth average rate; allows short bursts | APIs, outbound calls |
| Sliding Window | Precise request counting per window | Burst detection, abuse prevention |
| Fixed Window | Simple but allows boundary bursts | Internal rate limiting where precision is less critical |
| Leaky Bucket | Constant output rate regardless of input spikes | Traffic shaping |

- Return `429 Too Many Requests` with a `Retry-After` header specifying seconds until the next allowed request
- Apply rate limits per API key, user ID, or IP — never globally only
- Implement rate limits as close to the edge as possible (API gateway, CDN) to reduce backend load
- Log rate-limit hits with the client identifier for abuse analysis

## Health Checks

Three distinct probes — do not conflate them:

| Probe | Question | Failing means |
|-------|---------|--------------|
| Liveness | Is the process alive and not deadlocked? | Kill and restart the container |
| Readiness | Can this instance serve traffic right now? | Remove from load balancer pool |
| Startup | Has initialization completed? | Delay liveness/readiness checks |

- Expose all probes at `/health` with sub-paths: `/health/live`, `/health/ready`, `/health/startup`
- Readiness checks must verify critical dependencies (DB connection, cache availability)
- Liveness checks must be lightweight — never check external dependencies in liveness
- Return `200` on healthy, `503` on unhealthy; include a JSON body with individual component status
- Set appropriate Kubernetes probe parameters: `initialDelaySeconds`, `periodSeconds`, `failureThreshold`
