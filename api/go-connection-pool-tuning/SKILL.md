---
name: go-connection-pool-tuning
description: >
  Use this when sizing motadatagosdk/core/pool — memorypool (PoolSize ≤ 64,
  PoolLength = p95), resourcepool (MaxSize, OnCreate/OnReset/OnDestroy),
  workerpool (MinWorkers, MaxWorkers, MaxQueueSize). Covers healthcheck
  cadence, backoff on exhaustion, and the symptom-to-dial decision table.
  Triggers: pool sizing, MaxSize, MinWorkers, MaxWorkers, pool exhaustion, ErrPoolOverload, ErrPoolExhausted, connection pool, worker pool, resource pool.
---

# go-connection-pool-tuning (v1.0.0)

## Rationale

The target SDK exposes three distinct pool packages under `motadatagosdk/core/pool/`. Misconfiguring them fails in opposite directions: oversizing burns memory and hides contention during load tests; undersizing forces callers onto `ErrPoolExhausted` / `ErrQueueFull` fast paths that mask real throughput ceilings. The sizing rules below are grounded in the actual API surface of `memorypool.PoolConfig`, `resourcepool.PoolConfig[T]`, and `workerpool.PoolConfig`. Every number cites a config field that already exists — no invented knobs.

## Target SDK Convention

Current convention in motadatagosdk:
- `memorypool.NewPoolManager(&PoolConfig{PoolSize, PoolLength, Expandable, Global})` — bitmask-tracked slab of typed buffers. `PoolSize` is capped at 64 by the bitmask (`usedPools int64`).
- `resourcepool.NewResourcePool[T](PoolConfig[T]{MaxSize, OnCreate, OnReset, OnDestroy})` — channel-backed object pool for stateful, expensive-to-create resources. Lazy creation up to `MaxSize`.
- `workerpool.Init(PoolConfig{MinWorkers, MaxWorkers, Timeout, MaxQueueSize, PanicHandler})` — goroutine pool with a 1s-tick auto-scaler. `DefaultConfig` is `{MinWorkers: 2, MaxWorkers: 6, Timeout: 30s, MaxQueueSize: 10000}`.

If TPRD requests divergence: add the new knob to the existing `PoolConfig` struct (do not introduce a sibling config); propose in `docs/PROPOSED-SKILLS.md` if the change implies a new sizing axis this skill does not cover.

## Activation signals

- TPRD §7 declares a new client that acquires network sockets, DB handles, or compiled state (resourcepool) or submits async work (workerpool).
- TPRD §5 NFR sets a `p99` latency or a `max_concurrent_connections` budget.
- `sdk-profile-auditor-go` (M3.5) reports `sync.(*Mutex).Lock > 5%` on a pool Acquire — tells you the pool is contended, sizing is wrong.
- `sdk-benchmark-devil-go` reports regression concentrated on the pool Get/Put bench.
- Reviewer sees a fresh `sync.Pool` or hand-rolled channel pool in PR diff — redirect to the existing packages.

## GOOD examples

### 1. Sizing `resourcepool` for a network client (MaxSize = expected concurrent in-flight × 1.25)

```go
// Dragonfly client pool: p99 concurrent operations measured at 80 in soak.
// MaxSize = ceil(80 * 1.25) = 100. Headroom absorbs short bursts before
// callers hit ErrPoolExhausted from create() when context is nil.
cfg := resourcepool.PoolConfig[*redisConn]{
    MaxSize: 100,
    OnCreate: func() (*redisConn, error) {
        ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
        defer cancel()
        return dialRedis(ctx, endpoint)
    },
    OnReset: func(c *redisConn) error {
        // Light: flush pipeline buffer, clear auth cache. No network round trip.
        return c.resetPipeline()
    },
    OnDestroy: func(c *redisConn) {
        _ = c.Close()
    },
}
pool, err := resourcepool.NewResourcePool(cfg)
if err != nil {
    return nil, fmt.Errorf("pool init: %w", err)
}

// Caller-side: always use Get(ctx) with a deadline, never TryGet, when latency
// matters more than strict non-blocking. Get with a cancelled ctx returns
// ctx.Err(), NOT ErrPoolExhausted — classify accordingly in error handling.
res, err := pool.Get(ctx)
if err != nil {
    return err
}
defer pool.Put(res)
```

### 2. Sizing `workerpool` for fan-out batch work (MaxWorkers = runtime.NumCPU() × 2, MaxQueueSize bounded)

