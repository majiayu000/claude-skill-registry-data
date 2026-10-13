---
name: go-concurrency-patterns
description: >
  Use this when writing goroutine-spawning Go code, designing worker pools,
  wiring graceful shutdown, choosing between channels and mutexes, or reviewing
  concurrent code for races. Covers errgroup, channels, context cancellation,
  worker pools, sync.Pool, and the race detector.
  Triggers: goroutine, errgroup, channel, context cancellation, worker pool, sync.Pool, race detection.
---



# Go Concurrency Patterns

Standardizes concurrency design across all microservices. Every
service uses consistent patterns for worker pools, NATS consumer topology,
graceful shutdown, and safe concurrent data access.

## When to Activate

- When designing worker pools for background processing
- When implementing NATS JetStream consumer goroutine topology
- When designing graceful shutdown sequences
- When choosing between channels and mutexes for synchronization
- When optimizing high-allocation hot paths with sync.Pool
- When writing or reviewing tests for concurrent code

Used by: concurrency-designer, sdk-designer.

## Worker Pool with errgroup

Use `golang.org/x/sync/errgroup` for structured concurrency with error
propagation and automatic context cancellation on first failure.

```go
// pkg/worker/pool.go
package worker

import (
    "context"

    "golang.org/x/sync/errgroup"
    "go.uber.org/zap"
)

// Job represents a unit of work processed by the pool.
type Job struct {
    TenantID string
    Payload  []byte
}

// RunPool processes jobs with bounded concurrency. Returns the first error
// encountered; all workers are cancelled when one fails.
func RunPool(
    ctx context.Context,
    jobs <-chan Job,
    concurrency int,
    handler func(ctx context.Context, job Job) error,
    logger *zap.Logger,
) error {
    g, ctx := errgroup.WithContext(ctx)
    g.SetLimit(concurrency)

    for job := range jobs {
        j := job // capture for closure (Go <1.26 safety)
        g.Go(func() error {
            if err := handler(ctx, j); err != nil {
                logger.Error("job failed",
                    zap.String("tenant_id", j.TenantID),
                    zap.Error(err),
                )
                return err
            }
            return nil
        })
    }
    return g.Wait()
}
```

## Channel-Based Fan-Out/Fan-In

Distribute work across N goroutines (fan-out), then collect results into
a single channel (fan-in).

```go
// pkg/pipeline/fanout.go
package pipeline

import (
    "context"
    "sync"
)

// Result wraps a pipeline stage output.
type Result[T any] struct {
    Value T
    Err   error
}

// FanOut distributes items across workers and merges results.
func FanOut[In, Out any](
    ctx context.Context,
    items []In,
    concurrency int,
    process func(ctx context.Context, item In) (Out, error),
) []Result[Out] {
    in := make(chan In, len(items))
    out := make(chan Result[Out], len(items))

    // Fan-out: N workers read from shared input channel.
    var wg sync.WaitGroup
    for range concurrency {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for item := range in {
                if ctx.Err() != nil {
                    return
                }
                val, err := process(ctx, item)
                out <- Result[Out]{Value: val, Err: err}
            }
        }()
    }

    // Feed input channel.
    for _, item := range items {
        in <- item
    }
    close(in)

    // Fan-in: close output channel when all workers finish.
    go func() {
        wg.Wait()
        close(out)
    }()

    results := make([]Result[Out], 0, len(items))
    for r := range out {
        results = append(results, r)
    }
    return results
}
```

## Graceful Shutdown with signal.NotifyContext

Every service follows this shutdown order:
signal -> context cancel -> drain NATS -> drain workers -> close DB pool.

