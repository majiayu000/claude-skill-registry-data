---
name: nethttp-architect
version: 1.0.2
description: Framework-specific delta on rest-api-architect — Go stdlib net/http (Go 1.22+ ServeMux, no router) on Go 1.26. Feature layout, struct-tag validation, RFC 9457 errors, JWT or IdP auth, graceful shutdown, OpenAPI via kin-openapi. Read rest-api-architect first for the cross-cutting REST conventions. Use when scaffolding or reviewing a stdlib net/http service.
---

# net/http Architecture

Targets the stdlib **`net/http`** on **Go 1.26**, using the Go 1.22+ enhanced `ServeMux` (method matching, path variables, host matching) — no router framework. Companion to [go-architect](../../languages/go-architect/SKILL.md), [rest-api-architect](../../protocols/rest-api-architect/SKILL.md), and [sql-architect](../../databases/sql-architect/SKILL.md). Implementation skeletons in [RECIPES.md](RECIPES.md); pinned deps in [STACK.md](STACK.md).

## 1. Project structure — feature-based

Same shape as `gin-architect` and `fastapi-architect`: one folder per bounded context under `internal/`, each with `handlers.go`, `service.go`, `repo.go`, `dto.go`, `queries/`. Full tree in [RECIPES.md](RECIPES.md).

- **`handlers.go`** depends on `service.go`; never reaches into `repo.go` directly.
- **`service.go`** is pure Go — no `net/http` imports. Easy to unit-test.
- **`dto.go`** holds wire types; never reuse domain structs as DTOs.

## 2. Routing — `http.ServeMux` with method patterns (Go 1.22+)

The stdlib `ServeMux` supports method matching, path wildcards (`{id}`), and host matching. No third-party router needed. Registration skeleton in [RECIPES.md](RECIPES.md).

- **Method patterns:** `"GET /v1/users/{id}"` — method + path in one string. Mismatched methods auto-return `405 Method Not Allowed`.
- **Path variables:** `id := r.PathValue("user_id")` — typed parsing happens in your handler.
- **Trailing slash:** `"GET /v1/users/"` matches everything under the prefix; `"GET /v1/users/{$}"` matches only the exact path. Be explicit.
- **No "group" abstraction in stdlib** — write the prefix per route or use a small helper. Don't reach for a router framework just for syntactic sugar.

## 3. Request validation

