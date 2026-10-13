---
name: go-client-shutdown-lifecycle
description: >
  Use this when designing the Close() contract for an SDK client that owns
  goroutines, connection pools, or buffered channels — idempotency via
  sync.Once or atomic.Bool CAS, context-driven abort, drain-with-timeout,
  ordered sub-resource teardown so goleak.VerifyTestMain stays clean.
  Triggers: Close(), sync.Once, atomic.Bool, CompareAndSwap, drain, goleak.VerifyTestMain, t.Cleanup, context.Canceled.
---

# go-client-shutdown-lifecycle (v1.0.0)

## Rationale

Every SDK client owns at least one goroutine (metrics scraper, background
connection health checker, pubsub demultiplexer) and at least one system
resource (connection pool, file descriptor, buffered channel). The `Close()`
method is the **single** contract the caller has to reclaim all of that. Three
invariants are non-negotiable:

1. **Idempotent** — `Close()` on an already-closed client returns `nil` without side effects. Callers commonly `defer c.Close()` after a `defer c.Close()` in a test harness; the second call must not re-close a `chan struct{}` (panic) or double-decrement a pool.
2. **Ordered teardown** — sub-resources stop in reverse dependency order. Background goroutines first (they may still emit metrics into the pool); the pool last. Deadlock-free: the loop goroutine must exit BEFORE the resource it was reading from is closed.
3. **Drain vs abort is the caller's call** — expose a context-driven abort path. A caller with a `30s` deadline passes `ctx`; drain stops when ctx expires. A caller who wants "stop now, drop in-flight" passes a cancelled context.

The `goleak.VerifyTestMain` gate (guardrail G63 + convention) fails the test
binary if any goroutine outlives `m.Run()`. That turns lifecycle bugs into
immediate BLOCKERs.

## Activation signals

- New SDK client owns a goroutine or connection pool
- TPRD §Skills-Manifest lists `go-client-shutdown-lifecycle`
- Reviewer (`sdk-api-ergonomics-devil-go`, `sdk-convention-devil-go`) flags `Close` shape
- `goleak` test fails in CI

## GOOD examples

### 1. Idempotent `Close` via `atomic.Bool.CompareAndSwap`

From `core/l2cache/dragonfly/cache.go`:

```go
type Cache struct {
    rdb     *redis.Client
    scraper *poolStatsScraper
    closed  atomic.Bool
}

// Close shuts down the pool-stats scraper and the underlying go-redis
// client. Idempotent; second and subsequent calls return nil without
// side effects.
func (c *Cache) Close() error {
    if !c.closed.CompareAndSwap(false, true) {
        return nil // already closed — fast path, no error
    }
    // Scraper first: stops monotonic-gauge reads before the pool dies.
    if c.scraper != nil {
        c.scraper.stop()
    }
    if c.rdb == nil {
        return nil
    }
    if err := c.rdb.Close(); err != nil {
        // Pool-already-closed during race is expected on double Close.
        if errors.Is(err, redis.ErrClosed) {
            return nil
        }
        return fmt.Errorf("%w: %v", ErrUnavailable, err)
    }
    return nil
}
```

### 2. Goroutine with `sync.Once` on both start and stop + drain-with-timeout

From `core/l2cache/dragonfly/poolstats.go`:

```go
type poolStatsScraper struct {
    interval  time.Duration
    done      chan struct{}
    stopped   chan struct{}
    once      sync.Once
    stopOnce  sync.Once
}

func (s *poolStatsScraper) start() {
    s.once.Do(func() { go s.run() })
}

func (s *poolStatsScraper) run() {
    defer close(s.stopped)           // signals completion
    t := time.NewTicker(s.interval)
    defer t.Stop()
    for {
        select {
        case <-s.done:
            return
        case <-t.C:
            // ... emit metrics ...
        }
    }
}

// stop signals the scraper and waits up to scraperStopTimeout for
// confirmation. Idempotent.
func (s *poolStatsScraper) stop() {
    s.stopOnce.Do(func() { close(s.done) })
    select {
    case <-s.stopped:
        // clean exit
    case <-time.After(scraperStopTimeout):
        logger.Warn(context.Background(),
            "dragonfly: pool-stats scraper stop timed out")
    }
}
```

