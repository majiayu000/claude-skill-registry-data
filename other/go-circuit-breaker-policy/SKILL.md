---
name: go-circuit-breaker-policy
description: >
  Use this when wrapping an external-dependency call site (Redis, NATS, HTTP,
  SQL) with motadatagosdk/core/circuitbreaker — picking thresholds, classifying
  caller-bug vs server-fault errors, wiring OnStateChange + ErrCircuitOpen
  through the public error model, and observing transitions without leaking
  goroutines.
  Triggers: circuit breaker, CircuitBreaker, ErrCircuitOpen, gobreaker, FailureThreshold, half-open, StateOpen, fail-fast, transient failure.
---

# go-circuit-breaker-policy (v1.0.0)

## Rationale

Unbounded retries against a failing dependency turn a transient outage into a cascading one: the caller queues up work, the dependency gets hammered on recovery, and the system enters a flap loop. The target SDK already ships a thin wrapper over `sony/gobreaker` at `motadatagosdk/core/circuitbreaker/` — new clients MUST reuse it rather than hand-rolling failure counters. The core decision a client author faces is not *whether* to wrap calls, but *which errors count as failures* (`IsSuccessful`), *how to classify caller-bug vs. server-fault errors*, and *how to surface `ErrCircuitOpen` through the public error model*.

## Activation signals

- New client in `motadatagosdk/core/` or `motadatagosdk/events/` that calls an external dependency (Redis / Dragonfly / Postgres / NATS / HTTP upstream)
- TPRD §7 declares an `ErrCircuitOpen` sentinel or requires a "circuit_transitions" OTel counter
- Client already has a `Config` struct and needs to accept an optional breaker
- Error-classification work (transient vs. permanent) — the same taxonomy drives both breaker counting and `idempotent-retry-safety`
- Reviewer cites "no failure cap" or "no fail-fast on known-bad dependency"

## GOOD examples

### GOOD 1: Constructing the SDK breaker with domain defaults

Source: `motadatagosdk/core/circuitbreaker/circuitbreaker.go`. The SDK exposes `Config` + `DefaultConfig(name)` + `NewCircuitBreaker(config)`. Defaults are filled in `NewCircuitBreaker` so zero-valued fields stay safe.

```go
import "motadatagosdk/core/circuitbreaker"

cfg := circuitbreaker.DefaultConfig("dragonfly-primary")
cfg.FailureThreshold = 5             // 5 consecutive failures → Open
cfg.Timeout          = 30 * time.Second // Open → Half-Open after 30s
cfg.MaxRequests      = 1             // one probe in Half-Open
cfg.SuccessThreshold = 1             // single success → Closed
cfg.OnStateChange = func(name string, from, to circuitbreaker.State) {
    logger.Info(context.Background(), "circuit transition",
        logger.String("breaker", name),
        logger.String("from", from.String()),
        logger.String("to", to.String()))
}
cb := circuitbreaker.NewCircuitBreaker(cfg)
```

### GOOD 2: Error classification decides what counts as a failure

Source: `motadatagosdk/core/l2cache/dragonfly/circuit_classify.go`. Cache misses, wrong-type, auth, context-cancel, config errors MUST NOT trip the breaker. Only server-side faults (timeout, unavailable, pool-exhausted) count. Unmapped errors default-deny to "count as failure" so unknown errors still protect the caller.

```go
func isCBFailure(err error) bool {
    if err == nil { return false }
    switch {
    // Caller-bug / miss / cancel: do NOT count.
    case errors.Is(err, ErrNil),
        errors.Is(err, ErrWrongType),
        errors.Is(err, ErrAuth),
        errors.Is(err, ErrCanceled),
        errors.Is(err, ErrInvalidConfig):
        return false
    // Server faults: DO count.
    case errors.Is(err, ErrTimeout),
        errors.Is(err, ErrUnavailable),
        errors.Is(err, ErrPoolExhausted),
        errors.Is(err, ErrNotConnected):
        return true
    }
    return true // default-deny
}
```

### GOOD 3: Observing state transitions without a background goroutine

Source: same package — `runThroughCircuit`. The wrapper reads `cb.State()` before and after each `Execute` call; when they differ it increments the `circuit_transitions` counter with bounded `{from, to}` labels. No observer goroutine is needed (avoids a `goroutine-leak-prevention` hazard).

```go
func (c *Cache) runThroughCircuit(ctx context.Context, fn func(context.Context) error) error {
    cb := c.cfg.CircuitBreaker
    if cb == nil { return fn(ctx) } // nil breaker = direct call, zero overhead
    before := cb.State()
    var rawErr error
    _, cbErr := cb.Execute(func() (any, error) {
        rawErr = fn(ctx)
        if rawErr == nil || !isCBFailure(mapErr(rawErr)) {
            return nil, nil
        }
        return nil, mapErr(rawErr)
    })
    if after := cb.State(); after != before {
        globalMetrics().circuitTransitions.Inc(ctx, metrics.Labels{
            "from": stateLabel(before), "to": stateLabel(after),
        })
    }
    if errors.Is(cbErr, utils.ErrCircuitOpen) {
        return fmt.Errorf("%w: %v", ErrCircuitOpen, cbErr)
    }
    return rawErr
}
```

