---
name: golang-arch
description: >
  Apply Go monorepo and hexagonal architecture decisions for 10–50 service
  codebases. Covers module layout, DDD package structure, dependency rules,
  linting boundaries, testing, CI/CD, and modern patterns. Triggers when user
  asks about "Go monorepo architecture", "hexagonal Go", "golang architecture
  review", "Go DDD layout", or invokes /golang-arch.
---

# Go Monorepo Architecture Skill

You are advising on Go monorepo architecture for a 10–50 service codebase with
a single `go.mod`, DDD/hexagonal (ports-and-adapters) design, GitHub Actions
CI/CD, and monorepo-wide releases. Use the decision framework below.

## 1. Module Layout

### Prefer the official Go layout

Follow `go.dev/doc/modules/layout`, not `github.com/golang-standards/project-layout`.

```
repo/
  go.mod
  go.sum
  cmd/                    # thin main packages only
    svc-orders/main.go
    svc-inventory/main.go
  internal/               # all application code
    shared/
      domain/             # cross-cutting value objects (Money, TenantID)
      events/             # cross-service event contracts
      platform/           # telemetry, HTTP server, DB helpers
      testhelpers/        # Testcontainers, fixtures
    orders/               # bounded context
      domain/
      application/
      adapter/
      port/
    inventory/
  api/                    # protobuf / OpenAPI specs
  build/                  # Dockerfiles
  deploy/                 # Helm / k8s
```

Rules:
- `cmd/` contains only wiring: config, telemetry, DB connection, DI, start server.
- `internal/` is module-private; use nested `internal/` to hide service internals.
- Avoid `pkg/` unless it marks stable public API staging.
- No `util`, `common`, `helpers`, `service`, `handler` god packages.

### Single `go.mod` vs `go.work`

Choose single `go.mod` when:
- release cadence is unified,
- ≤ 50 services,
- atomic cross-cutting changes are valuable,
- team size is ≤ 5–10 teams.

Use `go.work` only as a gitignored local dev convenience, never as a CI artifact.

Break to multi-module only when:
- services need incompatible major versions of the same dependency,
- release schedules genuinely diverge,
- `go.sum` becomes a persistent merge-conflict bottleneck.

### Toolchain directive

Use Go 1.21+ `toolchain` directive for reproducible builds:

```go
module github.com/myorg/myrepo

go 1.22.0
toolchain go1.22.3
```

In GitHub Actions:

```yaml
- uses: actions/setup-go@v5
  with:
    go-version-file: go.mod
```

## 2. Hexagonal Package Structure

Per bounded context:

```
internal/orders/
  domain/               # pure Go, no I/O
    model/              # aggregates, value objects, IDs
    repository/         # interfaces only
    service/            # domain services
    events/             # domain events
  application/          # use cases
    command/
    query/
    dto/
  adapter/              # driven adapters
    postgres/
    kafka/
    outbox/
    httpclient/
  port/                 # driving adapters
    rest/
    grpc/
```

Dependency rule (only inward):

```
domain ← application ← adapter
                     ← port
```

| Package | May import | Must not import |
|---|---|---|
| `domain/*` | stdlib, `internal/shared/domain` | adapter, application, port, infra libs |
| `application/*` | domain, `internal/shared/platform` | adapter, port, infra libs |
| `adapter/*` | domain, application, infra libs | port |
| `port/*` | application, domain | adapter internals |

### Domain layer rules

- Aggregates enforce invariants via exported methods; no setters.
- Value objects are immutable; constructors validate.
- Entity IDs are distinct types, not `string` aliases.
- Domain events are past-tense, versioned (`orders.v1.OrderCreated`).
- Repository interfaces live in `domain/repository/`; adapters implement them.
- Use `Reconstitute` for loading aggregates from storage without re-validating.

Example compile-time interface check:

```go
var _ repository.OrderRepository = (*postgres.OrderRepository)(nil)
```

### Adapter rules

- Wrap errors with context at the adapter: `fmt.Errorf("saving order %s: %w", id, err)`.
- Record OTel spans in adapters, not domain.
- Close resources: `rows.Close()`, `resp.Body.Close()`, `ticker.Stop()`.

### Port rules

- Handlers are thin: decode input, call application, encode output, translate errors.
- No infrastructure imports in handlers.

### Shared domain

Only extract to `internal/shared/domain/` when the type is:
- truly cross-cutting (TenantID, Money, EmailAddress),
- has no infrastructure imports,
- stable and domain-universal.

Never share full aggregates (`Order`, `Product`) across services; reference by ID.

## 3. Architecture Enforcement

### `internal/` visibility

Go's `internal/` rule prevents external modules from importing packages. It does
**not** prevent domain from importing adapter within the same bounded context.
Use linting for layer enforcement.

### `depguard` rules

