---
name: golang
description: Go patterns, concurrency with goroutines/channels, error handling, interfaces, and production-grade service architecture
layer: domain
category: backend
triggers:
  - "golang"
  - "go lang"
  - "goroutine"
  - "go concurrency"
  - "go interface"
  - "go error handling"
inputs:
  - "Go application requirements"
  - "Concurrency design needs"
  - "Service architecture specifications"
outputs:
  - "Idiomatic Go implementations"
  - "Concurrency patterns"
  - "Production deployment configurations"
linksTo:
  - microservices
  - postgresql
  - redis
  - message-queues
  - graphql
  - websockets
linkedFrom:
  - error-handling
  - logging
  - testing
preferredNextSkills:
  - postgresql
  - redis
  - microservices
fallbackSkills:
  - rust
  - nodejs
riskLevel: low
memoryReadPolicy: selective
memoryWritePolicy: none
sideEffects: []
---

# Go Domain Skill

## Purpose

Provide expert-level guidance on writing idiomatic Go code, including concurrency patterns with goroutines and channels, error handling, interface design, testing, and production-grade service architecture.

## Key Patterns

### 1. Project Structure

```
myservice/
├── cmd/
│   └── server/
│       └── main.go           # Entry point
├── internal/
│   ├── domain/
│   │   ├── user.go           # Domain types
│   │   └── errors.go         # Domain errors
│   ├── service/
│   │   ├── user.go           # Business logic
│   │   └── user_test.go
│   ├── repository/
│   │   ├── postgres/
│   │   │   └── user.go       # Postgres implementation
│   │   └── repository.go     # Interface definitions
│   ├── handler/
│   │   ├── user.go           # HTTP handlers
│   │   └── middleware.go
│   └── config/
│       └── config.go
├── pkg/                       # Reusable packages (if any)
├── migrations/
├── go.mod
├── go.sum
└── Makefile
```

### 2. Interface Design

```go
package repository

import "context"

// Define interfaces where they are USED, not where implemented.
// Keep interfaces small -- prefer 1-3 methods.

type UserReader interface {
    GetUser(ctx context.Context, id string) (*domain.User, error)
    ListUsers(ctx context.Context, opts ListOptions) ([]domain.User, error)
}

type UserWriter interface {
    CreateUser(ctx context.Context, u *domain.User) error
    UpdateUser(ctx context.Context, u *domain.User) error
    DeleteUser(ctx context.Context, id string) error
}

// Compose interfaces when needed
type UserRepository interface {
    UserReader
    UserWriter
}

// Accept interfaces, return structs
type UserService struct {
    repo   UserRepository
    cache  Cache
    logger *slog.Logger
}

func NewUserService(repo UserRepository, cache Cache, logger *slog.Logger) *UserService {
    return &UserService{repo: repo, cache: cache, logger: logger}
}
```

### 3. Error Handling

```go
package domain

import (
    "errors"
    "fmt"
)

// Sentinel errors for expected conditions
var (
    ErrNotFound      = errors.New("not found")
    ErrAlreadyExists = errors.New("already exists")
    ErrUnauthorized  = errors.New("unauthorized")
    ErrForbidden     = errors.New("forbidden")
)

// Structured error type for rich context
type AppError struct {
    Code    string
    Message string
    Err     error
}

func (e *AppError) Error() string {
    if e.Err != nil {
        return fmt.Sprintf("%s: %s: %v", e.Code, e.Message, e.Err)
    }
    return fmt.Sprintf("%s: %s", e.Code, e.Message)
}

func (e *AppError) Unwrap() error {
    return e.Err
}

// Wrap errors with context at each layer
func (s *UserService) GetUser(ctx context.Context, id string) (*User, error) {
    user, err := s.repo.GetUser(ctx, id)
    if err != nil {
        if errors.Is(err, ErrNotFound) {
            return nil, fmt.Errorf("user %s: %w", id, err)
        }
        return nil, fmt.Errorf("getting user %s: %w", id, err)
    }
    return user, nil
}

// In handlers, map to HTTP status codes
func (h *UserHandler) GetUser(w http.ResponseWriter, r *http.Request) {
    user, err := h.service.GetUser(r.Context(), chi.URLParam(r, "id"))
    if err != nil {
        switch {
        case errors.Is(err, domain.ErrNotFound):
            writeError(w, http.StatusNotFound, err.Error())
        case errors.Is(err, domain.ErrForbidden):
            writeError(w, http.StatusForbidden, "access denied")
        default:
            h.logger.Error("unexpected error", "error", err)
            writeError(w, http.StatusInternalServerError, "internal error")
        }
        return
    }
    writeJSON(w, http.StatusOK, user)
}
```

### 4. Concurrency Patterns

