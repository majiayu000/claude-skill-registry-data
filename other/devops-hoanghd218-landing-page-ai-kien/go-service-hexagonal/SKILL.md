---
name: go-service-hexagonal
description: Define, review, and scaffold Go service directory structures using hexagonal (ports-and-adapters / “jexagonal”) architecture and Go best practices. Use when creating or refactoring Go services, deciding package boundaries, organizing cmd/internal/api/config/deploy/migrations, or choosing layouts for common service types (HTTP REST API, gRPC API, async worker/consumer, scheduled job, CLI, multi-binary repos).
---

# Go Service Hexagonal

## Workflow

### 1) Choose the repo shape

- Use **single-service repo** when one deployable dominates the repo.
- Use **multi-binary repo** when multiple deployables share a domain and are released together (API + worker + migrator).
- Use **monorepo** when many services share tooling but keep each service isolated under `<service>/cmd/<service>-<binary>` and `<service>/internal/...`.

### 2) Choose the service kind

- HTTP REST/JSON API → use `references/layout-http-rest.md`
- gRPC API → use `references/layout-grpc.md`
- Worker/consumer/scheduler/job → use `references/layout-worker.md`
- CLI (ops tools, admin, local runner) → use `references/layout-cli.md`

### 3) Apply hexagonal (ports-and-adapters) boundaries

- Put **business rules** in `internal/domain`.
- Put **use cases** in `internal/app` and define **inbound ports** in `internal/interface`.
- Define **outbound ports** (interfaces to DB, queues, HTTP clients) in `internal/adapter`.
- Implement inbound adapters in `internal/interface/*` (primary) and outbound adapters in `internal/adapter/*` (secondary).
- Perform all wiring in a single composition root: `internal/bootstrap.Compose(settingsRepo)` and keep `cmd/*` thin.

Use `references/architecture-rules.md` as the dependency rulebook.

## Scaffolding

Run the scaffolder to generate a starting tree plus minimal compileable stubs:

`python3 scripts/scaffold_hex_service.py --root <repo> --service <name> --kinds http,worker`

HTTP scaffolding defaults to Echo. For explicit Echo:

`python3 scripts/scaffold_hex_service.py --root <repo> --service <name> --kinds http --http-framework echo`

For a pure `net/http` baseline:

`python3 scripts/scaffold_hex_service.py --root <repo> --service <name> --kinds http --http-framework nethttp`

HTTP scaffolds include `GET /health/live` and `GET /health/ready`, plus request logging using Logrus (`github.com/sirupsen/logrus`).

Optional (opt-in) HTTP debug endpoints:

- `--http-pprof` adds handlers under `GET /debug/pprof/*` (pprof index + profiles).
- `--http-trace` adds `GET /debug/pprof/trace` (execution trace).
- These run on a separate debug HTTP server and are activated only when `PPROF_PORT` is set (e.g. `PPROF_PORT=6060`); optionally set `PPROF_ADDR` to change the bind address (default `127.0.0.1`).
- The handler mux is scaffolded as a dedicated inbound adapter: `internal/interface/debughttp`.

For new projects, if `--module` is omitted the module path defaults to the `<repo>` folder name (no `github.com/...` assumption).
If `go.mod` is created (new project), the scaffolder runs `go mod tidy` to fetch dependencies (Echo + Logrus). Use `--skip-deps` to skip.

Generated projects include required `README.md`, `AGENTS.md`, and `Makefile` at repo root.
When HTTP is scaffolded, the project also includes `test/health_test.go`.

Then edit the generated packages to match your domain and ports.

## Reference Index

Read `references/index.md` and then open only the layout file(s) you need for the chosen service kind.
