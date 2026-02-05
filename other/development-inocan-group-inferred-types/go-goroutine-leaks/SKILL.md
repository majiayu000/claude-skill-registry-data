---
name: go-goroutine-leaks
description: Prevent goroutine leaks with proper shutdown mechanisms
---

# Goroutine Leak Prevention

## Pattern
Every goroutine must have a way to exit. Use channels or context for shutdown signals.

## CORRECT - Done channel
```go
type Worker struct {
    done chan struct{}
}

func (w *Worker) Start() {
    w.done = make(chan struct{})
    go func() {
        for {
            select {
            case <-w.done:
                return
            case <-time.After(1 * time.Second):
                // do work
            }
        }
    }()
}

func (w *Worker) Stop() {
    close(w.done)
}
```

## CORRECT - Context
```go
func StartWorker(ctx context.Context) {
    go func() {
        ticker := time.NewTicker(1 * time.Second)
        defer ticker.Stop()

        for {
            select {
            case <-ctx.Done():
                return
            case <-ticker.C:
                // do work
            }
        }
    }()
}
```

## WRONG - No exit mechanism
```go
func StartWorker() {
    go func() {
        for {
            // Runs forever - goroutine leak!
            time.Sleep(1 * time.Second)
            // do work
        }
    }()
}
```

## WRONG - Unbuffered channel send can block
```go
func GetData() string {
    ch := make(chan string)
    go func() {
        ch <- fetchData() // Blocks forever if nobody reads
    }()

    // If timeout happens, goroutine leaks
    select {
    case result := <-ch:
        return result
    case <-time.After(1 * time.Second):
        return "timeout"
    }
}
```

## Fix with buffered channel
```go
func GetData() string {
    ch := make(chan string, 1) // Buffer size 1
    go func() {
        ch <- fetchData() // Won't block
    }()

    select {
    case result := <-ch:
        return result
    case <-time.After(1 * time.Second):
        return "timeout"
    }
}
```

## Rules
1. Every `go func()` needs an exit condition
2. Use `select` with `ctx.Done()` or done channel
3. Buffered channels (size 1) for single sends
4. Close channels to signal completion
5. Test with `runtime.NumGoroutine()` to detect leaks

## Detection
```go
func TestNoLeaks(t *testing.T) {
    before := runtime.NumGoroutine()

    worker := NewWorker()
    worker.Start()
    worker.Stop()

    time.Sleep(100 * time.Millisecond) // Allow cleanup
    after := runtime.NumGoroutine()

    if after > before {
        t.Errorf("goroutine leak: before=%d after=%d", before, after)
    }
}
```