```go
// Worker pool pattern
func processItems(ctx context.Context, items []Item, workers int) ([]Result, error) {
    var (
        wg      sync.WaitGroup
        mu      sync.Mutex
        results = make([]Result, 0, len(items))
        errs    []error
        sem     = make(chan struct{}, workers)
    )

    for _, item := range items {
        wg.Add(1)
        sem <- struct{}{} // Acquire semaphore

        go func(item Item) {
            defer wg.Done()
            defer func() { <-sem }() // Release semaphore

            result, err := processItem(ctx, item)

            mu.Lock()
            defer mu.Unlock()
            if err != nil {
                errs = append(errs, err)
            } else {
                results = append(results, result)
            }
        }(item)
    }

    wg.Wait()
    return results, errors.Join(errs...)
}

// errgroup for structured concurrency
import "golang.org/x/sync/errgroup"

func fetchAll(ctx context.Context, urls []string) ([]Response, error) {
    g, ctx := errgroup.WithContext(ctx)
    g.SetLimit(10) // Max concurrent goroutines

    responses := make([]Response, len(urls))

    for i, url := range urls {
        g.Go(func() error {
            resp, err := fetch(ctx, url)
            if err != nil {
                return fmt.Errorf("fetching %s: %w", url, err)
            }
            responses[i] = resp // Safe: each goroutine writes to unique index
            return nil
        })
    }

    if err := g.Wait(); err != nil {
        return nil, err
    }
    return responses, nil
}

// Fan-out, fan-in with channels
func fanOutFanIn(ctx context.Context, input <-chan Job, workers int) <-chan Result {
    results := make(chan Result)

    var wg sync.WaitGroup
    for i := 0; i < workers; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for job := range input {
                select {
                case <-ctx.Done():
                    return
                case results <- process(job):
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

// Context-aware operations -- ALWAYS propagate context
func (s *UserService) CreateUser(ctx context.Context, u *User) error {
    // Context carries deadlines, cancellation, and values
    if err := s.validate(ctx, u); err != nil {
        return err
    }

    // Use context for database operations
    if err := s.repo.CreateUser(ctx, u); err != nil {
        return fmt.Errorf("creating user: %w", err)
    }

    // Background work should use a separate context
    go func() {
        bgCtx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
        defer cancel()
        s.sendWelcomeEmail(bgCtx, u)
    }()

    return nil
}
```

### 5. HTTP Server with Graceful Shutdown

```go
func main() {
    cfg := config.Load()
    logger := slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
        Level: cfg.LogLevel,
    }))

    // Initialize dependencies
    db, err := sql.Open("postgres", cfg.DatabaseURL)
    if err != nil {
        logger.Error("failed to connect to database", "error", err)
        os.Exit(1)
    }
    db.SetMaxOpenConns(cfg.DBMaxConns)
    db.SetMaxIdleConns(cfg.DBMaxConns / 2)
    db.SetConnMaxLifetime(30 * time.Minute)

    // Build application
    repo := postgres.NewUserRepository(db)
    svc := service.NewUserService(repo, logger)
    handler := handler.NewRouter(svc, logger)

    srv := &http.Server{
        Addr:         ":" + cfg.Port,
        Handler:      handler,
        ReadTimeout:  15 * time.Second,
        WriteTimeout: 15 * time.Second,
        IdleTimeout:  60 * time.Second,
    }

    // Start server
    go func() {
        logger.Info("server starting", "port", cfg.Port)
        if err := srv.ListenAndServe(); err != nil && !errors.Is(err, http.ErrServerClosed) {
            logger.Error("server error", "error", err)
            os.Exit(1)
        }
    }()

    // Graceful shutdown
    quit := make(chan os.Signal, 1)
    signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
    <-quit

    logger.Info("shutting down server...")
    ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer cancel()

    if err := srv.Shutdown(ctx); err != nil {
        logger.Error("forced shutdown", "error", err)
    }

    db.Close()
    logger.Info("server stopped")
}
```

## Best Practices

1. **Accept interfaces, return structs** -- define interfaces at the call site
2. **Always propagate `context.Context`** as the first parameter
3. **Wrap errors with `fmt.Errorf("context: %w", err)`** at every layer
4. **Use `slog`** (Go 1.21+) for structured logging
5. **Use `errgroup`** instead of manual `sync.WaitGroup` + error collection
6. **Keep goroutine lifetimes bounded** -- always have a cancellation path
7. **Use `go vet`, `staticcheck`, and `golangci-lint`** in CI
8. **Prefer table-driven tests** with `t.Run()` subtests
9. **Use `internal/` package** to prevent external imports of private code
10. **Set `GOMAXPROCS`** appropriately in containerized environments (use `automaxprocs`)

## Common Pitfalls

| Pitfall | Impact | Fix |
|---------|--------|-----|
| Goroutine leak (no cancellation path) | Memory/CPU leak | Always use context cancellation or `done` channel |
| Race condition on shared state | Data corruption | Use `sync.Mutex`, channels, or `sync/atomic` |
| Closing a channel from receiver side | Panic | Only the sender should close channels |
| Ignoring errors (using `_`) | Silent failures | Handle or explicitly log every error |
| `defer` in a loop | Resource accumulation | Extract to a function so defer runs per iteration |
| Using `interface{}` / `any` liberally | Loses type safety | Use generics (Go 1.18+) |
| Not setting HTTP server timeouts | Slowloris attacks | Always set Read/Write/Idle timeouts |
