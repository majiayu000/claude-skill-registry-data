---
name: go-concurrency
description: Go concurrency patterns - goroutines, channels, sync primitives
sasmp_version: "1.3.0"
bonded_agent: 02-go-concurrency
bond_type: PRIMARY_BOND
---

# Go Concurrency Skill

Master Go concurrency patterns for safe, efficient parallel programming.

## Overview

Production-ready concurrency patterns including goroutines, channels, sync primitives, and common pitfalls to avoid.

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| pattern | string | yes | - | Pattern: "worker-pool", "fan-out", "pipeline", "semaphore" |
| workers | int | no | runtime.NumCPU() | Number of concurrent workers |
| buffer_size | int | no | 0 | Channel buffer size |

## Core Topics

### Goroutines with Context
```go
func ProcessItems(ctx context.Context, items []Item) error {
    g, ctx := errgroup.WithContext(ctx)

    for _, item := range items {
        item := item // capture loop variable
        g.Go(func() error {
            select {
            case <-ctx.Done():
                return ctx.Err()
            default:
                return process(item)
            }
        })
    }

    return g.Wait()
}
```

### Worker Pool
```go
func WorkerPool[T, R any](ctx context.Context, workers int, jobs <-chan T, fn func(T) R) <-chan R {
    results := make(chan R, workers)

    var wg sync.WaitGroup
    for i := 0; i < workers; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for {
                select {
                case <-ctx.Done():
                    return
                case job, ok := <-jobs:
                    if !ok {
                        return
                    }
                    results <- fn(job)
                }
            }
        }()
    }

    go func() {
        wg.Wait()
        close(results)
    }()

    return results
}
```

### Rate Limiter
```go
type RateLimiter struct {
    tokens chan struct{}
}

func NewRateLimiter(rate int, interval time.Duration) *RateLimiter {
    rl := &RateLimiter{
        tokens: make(chan struct{}, rate),
    }

    go func() {
        ticker := time.NewTicker(interval / time.Duration(rate))
        defer ticker.Stop()
        for range ticker.C {
            select {
            case rl.tokens <- struct{}{}:
            default:
            }
        }
    }()

    return rl
}

func (rl *RateLimiter) Wait(ctx context.Context) error {
    select {
    case <-ctx.Done():
        return ctx.Err()
    case <-rl.tokens:
        return nil
    }
}
```

### Mutex Patterns
```go
type SafeCounter struct {
    mu    sync.RWMutex
    count map[string]int
}

func (c *SafeCounter) Inc(key string) {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.count[key]++
}

func (c *SafeCounter) Get(key string) int {
    c.mu.RLock()
    defer c.mu.RUnlock()
    return c.count[key]
}
```

## Retry Logic

```go
func RetryWithBackoff(ctx context.Context, fn func() error) error {
    backoff := []time.Duration{
        100 * time.Millisecond,
        500 * time.Millisecond,
        2 * time.Second,
        5 * time.Second,
    }

    var lastErr error
    for i, delay := range backoff {
        if err := fn(); err != nil {
            lastErr = err
            select {
            case <-ctx.Done():
                return ctx.Err()
            case <-time.After(delay):
                continue
            }
        }
        return nil
    }
    return fmt.Errorf("max retries exceeded: %w", lastErr)
}
```

## Unit Test Template

```go
func TestWorkerPool(t *testing.T) {
    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()

    jobs := make(chan int, 10)
    for i := 0; i < 10; i++ {
        jobs <- i
    }
    close(jobs)

    results := WorkerPool(ctx, 3, jobs, func(n int) int {
        return n * 2
    })

    var sum int
    for r := range results {
        sum += r
    }

    expected := 90 // sum of 0*2 + 1*2 + ... + 9*2
    if sum != expected {
        t.Errorf("got %d, want %d", sum, expected)
    }
}
```

## Troubleshooting

### Failure Modes
| Symptom | Cause | Fix |
|---------|-------|-----|
| `deadlock!` | Blocked channel | Add buffer or close properly |
| `DATA RACE` | Shared state | Use mutex or channel |
| Goroutine leak | Missing close/cancel | Always use context |
| `send on closed` | Multiple closers | Single owner pattern |

### Debug Commands
```bash
go test -race -v ./...
go build -race -o app ./cmd/api
GODEBUG=gctrace=1 ./app  # GC tracing
```

## Usage

```
Skill("go-concurrency")
```
