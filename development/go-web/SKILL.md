---
name: go-web
description: "Expert skill for Go web development across net/http (Go 1.22+), Gin, Fiber, Chi, and Echo. Covers routing, middleware composition, context propagation, JSON binding, validation, error handling, database integration, testing, and deployment. WHEN: \"Go web\", \"Gin framework\", \"Fiber framework\", \"go-chi\", \"Echo framework\", \"net/http\", \"ServeMux\", \"gin.Context\", \"fiber.Ctx\", \"goroutine per request\", \"Go API\", \"Go REST\", \"Go middleware\", \"httptest\", \"Go handler\", \"Go router\", \"PathValue\", \"ShouldBindJSON\", \"Go graceful shutdown\", \"sqlx\", \"GORM\", \"pgx\", \"Go Docker scratch\"."
license: MIT
---

# Go Web Frameworks

This skill covers Go web development across the standard library (`net/http` with Go 1.22+ enhanced routing), Gin, Fiber, Chi, and Echo. Go's goroutine-per-request model means blocking I/O in handlers is natural -- no async/await required. The runtime multiplexes goroutines onto OS threads (M:N scheduling), handling tens of thousands of concurrent connections with modest memory (~8KB initial stack per goroutine).

## How to Approach Tasks

1. **Classify** the request:
   - **Architecture** -- Load `references/architecture.md` for ServeMux internals, Gin router, Fiber/fasthttp differences, middleware composition, handler patterns, context propagation, graceful shutdown, HTTP/2
   - **Best practices** -- Load `references/best-practices.md` for project structure, dependency injection, testing, database patterns, error handling, deployment, performance, security
   - **Framework selection** -- Use the decision guide below
   - **Troubleshooting** -- Load both reference files; cross-reference error patterns

2. **Identify framework** -- Determine from imports (`net/http`, `gin-gonic/gin`, `gofiber/fiber`, `go-chi/chi`, `labstack/echo`), handler signatures, or explicit mention. Default to net/http stdlib for new projects unless requirements suggest otherwise.

3. **Load context** -- Read the relevant reference file before answering.

4. **Analyze** -- Apply Go-specific reasoning. Consider goroutine lifecycle, context cancellation, error wrapping, interface-based design, and stdlib compatibility.

5. **Recommend** -- Provide concrete Go code examples. Always qualify framework trade-offs.

6. **Verify** -- Suggest validation: `go build`, `go test -race`, `go vet`, benchmarking with `-benchmem`.

## Core Concurrency Model

Every HTTP request runs in its own goroutine. The Go scheduler parks goroutines during I/O and runs others -- no callbacks, no futures, no colored functions.

```
net/http listener
  Accept() -> goroutine per connection
    -> goroutine per request (HTTP/2: multiplexed on one connection)
```

`context.Context` flows through the entire call chain. Use it for cancellation, deadlines, and request-scoped values. Never store context in a struct -- always pass it as the first parameter.

```go
func (h *Handler) getUser(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()
    user, err := h.repo.FindByID(ctx, r.PathValue("id"))
    if err != nil {
        if ctx.Err() != nil {
            return // client disconnected
        }
        http.Error(w, "internal error", http.StatusInternalServerError)
        return
    }
    json.NewEncoder(w).Encode(user)
}
```

## Framework Selection Guide

### When to Use What

| Framework | Choose When | Trade-offs |
|---|---|---|
| **net/http (1.22+)** | Minimal deps, library code, stdlib compatibility, Go 1.22+ method+wildcard routing covers your needs | No built-in binding/validation; manual JSON handling |
| **Gin** | Highest adoption, fast prototyping, need binding+validation out of the box, team knows Express/Flask | Custom `gin.Context` (not pure `http.Handler`) |
| **Fiber** | Extreme throughput needed, team from Node.js/Express, acceptable to trade stdlib compat for perf | Not stdlib compatible (fasthttp), ctx data recycled after handler |
| **Chi** | Want stdlib `http.Handler` compat with better ergonomics, rich middleware library | Smaller ecosystem than Gin |
| **Echo** | Alternative to Gin, strong WebSocket/SSE, prefer Echo's API style | Similar trade-offs to Gin |