### 3. Context-driven abort on a `Close(ctx)`-style method

```go
// Close drains in-flight requests, then releases the pool. If ctx is
// cancelled, Close aborts immediately (in-flight requests are returned
// context.Canceled from their own call sites).
func (c *Client) Close(ctx context.Context) error {
    if !c.closed.CompareAndSwap(false, true) {
        return nil
    }
    close(c.quit) // signal workers to stop accepting new work
    done := make(chan struct{})
    go func() { c.wg.Wait(); close(done) }() // wait for workers to drain
    select {
    case <-done:
        return c.pool.Close()
    case <-ctx.Done():
        // Abort: skip drain, close pool anyway to release FDs.
        _ = c.pool.Close()
        return ctx.Err()
    }
}
```

## BAD examples

### 1. Non-idempotent close: second call panics

```go
// BAD: close on an already-closed channel panics.
func (c *Client) Close() error {
    close(c.quit) // second call = panic
    return c.pool.Close()
}
```

### 2. Race between `New` and `Close` — scraper start not guarded

```go
// BAD: if Close runs before run() reaches its first select,
// the goroutine never exits.
func (s *scraper) start() { go s.run() }
func (s *scraper) run() {
    for {
        select {
        case <-s.done: return
        // ... no ticker; goroutine leaks if done was closed before loop
        }
    }
}
```

Fix: always wire `done` via `newScraper` before `go run()`; use `sync.Once`
on `start`.

### 3. Teardown out of order: pool before goroutine

```go
// BAD: scraper still reading from rdb after rdb.Close() → panic on nil.
func (c *Cache) Close() error {
    c.rdb.Close()      // pool gone
    c.scraper.stop()   // scraper's last tick reads from nil pool
    return nil
}
```

## Decision criteria

| Question | Answer |
|---|---|
| Single idempotency guard | `atomic.Bool.CompareAndSwap` on struct field OR `sync.Once` wrapping the close body |
| Double-close returns error? | **No**. Return `nil`. Caller convenience > strict protocol. |
| Close accepts `ctx`? | Only if teardown can take a bounded, caller-chosen time (drain). `io.Closer` shape (`Close() error`) is fine when stop is near-instant. |
| Teardown order | Goroutines → channels they read → connection pool → FDs |
| Timeout on drain | Yes — hard upper bound (e.g. `scraperStopTimeout = 5s`); log WARN and move on |
| Stop-channel or context for loops? | Both: `select { case <-s.done: case <-ctx.Done(): case <-t.C: ... }` |
| Goleak test | `goleak.VerifyTestMain(m)` in `TestMain`; every goroutine the package spawns must exit |

## Cross-references

- `goroutine-leak-prevention` — the goleak harness and common leak shapes
- `go-context-deadline-patterns` — context propagation into shutdown paths
- `lifecycle-events` — OTel spans for New/Close
- `go-credential-provider-pattern` — stop cred-refresh goroutine in Close
- `network-error-classification` — `ErrPoolClosed` sentinel returned after Close

## Guardrail hooks

- **G43.sh** — compile-time `var _ io.Closer = (*T)(nil)` assertion for clients that implement Closer
- **G48.sh** — no `init()`; lifecycle must be explicit
- **G60.sh** — `-race` catches close/start races
- **G63.sh** — `go test -count=3 -race` flushes intermittent teardown flakes
- Convention: `goleak.VerifyTestMain(m)` in `TestMain` is a testing-lead checklist item
- Devil: `sdk-convention-devil-go` — verifies `Close` method name matches sibling packages (not `Shutdown`, not `Stop`)