Example `.golangci.yml` snippet:

```yaml
linters-settings:
  depguard:
    rules:
      domain-layer-purity:
        files:
          - "**/domain/**/*.go"
        deny:
          - pkg: "database/sql"
            desc: "domain layer must not import database/sql"
          - pkg: "github.com/jackc/pgx"
            desc: "domain layer must not import postgres driver"
          - pkg: "net/http"
            desc: "domain layer must not import HTTP packages"
```

Also consider `go-arch-lint` and architecture-as-tests for stricter enforcement.

## 4. Linting

Use `golangci-lint` v2 schema from the repository root with `./...`.

### Tier 1 — enable immediately

- `errcheck`
- `govet` with `shadow`
- `staticcheck`
- `unused`
- `ineffassign`
- `bodyclose`
- `noctx`
- `gofumpt`
- `misspell`
- `revive`

### Tier 2 — enable after codebase is clean

- `errorlint`
- `wrapcheck` (exclude own module)
- `nilnil`
- `exhaustive`
- `contextcheck`
- `spancheck`
- `sqlclosecheck`
- `rowserrcheck`
- `copyloopvar`
- `reassign`
- `predeclared`
- `sloglint`

### Security

- `gosec`
- `govulncheck ./...` in CI

### Race detector

Always run `go test -race ./...` in CI.

## 5. Testing

Test pyramid:

| Layer | Test type | Tooling |
|---|---|---|
| Domain | Unit tests | plain Go tests, no Docker |
| Application | Unit tests with fakes | in-memory repository implementations |
| Adapter | Integration tests | Testcontainers-Go, build tag `integration` |
| Port | Handler tests | `httptest.NewServer` |

Rules:
- Place `_test.go` next to code for white-box tests.
- Use `_test` package for black-box integration tests.
- Table-driven tests with `t.Run(tc.name, ...)`.
- `t.Parallel()` as first statement when safe.
- Fuzz parsers/decoders of untrusted input.
- Benchmarks use `b.ReportAllocs()` and `benchstat` for comparisons.

## 6. CI/CD

### PR pipeline

1. Lint: `golangci-lint run ./...`
2. Verify `go.mod`/`go.sum` tidy: `go mod tidy && git diff --exit-code`
3. Unit tests: `go test -short ./...`
4. Race tests: `go test -race ./...`
5. Integration tests: `go test -tags=integration ./...`
6. `govulncheck ./...`
7. Affected-change detection so one service change does not rebuild all 50.

### Cache

Cache `~/.cache/go-build`, `~/go/pkg/mod`, and `~/.cache/golangci-lint`.

### Release

Use GoReleaser for monorepo-wide releases; all services ship together.

## 7. Dependency Management

- Commit `go.mod` and `go.sum`.
- Run `go mod tidy` in CI and fail on diff.
- Use Dependabot/Renovate to serialize dependency updates.
- Avoid `replace` directives in single-module monorepos.
- Vendoring only for regulated industries or air-gapped builds.

## 8. Modern Patterns

- **CQRS**: separate command and query handlers; read models can differ from write models.
- **Outbox Pattern**: publish domain events transactionally via an outbox table.
- **Connect-go / Buf**: use `paths=source_relative`; version proto APIs under `v1/`, `v2/`.
- **OpenTelemetry**: trace every cross-service call; carry trace ID in logs; use RED/USE metrics.
- **slog**: structured logging; pass logger via context or explicit injection, not globals.
- **Generics**: use for genuine container/algorithm duplication; prefer `slices`/`maps`/`cmp` from stdlib.

## 9. Anti-Patterns to Reject

- Package-by-layer (`internal/handler`, `internal/service`, `internal/repository`).
- `Manager`/`Service`/`Handler` god structs.
- Reflexive getters/setters; public fields are idiomatic without validation.
- `interface{}/any` where concrete types or small interfaces work.
- `panic` in library code.
- Storing `context.Context` in a struct field.
- Passing request `ctx` to goroutines that outlive the request.
- `defer` inside hot loops without measurement.

## 10. Quick Reference

```bash
# List deps compiled into a service
go list -deps ./cmd/svc-orders/...

# Tidy and verify
go mod tidy && git diff --exit-code go.mod go.sum

# Lint all
golangci-lint run ./...

# Test with race detector
go test -race -timeout 5m ./...

# Integration tests only
go test -tags=integration ./...

# Vulnerability scan
govulncheck ./...
```

## Key References

- Official Go module layout: https://go.dev/doc/modules/layout
- Effective Go: https://go.dev/doc/effective_go
- Go Code Review Comments: https://go.dev/wiki/CodeReviewComments
- golangci-lint: https://golangci-lint.run/
- Testcontainers-Go: https://golang.testcontainers.org/
- OpenTelemetry Go: https://opentelemetry.io/docs/languages/go/
