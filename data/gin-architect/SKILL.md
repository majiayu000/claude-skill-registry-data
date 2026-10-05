---
name: gin-architect
version: 1.0.2
description: Framework-specific delta on rest-api-architect — Gin 1.12 on Go 1.26. Feature layout, struct-tag validation, RFC 9457 errors, in-house JWT or external IdP, route groups for URL-prefix versioning, OpenAPI. Read rest-api-architect first for the cross-cutting REST conventions. Use when scaffolding or reviewing a Gin service.
---

# Gin Architecture

Targets **Gin 1.12** on **Go 1.26**. Companion to [go-architect](../../languages/go-architect/SKILL.md), [rest-api-architect](../../protocols/rest-api-architect/SKILL.md), and [sql-architect](../../databases/sql-architect/SKILL.md). Implementation skeletons in [RECIPES.md](RECIPES.md); pinned deps in [STACK.md](STACK.md).

## 1. Project structure — feature-based

One folder per bounded context. Each feature owns its routes, service, repo, DTOs, and SQL files. Mirrors [fastapi-architect](../fastapi-architect/SKILL.md) so polyglot teams can navigate either side. Full tree in [RECIPES.md](RECIPES.md).

- **`handlers.go`** depends on `service.go`; never reaches into `repo.go` directly.
- **`service.go`** is pure Go — no `gin` imports. Easy to unit-test without a fake `*gin.Context`.
- **`dto.go`** holds wire types with `json:` and `binding:` (validator) tags. **Never reuse domain structs as DTOs** — that's how internal fields leak into the API.

## 2. Routing & versioning

URL-prefix versioning via route groups. One group per version, one sub-group per feature. Registration skeleton in [RECIPES.md](RECIPES.md).

- **One `Register(rg, deps)` function per feature** — keeps `main.go` thin.
- **Path params typed at parse time:** `id, err := uuid.Parse(c.Param("user_id"))` — return 400 on parse failure.
- **Use `gin.RouterGroup`, not bare `Engine.GET`,** so versioning + per-group middleware stays clean.

## 3. Request validation

Use struct tags with `go-playground/validator` (canonical per [go-architect](../../languages/go-architect/SKILL.md#11-dependencies--logging)). Bind via `c.ShouldBindJSON` / `c.ShouldBindUri` / `c.ShouldBindQuery` — never `c.MustBindWith` (panics; we don't panic in handlers).

```go
type CreateUserReq struct {
    Email    string `json:"email"    binding:"required,email"`
    Password string `json:"password" binding:"required,min=12"`
}
```

- **`binding:"required"`** on every field that isn't truly optional.
- **Custom validators** registered once at startup: `validate.RegisterValidation("uuid_v7", isUUIDv7)`.
- **`binding:"omitempty"`** on PATCH partial-update DTOs — let absent fields mean "leave unchanged."

## 4. Response shaping

- **Return DTOs, not domain types.** `c.JSON(200, dto.UserResponse{...})` — DTOs control what leaks.
- **`json:"-"`** on any DTO field that should never serialize (passwords, internal IDs).
- **Status code with `c.JSON(http.StatusCreated, ...)`** — explicit, not Gin's default 200.
- **Empty body uses `c.Status(http.StatusNoContent)`**, not `c.JSON(204, nil)` (sends `null`).

## 5. Dependency injection

Explicit constructors per [go-architect §3](../../languages/go-architect/SKILL.md#3-instantiation). No globals, no `init()` magic. Dependencies live in a `Deps` struct wired in `main.go`. For larger graphs use `uber-go/fx` (canonical per go-architect); for services with <10 dependencies, hand-wired is clearer.

## 6. Lifespan & graceful shutdown

Open shared resources in `main.go`, never per-request. Close them on shutdown signal via `signal.NotifyContext` (Go 1.26 records which signal fired). Full skeleton in [RECIPES.md](RECIPES.md).

- **`ReadHeaderTimeout`** is mandatory — without it, Slowloris can pin connections forever.
- **Graceful shutdown timeout** > longest expected request duration.

## 7. Authentication & authorization

**Patterns** (in-house JWT vs external IdP, Argon2id, JWT lifetimes, JWKS verification, switching criterion) live in [rest-api-architect/AUTH_PATTERNS.md](../../protocols/rest-api-architect/AUTH_PATTERNS.md). Gin specifics:

- **Pattern A — in-house JWT** via `golang-jwt/jwt/v5` + `argon2` from `golang.org/x/crypto`. Middleware skeleton in [RECIPES.md](RECIPES.md).
- **Pattern B — external IdP**: `jwt.ParseWithClaims` with a `Keyfunc` that resolves keys via a JWKS client. Cache JWKS in-process with TTL.
- **Authorization per route, never global** — `RequireScope(...)` composed alongside `AuthRequired(secret)` on the route declaration (see [RECIPES.md](RECIPES.md)).

## 8. Error handling — RFC 9457 middleware

A central `problem` package emits `application/problem+json` (per [rest-api-architect §7](../../protocols/rest-api-architect/SKILL.md#7-error-contracts--rfc-9457-problem-details)). Handlers either call `problem.Render(c, p)` directly or `c.Error(err)` and let the recovery middleware convert. Renderer in [RECIPES.md](RECIPES.md).

- **One handler per domain-error family** — map known sentinel errors to `Problem` types in a single switch.
- **`gin.Recovery`** with a custom `RecoveryHandler` that emits a 500 `Problem` with `correlation_id` — never a stack trace.

## 9. Middleware order

Outermost first; order matters.

```go
r := gin.New()  // not gin.Default — we set logging ourselves
r.Use(
    middleware.RequestID(),             // 1. assign correlation_id
    middleware.SLog(),                  // 2. structured access log
    gin.Recovery(),                     // 3. convert panics → 500 problem
    middleware.CORS(cfg.CORS),          // 4. preflight handling
    gzip.Gzip(gzip.DefaultCompression), // 5. response compression
)
```

- **Never `gin.Default()`** in production — its logger writes unstructured text to stdout. Use `slog` (per go-architect).
- **Auth is per-route middleware**, never global (see §7).
- **Recovery before CORS** — a panic that bypasses CORS handler returns no headers; the browser shows a misleading CORS error.

## 10. Concurrency, not "background tasks"

Go has no FastAPI-style `BackgroundTasks`. To run work after the response, derive a new `context.Context` from `context.Background()` (request context is cancelled the moment the response writes), set a timeout, log errors. Anything serious (retryable, distributed, scheduled) belongs in a real task queue, not a goroutine.

## 11. Testing

`httptest.NewRecorder` + the engine directly — no real socket. Skeleton in [RECIPES.md](RECIPES.md).

- **Test-DB strategy:** mirror `sql-architect` — wrap each test in a rolled-back transaction, or use a per-test schema with `golang-migrate`.
- **Table-driven tests** (per go-architect §9) for request validation paths — one row per (input, expected status, expected error type).

## 12. OpenAPI generation

- **Default: `swaggo/swag`** — `// @` annotation comments above handlers; `swag init` generates `docs/swagger.json` and `swagger.yaml`. Predictable, mature.
- **For full OpenAPI 3.1 control: `getkin/kin-openapi`** — write the spec in code; serve it; use it to validate requests at runtime. More work but no annotation noise.
- **CI snapshot-tests the spec** (per [rest-api-architect §15](../../protocols/rest-api-architect/SKILL.md#15-openapi-as-the-source-of-truth)).
- **Internal endpoints excluded** with `// @Hidden` (swag) or by not registering them in the spec route group.
