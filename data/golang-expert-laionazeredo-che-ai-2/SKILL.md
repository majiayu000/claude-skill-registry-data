---
name: "golang-expert"
description: "Universal expert guide for Golang development. Covers code style, concurrency, context, data structures, database access, design patterns, documentation, error handling, naming conventions, performance optimization, security, and testing."
---

# Golang Expert Guide

This skill is the definitive source for idiomatic Golang development, consolidating best practices across all engineering domains.

## 🛠 Core Principles
- **KISS & YAGNI**: Avoid premature abstraction. A little copying is better than a little dependency.
- **Composition over Inheritance**: Use interfaces to define behavior, not hierarchies.
- **Explicit over Implicit**: No hidden magic. Errors are values, not exceptions.

## 📏 Code Style & Naming
- **Naming**: Use `MixedCaps` (PascalCase/camelCase), no snake_case. Acronyms stay capitalized (e.g., `HTTPClient`).
- **Structure**: Package doc first, then imports, constants, types, constructors, methods.
- **Exporting**: Unexport aggressively. Only export what is necessary for the public API.
- **Formatting**: Always use `gofmt` or `gofumpt`.

## ⚡ Concurrency & Context
- **Goroutines**: Every goroutine must have a clear exit strategy (context or done channel).
- **Channels**: Share memory by communicating. Use unbuffered channels by default. Only senders close channels.
- **Context**: Pass `ctx context.Context` as the first parameter. Propagate it through all layers. Never store context in structs. Use `context.WithoutCancel` for background work that must outlive the request.

## 🗃 Data Structures & Performance
- **Slices**: Preallocate capacity with `make([]T, 0, cap)` when the size is known.
- **Maps**: Not thread-safe. Use `sync.Mutex` or `sync.Map` for concurrent access.
- **Performance**: Optimize only after profiling. Use `sync.Pool` for hot-path allocations.

## 🛡 Security & Error Handling
- **Errors**: Wrap errors with `%w` for context. Use `errors.Is` and `errors.As`.
- **Security**: Prevent SQL injection using parameterized queries. Use `gosec` for SAST.
- **PII**: Never log raw PII. Use structured logging (`slog`).

## 🧪 Testing & Quality
- **Table-Driven Tests**: Use anonymous structs for test cases with explicit `name` fields.
- **Mocks**: Use interfaces to mock dependencies. Prefer `testify` (assert, require, suite) for assertions; avoid `gomock` unless generated proto mocks.
- **Race Detection**: Always run tests with `-race`. CI NON-NEGOTIABLE: `-race -count=1` (count=1 disables test caching for correctness).
- **Linting CI**: Pipeline NON-NEGOTIABLE block on `golangci-lint run` with a curated config (govet, errcheck, gosimple, unused, staticcheck, misspell, gosec, prealloc, nilerr, asasalint).

---

## 🛜 HTTP Routers & Middleware Chains  (E04 Gap B03 · CHE_RULES §XI Table 2 row 740)

Pick one router per project. NEVER mix routers in the same binary:

| Router | When to use |
| --- | --- |
| `net/http` + `chi` (stdlib-compatible) | Default for APIs < 100 routes. `chi.Router` patterns play nicely with `http.Handler`; enables `r.Route("/v1", ...)` grouping with sub-middleware scopes. |
| Gin | High-throughput JSON APIs with built-in binding/validation. Batteries included but closed ecosystem — `gin.HandlerFunc` is NOT `http.HandlerFunc` without adapter. |
| Echo | Balanced batteries + stdlib compat via `echo.WrapHandler`. Good for teams wanting middleware conventions without Gin lock-in. |
| Fiber | Lowest allocations (fasthttp under the hood). Use ONLY when raw RPS matters; NOT http.Handler compatible — hardest to swap later. |

