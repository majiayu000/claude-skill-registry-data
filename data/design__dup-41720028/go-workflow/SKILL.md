---
name: go-workflow
description: Go project workflow guidelines. Activate when working with Go files (.go), go.mod, Go modules, golang, or Go-specific tooling.
location: user
---

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119.

# Go Projects Workflow

Guidelines for working with Go projects using modern tooling.

## Tool Grid

| Task | Tool | Command |
|------|------|---------|
| Lint | golangci-lint | `golangci-lint run` |
| Format | goimports | `goimports -w .` |
| Build | go build | `go build ./...` |
| Test | go test | `go test ./...` |
| Coverage | go test | `go test -cover ./...` |
| Fuzzing | native | `go test -fuzz=Fuzz` |
| Race detection | built-in | `go test -race ./...` |
| Vulnerability | govulncheck | `govulncheck ./...` |

---

## Go Modules

### go.mod Management

- You MUST use Go modules for all new projects
- You SHOULD run `go mod tidy` after adding or removing dependencies
- You MUST NOT commit a go.mod with `replace` directives unless for local development
- You SHOULD use exact version pinning for critical dependencies

```go
// Good: explicit version
require github.com/pkg/errors v0.9.1

// Avoid: pseudo-versions when tagged releases exist
require github.com/pkg/errors v0.0.0-20210101000000-abcdef123456
```

### go.sum Handling

- You MUST commit go.sum to version control
- You SHOULD NOT manually edit go.sum
- Run `go mod verify` to check integrity

### Dependency Updates

```bash
# Update all dependencies
go get -u ./...

# Update specific dependency
go get -u github.com/pkg/errors

# Update to specific version
go get github.com/pkg/errors@v0.9.1

# Remove unused dependencies
go mod tidy
```

---

## Error Handling

### Error Wrapping

- You MUST wrap errors with context using `fmt.Errorf` and `%w`
- You SHOULD include the operation that failed in the error message

```go
// Good: wrapped with context
if err != nil {
    return fmt.Errorf("failed to open config file %s: %w", path, err)
}

// Bad: loses error chain
if err != nil {
    return fmt.Errorf("failed to open config: %v", path)
}
```

### Custom Error Types

- You SHOULD define custom error types for domain-specific errors
- You MUST implement the `error` interface

```go
type NotFoundError struct {
    Resource string
    ID       string
}

func (e *NotFoundError) Error() string {
    return fmt.Sprintf("%s with ID %s not found", e.Resource, e.ID)
}
```

### Error Checking

- You MUST use `errors.Is()` for sentinel error comparison
- You MUST use `errors.As()` for type assertion on errors

```go
// Good: unwraps error chain
if errors.Is(err, os.ErrNotExist) {
    // handle missing file
}

// Good: extract typed error
var notFound *NotFoundError
if errors.As(err, &notFound) {
    // handle not found
}

// Bad: direct comparison (breaks with wrapping)
if err == os.ErrNotExist {
    // may not match wrapped errors
}
```

### Sentinel Errors

- You SHOULD define sentinel errors as package-level variables
- You MUST use `errors.New()` for simple sentinel errors

```go
var (
    ErrNotFound     = errors.New("resource not found")
    ErrUnauthorized = errors.New("unauthorized access")
)
```

---

## Context Propagation

### Function Signatures

- You MUST pass `context.Context` as the first parameter
- You MUST name the parameter `ctx`

```go
// Good
func FetchUser(ctx context.Context, id string) (*User, error) {
    // ...
}

// Bad: context not first
func FetchUser(id string, ctx context.Context) (*User, error) {
    // ...
}
```

### Context Usage

- You MUST NOT store context in structs
- You SHOULD check for context cancellation in long-running operations
- You SHOULD use `context.WithTimeout` or `context.WithDeadline` for operations with time limits

```go
func ProcessItems(ctx context.Context, items []Item) error {
    for _, item := range items {
        select {
        case <-ctx.Done():
            return ctx.Err()
        default:
            if err := process(ctx, item); err != nil {
                return err
            }
        }
    }
    return nil
}
```

### Context Values

- You SHOULD avoid using `context.WithValue` for passing optional parameters
- Context values SHOULD only be used for request-scoped data (trace IDs, auth tokens)
- You MUST use typed keys to avoid collisions