```go
// cmd/server/main.go
func main() {
    logger, _ := zap.NewProduction()
    defer logger.Sync()

    // Phase 1: Trap OS signals, derive cancellable context.
    ctx, stop := signal.NotifyContext(
        context.Background(), syscall.SIGINT, syscall.SIGTERM,
    )
    defer stop()

    // Phase 2: Initialize resources.
    nc, _ := nats.Connect(nats.DefaultURL)
    js, _ := nc.JetStream()
    pool, _ := pgxpool.New(ctx, connString)

    // Phase 2a: Auto-create per-service JetStream stream.
    js.AddStream(&nats.StreamConfig{
        Name:     "MY-SERVICE",
        Subjects: []string{"tenant.*.my-service.>", "my-service._reply.>"},
    })

    // Phase 3: Start consumers with JetStream queue group subscriptions (pass ctx).
    // ALL subscriptions MUST use js.QueueSubscribe -- bare nc.Subscribe() is FORBIDDEN — use nc.QueueSubscribe() for requests or js.QueueSubscribe() for events.
    sub, _ := js.QueueSubscribe("tenant.*.my-service.>", "my-service",
        handler, nats.Durable("my-service-worker"), nats.ManualAck(),
    )
    workerCancel := startWorkers(ctx, pool, logger)

    // Phase 4: Block until signal.
    <-ctx.Done()
    logger.Info("shutdown signal received")

    // Phase 5: Drain JetStream subscriptions in reverse-dependency order.
    shutdownCtx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer cancel()

    _ = sub.Drain()          // Drain JetStream subscriptions (stops new messages)
    workerCancel()           // Cancel in-flight jobs
    _ = shutdownCtx          // Available for timed drain steps
    nc.Close()               // Close NATS connection
    pool.Close()             // Close database pool
    logger.Info("shutdown complete")
}
```

## NATS JetStream Consumer Goroutine Management

JetStream queue group subscribers are the ONLY consumer pattern. Core NATS
`nc.Subscribe() without queue group is FORBIDDEN — use nc.QueueSubscribe() for request handlers or js.QueueSubscribe() for event subscribers. All subscribers MUST use `js.QueueSubscribe`
with a queue group matching the service name.

### Push Consumer with Queue Group (Primary Pattern)

```go
// internal/adapters/nats/consumer.go
package nats

import (
    "context"
    "time"

    "github.com/nats-io/nats.go"
    "go.uber.org/zap"
)

type ConsumerConfig struct {
    Subject    string
    QueueGroup string // MUST be set -- bare Subscribe is FORBIDDEN
    Durable    string
    AckWait    time.Duration
    MaxDeliver int
}

// RunConsumer creates a JetStream queue group subscription.
// ALL subscriptions MUST use QueueSubscribe with a queue group.
func RunConsumer(
    ctx context.Context,
    js nats.JetStreamContext,
    cfg ConsumerConfig,
    handler func(ctx context.Context, msg *nats.Msg) error,
    logger *zap.Logger,
) (*nats.Subscription, error) {
    sub, err := js.QueueSubscribe(cfg.Subject, cfg.QueueGroup,
        func(msg *nats.Msg) {
            if err := handler(ctx, msg); err != nil {
                logger.Error("handle failed", zap.Error(err))
                _ = msg.Nak()
                return
            }
            _ = msg.Ack()
        },
        nats.Durable(cfg.Durable),
        nats.ManualAck(),
        nats.AckWait(cfg.AckWait),
        nats.MaxDeliver(cfg.MaxDeliver),
    )
    if err != nil {
        return nil, fmt.Errorf("queue subscribe %s (group: %s): %w", cfg.Subject, cfg.QueueGroup, err)
    }
    return sub, nil
}
```

### Pull Consumer with Fetch (Batch Processing Only)

Use pull consumers only when backpressure control is needed (analytics,
reporting). Still requires JetStream -- core NATS is never used.

```go
type PullConsumerConfig struct {
    Subject     string
    Durable     string
    FetchBatch  int
    AckWait     time.Duration
    MaxDeliver  int
    Concurrency int
}

// RunPullConsumer launches fetch goroutines managed by errgroup.
// Returns when ctx is cancelled; all goroutines are guaranteed stopped.
func RunPullConsumer(
    ctx context.Context,
    js nats.JetStreamContext,
    cfg PullConsumerConfig,
    handler func(ctx context.Context, msg *nats.Msg) error,
    logger *zap.Logger,
) error {
    sub, err := js.PullSubscribe(cfg.Subject, cfg.Durable,
        nats.AckWait(cfg.AckWait),
        nats.MaxDeliver(cfg.MaxDeliver),
    )
    if err != nil {
        return fmt.Errorf("pull subscribe %s: %w", cfg.Subject, err)
    }

    g, ctx := errgroup.WithContext(ctx)
    for i := range cfg.Concurrency {
        workerID := i
        g.Go(func() error {
            for {
                if ctx.Err() != nil {
                    return nil
                }
                msgs, err := sub.Fetch(cfg.FetchBatch, nats.MaxWait(5*time.Second))
                if err != nil {
                    continue // timeout or temporary error
                }
                for _, msg := range msgs {
                    if hErr := handler(ctx, msg); hErr != nil {
                        logger.Error("handle failed",
                            zap.Int("worker", workerID), zap.Error(hErr))
                        _ = msg.Nak()
                        continue
                    }
                    _ = msg.Ack()
                }
            }
        })
    }
    return g.Wait()
}
```

## Race Condition Prevention: Mutex vs Channel

| Scenario | Use | Rationale |
|----------|-----|-----------|
| Passing data between goroutines | Channel | Transfers ownership of values |
| N producers, 1 consumer queue | Buffered channel | Natural producer-consumer queue |
| Protecting shared state (counter, map) | `sync.Mutex` | Simpler than channel for guarding |
| Read-heavy, write-rare state | `sync.RWMutex` | Allows concurrent readers |
| One-time initialization | `sync.Once` | Cheaper and clearer than mutex+bool |
| Broadcast shutdown notification | `context.Context` | Propagates to entire call tree |
| Counting active goroutines | `sync.WaitGroup` | Purpose-built for fork-join |

**Rule of thumb**: Use channels to transfer data; use mutexes to protect data.

## sync.Pool for High-Allocation Paths

Use `sync.Pool` to reuse frequently allocated objects on hot paths such
as JSON encoding buffers or protobuf marshalers.

```go
// pkg/encoding/pool.go
package encoding