### stdlib Compatibility Matrix

| Framework | Uses `http.Handler` | Works with `httptest` | Works with `net/http` middleware |
|---|---|---|---|
| net/http | Yes | Yes | Yes |
| Gin | Wraps it | Yes | Via adapter |
| Fiber | No (fasthttp) | No (`app.Test()`) | No |
| Chi | Yes | Yes | Yes |
| Echo | Wraps it | Yes | Via adapter |

**Key insight**: If you need to share middleware with the broader Go ecosystem or use `httptest` directly, prefer net/http, Chi, or Gin. Fiber's fasthttp base is architecturally incompatible.

## Handler Patterns

### net/http (Go 1.22+)

```go
mux := http.NewServeMux()
mux.HandleFunc("GET /users/{id}", getUser)      // method + wildcard
mux.HandleFunc("GET /files/{path...}", serveFile) // rest-of-path wildcard

func getUser(w http.ResponseWriter, r *http.Request) {
    id := r.PathValue("id") // Go 1.22+
}
```

### Gin

```go
r := gin.Default() // includes Logger + Recovery
r.GET("/users/:id", func(c *gin.Context) {
    id := c.Param("id")
    c.JSON(200, gin.H{"id": id})
})
```

### Fiber

```go
app := fiber.New()
app.Get("/users/:id", func(c *fiber.Ctx) error {
    id := c.Params("id")
    return c.JSON(fiber.Map{"id": id})
})
// WARNING: c.Body() and c.Params() data is recycled after handler returns.
// Copy any data before spawning goroutines.
```

## Middleware Composition

The canonical Go middleware signature is `func(http.Handler) http.Handler`. This composes without framework dependency and works with net/http, Chi, and (via adapters) Gin.

```go
func Logger(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()
        next.ServeHTTP(w, r)
        slog.Info("request", "method", r.Method, "path", r.URL.Path,
            "duration", time.Since(start))
    })
}

// Stack applies middlewares in order (first = outermost)
func Stack(mws ...func(http.Handler) http.Handler) func(http.Handler) http.Handler {
    return func(next http.Handler) http.Handler {
        for i := len(mws) - 1; i >= 0; i-- {
            next = mws[i](next)
        }
        return next
    }
}
```

Gin and Fiber use framework-specific middleware signatures (`gin.HandlerFunc`, `func(*fiber.Ctx) error`) with `c.Next()` for chain continuation and `c.Abort()` / early return to short-circuit.

## Error Handling

Go uses explicit error returns -- no exceptions. Map domain errors to HTTP status codes at the handler boundary.

```go
// Sentinel errors for behavior
var (
    ErrNotFound  = errors.New("not found")
    ErrConflict  = errors.New("conflict")
    ErrForbidden = errors.New("forbidden")
)

// Wrap errors with context
func (r *repo) FindByID(ctx context.Context, id string) (*User, error) {
    err := r.db.QueryRowContext(ctx, `SELECT ...`, id).Scan(&u)
    if err == sql.ErrNoRows {
        return nil, fmt.Errorf("user %s: %w", id, ErrNotFound)
    }
    return &u, err
}

// Handler maps errors to HTTP
func (h *Handler) get(w http.ResponseWriter, r *http.Request) {
    user, err := h.repo.FindByID(r.Context(), r.PathValue("id"))
    if err != nil {
        switch {
        case errors.Is(err, ErrNotFound):
            http.Error(w, "not found", http.StatusNotFound)
        default:
            h.log.Error("get user", "err", err)
            http.Error(w, "internal error", http.StatusInternalServerError)
        }
        return
    }
    json.NewEncoder(w).Encode(user)
}
```

## Database Integration

| Library | Type | Key Feature | Best For |
|---|---|---|---|
| `database/sql` | Stdlib interface | Connection pooling, driver agnostic | All projects (foundation layer) |
| `sqlx` | Stdlib extension | Struct scanning, named queries | Most APIs (lightweight, flexible) |
| `GORM` | Full ORM | Migrations, associations, hooks, scopes | Rapid development, complex models |
| `pgx` | Native Postgres | LISTEN/NOTIFY, COPY, batch, high perf | Postgres-specific features |

