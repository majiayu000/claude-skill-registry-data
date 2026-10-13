---
name: go-backpressure-flow-control
description: >
  Use this when designing an SDK component that admits work (publish, submit,
  send, fan-out) faster than its downstream can drain — picking between
  bounded-channel block, ErrQueueFull fail-fast, or counted-drop policy.
  Covers semaphores, bounded worker queues, JetStream MaxAckPending, and
  size heuristics.
  Triggers: backpressure, bounded channel, semaphore, ErrQueueFull, MaxQueueSize, drop, block, flow control, ants, x/sync/semaphore.
---

# go-backpressure-flow-control (v1.0.0)

## Rationale

Unbounded queues look like a correctness fix ("we never lose work") but are a latency and memory bomb: the queue grows until the process OOMs or tail latency explodes past any SLO. Every SDK component that admits work (publisher, worker pool, consumer) MUST expose a bounded admission path + an explicit policy for what happens when the bound is reached — **block the producer**, **return an `ErrQueueFull` sentinel**, or **drop with metric**. No silent buffering. The target SDK already encodes this: `core/pool/workerpool` uses `ants.WithMaxBlockingTasks` to bound the wait queue and converts overflow to `utils.ErrQueueFull`; `events/jetstream` relies on JetStream's `MaxDeliver` + AckWait to apply server-side flow control. The decision is always *which* of the three policies fits — not whether to bound.

## Activation signals

- Designing a publish / submit / send API that could be called faster than its backend drains
- Adding a worker pool or fan-out stage
- Integration tests show memory growing under load
- TPRD §5 mentions `MaxQueueSize`, `MaxInflight`, `MaxConcurrent`, or `ErrQueueFull`
- Benchmarks show p99 latency diverging from p50 under sustained load (queue buildup)
- Reviewer cites "unbounded channel" or "no backpressure"

## GOOD examples

### GOOD 1: Bounded queue with ErrQueueFull on overflow (target SDK workerpool)

Source: `motadatagosdk/core/pool/workerpool/pool.go`. The pool wraps `ants` with `WithMaxBlockingTasks(MaxQueueSize)` and `WithNonblocking(false)` — this bounds the number of submitters that may block waiting for a worker. Overflow returns `ants.ErrPoolOverload`, converted to the SDK's `utils.ErrQueueFull` sentinel so callers can distinguish "backend is saturated" from "backend is broken".

```go
antsOptions := []ants.Option{
    ants.WithExpiryDuration(time.Minute),
    ants.WithPreAlloc(true),
    ants.WithNonblocking(false),               // block, don't drop
}
if config.MaxQueueSize > 0 {                   // bound the blocking set
    antsOptions = append(antsOptions, ants.WithMaxBlockingTasks(config.MaxQueueSize))
}
// ...
err := workerPool.antsPool.Submit(func() { /* task */ })
if errors.Is(err, ants.ErrPoolOverload) {
    return utils.ErrQueueFull                  // caller decides: retry, shed, fail
}
```

### GOOD 2: Counting semaphore for bounded concurrency (context-aware)

Source: `skills/go-concurrency-patterns/SKILL.md` cross-reference, canonical pattern. Uses a buffered channel of size `N` as a counting semaphore. Acquire blocks until a slot is free OR the context cancels — the caller's deadline governs wait time. Release is non-blocking.

```go
type Semaphore struct{ ch chan struct{} }

func NewSemaphore(n int) *Semaphore { return &Semaphore{ch: make(chan struct{}, n)} }

func (s *Semaphore) Acquire(ctx context.Context) error {
    select {
    case s.ch <- struct{}{}: return nil
    case <-ctx.Done():       return ctx.Err() // deadline-exceeded bubbles up
    }
}
func (s *Semaphore) Release() { <-s.ch }

// Usage — the caller's ctx decides how long to wait for a slot:
if err := sem.Acquire(ctx); err != nil { return err }
defer sem.Release()
```

For a richer API (weighted acquire, `TryAcquire`), use `golang.org/x/sync/semaphore.Weighted` — same shape, just bytes-count instead of slot-count.

### GOOD 3: Drop-oldest policy with metric (telemetry-safe ring buffer)

When dropping is the correct policy (telemetry, metrics sampling), the drop MUST be observable. A channel `select` with a `default` case performs a non-blocking send; failed sends increment a counter.

```go
type SamplingBuffer struct {
    ch     chan Event
    drops  atomic.Uint64
}

func (b *SamplingBuffer) Offer(e Event) {
    select {
    case b.ch <- e:
        // admitted
    default:
        b.drops.Add(1) // drop + count; never block the producer
    }
}
```

Rule: dropping without a metric is a bug. Ops must be able to answer "how many events did we shed?".

### GOOD 4: Server-side flow control via JetStream ack semantics

Source: `motadatagosdk/events/jetstream/` uses `nats.AckWait` + `nats.MaxDeliver` + `nats.ManualAck`. Unacked messages are redelivered after `AckWait`; `MaxDeliver` caps redelivery. This IS backpressure — a slow consumer can't be flooded beyond its parallelism because unacked messages queue at the stream, not the process.

