---
name: mav-bp-error-handling
description: Error handling conventions for all applications. Covers error propagation, retry strategies, circuit breakers, graceful degradation, error boundaries, and typed errors. Applied when writing or reviewing error handling code.
user-invocable: false
disable-model-invocation: true
---

# Error Handling Standards

Maverick's hard rules for intentional, typed, resilient error handling.

## Maverick's Rules

- **Never swallow silently** — every `catch` handles, logs, or re-throws. An empty `catch` is a bug.
- **Catch at boundaries only** — throw/return from low-level code, catch at service boundaries and the outermost handler. Catching at every layer duplicates logging and loses stack traces. No catch-and-re-throw without adding context.
- **Typed errors** — every application error carries `type` (machine-readable classification), `message`, `context` (structured metadata), and `cause` (wrapped original). Never `throw new Error("failed")`.
- **Log-level mapping: 4xx → `warn`, 5xx → `error`** — client errors are expected (track volume, no alert unless it spikes); server errors require investigation and alert when persistent. Log levels and alerting per `mav-bp-operability`.
- **Retry policy** — 3 attempts max (1 initial + 2 retries) unless configured otherwise; exponential backoff (`base * 2^attempt`) with jitter. Retry only transient failures: timeouts, 429, 502, 503, 504. Never retry 400/401/403/404 or non-idempotent operations without idempotency keys.
- **Never expose internals to clients** — no stack traces, SQL/database messages, file paths, internal service names, or dependency versions in responses. Return a safe message, a machine-readable error type, and a request/correlation ID.
- **Critical paths must not depend on non-critical services** — degrade the feature (visibly, and log/alert on degraded mode) rather than crash. Frontend: error boundaries around major UI sections with fallback UI and error reporting.
- **Fail fast on unrecoverable errors** — configuration failures, corruption, programming errors: crash immediately with a clear message; do not attempt recovery.

## Project Implementation Lookup

Check for `docs/maverick/skills/error-handling/SKILL.md`. If present, read it — it wins on specifics (library, config, conventions). If missing, proceed with these standards and note the gap in your summary.

## Detecting Error Handling Issues in Code Review

| Pattern                                             | Issue                          | Fix                                               |
| --------------------------------------------------- | ------------------------------ | ------------------------------------------------- |
| Empty `catch` block                                 | Silently swallowed error       | Handle, log, or re-throw                          |
| `catch (err) { return null }`                       | Lost error context             | Propagate the error or handle explicitly           |
| `throw new Error("failed")`                         | Untyped, no context            | Use typed error with structured metadata           |
| Retrying on 400/401/403                             | Retrying permanent failures    | Only retry transient errors (429, 5xx, timeouts)   |
| No retry on external HTTP calls                     | Fragile to transient failures  | Add retry with exponential backoff                 |
| Stack trace in API response                         | Leaking internals              | Return safe error with request ID only             |
| `catch` at every layer in the call stack            | Duplicate handling/logging     | Catch at the boundary, propagate elsewhere         |
| Feature crashes app when dependency is down         | No graceful degradation        | Degrade the feature, keep the app running          |
| No error boundary around UI sections                | Single component crashes page  | Wrap sections in error boundaries with fallback UI |
| Generic error message for all failures              | Poor user experience           | Distinguish client vs server errors                |

<!-- maverick-plugin-version: 4.0.2-dev -->
