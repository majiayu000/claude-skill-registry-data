---
name: error-handling
description: Implement explicit failure semantics, bounded retries and recovery. Triggers on "error handling", "错误处理".
---

# Error Handling

## When to use

- Implement explicit failure semantics, bounded retries and recovery.

**Not for:** debugging for a defect; incident-response for live containment.

## Steps

1. Identify operations, failure classes, ownership and user consequences.

2. Choose consistent boundary errors or results, preserve causes and sanitize public output.

3. Retry only transient failures with budgets and safe idempotency; add timeouts, cancellation or circuits when required.

4. Exercise real code with controlled failure inputs and verify recovery, telemetry and user feedback.

## Verify

- Errors are not swallowed; retries terminate and repeated actions and recovery have evidence.

## References

- [engineering-principles.md](../../../references/engineering-principles.md) — shared decision boundaries, scope and verification.
- [error-resilience.md](../../../skills/03-design/architecture/references/error-resilience.md) — system-level resilience architecture (cross-layer error propagation, failure posture); this skill is its implementation-level companion
- [references/retry-patterns.md](references/retry-patterns.md) — backoff/jitter formulas, circuit breaker state machine, idempotency-key patterns, retry budgets (with code)
