---
name: golang-checklist
description: >
  Apply the Go code review checklist during PR review, design review, or self-review.
  Covers style & idioms, error handling, design patterns, project architecture,
  concurrency, testing, performance, and security. Each item tagged MUST, SHOULD, or CONSIDER.
  Triggers when user asks to "review Go code", "check Go PR", "golang checklist",
  "review my Go", "Go code review", or invokes /golang-checklist.
---

# Go Code Checklist Skill

You are performing a structured Go code review using the canonical checklist below.
Work through the applicable sections for the diff/code at hand. Report findings
grouped by severity (MUST blocks merge, SHOULD needs justification, CONSIDER is advisory).

## How to Apply

1. On first read walk top-to-bottom.
2. For targeted reviews jump to the matching section (e.g., a concurrency PR → §6).
3. For fast PR reviews run §10 Quick Reference only, then dive into flagged sections.
4. Output findings as a markdown table: `| Severity | Section | Finding | Suggestion |`

---

## §2 Style & Idioms

### 2.1 Formatting & Tooling
- **MUST** All files pass `gofmt -s` and `goimports`.
- **MUST** `go vet ./...` is clean.
- **MUST** `staticcheck ./...` is clean or every finding has `//lint:ignore SAxxxx <reason>`.
- **SHOULD** `golangci-lint` enabled with: `govet`, `staticcheck`, `errcheck`, `ineffassign`, `gosimple`, `unused`, `misspell`, `gocritic`, `revive`, `gosec`.
- **SHOULD** Build tags use `//go:build`, not the deprecated `// +build`.
- **CONSIDER** `gofumpt` for stricter formatting.

### 2.2 Naming
- **MUST** Short-lived locals: 1–2 letters (`i`, `r`, `ctx`, `tx`). No `lineCount` inside a 5-line loop.
- **MUST** Receivers: 1–2 letters, consistent across all methods of the same type.
- **MUST** Initialisms as a unit: `URL`, `ID`, `HTTP`, `JSON` → `userID`, `ServeHTTP`, `parseURL`.
- **MUST** Exported names read well from outside; no stutter (`bytes.BytesBuffer` bad).
- **SHOULD** Single-method interfaces end in `-er`: `Reader`, `Writer`, `Stringer`.
- **SHOULD** Sentinel errors are `Err...`: `ErrNotFound`, `ErrInvalidInput`.
- **SHOULD** No Hungarian prefixes (`iCount`) or type suffixes (`userStruct`).

### 2.3 Comments & Documentation
- **MUST** Every exported identifier has a doc comment starting with the identifier name.
- **MUST** Package-level comment in exactly one file, starts with `Package <name> ...`.
- **SHOULD** Comments answer **why**; code shows **what**. Delete comments that merely restate the signature.
- **SHOULD** Every `TODO` has an issue link or name (`// TODO(#1234): ...`).

### 2.4 Control Flow
- **MUST** Prefer early returns; guard clauses first, happy path last.
- **MUST** No empty branches or dead code; `_ = x` forbidden in production.
- **SHOULD** `switch` over `if/else if` chains for single-value comparisons.
- **SHOULD** `defer` placed immediately after resource acquisition.
- **CONSIDER** No `defer` inside hot loops (per-iteration cost).

### 2.5 Types, Pointers & Zero Values
- **MUST** Types are zero-value usable where possible.
- **MUST** Mutexes embedded by value, never copied.
- **SHOULD** Pass small immutable values by value; large/mutating structs by pointer.
- **SHOULD** Avoid `nil` as meaningful state; prefer an enum or `(value, ok)`.

### 2.6 Imports
- **MUST** Imports grouped (stdlib, third-party, internal) and sorted by `goimports`.
- **MUST** Dot imports (`import . "x"`) only in test files.
- **SHOULD** Import aliases only for collisions or unwieldy proto packages.

---

## §3 Error Handling

### 3.1 Returning & Checking
- **MUST** Every returned error is checked. Blank identifier forbidden for errors.
- **MUST** `error` is the **last** return value.
- **MUST** On error, downstream values are zero-valued (`return nil, err`).
- **SHOULD** Handle each error exactly once: log, wrap+return, or recover — not both log and return.

### 3.2 Wrapping & Context
- **MUST** Wrap across layer boundaries: `fmt.Errorf("noun phrase: %w", err)`.
- **MUST** Wrap messages start with a noun phrase — NOT `failed to` or `error:`.
  - Good chain: `handle login: lookup user: query users: connection refused`
  - Bad chain: `failed to handle login: failed to lookup user: ...`
