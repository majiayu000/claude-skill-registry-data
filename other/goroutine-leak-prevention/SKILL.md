---
name: goroutine-leak-prevention
description: >
  Use this when designing any io.Closer / Close(ctx) / Stop() type, adding
  background workers/tickers/pubsub listeners, writing integration tests that
  exercise shutdown, or responding to an sdk-leak-hunter G63 failure. Covers
  cleanup contracts, goleak.VerifyTestMain wiring, leaky fan-out patterns
  (errgroup / sync.WaitGroup / context.WithCancel without Wait/cancel), and the
  shipping rules that prevent regressions.
  Triggers: goleak, goroutine leak, VerifyTestMain, Close() leak, context cancellation leak, fan-out leak, errgroup leak.
---

# goroutine-leak-prevention (v1.0.0)

## Rationale

Every long-lived SDK client spawns goroutines (pool maintenance tickers, worker fleets, connection health probes, pubsub listeners). Each one is a lifetime commitment: the goroutine must terminate when the owning client's `Close` completes or when the caller's `ctx` is cancelled. Leaks are usually invisible in unit tests (the test ends; the goroutine outlives it, polluting later tests or running off into the process heap in prod). `goleak.VerifyTestMain` makes the contract mechanical: any goroutine still alive at `TestMain` exit fails the build. The SDK pipeline treats G63 as a BLOCKER — no merge with a reachable leak.

## Activation signals

- Designing any type that returns an `io.Closer` or exposes a `Close(ctx)` / `Stop()` method
- Adding background workers, tickers, or pubsub listeners to a client
- Writing integration tests for a client that exercises the shutdown path
- Reviewing `sdk-leak-hunter-go` verdict, or responding to a G63 failure
- A devil cites `errgroup` / `sync.WaitGroup` / `context.WithCancel` without a visible `.Wait` / cancel call

## GOOD examples

### 1. `goleak.VerifyTestMain` on every new package

```go
// core/l2cache/dragonfly/cache_test.go — first function in the file.
package dragonfly

import (
    "testing"

    "go.uber.org/goleak"
)

func TestMain(m *testing.M) {
    goleak.VerifyTestMain(m,
        // Long-running goroutines owned by the stdlib OS signal handler; noisy on some CI hosts.
        goleak.IgnoreTopFunction("os/signal.loop"),
    )
}
```

One-line discipline: every new package ships with this. G63 enforces; `sdk-leak-hunter-go` fails closed if absent.

### 2. Idempotent `Close` that cancels + waits

```go
// Cache owns its own cancellable context; every goroutine derives from c.ctx.
type Cache struct {
    ctx    context.Context
    cancel context.CancelFunc
    wg     sync.WaitGroup
    closed atomic.Bool
}

func (c *Cache) spawnHealthcheck(interval time.Duration) {
    c.wg.Add(1)
    go func() {
        defer c.wg.Done()
        t := time.NewTicker(interval)
        defer t.Stop()
        for {
            select {
            case <-c.ctx.Done():
                return
            case <-t.C:
                c.probe()
            }
        }
    }()
}

func (c *Cache) Close() error {
    if !c.closed.CompareAndSwap(false, true) {
        return nil
    }
    c.cancel()
    c.wg.Wait()
    return nil
}
```

Invariants: `cancel` before `Wait` (else deadlock), `Add` before `go` (else race), `defer Done` inside the goroutine (else a panic leaks it).

### 3. `errgroup` with a derived context

```go
func (c *Cache) FanOutWrite(ctx context.Context, keys []string, vals [][]byte) error {
    g, gctx := errgroup.WithContext(ctx)
    g.SetLimit(runtime.GOMAXPROCS(0))
    for i, k := range keys {
        i, k := i, k
        g.Go(func() error {
            return c.setOne(gctx, k, vals[i])
        })
    }
    return g.Wait()
}
```

`errgroup.WithContext` gives siblings a cancellable handle; `g.Wait` is a leak fence — no goroutine outlives the call.

## BAD examples (anti-patterns)

### 1. `go func(){ ... }()` with no cancellation path

```go
// BAD — nothing stops this goroutine.
func (c *Cache) spawnMetricsReporter() {
    go func() {
        for {
            time.Sleep(10 * time.Second)
            c.flushMetrics()
        }
    }()
}
```

Fix: derive from `c.ctx`, select on `Done`, track with `wg`.

### 2. `Add` inside the goroutine, not before `go`

```go
// BAD — race: Wait may fire before Add lands, missing the goroutine.
func (c *Cache) buggyFanOut() {
    go func() {
        c.wg.Add(1)
        defer c.wg.Done()
        c.work()
    }()
    c.wg.Wait()
}
```

Fix: `c.wg.Add(1)` on the calling goroutine, BEFORE `go func`.

### 3. `context.Background()` in background workers

```go
// BAD — no parent ctx to cancel; the worker is unkillable.
func (c *Cache) drainQueue() {
    go c.worker(context.Background())
}
```

Fix: pass `c.ctx` (client-scoped) or a `context.WithCancel(c.ctx)` subtree.

## Decision criteria

Apply this skill when:

- The client owns any goroutine with a lifetime longer than a single method call.
- You introduce a `time.Ticker`, `time.AfterFunc`, `errgroup`, `sync.WaitGroup`, or an unbuffered channel reader whose writer could outlive the caller.
- You are implementing or modifying `Close` / `Shutdown` / `Stop`.

Skip when:

- The goroutine is strictly method-scoped (runs inside the method and joins before return — no fan-out beyond one stack).
- You're writing pure stateless helpers (no goroutines at all).

Tradeoffs:

- Cancel-first-then-wait is slightly slower on Close than ignore-and-hope; the latter leaks and fails G63. Always cancel-first.
- `errgroup.SetLimit(0)` is unbounded concurrency — always bound unless the caller has already bounded the fan-out.

## Cross-references

- `go-concurrency-patterns` — broader errgroup / context / sync primitives with the canonical idioms.
- `go-client-shutdown-lifecycle` — the `Close` contract this skill enforces from the goroutine side.
- `go-context-deadline-patterns` — how to propagate `ctx.Deadline` through spawned workers.
- `go-backpressure-flow-control` — bounded concurrency patterns that pair with leak prevention.
- `go-testing-patterns` — `TestMain` placement + `goleak` option hygiene.
- `idempotent-retry-safety` — retry loops are a common leak surface; classify their cancellation path.

## Guardrail hooks

- **G63** `goleak.VerifyTestMain` must exist and run clean on every new-package test binary. BLOCKER.
- **G65** bench regression — leaks often surface as growing allocs/op or wall-clock drift between runs.
- **G104** alloc budget — a leak manifests as unbounded `allocs/op`.
- **G106** drift fail-fast — soak tests expose leaks that unit tests miss; a positive drift trend in goroutine count is a leak signature.
- **CLAUDE.md rule 14** — "tests cover real behavior; `goleak.VerifyTestMain` clean" is non-negotiable.

Owner devil: `sdk-leak-hunter-go` — runs `go test -race` + parses `goleak` output; blocks on any reachable goroutine.
