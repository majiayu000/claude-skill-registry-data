---
name: go-idempotent-retry-patterns
description: >
  Use this for the Go-specific realization of idempotent-retry-safety —
  sentinel-based `IsRetryable` predicate using `errors.Is`/`errors.As`,
  context-aware backoff with `select` on `ctx.Done()`, the
  `motadatagosdk/events/middleware/retry.go` composition pattern, and
  `crypto/rand` jitter math. Pairs with shared-core `idempotent-retry-safety`
  (taxonomy + decision criteria).
  Triggers: errors.Is, errors.As, IsRetryable, RetryMiddleware, MaxAttempts, time.After, ctx.Done, crypto/rand, jitter, HeaderMessageID, JetStream WithMsgID.
version: 1.0.0
last-evolved-in-run: v0.6.0-rc.0-sanitization
status: stable
tags: [go, retry, resilience, sdk]
---

# go-idempotent-retry-patterns (v1.0.0)

## Scope

Go realization of the rules in shared-core `idempotent-retry-safety`. The shared skill defines: which classes of error are retriable, why an idempotency envelope is required, why jittered exponential backoff. This skill is the Go code that realizes those rules.

## Retry predicate — sentinel-based, `errors.As` for typed errors

Pattern from `motadatagosdk/events/utils/errors.go`. Permissive default (unknown → retriable) BUT deterministic failures explicitly opt OUT.

```go
func IsRetryable(err error) bool {
    if err == nil {
        return false
    }
    switch {
    case errors.Is(err, ErrInvalidSubject),
        errors.Is(err, ErrInvalidMessage),
        errors.Is(err, ErrInvalidConfig),
        errors.Is(err, ErrSerializationFailed),
        errors.Is(err, ErrPermissionDenied),
        errors.Is(err, ErrDuplicateMsg),       // already dedup'd — retry = double-effect
        errors.Is(err, ErrShutdownInProgress),
        errors.Is(err, ErrConnectionClosed):
        return false
    }
    var serErr SerializationError
    if errors.As(err, &serErr) {
        return false
    }
    var cfgErr ConfigError
    if errors.As(err, &cfgErr) {
        return false
    }
    return true
}
```

Key points:
- `errors.Is` for sentinel comparison; `errors.As` for typed errors. Never string-match.
- `ctx.Err()` from caller cancellation MUST short-circuit to `false` (don't retry work the caller no longer wants).
- Predicate must be alloc-free — it's called on every error. `BenchmarkIsRetryable` verifies.

## Context-aware backoff with `select` on `ctx.Done()`

```go
func (r *RetryMiddleware) executeWithRetry(ctx context.Context, msg *nats.Msg, next PublishHandler) error {
    var lastErr error
    for attempt := 0; attempt <= r.config.MaxAttempts; attempt++ {
        if err := ctx.Err(); err != nil {
            return firstNonNil(lastErr, err)
        }
        if err := next(ctx, msg); err == nil {
            return nil
        } else {
            lastErr = err
        }
        if !r.shouldRetry(lastErr) || attempt >= r.config.MaxAttempts {
            return lastErr
        }
        if r.waitBackoff(ctx, attempt) != nil {
            return lastErr // ctx cancelled mid-sleep
        }
    }
    return lastErr
}

func (r *RetryMiddleware) waitBackoff(ctx context.Context, attempt int) error {
    select {
    case <-ctx.Done():
        return ctx.Err()
    case <-time.After(r.calculateBackoff(attempt)):
        return nil
    }
}
```

Critical: never `time.Sleep(d)` inside a retry loop. A cancelled context must abort the wait immediately. `select` on `<-ctx.Done()` is the only way.

Backoff math: `base = Initial * Multiplier^N`, cap at `MaxInterval`, jitter = `cap * Jitter * rand(-1,1)`, floor at `Initial`. Use `crypto/rand` (goroutine-safe, no mutex) for jitter.

## Idempotency envelope — receiver dedup makes retry safe

For NATS JetStream publish: `motadatagosdk/events/jetstream/publisher.go`:

```go
var opts []natsjs.PublishOpt
if msg.Header != nil {
    if msgID := msg.Header.Get(core.HeaderMessageID); msgID != "" {
        opts = append(opts, natsjs.WithMsgID(msgID)) // server dedup key
    }
}
ack, err := p.js.PublishMsg(ctx, msg, opts...)
```

JetStream's server-side dedup window collapses duplicate publishes. Without `WithMsgID`, retry on a transient publish error can cause double-write.

For HTTP POST/PATCH: caller MUST send `Idempotency-Key` header. Without it, retry on 5xx is unsafe.

## SDK convention pairing

- `events/middleware/retry.go` for publish-side retries (composable middleware, NOT a baked-in retry helper)
- `events/utils.IsRetryable` as the canonical predicate
- `core/pool/workerpool.WithRetry(retries, delay)` for in-process task retries
- Dragonfly cache (`core/l2cache/dragonfly/`) ships with `MaxRetries=0` — retries are caller-composed via `RetryMiddleware`

## Anti-patterns

**1. POST + no Idempotency-Key + retry on 5xx.** `for i := 0; i < 3; i++ { http.Post(...); }` — every retry may have actually committed; result is double-billing. Fix: add `Idempotency-Key` OR treat 5xx-on-POST as permanent.

**2. Backoff without jitter.** `time.Sleep(time.Duration(attempt) * time.Second)` — N clients see the same 503, all back off in lockstep, all retry simultaneously, dependency gets clobbered. Fix: `calculateBackoff` with `Jitter=0.1` (±10%) baseline.

**3. `time.Sleep` instead of `select` on backoff.** Caller cancels mid-sleep, goroutine blocks to completion. `goleak` will catch it. Fix: `select { case <-ctx.Done(): ...; case <-time.After(d): ... }`.

**4. Retry predicate that returns `true` on `context.Canceled`.** Caller gave up; wasting resources. Either check `ctx.Err()` before each attempt OR encode in the predicate (`errors.Is(err, context.Canceled) → false`).

## Cross-references

- shared-core `idempotent-retry-safety` — taxonomy, decision criteria, HTTP semantics
- `network-error-classification` — sentinel taxonomy that the predicate reads
- `go-circuit-breaker-policy` — breaker + retry are dual; same error taxonomy feeds both
- `go-context-deadline-patterns` — retry MUST respect `ctx.Deadline()`
- `go-error-handling-patterns` — sentinel definition + `errors.Is` discipline
- `goroutine-leak-prevention` — guards against the `time.Sleep` anti-pattern

## Guardrail hooks

- `goroutine-leak-prevention` (G63) — catches blocking-sleep retry loops that don't honor `ctx.Done()`
- `go-bench` regression (G65) — retry fast-path (first attempt success) MUST not regress
- `g104` (alloc budget) — `IsRetryable` MUST be alloc-free