```go
type contextKey string

const userIDKey contextKey = "userID"

func WithUserID(ctx context.Context, id string) context.Context {
    return context.WithValue(ctx, userIDKey, id)
}

func UserIDFromContext(ctx context.Context) (string, bool) {
    id, ok := ctx.Value(userIDKey).(string)
    return id, ok
}
```

---

## Concurrency Patterns

### Goroutines

- You MUST NOT start goroutines without a way to stop them
- You SHOULD use `sync.WaitGroup` to wait for goroutines to complete
- You MUST handle panics in goroutines

```go
func ProcessConcurrently(ctx context.Context, items []Item) error {
    var wg sync.WaitGroup
    errCh := make(chan error, len(items))

    for _, item := range items {
        wg.Add(1)
        go func(item Item) {
            defer wg.Done()
            defer func() {
                if r := recover(); r != nil {
                    errCh <- fmt.Errorf("panic: %v", r)
                }
            }()
            if err := process(ctx, item); err != nil {
                errCh <- err
            }
        }(item)
    }

    wg.Wait()
    close(errCh)

    for err := range errCh {
        if err != nil {
            return err
        }
    }
    return nil
}
```

### Channels

- You SHOULD prefer channels for communication between goroutines
- You MUST close channels from the sender side only
- You SHOULD use buffered channels when the number of items is known

```go
// Good: producer closes channel
func Generate(ctx context.Context, n int) <-chan int {
    ch := make(chan int)
    go func() {
        defer close(ch)
        for i := 0; i < n; i++ {
            select {
            case <-ctx.Done():
                return
            case ch <- i:
            }
        }
    }()
    return ch
}
```

### Sync Package

- You SHOULD use `sync.Mutex` for protecting shared state
- You SHOULD use `sync.RWMutex` when reads significantly outnumber writes
- You SHOULD use `sync.Once` for one-time initialization

```go
type Cache struct {
    mu    sync.RWMutex
    items map[string]Item
}

func (c *Cache) Get(key string) (Item, bool) {
    c.mu.RLock()
    defer c.mu.RUnlock()
    item, ok := c.items[key]
    return item, ok
}

func (c *Cache) Set(key string, item Item) {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.items[key] = item
}
```

---

## Testing

### Table-Driven Tests

- You SHOULD use table-driven tests for testing multiple cases

```go
func TestAdd(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"positive numbers", 2, 3, 5},
        {"negative numbers", -1, -2, -3},
        {"zero", 0, 0, 0},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := Add(tt.a, tt.b)
            if result != tt.expected {
                t.Errorf("Add(%d, %d) = %d; want %d", tt.a, tt.b, result, tt.expected)
            }
        })
    }
}
```

### Test Fixtures

- You SHOULD place test data in a `testdata/` directory
- The `testdata/` directory is ignored by the Go toolchain

```go
func TestParseConfig(t *testing.T) {
    data, err := os.ReadFile("testdata/config.json")
    if err != nil {
        t.Fatal(err)
    }
    // use data...
}
```

### Test Helpers

- You SHOULD use `t.Helper()` in test helper functions
- Helper functions SHOULD take `testing.TB` to work with both tests and benchmarks

```go
func assertNoError(t testing.TB, err error) {
    t.Helper()
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
}
```

### Race Detection

- You MUST run tests with `-race` flag in CI
- You SHOULD run `go test -race ./...` locally before pushing

```bash
# CI configuration
go test -race -coverprofile=coverage.out ./...
```

---

## Project Structure

### Standard Layout

```
myproject/
├── cmd/                    # Main applications
│   └── myapp/
│       └── main.go
├── internal/               # Private application code
│   ├── config/
│   ├── handlers/
│   └── service/
├── pkg/                    # Public library code
│   └── client/
├── api/                    # API definitions (OpenAPI, proto)
├── web/                    # Web assets
├── scripts/                # Build and CI scripts
├── testdata/               # Test fixtures
├── go.mod
├── go.sum
└── Makefile
```

### Package Organization

- `cmd/` SHOULD contain only main packages with minimal logic
- `internal/` MUST contain code that SHOULD NOT be imported by other projects
- `pkg/` MAY contain code intended for external use
- You SHOULD avoid deeply nested package structures

### Main Package

- The `main` package SHOULD be minimal
- You SHOULD move business logic to internal packages

```go
// cmd/myapp/main.go
package main

import (
    "log"
    "os"

    "myproject/internal/app"
)

func main() {
    if err := app.Run(os.Args[1:]); err != nil {
        log.Fatal(err)
    }
}
```

