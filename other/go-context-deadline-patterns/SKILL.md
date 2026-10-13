---
name: go-context-deadline-patterns
description: >
  Use this when writing any I/O method whose first param is ctx context.Context,
  wrapping another ctx-aware client, designing Close(ctx)/Drain(ctx) shutdown
  contracts, choosing a package-default timeout, or responding to reviewer
  flags about missing deadline checks or undeferred cancels. Covers ctx.Deadline()
  inheritance, cancellation safety, deadline-to-timeout bridging, and
  shortest-deadline-wins composition for stacked clients.
  Triggers: ctx.Deadline, context.WithTimeout, context.WithDeadline, cancel, defer cancel, deadline propagation, timeout, context.Canceled, shortest deadline wins.
---

# go-context-deadline-patterns (v1.0.0)

## Rationale

Every I/O method in the SDK takes `ctx context.Context` as its first parameter (Rule 6). The contract: the method MUST return before the deadline passes, MUST abort on cancellation, and MUST NOT outlive the caller's lifetime. Three failure modes this skill exists to prevent: (1) **silent deadline violation** — the method ignores `ctx.Deadline()` and makes the caller wait forever, (2) **cancel-leak** — `context.WithTimeout` / `WithCancel` is called without matching `defer cancel()`, leaking resources, (3) **stacked-client inversion** — a client that wraps another client imposes its own internal timeout that overrides the caller's shorter deadline. The target SDK encodes a consistent bridge: **if caller already set a deadline, respect it; only if not, apply a package-default timeout** — shortest deadline wins.

## Activation signals

- Writing any I/O method: its first param MUST be `ctx context.Context`
- Wrapping another client whose methods also accept `ctx` — passing through is mandatory
- `Close(ctx context.Context)` / `Drain(ctx)` — the SDK's graceful-shutdown contract takes a ctx
- Designing a default timeout ("if the caller didn't set one, we use 30s")
- Reviewer cites "no deadline check", "timeout overrides caller", or "cancel not deferred"
- Integration test flakes on tight-deadline case

## GOOD examples

### GOOD 1: Deadline probe + default-timeout bridge (shortest-deadline-wins)

Source: `motadatagosdk/events/jetstream/publisher.go` and `requester.go`. The pattern: probe `ctx.Deadline()`; if the caller DID set a deadline, do nothing — their deadline already governs. Only when they didn't, derive a `WithTimeout` using the package default. `defer cancel()` is mandatory to release the derived timer.

```go
// Publisher.Publish — bridge pattern
func (p *Publisher) Publish(ctx context.Context, subject string, msg *nats.Msg) (*PubAck, error) {
    if _, ok := ctx.Deadline(); !ok {
        var cancel context.CancelFunc
        ctx, cancel = context.WithTimeout(ctx, defaultPublishTimeout)
        defer cancel()
    }
    // Caller's deadline (if any) still governs; ours is a floor.
    return publish(ctx, p.js, subject, msg, p.middleware, p.maxPayload)
}
```

This is the canonical SDK pattern. `context.WithTimeout(parent, d)` already enforces shortest-deadline-wins — if parent has an earlier deadline, the derived context inherits it. You never need `min(parentDeadline, d)` manually.

### GOOD 2: Deadline → timeout bridge for a downstream API that wants a `time.Duration`

Source: `motadatagosdk/events/jetstream/publisher.go` (`Close`). When calling into a library that takes a `timeout time.Duration` instead of a `context.Context`, compute the remaining time from `ctx.Deadline()` and fall back to a package default.

```go
func (p *Publisher) Close(ctx context.Context) error {
    // ...
    timeout := defaultFlushTimeout
    if d, ok := ctx.Deadline(); ok {
        if r := time.Until(d); r > 0 {
            timeout = r  // honor caller's deadline as the flush ceiling
        }
    }
    return p.nc.FlushTimeout(timeout)
}
```

### GOOD 3: Drain loop with context-scoped deadline (graceful shutdown)

Source: `motadatagosdk/events/connection.go` (`Close`). When a shutdown op must poll for completion (NATS drain, pool reap), derive a scoped deadline from the caller's ctx and a config-level max; `select` against `deadline.Done()` to bound the wait AND `time.After` to pace the poll.

```go
func (c *Connection) Close(ctx context.Context) error {
    // ... mark closed ...
    if err := nc.Drain(); err != nil { nc.Close(); return nil }

    deadline, cancel := context.WithTimeout(ctx, c.config.DrainTimeout)
    defer cancel()

    for nc.IsDraining() {
        select {
        case <-deadline.Done():
            nc.Close() // budget exhausted — hard close
            return nil
        case <-time.After(drainPollInterval):
        }
    }
    return nil
}
```

### GOOD 4: Inside a blocking wait — never sleep, always select

Source: `motadatagosdk/events/middleware/retry.go`. A retry's backoff sleep MUST honor `ctx.Done()` — otherwise a cancelled caller waits through the full backoff.

```go
func (r *RetryMiddleware) waitBackoff(ctx context.Context, attempt int) error {
    select {
    case <-ctx.Done():                                return ctx.Err()
    case <-time.After(r.calculateBackoff(attempt)):   return nil
    }
}
```

## BAD examples (anti-patterns)

### BAD 1: Unconditionally overriding the caller's deadline

```go
// BAD: caller set ctx with a 100ms deadline for a user-facing API;
// this method now waits up to 30s regardless.
func (c *Client) Get(ctx context.Context, key string) ([]byte, error) {
    ctx, cancel := context.WithTimeout(ctx, 30*time.Second) // wrong
    defer cancel()
    return c.fetch(ctx, key)
}
```
Breaks: violates "shortest deadline wins" on the intent axis — even though `WithTimeout` technically inherits the parent's earlier deadline, the library is now advertising a 30s behavior it can't deliver. Fix: probe `ctx.Deadline()` first; only set a timeout when the caller didn't (GOOD 1).