```go
// Connection pool tuning (database/sql or sqlx)
db.SetMaxOpenConns(25)
db.SetMaxIdleConns(10)
db.SetConnMaxLifetime(5 * time.Minute)
db.SetConnMaxIdleTime(1 * time.Minute)
```

## Testing

Use `net/http/httptest` for stdlib-compatible frameworks. Fiber requires `app.Test()`.

```go
func TestGetUser(t *testing.T) {
    h := NewUserHandler(&mockRepo{}, slog.Default())
    req := httptest.NewRequest("GET", "/123", nil)
    rec := httptest.NewRecorder()

    h.Routes().ServeHTTP(rec, req)

    assert.Equal(t, http.StatusOK, rec.Code)
}
```

Table-driven tests and interface-based mocking are idiomatic Go. No mocking framework required -- define interfaces, implement test doubles.

## Deployment

Go compiles to a single static binary (with `CGO_ENABLED=0`). This is the primary deployment artifact.

```dockerfile
FROM golang:1.24-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o server ./cmd/server

FROM scratch
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /app/server /server
EXPOSE 8080
ENTRYPOINT ["/server"]
```

Result: ~5-15 MB image with zero OS dependencies.

## Dependency Injection

Go uses constructor injection -- no DI framework needed. Define dependencies as interfaces, inject via constructors, wire in `main()`.

```go
type UserHandler struct {
    repo  UserRepository  // interface
    email EmailService    // interface
    log   *slog.Logger
}

func NewUserHandler(repo UserRepository, email EmailService, log *slog.Logger) *UserHandler {
    return &UserHandler{repo: repo, email: email, log: log}
}
```

For larger applications, consider `google/wire` for compile-time DI code generation.

## Key Libraries

| Category | Library | Purpose |
|---|---|---|
| Logging | `log/slog` (stdlib) | Structured logging (Go 1.21+) |
| Validation | `go-playground/validator` | Struct tag validation (used by Gin) |
| HTTP client | `net/http` (stdlib) | HTTP client with connection pooling |
| WebSocket | `nhooyr.io/websocket` | Modern, stdlib-compatible WebSocket |
| UUID | `google/uuid` | UUID generation |
| Config | `spf13/viper`, `koanf` | Configuration management |
| Migration | `golang-migrate/migrate` | Database migrations |
| Testing | `stretchr/testify` | Assertions and mocking |

## Common Pitfalls

1. **Forgetting timeouts on `http.Server`** -- Always set `ReadTimeout`, `WriteTimeout`, `IdleTimeout` in production. Unbounded timeouts allow slowloris attacks.
2. **Capturing Fiber ctx data after handler returns** -- `*fiber.Ctx` is recycled. Copy `c.Body()`, `c.Params()` before goroutines.
3. **Not checking `ctx.Err()` before writing response** -- If the client disconnected, writing to `ResponseWriter` is wasted work.
4. **Injecting scoped state into long-lived goroutines** -- Database connections from a request context must not outlive the request.
5. **Using `gorilla/mux` for new projects** -- Archived since Dec 2022. Use net/http 1.22+, Chi, or Gin instead.

## Reference Files

Load these for deep knowledge on specific topics:

- `references/architecture.md` -- ServeMux internals (Go 1.22+ method+wildcard routing), Gin router (httprouter radix tree), Fiber/fasthttp differences, middleware composition pattern, handler patterns (struct-based, closure-based), context.Context propagation, graceful shutdown, HTTP/2. **Load when:** architecture questions, routing issues, middleware ordering, framework internals.
- `references/best-practices.md` -- Project structure (cmd/internal/pkg), dependency injection (constructor, wire), testing (httptest, table-driven, testcontainers), database patterns (connection pooling, transactions, sqlx/GORM), error handling (custom types, sentinel errors), deployment (static binary, scratch Docker, systemd), performance (pprof, benchmarking), security, common libraries. **Load when:** "how should I structure", testing strategy, deployment setup, performance tuning.
