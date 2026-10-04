---
name: go-design-patterns
description: "Idiomatic Golang design patterns — functional options, constructors, resource management, and architecture."
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Wed, 06 May 2026 05:10:00 GMT
---

## Core Principles

1. **Simplicity over Sophistication** — Apply patterns only when they solve a real problem.
2. **Explicit over Implicit** — Avoid `init()` functions and hidden global state.
3. **Fail Fast** — Validate at trust boundaries, trust internal code.
4. **Functional Options** — The preferred way to design constructors for complex types.
5. **Resource Lifecycle** — Every resource must have a clear owner and a guaranteed cleanup path (`defer Close()`).
6. **Graceful Shutdown** — Ensure the process can finish in-flight work before exiting.
7. **Timeout Every External Call** — Never hang indefinitely on an upstream service.

## Functional Options Pattern

Use this for types with many optional configuration parameters.

```go
type Server struct {
    port int
    timeout time.Duration
}

type Option func(*Server)

func WithPort(p int) Option {
    return func(s *Server) { s.port = p }
}

func NewServer(opts ...Option) *Server {
    s := &Server{port: 8080, timeout: 30 * time.Second} // Defaults
    for _, opt := range opts {
        opt(s)
    }
    return s
}
```

## Resource Management

Always `defer` cleanup immediately after a successful resource acquisition.

```go
f, err := os.Open(path)
if err != nil {
    return err
}
defer f.Close()
```

## Enums: Start at 1

Reserve the 0 value for "Unknown" or "Invalid" to catch uninitialized variables.

```go
type Status int

const (
    StatusUnknown Status = iota // 0
    StatusActive                // 1
    StatusInactive              // 2
)
```

## Resilience Patterns

- **Timeouts**: Use `context.WithTimeout`.
- **Retries**: Always check for context cancellation between retries.
- **Circuit Breakers**: Use for unstable external dependencies.
- **Rate Limiting**: Protect your own resources from exhaustion.

## Anti-patterns

- ❌ **`init()` Abuse** — Hard to test, hidden side effects, and can't return errors.
- ❌ **Mutable Globals** — Make testing and concurrency hard. Use dependency injection instead.
- ❌ **Panic for Control Flow** — Panic is for truly unrecoverable bugs, not business errors.
- ❌ **Unbounded Resources** — Missing limits on connections, goroutines, or buffers.
- ❌ **Premature Abstraction** — Don't create interfaces until you have at least two implementations.