**Middleware order MATTERS**. Outer-first execution:
1. 🔝 Recover / Panic handler (always OUTERMOST — catches anything downstream)
2. Request ID injection (`X-Request-Id` propagates to `context` + response)
3. Tracing (OpenTelemetry `otelhttp` / otelgin / otelecho middleware — BEFORE auth so failures are traced)
4. Structured access log (slog / zap — writes `status`, `latency_ms`, `method`, `route`, `trace_id`)
5. CORS
6. Body size limit (prevents OOM before deserialization)
7. Rate limiter (token bucket, global per-IP or per-user)
8. AuthN middleware (JWT / session validates identity — populates `ctx` with `userID`)
9. AuthZ / RBAC middleware (checks role / permission against populated identity)
10. 🔚 Route handler

**chi pattern — nested routing with scoped middleware (idiomatic):**
```go
r := chi.NewRouter()
r.Use(mw.Recoverer, mw.RequestID, otelhttp.NewMiddleware("server"))
r.Route("/v1", func(r chi.Router) {
    r.Use(mw.Logger)  // applies only to /v1/*
    r.Post("/login", handleLogin)  // public
    r.Route("/admin", func(r chi.Router) {
        r.Use(RequireRole("admin")) // applies only to /v1/admin/*
        r.Get("/users", handleListUsers)
    })
})
```

---

## 🗄 Database Access Patterns  (E04 Gap B03 · CHE_RULES §XI Table 2 rows 741-743)

Go has FOUR viable data layers with different trade-offs. Pick ONE per repo.

### L1 — `database/sql` + driver (pure stdlib)
- Use for: micro-services with < 10 hand-written queries.
- Rules: `db.SetMaxOpenConns(Ncpu*4)`, `db.SetMaxIdleConns(Ncpu*2)`, `db.SetConnMaxLifetime(30m)`.
- Always pass `ctx` to `QueryContext` / `ExecContext`. Use `sql.NullXxx` or `*T` for nullable columns.

### L2 — `sqlx` (thin stdlib extension — DEFAULT CHOICE for 60% of projects)
- Use for: CRUD apps wanting struct scanning / named parameters WITHOUT ORM overhead.
- NON-NEGOTIABLE: Use `sqlx.DB.Select` / `Get` for 1-N struct scans; `NamedExec` for `:param` bind vars that work across drivers.
- Transactions: always `tx := sqlxDB.BeginTxx(ctx, nil)` then `defer tx.Rollback()` before first statement; explicit `tx.Commit()` only AFTER the full happy path.

### L3 — GORM (full ORM — use only if prototyping speed matters)
- Use for: admin backends, internal tools, rapid iteration. NOT recommended for performance-critical hot paths.
- Rules: `gorm.Open(postgres.New(...), &gorm.Config{SkipDefaultTransaction: true})` disables implicit tx per query (2x faster). Always `db.WithContext(ctx).Where(...)`.
- **Associations**: Use `Preload("X")` or `Joins("X")` explicitly. Never `Preload(clause.Associations)` in production queries — it is a SELECT N+1 footgun.

### L4 — sqlc (compile-time SQL codegen — SAFEST & FASTEST for > 30 queries)
- Use for: services with stable, long-lived SQL. Write SQL files, sqlc generates type-safe Go. THIS IS NON-NEGOTIABLE when query count > 30.
- Workflow: write `schema.sql` + `query.sql` → `sqlc generate` → use generated `Querier` interface + `pgx` pool. Mocks are trivial because `Querier` is an interface.
- Pair with `github.com/jackc/pgx/v5/stdlib` or `pgxpool.Pool` as the connection pool for Postgres.

**Connection pool rule across ALL tiers**: Acquire timeout = `context.WithTimeout(ctx, 2s)` before pool `Acquire` to prevent queue storms under load. See E05 K8s startup/readiness probes for pool health signals.

---

## 🛰 gRPC (grpc-go)  (E04 Gap B03 · CHE_RULES §XI Table 2 row 744)

