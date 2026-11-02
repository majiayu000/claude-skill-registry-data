---
name: scaffold-go-service
description: Use when starting a Go HTTP service or adding one to a repo with no Go module yet — scaffolds stdlib net/http (1.22+ routing), cmd/ and internal/ layers, slog JSON logs, validated env config, problem+json errors, health/readiness, graceful shutdown and a golangci-lint v2 config.
---

# Scaffold Go Service

Rationale and rules: [go-patterns.md](go-patterns.md). Full file contents: [go-files.md](go-files.md). Shared standards: [service-layout.md](../_shared/service-layout.md), [config.md](../_shared/config.md), [stack-versions.md](../_shared/stack-versions.md).

## 1. Audit (change nothing)

```bash
cat .claude/stack-profile.md ~/.claude/stack-profile.md 2>/dev/null   # backend.track, database.orm, tests.layout, task_runner, observability
ls go.mod go.work .golangci.yml .golangci.yaml cmd internal 2>/dev/null
head -3 go.mod 2>/dev/null; go version; golangci-lint --version 2>/dev/null
grep -rlE 'go-chi/chi|gin-gonic/gin|labstack/echo|gofiber' --include=go.mod . 2>/dev/null
```

Read the profile first; detect only what it leaves open ([stack-profile.md](../../core/_shared/stack-profile.md)).
- `backend.track` is set and is not `go`: stop and name the track the profile says; suggest the matching scaffold skill.
- `backend.track` is unset and a router framework (`chi`, `gin`, `echo`, `fiber`) is already in `go.mod`: keep it, adapt step 5 (routes registered on that router). Do not ask.
- No Go toolchain: tell the user which Go line to install ([stack-versions.md](../_shared/stack-versions.md)); do not scaffold blind.

## 2. Decide

- No `go.mod`: full scaffold (steps 3 to 7). The module path comes from `git remote get-url origin` (`github.com/<org>/<repo>`), else ask once; never leave `example.com/svc`.
- `go.mod` present, no `cmd/<svc>` or `internal/`: add the layers around the existing code; do not move existing packages without being asked.
- All present and step 7 passes: report "already in place" and stop.

## 3. Detect track

| Question | Source | Default |
|---|---|---|
| Router | profile or `go.mod` | stdlib `http.ServeMux` with `GET /notes/{id}` patterns. `chi` only if already used, see [go-patterns.md](go-patterns.md) |
| Service name | repo folder name, kebab-case | `svc` in the files becomes this name |
| Database | `database.orm` | `sqlc`: add `internal/repository/db/` (sqlc output) and a `pgxpool` seam in `internal/platform/db/` via the sqlc skill of this catalogue; then a readiness check. `none`: skip |
| Tests | `tests.layout` | unit tests always `*_test.go` beside the code (Go convention); `tests-dir` applies to integration tests in `tests/` |
| Observability | `observability.otel` | `true`: bootstrap the SDK in `internal/platform/` before the logger ([observability.md](../../core/_shared/observability.md)) |
| Task runner | `task_runner` | `just`: recipes `run`, `test`, `lint`, `build` that call the commands in step 7 |

## 4. Install only what is missing

```bash
go mod init <module-path>          # only when go.mod is missing; writes the current go line
brew install golangci-lint          # or mise / the release binary; confirm it prints v2.x
```

The scaffold has no third-party runtime dependencies. Check `golangci-lint --version` against [stack-versions.md](../_shared/stack-versions.md); v1 configs do not load in v2.

## 5. Generate the seams

Create the files from [go-files.md](go-files.md), skipping any that exist. Replace `example.com/svc` with the module path in every import.

```
cmd/<svc>/main.go                        composition root, signal handling, graceful shutdown
internal/config/config.go                Load(lookup) -> Config, every invalid key reported
internal/platform/logging/logging.go     slog JSON, contract field names, redaction
internal/transport/httpapi/{server,problem}.go   routes, middleware, problem+json, readiness
internal/service/*.go                    use cases, no net/http
internal/repository/*.go                 storage; the only layer with SQL
.golangci.yml  .env.example
*_test.go beside each package
```

Rename `notes` to the first real module, or keep it as the worked example until one exists.

## 6. Wire

- `.gitignore`: add `/bin/`, `.env`, `coverage.out`.
- Local run: `set -a; . ./.env; set +a; go run ./cmd/<svc>`. Go does not read `.env`; see [config.md](../_shared/config.md).
- Readiness: add one `httpapi.ReadinessCheck{Name, Check}` per dependency in `main.go`. `Check` receives a context with a 2 s deadline.
- Shutdown: put pool close and telemetry flush after `srv.Shutdown`, in `run()`. Keep `ReadHeaderTimeout` set: the zero value of `http.Server` has no timeouts.
- Request context: handlers and services pass `r.Context()` down; repositories take `ctx` first. `BaseContext` ties every request to the signal context.
- `go.mod`: `go mod tidy` once; commit `go.sum`; CI runs `go mod verify` ([version-protocol.md](../../core/_shared/version-protocol.md)).
- OpenAPI is not generated here: stdlib handlers carry no schema. Add `oapi-codegen` or a hand-kept `openapi.yaml` when clients need one.
- CI, Docker and deploy are out of scope; the `devcore` and `infraskills` plugins own them.

## 7. Verify

```bash
gofmt -l .                          # expect: no output
go vet ./... && go test ./...       # expect: ok for config, logging, httpapi
golangci-lint config verify && golangci-lint run ./...   # expect: 0 issues
go build -o bin/<svc> ./cmd/<svc> && PORT=8131 ./bin/<svc> &   # expect JSON line "message":"listening"
curl -s localhost:8131/readyz       # expect {"status":"ok"}
curl -si localhost:8131/nope        # expect 404 and Content-Type: application/problem+json
PORT=abc ./bin/<svc>                # expect "fatal: config: PORT: ..." and exit 1
kill -TERM %1                       # expect "shutting down" in the log, exit code 0
```

A second run of this skill finds everything in place and changes nothing.

## References

- [go-patterns.md](go-patterns.md): why each choice, when to deviate.
- [go-files.md](go-files.md): the files.
- [service-layout.md](../_shared/service-layout.md), [config.md](../_shared/config.md).
- [logging-contract.md](../../core/_shared/logging-contract.md), [security-baseline.md](../../core/_shared/security-baseline.md).
