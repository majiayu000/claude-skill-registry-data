---
name: go-concurrency
description: Goroutine patterns for Go - WaitGroup, errgroup, bounded concurrency, fan-out/fan-in, and context cancellation. Use when running work concurrently, limiting how much runs at once, collecting results or errors from parallel operations, or making a long operation cancellable. Triggers on go func, sync.WaitGroup, wg.Go, errgroup, SetLimit, buffered channel semaphores, ctx.Done, and worker pools.
user-invocable: false
---

# Go Concurrency

**Pick the smallest primitive that carries the error semantics you need, and let the standard library handle the bookkeeping.**

## Pattern Selection

| Need | Pattern |
|---|---|
| Run N things, wait for all | `sync.WaitGroup` via `wg.Go` |
| Run N things, stop all on the first error | `errgroup` |
| Limit to M concurrent operations | `errgroup.SetLimit`, or a buffered-channel semaphore |
| Distribute a stream to workers and merge results | fan-out/fan-in |

`errgroup` is the default whenever an operation can fail, with `g.SetLimit(N)` added for bounded concurrency. Drop to a raw `sync.WaitGroup` only when errors are genuinely fire-and-forget, because a WaitGroup gives you no way to learn that half the work failed.

```go
import "golang.org/x/sync/errgroup"

g, ctx := errgroup.WithContext(ctx)
g.SetLimit(10)
for _, item := range items {
    g.Go(func() error {
        return process(ctx, item)
    })
}
return g.Wait() // the first error, or nil
```

Go 1.22 and later scope loop variables per iteration, so the old `item := item` capture before a goroutine is unnecessary on this baseline.

## WaitGroup, Fire and Forget

Errors are logged and dropped. Use it when a failure genuinely should not stop the rest.

```go
func processAll(ctx context.Context, items []Item) {
    var wg sync.WaitGroup
    for _, item := range items {
        wg.Go(func() {
            select {
            case <-ctx.Done():
                return
            default:
            }
            if err := process(item); err != nil {
                log.Error().Err(err).Str("item", item.ID).Msg("error processing item")
            }
        })
    }
    wg.Wait()
}
```

`wg.Go` spawns the goroutine and pairs `Add` with `Done` itself, which removes the failure mode where an early return skips the `Done`.

The logging call is zerolog in every project type, so this loop reads the same wherever it lands.

## errgroup, Stop on First Error

```go
func processAll(ctx context.Context, items []Item) error {
    g, ctx := errgroup.WithContext(ctx)
    for _, item := range items {
        g.Go(func() error {
            return process(ctx, item)
        })
    }
    return g.Wait()
}
```

`errgroup.WithContext` returns a context that is cancelled as soon as any goroutine returns an error, so the rest stop instead of finishing work whose result is already being discarded.

## errgroup with a Limit

```go
g, ctx := errgroup.WithContext(ctx)
g.SetLimit(10)
```

`SetLimit` blocks `g.Go` until a slot frees, which bounds concurrency without a second synchronization primitive to keep in step with the group.

## Buffered-Channel Semaphore

For bounded concurrency when first-error cancellation is not wanted.

```go
func processAll(ctx context.Context, items []Item) {
    sem := make(chan struct{}, 10)
    var wg sync.WaitGroup

    for _, item := range items {
        sem <- struct{}{} // acquire, blocks once 10 are running
        wg.Go(func() {
            defer func() { <-sem }() // release
            process(ctx, item)
        })
    }
    wg.Wait()
}
```

The acquire happens before `wg.Go`, not inside the goroutine. Acquiring inside means every goroutine is spawned immediately and then blocks, which bounds the work but not the goroutine count.

## Collecting Results

```go
func gather(ctx context.Context, items []Item) ([]Result, error) {
    g, ctx := errgroup.WithContext(ctx)
    results := make([]Result, len(items))

    for i, item := range items {
        g.Go(func() error {
            result, err := process(ctx, item)
            if err != nil {
                return err
            }
            results[i] = result
            return nil
        })
    }
    if err := g.Wait(); err != nil {
        return nil, err
    }
    return results, nil
}
```

Writing to a preallocated slice at a unique index needs no mutex, since no two goroutines touch the same element and the slice header itself never changes.

## Fan-Out / Fan-In

For a stream of items through a fixed pool. It is more machinery than `errgroup`, so reach for it only when you specifically need the channel-based pool.

```go
func fanOut(ctx context.Context, items []Item, workers int) []Result {
    jobs := make(chan Item)
    results := make(chan Result)

    var wg sync.WaitGroup
    for range workers {
        wg.Go(func() {
            for item := range jobs {
                select {
                case <-ctx.Done():
                    return
                case results <- process(ctx, item):
                }
            }
        })
    }

    go func() {
        wg.Wait()
        close(results)
    }()

    go func() {
        defer close(jobs)
        for _, item := range items {
            select {
            case <-ctx.Done():
                return
            case jobs <- item:
            }
        }
    }()

    var all []Result
    for result := range results {
        all = append(all, result)
    }
    return all
}
```

Each channel is closed by its own sender: the feeder closes `jobs`, and the goroutine that waits on the workers closes `results`. Closing from the receiving side panics as soon as a sender writes again.

## Context Cancellation

Long-running work checks the context before starting and inside loops, because a cancelled context that nothing reads is a cancellation that never happens.

```go
select {
case <-ctx.Done():
    return ctx.Err()
default:
}

for _, item := range items {
    select {
    case <-ctx.Done():
        return ctx.Err()
    default:
    }
    process(item)
}
```

Any call that accepts a context receives it, rather than `context.Background()` or `context.TODO()`:

```go
req, err := http.NewRequestWithContext(ctx, http.MethodGet, url, nil)
```

When the reason for a cancellation matters downstream, `context.WithCancelCause` carries it and `context.Cause(ctx)` reads it back, which turns a bare "context canceled" into the failure that actually triggered it.

## Common Mistakes

| Mistake | What goes wrong | Instead |
|---|---|---|
| `wg.Add(1)` plus `go func` plus `defer wg.Done()` | the pair drifts apart after an early return | `wg.Go(fn)` |
| Never checking `ctx.Done()` | the operation cannot be cancelled | check before the work and inside loops |
| Closing a channel from the receiver | a later send panics | only the sender closes |
| Acquiring the semaphore inside the goroutine | goroutines are unbounded, only the work is bounded | acquire before `wg.Go`, release with `defer` inside |