```go
// Deviating from DefaultConfig because CPU-bound stage benefits from
// NumCPU*2. MaxQueueSize must be finite — unbounded queue hides
// backpressure and grows memory without bound.
cfg := workerpool.PoolConfig{
    MinWorkers:   runtime.NumCPU(),      // warm baseline
    MaxWorkers:   runtime.NumCPU() * 2,  // scale ceiling the auto-scaler respects
    Timeout:      30 * time.Second,      // catches stuck tasks; tune to task p99
    MaxQueueSize: 10000,                 // ants.WithMaxBlockingTasks → ErrQueueFull
}
if err := workerpool.Init(cfg); err != nil {
    return fmt.Errorf("workerpool init: %w", err)
}

// Submit path classifies the failure mode so callers can shed load:
if err := workerpool.Async(task); errors.Is(err, utils.ErrQueueFull) {
    metrics.RecordShedLoad()
    return fmt.Errorf("pool saturated: %w", err)
}
```

### 3. Sizing `memorypool` for slab reuse on a parse hot path (PoolSize ≤ 64, PoolLength = p95 of input size)

```go
// memorypool uses a single int64 bitmask, so PoolSize MUST be ≤ 64.
// PoolLength is set to the p95 payload size measured in soak; that
// minimizes the expansion path (which logs and reallocates).
cfg := &memorypool.PoolConfig{
    PoolSize:   32,    // 32 concurrent parsers — stays well under 64 bitmask limit
    PoolLength: 4096,  // p95 payload size measured from soak; cache-line multiple
    Expandable: true,  // allow tail of distribution without hard failure
    Global:     false, // per-parser instance → no RWMutex contention
}
mgr := memorypool.NewPoolManager(cfg)

// Caller pattern: always defer Release, always check NotAvailable.
idx, buf := mgr.AcquireBytePool(inputLen)
if idx == NotAvailable {
    // Pool saturated — fall back to heap allocation rather than block.
    return parseWithHeap(input)
}
defer mgr.ReleaseBytePool(idx)
_ = buf // use buffer
```

### 4. Healthcheck cadence for `resourcepool` via `GetPoolStats`

```go
// resourcepool exposes PoolStats{Created, Used, Available, MaxSize, IsClosed}.
// Healthcheck polls at 10s cadence — matches auto-scaler's decision horizon
// in workerpool and gives Prometheus enough resolution without hammering the RWMutex.
ticker := time.NewTicker(10 * time.Second)
defer ticker.Stop()
for {
    select {
    case <-ctx.Done():
        return
    case <-ticker.C:
        stats := pool.GetPoolStats()
        utilization := float64(stats.Used) / float64(stats.MaxSize)
        poolUtilGauge.Set(utilization)
        // If utilization > 0.85 sustained, bump MaxSize in next release.
        // If utilization < 0.15 sustained, drop MaxSize — excess memory.
    }
}
```

### 5. Backoff on exhaustion — context deadline, not sleep loops

```go
// ErrPoolExhausted from resourcepool.create means capacity reached AND no
// ctx was passed. Pass a ctx with deadline so Get blocks on the channel
// until a Put happens — that IS the backoff.
func (c *Client) Do(ctx context.Context, req Request) (Response, error) {
    // Bound the blocking wait; if the pool stays empty we fail fast rather
    // than spinning a retry loop that just re-queues at the channel.
    getCtx, cancel := context.WithTimeout(ctx, 500*time.Millisecond)
    defer cancel()
    res, err := c.pool.Get(getCtx)
    if err != nil {
        // ctx.DeadlineExceeded here = pool saturation signal; surface it.
        return Response{}, fmt.Errorf("pool wait: %w", err)
    }
    defer c.pool.Put(res)
    return res.send(ctx, req)
}
```

## BAD examples

### 1. PoolSize > 64 on memorypool (silent data corruption via bitmask overflow)

```go
// BAD: memorypool tracks pool state with `usedPools int64`. PoolSize=128 means
// indices 64+ alias to indices 0+ when the bitmask shift overflows.
cfg := &memorypool.PoolConfig{PoolSize: 128, PoolLength: 4096, Expandable: false}
// → Release(65) clears bit (1<<65 mod 64) = bit 1, releasing the wrong pool.
```

Fix: cap `PoolSize` at 64. If you need more parallelism, spin up multiple `PoolManager` instances per shard.

### 2. Unbounded `MaxQueueSize` on workerpool (memory leak on traffic spike)