### Interceptor chain (order = outer → inner, same as HTTP):
Unary (client + server):
1. 🔝 Recovery (panic → `codes.Internal` — NEVER let panics propagate)
2. OTel tracing (`otelgrpc.UnaryServerInterceptor` + `otelgrpc.UnaryClientInterceptor`)
3. Structured access log (`status_code`, `method`, `peer`, `latency_ms`, `trace_id`)
4. Deadline validation / minimum deadline enforcement (prevents infinite calls)
5. AuthN: extract `authorization` metadata → validate JWT/session → inject identity into `ctx`
6. AuthZ RBAC check against identity
7. 🔚 Handler

Streaming: mirror the chain with `StreamServerInterceptor` variants.

### Deadline & cancellation contract (NON-NEGOTIABLE):
- **Client**: ALWAYS set per-call deadline with `grpc.WithTimeout(ctx, 250*time.Millisecond)` or `grpc.CallOption` — never rely on parent ctx alone.
- **Server**: Read deadline from incoming context: `if deadline, ok := ctx.Deadline(); ok` then short-circuit heavy work if remaining < threshold.
- **Metadata propagation**: Use `metadata.FromIncomingContext(ctx)` for inbound; `metadata.NewOutgoingContext` + `grpc.Peer` for outbound hops. Propagate `traceparent`, `x-request-id`, and `authorization` through every hop.

---

## 🖥️ CLI Applications (cobra + viper)  (E04 Gap B03 · CHE_RULES §XI Table 2 row 745)

### Conventions:
- Single binary, multiple subcommands: `mycli serve`, `mycli migrate`, `mycli seed`, `mycli version`.
- Precedence chain for config values (HIGHEST → LOWEST, NON-NEGOTIABLE):
  1. **Explicit CLI flag** (`--port`)
  2. **Environment variable** (`MYCLI_PORT`) — auto-mapped via viper with `AutomaticEnv()` + `SetEnvPrefix("MYCLI")` + `EnvKeyReplacer` (`.`/`-` → `_`)
  3. **Config file** (`config.yaml` in CWD or `$HOME/.mycli/`)
  4. **Hardcoded default** (in `flags.Int("port", 8080, "...")`)

### Cobra patterns:
```go
var rootCmd = &cobra.Command{
    Use:   "mycli",
    Short: "My service CLI",
    PersistentPreRunE: func(cmd *cobra.Command, args []string) error {
        // Loads viper config once, applies to ALL subcommands.
        // Validates env vars here; return error = CLI exits 1 cleanly.
        return validateConfig(v)
    },
}
```
- Use `PersistentFlags()` for flags that apply to every subcommand (e.g. `--log-level`, `--config`). Use regular `Flags()` for command-specific ones.
- NEVER use globals for flag values. Bind to a strongly-typed `Config` struct in `PersistentPreRunE` and inject down.

---

## 📝 Logging + Observability Integration  (E04 Gap B03 · CHE_RULES §XI Table 2 row 746 → companion E05 §Observability & engineering-contracts §19)

### slog (stdlib Go 1.21+) → DEFAULT for most services
- Bootstrap ONCE in `main()` with JSON handler: `logger := slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{Level: parseLevel(cfg.LogLevel)}))` then `slog.SetDefault(logger)`.
- Inject structured fields via `slog.LogAttrs(ctx, slog.LevelInfo, "request_handled", slog.String("route", r), slog.Int("status", s), slog.Duration("latency_ms", d), slog.String("trace_id", traceIdFromCtx(ctx)))`.
- NEVER call `.Error()` without a wrapped error: `slog.Error("db query failed", "err", err, "query", q)` (structured "err" key, NOT formatted into the message).

### zap (Uber) → use when allocations matter < 1µs per log
- Use `zap.NewProduction()` in prod, `zap.NewDevelopment()` for local. Always `defer logger.Sync()`.
- Prefer `logger.Info("msg", zap.String("trace_id", tid), zap.Int("status", s))` over `SugaredLogger` in hot paths (zero allocations).

