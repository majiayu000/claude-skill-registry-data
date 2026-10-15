---
name: tech
description: Use when writing or reviewing Go code in fusionaly-oss — adding routes, handlers, domain contexts, background jobs, the manager CLI, wiring the app, or writing tests. Covers the cartridge framework, matcha for the manager, Phoenix Contexts, lifecycle/shutdown, and the test conventions.
---

# Fusionaly Tech & Conventions

## Overview

Fusionaly is a Go monolith (Fiber + GORM + SQLite, React/Inertia frontend). The guiding principle: **the libraries do the heavy lifting; app code stays thin and domain-focused.** Boilerplate — HTTP server, routing, sessions, CSRF, rate limiting, static serving, Inertia, SQLite WAL/serialized writes, graceful shutdown, deploys — lives in `cartridge` (the app) and `matcha` (the manager). The app *reuses* them; it does not re-implement them.

This is a deliberate, pragmatic stance: Go favors explicit, no-magic code, but here we push recurring infrastructure into a shared library so each app is a small amount of clean domain code on top. Don't hand-roll what the library already provides.

## The stack at a glance

| Concern | Owner | Where |
|---|---|---|
| HTTP server, lifecycle, graceful shutdown, routing, sessions, CSRF, rate limiting, static/Inertia | **cartridge** | `cartridge.NewApplication(...)` |
| SQLite connection, WAL, serialized writes, migrations plumbing | **cartridge/sqlite** + `internal/database` | `dbManager`, `cartridge.Write` |
| Background jobs lifecycle (start/stop with the server) | **cartridge** `BackgroundWorker` | `internal/jobs` |
| Install / update / deploy / backup / image swap (self-hosted ops) | **matcha** | `cmd/manager` |
| Domain logic (analytics, events, websites, feed, agent, …) | **app** (Phoenix Contexts) | `internal/<domain>/` |
| Frontend | React 19 + Inertia | `web/src` |

## cartridge: configure, don't reinvent

cartridge is our own framework — repo **https://github.com/karloscodes/cartridge** (Go module `github.com/karloscodes/cartridge`). When something feels like boilerplate, check there before writing it.

The whole app boots by handing cartridge a config struct. `internal/app.go` is the one place that wires it, and it's ~120 lines:

```go
app, err := cartridge.NewApplication(cartridge.ApplicationOptions{
    Config:            cfg,
    Logger:            logger,                 // cartridge.NewLogger(cfg, nil)
    DBManager:         dbManager,              // wraps cartridge/sqlite
    ServerConfig:      serverConfig,           // CORS, SecFetchSite, ProxyHeader, StaticFS
    RouteMountFunc:    MountAppRoutes,         // your routes
    BackgroundWorkers: []cartridge.BackgroundWorker{jobsManager},
})
// Application embeds *cartridge.Application and adds DBManager.
```

cartridge then owns the server, signal handling, and graceful shutdown — including stopping the registered `BackgroundWorker`s. The app never writes a `main()` event loop or shutdown handler.