```go
sub, _ := js.QueueSubscribe(subject, queueGroup, handler,
    nats.ManualAck(),
    nats.AckWait(30*time.Second),      // unacked → requeue after 30s
    nats.MaxDeliver(5),                 // cap redeliveries
    nats.MaxAckPending(100),            // max in-flight per consumer
)
```

## BAD examples (anti-patterns)

### BAD 1: Unbounded channel

```go
// BAD: make(chan T) with no size → writer blocks; make(chan T, 1e6) →
// pretends to be bounded but is really "RAM-bounded". Either way, the
// admission rate is governed by luck, not policy.
ch := make(chan Job) // or make(chan Job, 1_000_000)
go func() { for j := range ch { process(j) } }()
for _, j := range jobs { ch <- j } // producer blocks or RAM dies
```
Breaks: no producer feedback, no ErrQueueFull sentinel, no observability. Fix: `workerpool.Submit` with `MaxQueueSize`.

### BAD 2: Time-based drop without count

```go
// BAD: silent drop. Ops sees latency spikes with no signal why.
select {
case ch <- item:
case <-time.After(10 * time.Millisecond):
    // dropped — but no counter, no log, no metric
}
```
Breaks: silent data loss. Fix: at minimum, increment a `dropped_total` counter with a reason label.

### BAD 3: Sleep-based "rate limit"

```go
// BAD: sleeps 100ms between sends. Not backpressure — just slow.
// Fails to admit bursts that downstream could handle; fails to back
// off when downstream is actually saturated.
for _, msg := range msgs {
    send(msg)
    time.Sleep(100 * time.Millisecond)
}
```
Breaks: wrong policy. Use a token bucket (`golang.org/x/time/rate.Limiter`) OR let the downstream signal (`ErrQueueFull`, circuit breaker) drive the pacing.

### BAD 4: Unbounded goroutine spawn

```go
// BAD: one goroutine per item, no limit. Exhausts schedulers, RAM,
// and any downstream resource. Also a goroutine-leak-prevention
// violation if the inner op blocks.
for _, item := range items { go process(item) }
```
Breaks: no concurrency ceiling. Fix: `errgroup.WithContext` + `g.SetLimit(N)` OR a semaphore.

## Decision criteria — drop vs. block vs. fail

| Work type | Policy | Rationale |
|---|---|---|
| User-facing request (API call, query) | **Fail** with `ErrQueueFull` | Caller has a deadline; failing fast lets them retry or shed |
| Durable event (message with message-id, JetStream publish) | **Block** on bounded queue | Correctness > latency; the caller chose this path |
| Telemetry / metrics / sampling | **Drop** with counter | Loss is acceptable; blocking hot paths is not |
| Batch job with no deadline | **Block** unbounded only if producer is trusted & rate-limited | Otherwise bound + fail |
| Fan-out over N items with bounded concurrency | Use **semaphore** + errgroup | Caller's ctx governs wait |

**Size heuristics**:
- Queue size should be ≥ 2× (expected latency × expected throughput) to smooth bursts, but small enough that a full queue's memory cost stays under the process budget.
- Concurrency limit (`SetLimit`, semaphore `n`): baseline `runtime.NumCPU()` for CPU-bound; `runtime.NumCPU() * 4` for I/O-bound; measure, don't guess.
- JetStream `MaxAckPending`: start at 100; raise only if consumer is provably idle.

**Never** solve backpressure by adding a bigger buffer. A bigger buffer just moves the failure mode from latency to memory.

## Target SDK Convention

Current convention in motadatagosdk:
- `core/pool/workerpool`: `MaxQueueSize` config field + `utils.ErrQueueFull` sentinel; `WithNonblocking(false)` = block-with-cap policy
- `events/jetstream`: server-side flow via `MaxAckPending` / `AckWait` / `MaxDeliver`
- `core/l2cache/dragonfly`: `PoolSize` + `PoolTimeout` on `redis.Options` (dial-time backpressure); `ErrPoolExhausted` sentinel when callers exceed pool capacity for longer than `PoolTimeout`
- No SDK-internal rate limiters — callers compose `x/time/rate` if they need pacing

If TPRD requests divergence (e.g., a ring buffer with drop-newest): declare in TPRD §5; `sdk-design-lead` records rationale; the drop MUST carry a counter.

## Cross-references

- `go-concurrency-patterns` — canonical semaphore + errgroup patterns
- `go-circuit-breaker-policy` — complementary: breaker trips on *failure*, backpressure trips on *saturation*; both produce fail-fast sentinels
- `go-context-deadline-patterns` — every `Acquire` MUST take `ctx` so the caller's deadline caps the wait
- `goroutine-leak-prevention` — bounded concurrency prevents per-item goroutine leaks
- `go-client-rate-limiting` — token-bucket pacing lives there; backpressure here is *admission*, rate-limit there is *pacing*

## Guardrail hooks

- **G63** (goleak) — an unbounded channel with no consumer path leaks the producer goroutine on shutdown; goleak catches it.
- **G65** (bench regression) — p99 / p999 latency under load is the ground truth for backpressure; regression here often means queue depth changed.
- **G104** (alloc budget) — `Offer` / `Submit` happy path MUST be alloc-free.
- **Integration flake-hunter** (`sdk-integration-flake-hunter-go`) — if a test under `-count=3` observes different outcomes at the queue boundary, the policy is race-prone (common symptom: `TryAcquire` without `ctx`).
