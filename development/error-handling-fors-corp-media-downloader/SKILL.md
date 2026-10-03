---
name: error-handling
description: Error handling and logging conventions — when to catch vs propagate, what to log at what level, how to fail safely. Use when writing code that can fail (I/O, network, parsing, external services) or when reviewing whether errors are handled correctly vs just silenced.
---

# Error handling & logging

## Handle at the right layer

- Catch an error only where you can actually do something useful with it — retry,
  fall back, translate it into a meaningful error for the caller, or surface it to a
  user. Catching just to log-and-swallow hides failures from whoever needed to know.
- Don't catch broad exception types (`except Exception`, `catch (e)`) unless
  re-raising/wrapping — a blanket catch silently swallows bugs unrelated to the
  failure you meant to handle.
- Let unexpected errors propagate to a top-level boundary that logs and fails
  loudly (a global handler, a process crash with a clear message) rather than
  continuing in a corrupted state.

## Fail loudly in development, gracefully in production

- A user-facing failure should never expose a raw stack trace, internal error
  message, or implementation detail — show a clear, actionable message and log the
  real detail server-side/internally.
- A silent failure (swallowed exception, ignored return code, empty catch block) is
  worse than a crash — it corrupts state invisibly and the bug surfaces somewhere
  unrelated, much later, much harder to trace.

## Logging levels, used consistently

- **error**: something failed and needs attention; include enough context (what
  operation, what input triggered it, correlation/request ID) to actually debug it
  without reproducing.
- **warn**: recovered automatically, or a caller did something that will bite them
  soon (using a deprecated path).
- **info**: significant lifecycle events (started, request handled, job completed) —
  not so verbose that a real error gets lost in noise.
- **debug**: detail useful only when actively troubleshooting, off by default.
- Never log secrets, tokens, passwords, or full PII — log identifiers/redacted
  forms instead.

## Retries & timeouts

- Anything crossing a network/process boundary needs an explicit timeout — an
  unbounded wait is a resource leak and a hidden failure mode.
- Retry only on errors that are actually transient (timeout, 503, connection reset),
  never on validation/auth errors, and use backoff (not a tight retry loop) to avoid
  hammering a struggling dependency.

## Error types

- Prefer typed/structured errors (custom error classes/enums, `Result`/`Either`-style
  return types where the language supports them) over stringly-typed errors your
  caller has to pattern-match with substring checks.
- Include the causal chain (wrap, don't discard, the original error) so a stack
  trace shows the real root cause, not just the last layer that noticed.

## When reviewing

Look for: empty catch blocks, catches that log but don't re-raise or handle,
missing timeouts on I/O, retries on non-idempotent operations, and error messages
that would leak internals if they reached an end user.