---

## Naming Conventions

### General Rules

- You MUST use MixedCaps (PascalCase for exported, camelCase for unexported)
- You MUST NOT use underscores in Go names
- You SHOULD use short names for local variables with small scope

```go
// Good
func ProcessUsers(users []User) error {
    for i, u := range users {
        // short names ok for loop variables
    }
}

// Bad
func ProcessUsers(users []User) error {
    for index, user := range users {
        // unnecessarily verbose
    }
}
```

### Package Names

- Package names MUST be lowercase, single-word
- You MUST NOT use underscores or mixedCaps
- Package name SHOULD NOT repeat the import path

```go
// Good
package http

// Bad
package httpClient
package http_client
```

### Interface Names

- Single-method interfaces SHOULD end in -er suffix
- You SHOULD NOT prefix interface names with "I"

```go
// Good
type Reader interface {
    Read(p []byte) (n int, err error)
}

type UserService interface {
    GetUser(ctx context.Context, id string) (*User, error)
}

// Bad
type IUserService interface {
    GetUser(ctx context.Context, id string) (*User, error)
}
```

### Acronyms

- Acronyms SHOULD be all caps or all lowercase
- You MUST be consistent within a project

```go
// Good
var httpClient *http.Client
var HTTPClient *http.Client  // exported
var userID string
var UserID string            // exported

// Bad
var HttpClient *http.Client
var userId string
```

---

## Interface Design

### Accept Interfaces, Return Structs

- Function parameters SHOULD accept interfaces when possible
- Functions SHOULD return concrete types

```go
// Good: accepts interface
func ProcessData(r io.Reader) error {
    // can accept any Reader
}

// Good: returns concrete type
func NewService(db *sql.DB) *Service {
    return &Service{db: db}
}

// Bad: returns interface (unless abstracting implementations)
func NewService(db *sql.DB) ServiceInterface {
    return &Service{db: db}
}
```

### Small Interfaces

- You SHOULD define small, focused interfaces
- You SHOULD compose larger interfaces from smaller ones

```go
// Good: small, focused interfaces
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}

type ReadWriter interface {
    Reader
    Writer
}
```

### Interface Location

- Interfaces SHOULD be defined where they are used, not where they are implemented
- This allows consumers to define only what they need

```go
// In consumer package
type UserGetter interface {
    GetUser(ctx context.Context, id string) (*User, error)
}

// Service implementation doesn't need to know about this interface
func NewHandler(users UserGetter) *Handler {
    return &Handler{users: users}
}
```

---

## Common Patterns

### Functional Options

- You SHOULD use functional options for configurable constructors

```go
type Server struct {
    addr    string
    timeout time.Duration
}

type Option func(*Server)

func WithTimeout(d time.Duration) Option {
    return func(s *Server) {
        s.timeout = d
    }
}

func NewServer(addr string, opts ...Option) *Server {
    s := &Server{
        addr:    addr,
        timeout: 30 * time.Second, // default
    }
    for _, opt := range opts {
        opt(s)
    }
    return s
}
```

### Graceful Shutdown

- You MUST handle OS signals for graceful shutdown
- You SHOULD use context for coordinating shutdown

```go
func main() {
    ctx, cancel := signal.NotifyContext(context.Background(),
        syscall.SIGINT, syscall.SIGTERM)
    defer cancel()

    srv := &http.Server{Addr: ":8080"}

    go func() {
        <-ctx.Done()
        shutdownCtx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
        defer cancel()
        srv.Shutdown(shutdownCtx)
    }()

    if err := srv.ListenAndServe(); err != http.ErrServerClosed {
        log.Fatal(err)
    }
}
```

---

## CI/CD Requirements

### Required Checks

- You MUST run `go build ./...` to verify compilation
- You MUST run `go test -race ./...` for race detection
- You SHOULD run `golangci-lint run` for static analysis
- You SHOULD run `govulncheck ./...` for vulnerability scanning

### Example GitHub Actions

```yaml
name: Go
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with:
          go-version: '1.22'
      - run: go build ./...
      - run: go test -race -coverprofile=coverage.out ./...
      - run: go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
      - run: golangci-lint run
      - run: go install golang.org/x/vuln/cmd/govulncheck@latest
      - run: govulncheck ./...
```