### BAD 2: WithTimeout / WithCancel without `defer cancel()`

```go
// BAD: derived context's resources never release. Timer keeps firing.
// Leak compounds across many calls.
func (c *Client) Do(ctx context.Context) error {
    ctx, _ = context.WithTimeout(ctx, 5*time.Second) // _ drops cancel
    return c.work(ctx)
}
```
Breaks: every `WithCancel` / `WithTimeout` / `WithDeadline` returns a `cancel` that MUST be called to release the derived timer. `go vet` and `govet/lostcancel` flag this. Fix: `ctx, cancel := ...; defer cancel()`.

### BAD 3: Using `context.Background()` inside a request handler

```go
// BAD: loses the caller's cancellation tree entirely. Work continues
// after the caller has timed out / cancelled.
func (s *Service) Handle(ctx context.Context, req Req) error {
    return s.downstream.Call(context.Background(), req) // severs ctx
}
```
Breaks: no propagation, no cancellation, no deadline. Fix: pass the caller's `ctx`. If you genuinely need work to outlive the caller (fire-and-forget audit log), derive with `context.WithoutCancel(ctx)` from Go 1.21+ and document why.

### BAD 4: time.Sleep inside a ctx-scoped op

```go
// BAD: doesn't honor cancellation. Caller's deadline passes; this
// goroutine sleeps through it. See goroutine-leak-prevention.
time.Sleep(backoff)
```
Breaks: a cancelled ctx won't stop a `time.Sleep`. Fix: `select { case <-ctx.Done(): ...; case <-time.After(backoff): ... }` (GOOD 4).

### BAD 5: Returning a value after the deadline passed

```go
// BAD: work ignored ctx, then returns nil at the end. Caller already
// moved on; the returned value is racing with the next request.
func (c *Client) Do(ctx context.Context, req Req) (*Resp, error) {
    return c.workIgnoringCtx(req), nil
}
```
Breaks: the ctx contract isn't just about aborting — it's about not doing work the caller no longer wants. Fix: check `ctx.Err()` at entry and at each logical step; pass ctx to every downstream call.

## Decision criteria

| Situation | Rule |
|---|---|
| Writing an I/O method | First param MUST be `ctx`; MUST pass `ctx` down; MUST check `ctx.Err()` at entry |
| Caller already set deadline | DO NOT override; inherit |
| Caller did NOT set deadline | Probe `ctx.Deadline()`; apply package-default `WithTimeout`; `defer cancel()` |
| Downstream takes `time.Duration` not `ctx` | Compute `time.Until(ctx.Deadline())`; fallback to default |
| Background task that must outlive the caller | `context.WithoutCancel(ctx)` (Go 1.21+) — document the reason |
| Blocking wait (sleep, channel, mutex) | MUST `select` on `ctx.Done()` |
| `Close()` / `Stop()` | Accept `ctx` so the caller can bound shutdown time; fall back to a config-level max |

**Stacking rule**: if client A wraps client B, A's method MUST forward `ctx` to B unchanged. A may add its *own* scoped timeout only when B's call is internal plumbing (e.g., a handshake), and even then the scope cannot exceed what `ctx.Deadline()` permits.

**Package defaults**: every package that uses the bridge pattern MUST declare its default timeout as an unexported const (`defaultPublishTimeout`, `defaultFlushTimeout`) in the same file, not in a shared constants module — keeps the value discoverable at the call site.

## Target SDK Convention

Current convention in motadatagosdk:
- Every I/O method takes `ctx context.Context` as first param (Rule 6)
- Bridge pattern: `if _, ok := ctx.Deadline(); !ok { ctx, cancel = context.WithTimeout(...); defer cancel() }`
- `Close(ctx)` / `Drain(ctx)` accept a context so the caller bounds shutdown
- Package-default timeouts are unexported consts in the same file as the method
- `motadatagosdk/utils` sentinel: `ErrCanceled` for context-canceled mapped errors (Dragonfly pattern: mapped error is classified NOT a circuit failure — cancellation is a caller signal, not a dependency fault)

If TPRD requests divergence (e.g., a method that must NOT inherit the caller's deadline — a reaper or watchdog): declare in TPRD §5, derive with `context.WithoutCancel(ctx)` in Go 1.21+, record rationale.

## Cross-references

- `idempotent-retry-safety` — every retry loop MUST check `ctx.Err()` at the top of each iteration AND use ctx-aware wait
- `goroutine-leak-prevention` — a goroutine that doesn't watch `ctx.Done()` leaks on cancellation; this skill's select patterns are the fix
- `go-client-shutdown-lifecycle` — `Close(ctx)` uses the drain pattern from GOOD 3
- `go-backpressure-flow-control` — `Semaphore.Acquire(ctx)` is a context-deadline pattern
- `go-circuit-breaker-policy` — breaker errors propagate while preserving `ctx.Err()` precedence (cancellation beats breaker-open on the error path)

## Guardrail hooks

- **G63** (goleak) — goroutines that sleep on `time.Sleep` or block on unbounded channel ops without watching `ctx.Done()` show up as leaks on cancellation tests.
- **G65** (bench regression) — adding unneeded `context.WithTimeout` allocations to a hot path regresses p50; the bridge pattern (GOOD 1) avoids this.
- **G104** (alloc budget) — `context.WithTimeout` allocates a timer; the `ctx.Deadline()`-probe-first pattern keeps the happy path allocation-free when the caller already set a deadline.
- **`go vet` / staticcheck `SA5001`, `lostcancel`** — catches missing `defer cancel()`. Part of the deterministic-first gate.