- **SHOULD** Wrap with a domain-specific error type at subsystem boundaries.
- **CONSIDER** `errors.Join(err1, err2)` (Go 1.20+) for multiple independent errors.

### 3.3 Inspection
- **MUST** `errors.Is(err, target)` for sentinel matching — never `err == target` for wrapped errors.
- **MUST** `errors.As(err, &target)` for typed errors — never type-assert a wrapped error directly.
- **SHOULD** Sentinel errors at package top scope: `var ErrNotFound = errors.New("not found")`.

### 3.4 Panics
- **MUST** `panic` reserved for irrecoverable bugs only. Not error handling.
- **MUST** Library code never panics on bad input — validate and return an error.
- **SHOULD** Top-level goroutines wrap entry points in `defer recover()` with stack logging.
- **SHOULD** `main` exits via `os.Exit(1)`, not `panic`, for expected failures.

### 3.5 Boundaries
- **MUST** HTTP/gRPC handlers translate errors to transport codes at the edge.
- **MUST** External error messages contain no stack traces, file paths, SQL fragments, or PII.
- **SHOULD** Internal errors get a request/trace ID before logging.
- **CONSIDER** Structured logging (`log/slog`, `zap`, `zerolog`) with error as typed field.

---

## §4 Design Patterns

### 4.1 Accept Interfaces, Return Structs
- **MUST** Parameters use the narrowest interface (`io.Writer`, not `*os.File`).
- **MUST** Constructors return concrete types, not interfaces (except `error` and unexported types).
- **SHOULD** Define interfaces in the **consumer** package, not the producer.
- **SHOULD** One-method interfaces preferred; >3 methods → split or use concrete type.

### 4.2 Functional Options
- **MUST** Functional options model **optional** config; required params are positional.
- **MUST** `type Option func(*Server)` (or `func(*Server) error` with validation).
- **MUST** Option names `With...`: `WithTimeout`, `WithLogger`, `WithTLS`.
- **SHOULD** Apply options after defaults; options never panic.
- **CONSIDER** Config struct simpler when <3 optional params; functional options worth it at 5+.

### 4.3 Constructors & Zero Values
- **MUST** Constructor is `NewT` returning `*T`; validation happens here.
- **SHOULD** Strive for zero-value usability (`var b bytes.Buffer` without `NewBuffer`).

### 4.4 Composition & Embedding
- **MUST** Embedding is has-a, not is-a. No embedding to fake inheritance.
- **MUST** Embed `sync.Mutex` only when the lock protects exactly the embedding struct's fields and type is unexported.
- **SHOULD** Prefer named field (`store Store`) over embedding when method promotion is unwanted.
- **SHOULD** No deep embedding chains (>1 level).

### 4.5 Strategy, Decorator, Observer
- **SHOULD** Strategy: one-method interface or `func(...)` type.
- **SHOULD** Decorator: function taking interface, returning same interface (`http.Handler` middleware).
- **SHOULD** Observer/pub-sub: channels + goroutine per subscriber; not callback registration.
- **CONSIDER** Builder is rarely idiomatic — functional options or config struct preferred.

### 4.6 Generics (Go 1.18+)
- **MUST** Generics for genuine duplication on containers/algorithms, not to model behavior (use interfaces).
- **SHOULD** Type params: `T`, `K`, `V` with constraint comments.
- **CONSIDER** Check `golang.org/x/exp/slices`, `maps` (stdlib since Go 1.21+) before writing generic helpers.

### 4.7 Anti-Patterns
- **MUST NOT** `interface{}`/`any` where concrete types or small interfaces work.
- **MUST NOT** Reflexive getters/setters. Public fields are idiomatic without validation.
- **MUST NOT** `Manager`/`Service`/`Handler` god struct. Split by responsibility.
- **SHOULD NOT** `reflect` outside serialization, ORMs, test helpers.

---

## §5 Project Architecture

### 5.1 Top-Level Layout
- **MUST** `go.mod` + `go.sum` committed at module root.
- **SHOULD** `cmd/<binary>/main.go` only for multi-binary repos; single binary can use root `main.go`.
- **SHOULD** `internal/` for code not importable by other modules.
- **MUST NOT** Mirror Java/Spring layout (`controllers/`, `services/`, `repositories/`); slice by domain.

### 5.2 Package Design
- **MUST** Package names: lowercase, single-word noun. No underscores, no camelCase.
- **MUST** No `util`, `common`, `helpers`, `misc`, `shared` packages.
- **MUST** Exported API is the minimum needed; everything else unexported.
- **SHOULD** Package compiles in <1 s; if not, it's too big — split.
- **SHOULD** No circular imports; invert dependencies via interfaces in the consumer.