### OTel + TraceId correlation (bridge to E05):
- Every log line in scope of a request MUST include the propagated `trace_id` (extracted from `otel.TraceIDFromSpanContext(otel.GetTraceSpanContext(ctx))`).
- `trace_id` format = same as `engineering-contracts §19` (16 bytes hex). PII hash rule: same as S07 CHE_RULES §X (raw emails/phones never in logs; hash correlation via `NOTIFICATION_PII_HASH_SECRET` or equivalent).

---

## 💊 Generics 1.18+ Helpers  (E04 Gap B03 · CHE_RULES §XI Table 2 row 747)

A small stdlib-style helpers package eliminates 80% of one-off boilerplate. Put these in a single `pkg/util/` file (NOT across the codebase):

```go
// Must panics on error (use ONLY in init() / constants / CLI arg parsing before main loop).
func Must[T any](v T, err error) T {
    if err != nil { panic(err) }
    return v
}

// Ptr converts a value literal to pointer (avoids `x := v; &x`).
func Ptr[T any](v T) *T { return &v }
func Deref[T any](p *T, fallback T) T {
    if p == nil { return fallback }
    return *p
}

// Slice transformations (pure, no allocation footguns):
func Map[A, B any](in []A, f func(A) B) []B { /* ... */ }
func Filter[T any](in []T, pred func(T) bool) []T { /* ... */ }
func Reduce[T, Acc any](in []T, acc Acc, f func(Acc, T) Acc) Acc { /* ... */ }
func Max[T cmp.Ordered](a, b T) T { if a > b { return a }; return b }
func Min[T cmp.Ordered](a, b T) T { if a < b { return a }; return b }
```
Rules: Keep helper count < 15 per project. If adding the 16th, stop — it is probably domain logic and belongs in a domain package.

---

## ♻️ Runtime — Graceful Shutdown + Health Probes  (E04 Gap B03 · CHE_RULES §XI Table 2 row 748 → companion E05 §K8s Probes)

### Graceful shutdown (2-phase, NON-NEGOTIABLE for any network service):
```go
// Phase 1 — stop accepting, drain inflight within deadline
ctx, stop := signal.NotifyContext(context.Background(),
    syscall.SIGINT, syscall.SIGTERM)
defer stop()

go srv.Serve(listener) // starts server in goroutine (NOT blocking main)

<-ctx.Done() // blocks until signal

// Phase 2 — shutdown with hard deadline after inflight drain window
graceCtx, cancel := context.WithTimeout(context.Background(), 25*time.Second)
defer cancel()

// Tear down ORDER MATTERS:
// 1. HTTP/gRPC server (stops accepting, waits handlers return) → 2. DB pool → 3. Redis → 4. Workers → 5. Logger flush
if err := srv.Shutdown(graceCtx); err != nil { slog.Warn("graceful shutdown incomplete", "err", err) }
dbPool.Close()
```
If `Shutdown()` returns before deadline → clean exit 0. If deadline fires → force-exit 1 (losing some inflight > 25s is preferable to OOMKill hanging pod).

### Health endpoints (E05 K8s companion):
- `GET /healthz` → Liveness probe. Returns 200 when process is alive. **Do NOT tie to DB/Redis here** (if you do, flapping infra kills all pods at once).
- `GET /readyz` → Readiness probe. Returns 200 ONLY when: listener bound + DB pool `Ping` OK + external dependency checks OK. Returns 503 during startup/shutdown window so K8s stops routing new traffic BEFORE shutdown (avoids 502s during rolling update).
- Use `chi` mount: `r.Get("/healthz", func(w http.ResponseWriter,_) { w.WriteHeader(200) })`. Keep handlers < 1ms.

---

## 🔵 B-P1 Go · Codegen ORM + DI + Mocks (E04 §XI P1 coverage 55% → ~65%)

### ent ORM (DEFAULT when domain > 15 entities, pure codegen 0 raw SQL leak)
ent = **schema-first typed codegen ORM**. If you hand-write 40+ SELECTs and the domain is rich (bounded contexts with 15+ types), use ent. Skip ent for projects < 5 tables (sqlc/sqlx simpler).
1. **Schema directory**, 1 file per entity:
   ```
   ent/schema/event.go → ent/schema/ticket.go → ent/schema/order.go
   ```