import (
    "bytes"
    "sync"
)

var bufPool = sync.Pool{
    New: func() any {
        return bytes.NewBuffer(make([]byte, 0, 4096))
    },
}

// GetBuffer returns a pooled buffer. Caller MUST call PutBuffer when done.
func GetBuffer() *bytes.Buffer {
    return bufPool.Get().(*bytes.Buffer)
}

// PutBuffer resets and returns the buffer to the pool.
func PutBuffer(buf *bytes.Buffer) {
    buf.Reset()
    bufPool.Put(buf)
}
```

**Rules for sync.Pool**:
- Never store pointers to pool-returned objects long-term.
- Always reset objects before returning to pool.
- Only use on profiler-identified hot paths, not speculatively.

## Goroutine Leak Prevention

| Rule | Why |
|------|-----|
| Always cancel derived contexts | Uncancelled contexts keep goroutines alive |
| Always close producer channels | Consumer goroutines block on `range` forever |
| Use `errgroup` or `WaitGroup` | Track every goroutine for clean shutdown |
| Set timeouts on all blocking ops | Prevents indefinite goroutine suspension |
| Check `ctx.Done()` in loops | Allows goroutines to exit on cancellation |

```go
// GOOD: Context cancellation prevents leak.
func fetchAll(ctx context.Context, urls []string) []string {
    ctx, cancel := context.WithTimeout(ctx, 10*time.Second)
    defer cancel() // ensures child goroutines can detect cancellation

    results := make(chan string, len(urls))
    var wg sync.WaitGroup
    for _, url := range urls {
        wg.Add(1)
        go func(u string) {
            defer wg.Done()
            // Respects context cancellation
            req, _ := http.NewRequestWithContext(ctx, "GET", u, nil)
            resp, err := http.DefaultClient.Do(req)
            if err != nil {
                return
            }
            defer resp.Body.Close()
            results <- u
        }(url)
    }
    go func() { wg.Wait(); close(results) }()

    var out []string
    for r := range results {
        out = append(out, r)
    }
    return out
}
```

## Bounded Concurrency with Semaphore Pattern

Use a buffered channel as a counting semaphore to limit concurrent
operations without a full worker pool.

```go
// pkg/concurrency/semaphore.go
package concurrency

import "context"

// Semaphore limits concurrent operations to N.
type Semaphore struct {
    ch chan struct{}
}

// NewSemaphore creates a semaphore with the given capacity.
func NewSemaphore(n int) *Semaphore {
    return &Semaphore{ch: make(chan struct{}, n)}
}

// Acquire blocks until a slot is available or ctx is cancelled.
func (s *Semaphore) Acquire(ctx context.Context) error {
    select {
    case s.ch <- struct{}{}:
        return nil
    case <-ctx.Done():
        return ctx.Err()
    }
}

// Release frees a semaphore slot.
func (s *Semaphore) Release() {
    <-s.ch
}
```

Usage in a handler:

```go
var sem = concurrency.NewSemaphore(10) // max 10 concurrent DB queries