### 5.3 Domain-Sliced Layout (Default)

```
myservice/
  go.mod
  cmd/
    api/main.go
    worker/main.go
  internal/
    user/
      user.go        # domain types + interfaces
      service.go     # application logic
      postgres.go    # persistence adapter
      http.go        # transport adapter
    billing/
    platform/
      config/
      database/
      observability/
```

- **SHOULD** Default to domain-sliced layout; each capability under `internal/`.
- **SHOULD** Cross-cutting infra under `internal/platform/`.

### 5.4 Hexagonal / Ports & Adapters
- **SHOULD** Core (domain + use cases) imports nothing from adapters.
- **SHOULD** Ports are interfaces declared by the core (`UserRepository`, `EmailSender`).
- **SHOULD** Adapters implement ports; wire them in `cmd/*/main.go` (composition root).
- **CONSIDER** DI library (Wire, fx) only when manual wiring >30 deps; prefer Wire (compile-time).
- **MUST NOT** Framework types (`*echo.Context`, `*grpc.Server`) in core domain code.

### 5.5 Modules & Versioning
- **MUST** One `go.mod` per release-coupled unit.
- **MUST** Anything outside `internal/` is public API; breaking changes need major version bump.
- **SHOULD** `go mod tidy` in CI; fail on diff.
- **SHOULD** `go.work` for local multi-module dev; do not commit for shared use.

---

## §6 Concurrency

### 6.1 Context Propagation
- **MUST** I/O and goroutine-spawning functions accept `ctx context.Context` as **first** param.
- **MUST** `context.Context` never stored in a struct field.
- **MUST** `defer cancel()` immediately after every `context.WithCancel/WithTimeout/WithDeadline`.
- **MUST** Long-running loops `select` on `<-ctx.Done()` and return `ctx.Err()`.
- **MUST NOT** `context.TODO()` in production paths.
- **MUST NOT** Pass a request `ctx` to a goroutine that outlives the request; use `context.WithoutCancel` (Go 1.21+) or fresh `context.Background()` with its own timeout.

### 6.2 Goroutine Lifecycle
- **MUST** Every `go func(){}()` answers: who waits for it and how does it stop.
- **MUST** Goroutines from request handlers are bounded (`errgroup.WithContext` + `g.Wait()`).
- **MUST** Top-level goroutines recover from panics and log stack.
- **SHOULD** `errgroup.Group` for fan-out with error coordination; `WaitGroup` for wait-only.
- **SHOULD** Bound concurrency: `errgroup.SetLimit(n)` or buffered semaphore channel.
- **SHOULD** `goleak.VerifyTestMain` in `TestMain` for packages with concurrent code.

### 6.3 Channels vs Mutexes
- **MUST** Only the **sender** closes a channel.
- **MUST** `chan struct{}` for pure signaling.
- **MUST** Receivers handle closed case: `v, ok := <-ch`.
- **SHOULD** Buffered channels sized for a documented reason.
- **SHOULD** `sync.Mutex` for short shared-state ops; `sync.RWMutex` only when reads dominate 10:1+.

### 6.4 Common Leak Patterns
- **MUST** `time.After` inside `select` leaks until fired; use `time.NewTimer` + `defer t.Stop()`.
- **MUST** `http.Response.Body` closed and drained even on non-2xx or early return.
- **MUST** `sql.Rows` closed via `defer rows.Close()`; check `rows.Err()` after loop.
- **MUST** Tickers stopped: `defer ticker.Stop()`.
- **SHOULD** CI: `go test -race -count=1 ./...` + `goleak` per package with concurrent code.

### 6.5 Race Detector
- **MUST** CI runs full test suite with `-race` on every PR.
- **MUST** A test failing under `-race` blocks merge — fix the synchronization.
- **SHOULD** Load/integration tests run under `-race` at minimum nightly.

---

## §7 Testing & Quality

### 7.1 Test Structure
- **MUST** Tests in `_test.go` beside code; white-box `package foo`, black-box `package foo_test`.
- **MUST** Helpers call `t.Helper()` so failures point to the caller.
- **MUST** Tests are deterministic — no wall-clock time, map iteration order, or network without a fake.
- **SHOULD** Test names describe scenario: `TestParser_RejectsTrailingComma`, not `TestParse2`.
- **SHOULD** `t.Cleanup(...)` for tear-down; `t.TempDir()` for test files.

### 7.2 Table-Driven Tests
- **MUST** Multi-case tests use `[]struct{name string; ...}` + `t.Run(tc.name, ...)`.
- **MUST** Map-keyed cases accept randomised iteration — it surfaces ordering bugs.
- **SHOULD** Each case asserts one behavior.

