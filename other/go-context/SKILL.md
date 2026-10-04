---
name: go-context
description: "Idiomatic context.Context usage in Golang — creation, propagation, cancellation, timeouts, and deadlines."
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Wed, 06 May 2026 04:20:00 GMT
---

## Best Practices

1. **Propagate context** — Pass the same context through the entire call chain (Handler -> Service -> DB).
2. **First parameter** — Context MUST be the first parameter, named `ctx context.Context`.
3. **Never store in structs** — Pass it explicitly through function parameters.
4. **Never pass nil** — Use `context.TODO()` if you're not sure what context to use.
5. **Always call cancel** — When using `WithCancel`, `WithTimeout`, or `WithDeadline`, always defer the `cancel()` function.
6. **Use background at top level only** — `context.Background()` should only be used in `main`, `init`, or tests.
7. **Use `context.WithoutCancel` (Go 1.21+)** — For background work that must outlive the request (e.g., audit logging).
8. **Context values for metadata only** — Use context values for request-scoped data like TraceID, UserID. Never for optional parameters.

## Creating Contexts

| Situation | Use |
| --- | --- |
| Entry point (main, tests) | `context.Background()` |
| HTTP handler | `r.Context()` |
| Timeout/Deadline | `context.WithTimeout(parent, duration)` |
| Manual cancellation | `context.WithCancel(parent)` |
| Detached background work | `context.WithoutCancel(ctx)` |

## Propagation Example

```go
func (s *Service) HandleRequest(ctx context.Context, id string) error {
    // Pass ctx to DB
    user, err := s.db.GetUser(ctx, id)
    if err != nil {
        return err
    }
    
    // Create sub-context with timeout for external API
    apiCtx, cancel := context.WithTimeout(ctx, 2*time.Second)
    defer cancel()
    
    return s.api.Notify(apiCtx, user)
}
```

## Listening for Cancellation

```go
func longRunningTask(ctx context.Context) error {
    for {
        select {
        case <-ctx.Done():
            return ctx.Err() // returns context.Canceled or context.DeadlineExceeded
        default:
            // Do work in small chunks
            doWork()
        }
    }
}
```

## Anti-patterns

- ❌ **Creating `context.Background()` in the middle of a request path**.
- ❌ **Storing context in a global variable or struct field**.
- ❌ **Ignoring `ctx.Done()` in long-running loops or blocking operations**.
- ❌ **Using context values to pass regular function arguments**.
- ❌ **Forgetting to call `cancel()`**, causing a context leak.