2. **Codegen step NON-NEGOTIABLE checked into CI**: `go generate ./ent/` → emits `ent/client.go` + 40 typed methods. CI MUST run `go generate` and `git diff --exit-code` to ensure generated code matches schema. If not → FAIL build.
3. **Hooks / Privacy policies**: ent.Privacy = row-level RBAC in the generated layer, no manual WHERE. Example privacy rule that returns `ent.DenyIfNoViewer()` for ALL mutations if there's no authenticated user → impossible to forget in a handler.
4. **Ent edge traversals**: `client.QueryUser().QueryOrders().Where(order.StatusEQ(...)).All(ctx)` — typed joins, zero string queries.

### Google Wire Compile-Time DI vs Uber Fx Runtime DI (DECISION):
| Situation | Pick | Rule |
| --- | --- | --- |
| Clean startup time, NO reflection, compile-time errors | **Wire** (`wire.NewSet` + `wire.Build`) | 100% codegen. DI graph errors → compile fails. DEFAULT 90% Go services. |
| Dynamic plugins loaded at runtime, conditional modules | **Uber Fx** | `fx.Provide` + `fx.Invoke`. Runtime panics if graph wrong (compile cannot catch). Use ONLY for plugin architectures. |
Wire workflow minimal:
```go
// wire.go
//go:build wireinject
var ProviderSet = wire.NewSet(NewDB, NewOrderRepo, NewOrderService, NewHandler)
func InitializeApp() (*App, func(), error) { wire.Build(ProviderSet); return nil, nil, nil }
```
Run `go generate → wire_gen.go` → 100% typed graph, no `service.NewService(db.NewDB(conf))` constructors 10 deep = maint cost -80%.

### Testify Mocks + Suite (DEFAULT testing framework companion)
- **`suite.Suite`** with SetupTest/TearDownTest replaces duplicated `t.Cleanup` boilerplate in every test function.
- **`gomock` / `testify/mock` for interfaces**: NEVER mock concrete structs. Mock ONLY interfaces. Hand-written mocks for 1-2 methods; `mockgen` codegen for interfaces > 3 methods.
- **Verify mock calls**: `mockRepo.AssertExpectations(t)` at end of EVERY test using a mock — if you forgot to expect a call that was made, test FAIL (catches regressions you wouldn't otherwise).
- **Table-driven pattern PRESERVED + suite**:
  ```go
  func (s *OrderServiceSuite) TestCreateOrder() {
      cases := []struct{ name string; in CreateIn; wantErr bool }{
          {"ok", CreateIn{UserID: 1, ItemIDs: []int64{5}}, false},
          {"empty items", CreateIn{UserID: 1, ItemIDs: nil}, true},
      }
      for _, tc := range cases { s.Run(tc.name, func() { ... }) }
  }
  ```

## 🔗 References
- [Effective Go](https://go.dev/doc/effective_go)
- [Go Code Review Comments](https://github.com/golang/go/wiki/CodeReviewComments)
- [chi router](https://github.com/go-chi/chi) · [gin](https://gin-gonic.com) · [echo](https://echo.labstack.com) · [fiber](https://gofiber.io)
- [sqlx](https://jmoiron.github.io/sqlx) · [GORM](https://gorm.io) · [sqlc](https://sqlc.dev) · [pgx](https://github.com/jackc/pgx)
- [grpc-go](https://grpc.io/docs/languages/go)
- [cobra](https://cobra.dev) · [viper](https://github.com/spf13/viper)
- [slog pkg.go.dev](https://pkg.go.dev/log/slog) · [uber-go/zap](https://github.com/uber-go/zap)
- [OpenTelemetry Go (otel-go)](https://opentelemetry.io/docs/languages/go)
- [ent ORM](https://entgo.io) · [google/wire](https://github.com/google/wire) · [testify](https://github.com/stretchr/testify)