```go
// BAD: MaxQueueSize=0 → ants.WithNonblocking(false) without WithMaxBlockingTasks
// → goroutines submit indefinitely, the blocking queue grows unbounded, OOM.
workerpool.Init(workerpool.PoolConfig{
    MinWorkers:   4,
    MaxWorkers:   16,
    MaxQueueSize: 0, // "unlimited" — forbidden in production
})
```

Fix: always set `MaxQueueSize` to a finite number (`10000` is the DefaultConfig). Callers treat `ErrQueueFull` as a shed-load signal.

### 3. Heavy `OnReset` on resourcepool (turns every Put into a network round trip)

```go
// BAD: OnReset does a round trip per release. Put() is on the hot path;
// this doubles every client's observed RTT.
cfg.OnReset = func(c *redisConn) error {
    return c.Ping(context.Background()) // network call on every release!
}
```

Fix: `OnReset` should touch memory only. Validate liveness on Get via a separate healthcheck ticker or fail-on-first-use (`Put` the conn back, let the next Get error trigger `OnDestroy`).

### 4. `TryGet` on the latency-critical path (immediate ErrPoolExhausted under load)

```go
// BAD: TryGet never blocks; under any saturation it returns ErrPoolExhausted
// and the caller degrades to an error response instead of waiting 2ms.
res, err := pool.TryGet()
if err != nil {
    return http.StatusServiceUnavailable // false 503 on a normally healthy pool
}
```

Fix: `TryGet` is for opportunistic fast paths (cache warmup, speculative prefetch). For request-serving paths, use `Get(ctx)` with a bounded deadline.

### 5. Hand-rolling a sync.Pool parallel to resourcepool

```go
// BAD: New package introduces its own sync.Pool for *conn. Now we have
// two leak surfaces, two metric shapes, two lifecycle stories.
var connPool = sync.Pool{New: func() any { return dialNew() }}
```

Fix: use `resourcepool.NewResourcePool[*conn]` — it gives you `OnDestroy` (sync.Pool has no destroy hook), bounded `MaxSize`, `GetPoolStats` for OTel, and `CloseWithTimeout` for graceful shutdown.

## Decision criteria

| Symptom | Dial |
|---|---|
| `sdk-profile-auditor-go` reports lock contention >5% on pool Get | Increase `MaxSize` (resourcepool) or `MaxWorkers` (workerpool); or switch `memorypool.Global: true → false` for per-goroutine slabs |
| `allocs/op` over budget (G104 FAIL) and alloc site is inside a hot path | Add `memorypool.Pool[T]` for the hot buffer; `PoolSize = NumCPU`, `PoolLength = p95 size` |
| `ErrQueueFull` rate > 1% sustained | Raise `MaxQueueSize` AND raise `MaxWorkers` (queue growth without worker growth = deferred OOM) |
| `ErrPoolExhausted` rate > 0% | Raise `MaxSize`; OR shorten `Get(ctx)` deadline so callers fail fast without blocking the channel |
| Pool utilization < 0.15 sustained in Prometheus | Lower `MaxSize` / `MaxWorkers` — each in-flight worker costs goroutine stack + scheduler pressure |
| `TestPoolLeak` fires on shutdown | Caller forgot `defer Release/Put` — grep for `Acquire` without matching `defer` |

## Cross-references

- `go-concurrency-patterns` — semaphore, errgroup, sync.Pool rules (what NOT to substitute for these packages)
- `go-backpressure-flow-control` — classifying `ErrQueueFull` / `ErrPoolExhausted` as shed-load signals
- `goroutine-leak-prevention` — workerpool `CloseWithTimeout` + `waitGroup` lifecycle
- `go-otel-instrumentation` — export `GetPoolStats` / `Stats` via MeterProvider gauges
- `go-client-shutdown-lifecycle` — ordered shutdown: stop accepting → drain workerpool → close resourcepool → release memorypool

## Guardrail hooks

- **G104** (alloc budget) — `allocs_per_op` in perf-budget.md; overruns often point to a missing memorypool reuse.
- **G109** (profile-no-surprise) — unexpected `sync.(*Mutex).Lock` in top-10 CPU = pool sized wrong.
- **G107** (complexity sweep) — scaling sweep at N ∈ {10, 100, 1k, 10k}; sub-linear growth requires that pool Get/Put is O(1), which depends on sizing not forcing creation on every call.
- **G105/G106** (soak/drift) — 30+ min soak required; pool utilization trend shows up here before it shows up in short benches.