Key sub-packages you reuse (don't reinvent): `cartridge/inertia` (`inertia.RenderPage`), `cartridge/cache` (`cache.Cache[K,V]`), `cartridge.Write` / `ctx.WriteTx` (queued writes; `sqlite.ErrBusy` when the queue is full), `cartridge/testsupport` (test DBs), flash, session.

## Phoenix Contexts: thin handlers, fat contexts

Each domain is a package under `internal/<domain>/` exposing **top-level functions that take `*gorm.DB`** — no service objects, no HTTP imports.

```go
// internal/settings/setting.go  — a context: plain functions + a model
type Setting struct { ID uint; Key string; Value string /* ... */ }

func GetAgentAPIKey(db *gorm.DB) (string, error) { /* ... */ }
func RegenerateAgentAPIKey(db *gorm.DB) (string, error) { /* ... */ }
```

```go
// internal/http/*_handler.go — handlers stay thin: parse, delegate, render
func DashboardAction(ctx *cartridge.Context) error {
    metrics := analytics.GetDashboardMetrics(ctx.DB(), websiteID, tf)  // context does the work
    return inertia.RenderPage(ctx.Ctx, "Dashboard", inertia.Props{"metrics": metrics})
}
```

Rules: contexts never import `internal/http`; handlers never hold business logic; writes that can come in volume (ingest, event processing, jobs) go through `cartridge.Write(ctx, dbManager, fn)` or `ctx.WriteTx(fn)`: one write at a time, in order, and `sqlite.ErrBusy` (answer 503 + Retry-After) when the queue is full. Never retry on the server, and never mark an event failed because of `ErrBusy`. Rare user actions (password change, logout) may use `db.Transaction`. Pages use Inertia + PRG (no `fetch()` for page data).

## matcha: the manager owns ops

matcha is our own deploy/update tool — repo **https://github.com/karloscodes/matcha** (Go module `github.com/karloscodes/matcha`). `cmd/manager` is a thin wrapper over `matcha` — install, update, deploy, backup, image swap are library calls, not bespoke shell:

```go
m := matcha.New(matcha.Config{Name: "fusionaly", AppImage: "karloscodes/fusionaly:latest",
    HealthPath: "/_health", Volumes: []string{"/app/storage", "/app/logs"},
    CronUpdates: true, Backups: true, ManagerRepo: "karloscodes/fusionaly-oss"})
// commands delegate: m.Install(), m.Update(), m.Deploy(), m.BackupDB(), m.SetImage(...)
```

Add a manager command by mirroring an existing one (`runMigrateToOSS` mirrors the structure of the others). Don't script Docker by hand.

## Background jobs & shutdown

Jobs are a `BackgroundWorker` registered with cartridge, so they start and stop with the server. The scheduler runs each job on a ticker through `executeJobSafely` (panic-safe, single-flight). A job is just a struct with `Run() error` — the scheduler owns timing; jobs never spin their own goroutine/ticker. See `internal/jobs/scheduler.go` + `internal/jobs/feed.go`.

## Testing conventions

- **Real behavior, no mocks.** Use a real SQLite test DB via `testsupport.SetupTestDBManager(t)` (wraps `cartridge/testsupport`). Register new models in `testsupport.allModels()`.
- **Env:** tests require `FUSIONALY_ENV=test` — run with `make test` (sets it for you), not bare `go test`.
- **Four phases** with blank lines between: setup, exercise, verify, teardown. Assert with testify `assert`/`require`.
- **Contexts via `t.Run`** for related scenarios ("with valid key", "with no key"). 
- **Table-driven only when the cases are open-ended/homogeneous** — e.g. a list of SQL strings each expected to be rejected (`internal/agent/agent_test.go` `TestValidateReadOnlyQuery`). Don't force a table when a few `t.Run` blocks read clearer.
- E2E (`e2e/`) is Playwright, **sequential** (`workers: 1`, story order 001→…); specs build on each other (onboarding creates the user — setup does not). Wait on conditions, never race `networkidle`.

## Common mistakes

| Mistake | Instead |
|---|---|
| Writing a `main()` loop, shutdown handler, or middleware cartridge already provides | Configure `ApplicationOptions`; let cartridge own it |
| Business logic in an `internal/http` handler | Move it to the domain context; handler just parses + renders |
| A context importing `internal/http` | Contexts are HTTP-agnostic; pass `*gorm.DB` |
| Raw `db.Exec` writes scattered around | `cartridge.Write(...)` (single-writer queue) |
| Hand-rolled Docker/deploy logic in the manager | A `matcha` call |
| Mocks in tests | Real test DB via `testsupport` |
| A job that starts its own ticker/goroutine | `Run() error` + register in the scheduler |
| `fetch()` for page data | Inertia props + PRG |