`go-playground/validator` (canonical per [go-architect](../../languages/go-architect/SKILL.md#11-dependencies--logging)) — bind via `json.NewDecoder(r.Body).Decode(&req)` then `validate.Struct(&req)`.

```go
type CreateUserReq struct {
    Email    string `json:"email"    validate:"required,email"`
    Password string `json:"password" validate:"required,min=12"`
}
```

- **`json.Decoder.DisallowUnknownFields()`** at decoder construction — equivalent of Pydantic's `extra="forbid"`. Reject unknown fields rather than silently dropping them.
- **One shared `*validator.Validate`** stored on the handler, not per-request — instantiation is expensive.
- **Limit body size:** wrap `r.Body` with `http.MaxBytesReader(w, r.Body, 1<<20)` before decode — prevents memory exhaustion from oversized payloads.

## 4. Response shaping

A tiny helper to serialise JSON consistently — every handler uses it.

```go
func writeJSON(w http.ResponseWriter, status int, v any) {
    w.Header().Set("Content-Type", "application/json; charset=utf-8")
    w.WriteHeader(status)
    if v != nil {
        _ = json.NewEncoder(w).Encode(v)
    }
}
```

- **Set headers before `WriteHeader`** — once headers are sent, you can't change them.
- **`http.StatusNoContent`** for empty responses (skip `writeJSON` body).
- **Return DTOs, not domain types.** Same discipline as gin-architect.

## 5. Dependency injection

Explicit constructors. Dependencies wired in `main.go`; `*Deps` is passed where needed. For larger graphs, `uber-go/fx` (canonical per go-architect). Hand-wired is clearer for small services.

## 6. Lifespan & graceful shutdown

Identical pattern to gin-architect — the server abstraction is `http.Server`, not `*gin.Engine`. `signal.NotifyContext` for shutdown trigger; the cause records which signal (Go 1.26). All four timeouts (`ReadHeaderTimeout`, `ReadTimeout`, `WriteTimeout`, `IdleTimeout`) are **mandatory in production** — defaults are "unlimited," which is a DoS vector. Full skeleton in [RECIPES.md](RECIPES.md).

## 7. Middleware — function wrapping

stdlib has no middleware abstraction. The standard pattern: a function that takes `http.Handler` and returns `http.Handler`. Compose with a tiny `Chain` helper (in [RECIPES.md](RECIPES.md)).

- **Outermost first** in `Chain` — Recover wraps everything so even middleware panics are caught.
- **Standard chain order:** Recover → RequestID → SLog → CORS → GZip.
- **Auth is per-route, not global** — apply `AuthRequired` only where needed (see §8).
- **Never write your own logger middleware that calls `log.Printf`** — use `slog` (per go-architect).

## 8. Authentication & authorization

**Patterns** live in [rest-api-architect/AUTH_PATTERNS.md](../../protocols/rest-api-architect/AUTH_PATTERNS.md). stdlib specifics:

- **Pattern A — in-house JWT** via `golang-jwt/jwt/v5` + `argon2`. Middleware skeleton in [RECIPES.md](RECIPES.md).
- **Pattern B — external IdP**: `jwt.ParseWithClaims` with a `Keyfunc` that resolves keys via cached JWKS. Verify `aud` and `iss` explicitly.
- **Authorization per route, never global** — `RequireScope` middleware composed with `AuthRequired` (see [RECIPES.md](RECIPES.md)). When the wrap chain gets ugly, build a small helper that takes multiple `Middleware`s and the final handler.

## 9. Error handling — RFC 9457

Same `problem` package shape as `gin-architect`. Helpers take `http.ResponseWriter` + `*http.Request` instead of `*gin.Context`. Writer skeleton in [RECIPES.md](RECIPES.md). The `Recover` middleware catches panics and emits a 500 problem with the correlation id — never a stack trace.

## 10. Concurrency, not "background tasks"

Same guidance as gin-architect — Go has no FastAPI-style `BackgroundTasks`. Detach with `context.Background()`, log errors, set timeouts.

```go
ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
go func() {
    defer cancel()
    if err := h.svc.SendWelcomeEmail(ctx, user.ID); err != nil {
        slog.ErrorContext(ctx, "welcome email failed", "user_id", user.ID, "err", err)
    }
}()
```

## 11. Testing

`httptest.NewRecorder` + the handler directly — no real socket. Skeleton in [RECIPES.md](RECIPES.md).

- **`testing/synctest`** (per go-architect §9) for any test that depends on goroutine completion timing — deterministic without `time.Sleep`.
- **Table-driven** request-validation tests.

## 12. OpenAPI generation

stdlib `net/http` has no annotation-based generator like `swaggo/swag` (which is Gin-coupled). Two practical options:

- **`getkin/kin-openapi`** — write the OpenAPI 3.1 spec in code, serve it at `/v1/openapi.json`, optionally use it for runtime request validation. The intended choice for stdlib.
- **Hand-written `openapi.yaml`** committed to the repo, served as a static file. Cheapest, but drifts; pair with the OpenAPI snapshot test from [rest-api-architect §15](../../protocols/rest-api-architect/SKILL.md#15-openapi-as-the-source-of-truth).

CI snapshot-tests the spec either way.

## When to pick `net/http` over Gin

- **Minimal dependencies** matter (binary size, supply chain, audit).
- **Tight integration with stdlib middleware ecosystem** (third-party `func(http.Handler) http.Handler` chains work everywhere).
- **Forward compatibility** — Go's HTTP server gets faster every release; framework-coupled code lags.
- **Predictable behavior** — no framework-specific surprises (recovery semantics, body re-reads, etc.).

Pick **Gin** when: richer middleware/plugin ecosystem out of the box, team familiar with framework patterns, or you need features Gin provides that aren't in stdlib. Both bundles (`gin` and `nethttp`) are valid; this skill targets `nethttp` projects.