### 7.3 Parallelism
- **MUST** `t.Parallel()` is the first statement of a parallel test.
- **MUST** `t.Parallel()` called before `context.WithTimeout`.
- **MUST** Parallel tests don't mutate process-global state.
- **SHOULD** `t.Setenv` and `t.Parallel()` are mutually exclusive.

### 7.4 Test Doubles
- **SHOULD** Prefer fakes (in-memory implementations) over generated mocks.
- **SHOULD** Mocks only for verifying call sequence or arguments to outbound calls.
- **CONSIDER** `httptest.NewServer` over mocked transports for HTTP clients.

### 7.5 Golden Files
- **MUST** Golden files under `testdata/`.
- **MUST** Strip non-deterministic fields (timestamps, random IDs, paths) before comparison.
- **SHOULD** Provide `-update` flag to rewrite; CI runs without it.

### 7.6 Fuzzing
- **SHOULD** Fuzz tests for any parser, decoder, or normalizer of untrusted input.
- **SHOULD** Seed corpus from prior bug reports.

### 7.7 Benchmarks
- **MUST** `b.ReportAllocs()` in every benchmark.
- **MUST** Loop body runs `b.N` times; setup uses `b.ResetTimer()`.
- **SHOULD** Compare runs with `benchstat`.

### 7.8 Coverage
- **SHOULD** Track coverage trend, not absolute number.
- **MUST NOT** Add tests with no assertions to game coverage.

---

## §8 Performance & Reliability

### 8.1 Profiling Workflow
- **MUST** `net/http/pprof` on a **private** port only.
- **MUST** Match symptom to profile type:
  - High CPU → CPU profile
  - Memory growth → two heap profiles spaced apart, diff with `-base`
  - Goroutine count rising → goroutine profile
  - Latency without CPU → block profile
  - Lock contention → mutex profile
- **MUST** Collect profiles under load, not at idle.
- **CONSIDER** PGO (Go 1.21+) with recent production CPU profile as `default.pgo` (~3% CPU win).

### 8.2 Allocations & Escape Analysis
- **MUST** Hot paths profiled with `b.ReportAllocs()`.
- **SHOULD** `go build -gcflags="-m -m"` to inspect escape analysis.
- **SHOULD** Preallocate slices/maps when size is known: `make([]T, 0, n)`.
- **SHOULD** `sync.Pool` for large, short-lived, hot-path allocations.
- **CONSIDER** Replace `fmt.Sprintf` on hot paths with `strconv` or concatenation.

### 8.3 Resource Hygiene
- **MUST** Every `os.Open`, `net.Dial`, `sql.DB.Query`, `http.Get` paired with `defer Close()`.
- **MUST** `sql.DB` and `http.Client` are long-lived shared values — created once at startup.
- **MUST** Outbound `http.Client` has explicit timeout (`Timeout: 10*time.Second`).
- **MUST** `http.Server` sets `ReadHeaderTimeout` (+ `ReadTimeout`, `WriteTimeout`, `IdleTimeout`).
- **SHOULD** Connection pools have explicit `SetMaxOpenConns`, `SetMaxIdleConns`, `SetConnMaxLifetime`.

### 8.4 Graceful Shutdown
- **MUST** Servers trap `SIGTERM`/`SIGINT` via `signal.NotifyContext` and call `Shutdown(ctx)` with bounded deadline.
- **MUST** In-flight requests finish; new connections rejected during shutdown.
- **SHOULD** Health-check endpoints flip to "not ready" before the grace period.

### 8.5 Observability
- **MUST** Structured logging (`log/slog`, `zap`, `zerolog`). No `log.Printf("%v: %v", k, v)`.
- **MUST** Every request-path log carries request ID and trace ID.
- **SHOULD** RED metrics per endpoint; USE metrics per resource.
- **SHOULD** Distributed tracing (OpenTelemetry) on every outbound call.

---

## §9 Security & Supply Chain

### 9.1 Vulnerability Management
- **MUST** `govulncheck ./...` in CI; blocks merge on reachable findings.
- **MUST** Fix via `go get pkg@fixed-version && go mod tidy`; re-run scan.
- **SHOULD** Weekly `govulncheck` against `main` even without PRs.

### 9.2 Module & Dependency Hygiene
- **MUST** `go.sum` committed.
- **MUST** `go mod tidy` in CI; fail on diff.
- **MUST** Keep `GOPROXY=https://proxy.golang.org,direct` and `GOSUMDB=sum.golang.org` unless air-gapped.
- **SHOULD** Audit every new direct dependency in review.

