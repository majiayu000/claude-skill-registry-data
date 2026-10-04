---
name: go-concurrency
description: "Golang concurrency patterns. Use when writing or reviewing concurrent Go code involving goroutines, channels, select, locks, sync primitives, errgroup, singleflight, worker pools, or fan-out/fan-in pipelines."
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Wed, 06 May 2026 04:10:00 GMT
---

## Core Principles

1. **Every goroutine must have a clear exit** — without a shutdown mechanism (context, done channel, WaitGroup), they leak and accumulate.
2. **Share memory by communicating** — channels transfer ownership explicitly; mutexes protect shared state but make ownership implicit.
3. **Send copies, not pointers** on channels — sending pointers creates invisible shared memory, defeating the purpose of channels.
4. **Only the sender closes a channel** — closing from the receiver side panics if the sender writes after close.
5. **Specify channel direction** (`chan<-`, `<-chan`) — the compiler prevents misuse at build time.
6. **Default to unbuffered channels** — larger buffers mask backpressure; use them only with measured justification.
7. **Always include `ctx.Done()` in select** — without it, goroutines leak after caller cancellation.
8. **Never use `time.After` in loops** — each call creates a timer that lives until it fires. Use `time.NewTimer` + `Reset`.

## Channel vs Mutex vs Atomic

| Scenario | Use | Why |
| --- | --- | --- |
| Passing data between goroutines | Channel | Communicates ownership transfer |
| Coordinating goroutine lifecycle | Channel + context | Clean shutdown with select |
| Protecting shared struct fields | `sync.Mutex` / `sync.RWMutex` | Simple critical sections |
| Simple counters, flags | `sync/atomic` | Lock-free, lower overhead |
| Caching expensive computations | `sync.Once` / `singleflight` | Execute once or deduplicate |

## WaitGroup vs errgroup

| Need | Use | Why |
| --- | --- | --- |
| Wait for goroutines, errors not needed | `sync.WaitGroup` | Fire-and-forget |
| Wait + collect first error | `errgroup.Group` | Error propagation |
| Wait + cancel siblings on first error | `errgroup.WithContext` | Context cancellation on error |
| Wait + limit concurrency | `errgroup.SetLimit(n)` | Built-in worker pool |

## Examples

### Context-aware Goroutine
```go
func worker(ctx context.Context, jobs <-chan int) {
    for {
        select {
        case <-ctx.Done():
            return
        case job, ok := <-jobs:
            if !ok {
                return
            }
            process(job)
        }
    }
}
```

### Using errgroup for parallel tasks
```go
g, ctx := errgroup.WithContext(ctx)
g.SetLimit(10) // Limit concurrency

for _, item := range items {
    item := item // Create local copy
    g.Go(func() error {
        return process(ctx, item)
    })
}

if err := g.Wait(); err != nil {
    return err
}
```

## Anti-patterns

- ❌ **Fire-and-forget goroutines** without any way to stop them.
- ❌ **Closing a channel from the receiver side**.
- ❌ **Using `time.After` inside a loop**.
- ❌ **Starting a goroutine without adding to a WaitGroup first** (race condition).
- ❌ **Holding a mutex across a blocking I/O operation**.