func (h *Handler) BulkProcess(ctx context.Context, items []Item) error {
    g, ctx := errgroup.WithContext(ctx)
    for _, item := range items {
        it := item
        g.Go(func() error {
            if err := sem.Acquire(ctx); err != nil {
                return err
            }
            defer sem.Release()
            return h.processOne(ctx, it)
        })
    }
    return g.Wait()
}
```

## NATS JetStream Consumer Patterns

NATS JetStream is the sole inter-service communication mechanism. These
consumer patterns are essential for all domain services.

### Push vs Pull Consumers

| Pattern | When to Use | Example |
|---------|-------------|---------|
| Push (QueueSubscribe) | Low-latency event processing, auto-delivery | Domain event handlers |
| Pull (PullSubscribe + Fetch) | Batch processing, backpressure control | Analytics, reporting |

### Queue Groups for Load Balancing (MANDATORY)

All service replicas MUST use JetStream queue groups to ensure only one
replica processes each message. Without queue groups, every replica
receives every message. Core NATS `nc.Subscribe`/`nc.QueueSubscribe` is
FORBIDDEN -- always use `js.QueueSubscribe`.

```go
// GOOD: JetStream queue group ensures one replica processes each message
sub, err := js.QueueSubscribe(
    "tenant.*.order-service.order.>",
    "order-service",          // queue group = service name
    handler,
    nats.Durable("order-service-main"),
    nats.ManualAck(),
    nats.AckWait(30*time.Second),
    nats.MaxDeliver(5),
)
```

### Consumer Ack Strategies

| Strategy | When to Use | Risk |
|----------|-------------|------|
| `AckExplicit` + `ManualAck()` | Default for all consumers | None (safest) |
| `AckAll` | Ordered batch processing only | Data loss if crash mid-batch |
| `AckNone` | Never use in production | Message loss guaranteed |

Always use `AckExplicit` with `ManualAck()`. Call `msg.Ack()` only after
successful processing, `msg.Nak()` for retriable failures, and `msg.Term()`
for permanent failures (send to DLQ).

## Testing Concurrent Code

- **Race detector**: Always run `go test -race -count=1 ./...` in CI
- **Parallel tests**: Use `t.Parallel()` for concurrent test execution
- **Goroutine leak detection**: Use `go.uber.org/goleak` in `TestMain`
- **Timeout contexts**: Wrap test bodies in `context.WithTimeout` (5s default)

## Examples

### GOOD: errgroup with Bounded Concurrency

```go
g, ctx := errgroup.WithContext(ctx)
g.SetLimit(5) // max 5 concurrent goroutines
for _, tenant := range tenants {
    t := tenant
    g.Go(func() error {
        return syncTenant(ctx, t)
    })
}
if err := g.Wait(); err != nil {
    logger.Error("sync failed", zap.Error(err))
}
```

### BAD: Unbounded Goroutine Spawn

```go
// BAD: Spawns N goroutines with no limit, no WaitGroup, no error handling.
for _, tenant := range tenants {
    go syncTenant(context.Background(), tenant)
}
```

### GOOD: Proper Channel Lifecycle

```go
out := make(chan Result, len(items))
var wg sync.WaitGroup
for _, item := range items {
    wg.Add(1)
    go func(it Item) {
        defer wg.Done()
        out <- process(it)
    }(item)
}
go func() { wg.Wait(); close(out) }() // producer closes channel
for r := range out { collect(r) }
```

### BAD: Consumer Closes Channel

```go
// BAD: Consumer closes channel; producer panics on next send.
go func() { close(out) }()
```

## Common Mistakes

1. **Spawning unbounded goroutines** -- Launching `go func()` in a loop
   without a semaphore or `errgroup.SetLimit` can exhaust memory. Always
   bound concurrency to a known limit.

2. **Forgetting `defer cancel()` on derived contexts** -- Every
   `context.WithCancel`, `WithTimeout`, or `WithDeadline` must have a
   matching `defer cancel()` to release resources and signal child
   goroutines.

3. **Using `context.Background()` inside request handlers** -- This
   discards the caller's deadline and cancellation. Always derive from
   the incoming `ctx`.

4. **Sharing `*sql.Tx` across goroutines** -- Database transactions are
   not goroutine-safe. Each goroutine must acquire its own connection
   from the pool.

5. **Reading/writing maps concurrently without protection** -- Go maps
   are not safe for concurrent access. Use `sync.RWMutex` or `sync.Map`.

6. **Draining NATS after closing the connection** -- Always call
   `sub.Drain()` on JetStream subscriptions before `nc.Close()`.
   Reversing the order drops in-flight messages silently.

7. **Using core NATS subscribe instead of JetStream** -- Core NATS
   `nc.Subscribe` and `nc.QueueSubscribe` are FORBIDDEN. All
   subscriptions must use JetStream `js.QueueSubscribe` with queue
   groups for proper message persistence and load balancing.