### 9.3 Input Validation
- **MUST** All external input validated at the boundary — parse, don't validate.
- **MUST** Parameterized SQL only; never string-concatenate queries.
- **MUST** `html/template` for HTML (auto-escaping); `encoding/json` for JSON.
- **SHOULD** `http.MaxBytesReader` on request bodies.

### 9.4 Crypto & Secrets
- **MUST** `crypto/rand` for tokens, IDs, nonces — never `math/rand`.
- **MUST** `crypto/subtle.ConstantTimeCompare` for secret comparison.
- **MUST** Passwords: `bcrypt`, `argon2id`, or `scrypt` — never SHA-family alone.
- **MUST** TLS `MinVersion: tls.VersionTLS12`.
- **MUST** Secrets from env vars or secret manager; never committed or logged.
- **SHOULD** `Redact()` method or `go-redact` library to prevent accidental logging of sensitive fields.

### 9.5 Safe Defaults
- **MUST** Start in most restrictive configuration; opt in explicitly.
- **MUST** No package-level mutable globals affecting security behavior.
- **CONSIDER** `gosec` in `golangci-lint` for foot-gun detection.

---

## §10 Quick Reference (Fast PR Review)

### Mechanical
- [ ] `gofmt`/`goimports` clean, `go vet` clean, `staticcheck` clean.
- [ ] `go test -race ./...` passes.
- [ ] `go mod tidy` produces no diff.
- [ ] `govulncheck ./...` clean.

### Naming & Style
- [ ] Names short locally, descriptive at distance; receivers 1–2 letters, consistent.
- [ ] Initialisms uppercased as a unit (`URL`, `ID`, `HTTP`).
- [ ] Exported identifiers have doc comments starting with the identifier name.
- [ ] No god packages (`util`, `common`, `helpers`).

### Errors
- [ ] No `_ = err`. Every error checked.
- [ ] Wraps use `%w` and a short noun-phrase context (no `failed to`).
- [ ] `errors.Is` / `errors.As` for inspection; sentinels named `Err...`.
- [ ] No `panic` in library code; `main` exits via `os.Exit(1)`.

### Concurrency
- [ ] `ctx context.Context` is first param of any I/O or goroutine-spawning function.
- [ ] `defer cancel()` immediately follows every `context.With...`.
- [ ] Every `go` statement: clear owner + clear exit condition.
- [ ] `errgroup` for fan-out; bounded concurrency.
- [ ] `http.Response.Body` closed/drained; `sql.Rows.Close` deferred; tickers stopped.
- [ ] `goleak.VerifyTestMain` in packages with concurrent code.

### Design
- [ ] Accept interfaces, return concrete types; interfaces at the consumer.
- [ ] Functional options for optional config only; required params positional.
- [ ] Zero-value usability where feasible; otherwise `New*` with validation.
- [ ] No reflexive getters/setters; no god types.

### Architecture
- [ ] `internal/` enforces privacy; `cmd/` only for multi-binary repos.
- [ ] Domain-sliced packages; no technical-layer slicing.
- [ ] Core depends on ports; adapters depend on core. No framework types in core.
- [ ] One `go.mod` per release-coupled unit.

### Testing
- [ ] Table-driven with `t.Run` subtests.
- [ ] `t.Parallel()` is first statement; called before `context.WithTimeout`.
- [ ] Fakes preferred over mocks; golden files only under `testdata/`.
- [ ] Fuzz tests for any parser/decoder of untrusted input.

### Performance & Reliability
- [ ] Outbound `http.Client` and `http.Server` have explicit timeouts.
- [ ] `sql.DB` / `http.Client` are long-lived shared instances.
- [ ] Graceful shutdown via `signal.NotifyContext` + `Shutdown(ctx)`.
- [ ] Structured logging with request/trace IDs; RED + USE metrics.

### Security
- [ ] Parameterized SQL; `html/template` for HTML; `crypto/rand` for tokens.
- [ ] Passwords: `bcrypt`/`argon2id`; secrets from env/secret manager, never logged.
- [ ] `http.MaxBytesReader` on request bodies; TLS 1.2+.

---

## Key References

| # | Title | URL |
|---|-------|-----|
| — | Effective Go | https://go.dev/doc/effective_go |
| — | Go Wiki: Code Review Comments | https://go.dev/wiki/CodeReviewComments |
| — | Google Go Style Guide | https://google.github.io/styleguide/go/ |
| — | Uber Go Style Guide | https://github.com/uber-go/guide/blob/master/style.md |
| — | Go Wiki: Table-Driven Tests | https://go.dev/wiki/TableDrivenTests |
| — | govulncheck | https://pkg.go.dev/golang.org/x/vuln/cmd/govulncheck |
