---
name: go-context-cancellation
description: Context cancellation patterns for graceful shutdown
---

# Context Cancellation

## Pattern
Pass `context.Context` as first parameter. Check `ctx.Done()` in goroutines and long operations.

## CORRECT
```go
func ProcessItems(ctx context.Context, items []string) error {
    for _, item := range items {
        select {
        case <-ctx.Done():
            return ctx.Err()
        default:
            if err := processItem(item); err != nil {
                return err
            }
        }
    }
    return nil
}

func main() {
    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()

    if err := ProcessItems(ctx, items); err != nil {
        log.Printf("processing failed: %v", err)
    }
}
```

## WRONG - No context checking
```go
func ProcessItems(items []string) error {
    for _, item := range items {
        // No way to cancel - runs forever if stuck
        if err := processItem(item); err != nil {
            return err
        }
    }
    return nil
}
```

## Rules
1. Context is first parameter: `func Do(ctx context.Context, ...)`
2. Always call `cancel()` via `defer` to prevent leaks
3. Check `ctx.Done()` in loops and before expensive operations
4. Propagate context to downstream calls
5. Use `context.WithTimeout` or `WithDeadline` for time limits

## Common Patterns
```go
// HTTP server with context
func handler(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context() // Request context
    result, err := fetchData(ctx)
    // ...
}

// Worker with cancellation
func worker(ctx context.Context) {
    for {
        select {
        case <-ctx.Done():
            return
        case work := <-workCh:
            process(work)
        }
    }
}
```