## BAD examples (anti-patterns)

### BAD 1: Counting caller-bug errors as failures

```go
// BAD: every wrong-type error trips the breaker. A misbehaving caller
// can DoS the whole client pool by spamming a bad key.
_, cbErr := cb.Execute(func() (any, error) {
    return nil, c.rdb.Get(ctx, key).Err() // ErrWrongType counts here
})
```
Breaks: a correctness bug in one caller opens the circuit for every other caller. Fix: wrap `fn` and return `nil` error to the breaker for caller-bug sentinels, as in GOOD 2.

### BAD 2: Hand-rolling a failure counter instead of reusing `circuitbreaker`

```go
// BAD: duplicates the resilience toolkit; has no half-open probe, no
// state transitions, no OTel wiring, no `ErrCircuitOpen` sentinel.
type myCB struct{ mu sync.Mutex; fails int }
func (m *myCB) call(fn func() error) error {
    m.mu.Lock(); defer m.mu.Unlock()
    if m.fails >= 5 { return errors.New("too many fails") }
    if err := fn(); err != nil { m.fails++; return err }
    m.fails = 0
    return nil
}
```
Breaks: violates Rule 6 ("Resilience toolkit — clients reuse `core/circuitbreaker/`"). No recovery path, no observability, ambiguous error type. Fix: import `motadatagosdk/core/circuitbreaker`.

### BAD 3: Infinite timeout + no `OnStateChange` hook

```go
// BAD: a breaker that never reopens + emits no signal.
cfg := circuitbreaker.Config{
    Name:             "svc",
    FailureThreshold: 3,
    Timeout:          0, // treated as default (60s) — but a LITERAL zero intent is wrong
}
// No OnStateChange → ops team never learns the circuit opened.
```
Breaks: silent degradation. Even when `Timeout=0` is defaulted by `NewCircuitBreaker`, the intent is unclear; the missing `OnStateChange` hook defeats observability (rule 6 "OTel wiring").

## Decision criteria

| Situation | Apply? |
|---|---|
| Client calls external network dependency (Redis, NATS, HTTP, SQL) | YES — SHOULD wrap all data-path ops |
| In-process pure computation (encoding, hashing) | NO — no failure to protect against |
| A single operation that MUST succeed exactly once (publish with idempotency key) | YES, but pair with `idempotent-retry-safety` — breaker only fails fast |
| Optional in Config (caller may opt out for tests or single-call scripts) | YES — `cfg.CircuitBreaker = nil` must be a zero-overhead path (see GOOD 3) |

**Threshold heuristics** (tune in TPRD §5, not hard-coded):
- `FailureThreshold`: baseline 5 consecutive failures — higher for noisy dependencies, lower for mission-critical.
- `Timeout` (Open → Half-Open): baseline 30–60s. Too short = flapping; too long = user-visible outage.
- `MaxRequests` in Half-Open: 1 for cheap probes; higher only when probe cost is negligible AND you want faster convergence.
- `SuccessThreshold`: 1 for fast recovery. Raise only when flap-prone.

Never share one breaker across unrelated dependencies (anti-pattern from `circuitbreaker.go` godoc). One circuit per logical dependency.

## Target SDK Convention

Current convention in motadatagosdk: `Config.CircuitBreaker *circuitbreaker.CircuitBreaker` — optional pointer, nil = disabled (no indirection cost). `OnStateChange` wired through `motadatagosdk/otel` package (not raw OTel). `ErrCircuitOpen` re-exported from the client package as its own sentinel so `errors.Is(err, pkg.ErrCircuitOpen)` works at call sites.

If TPRD requests divergence (e.g., mandatory breaker not optional): declare in TPRD §5; `sdk-design-lead` records the deviation in `runs/<id>/design/deviations.md` with rationale.

## Cross-references

- `idempotent-retry-safety` — breaker fails fast; retry decides *which* failures to back off on. Same error taxonomy feeds both.
- `go-error-handling-patterns` — sentinel model for `ErrCircuitOpen`, `errors.Is`, error wrapping.
- `go-otel-instrumentation` — `circuit_transitions` counter + state-change logger.
- `go-client-shutdown-lifecycle` — breaker has no resource; but if `OnStateChange` spawns a goroutine, it MUST be joined on `Close()`.
- `go-concurrency-patterns` — synchronous transition-observer pattern (GOOD 3) avoids a background observer leak.

## Guardrail hooks

- **G63** (`goleak`) — catches observer goroutines the breaker wiring leaks. Forces the synchronous-observe pattern.
- **G65** (bench regression) — breaker overhead is ~100ns in Closed; regressions here mean the nil-breaker fast-path was broken.
- **G104** (alloc budget) — `Execute` MUST be alloc-free on the happy path; perf-budget.md declares `allocs_per_op: 0` for wrapped hot ops.
- **G61** (OTel wiring) — `OnStateChange` must publish via `motadatagosdk/otel`, not raw OTel — enforced at design review.
