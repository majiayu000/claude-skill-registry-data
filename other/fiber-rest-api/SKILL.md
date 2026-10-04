---
name: fiber-rest-api
category: api
description: Use when adding or changing a Go HTTP endpoint — Fiber v2 or v3 (detect which), thin handlers, central error mapping, boundary validation; the same rules apply to net/http, chi, echo or gin
tech_stack: Go
source: Fiber docs (MIT), adapted
---
# Go HTTP Endpoint Patterns

## Overview

A handler is a translator: HTTP in → service call → HTTP out. Business logic never lives there. The recurring defects are fat handlers, per-handler error mapping that drifts, endpoints that quietly drop the auth middleware their neighbors have, and copying a value Fiber is about to reuse.

**Core principle:** handlers parse, validate, delegate, and map. Nothing else.

## Detect the repo's router and framework version first

```
grep -E 'gofiber/fiber/v[23]|go-chi/chi|labstack/echo|gin-gonic/gin' go.mod
```

Never change the router or the Fiber major version in a feature task; a repo on Fiber v2 stays v2 (security-fix branch only). A brand-new repo with no router yet gets Fiber v3 (needs Go ≥1.25) unless the task says otherwise.

## Fiber v2 → v3

| | v2 | v3 |
|---|---|---|
| Handler signature | `func(c *fiber.Ctx) error` | `func(c fiber.Ctx) error` |
| Body | `c.BodyParser(&req)` | `c.Bind().Body(&req)` |
| Query / params | `c.QueryParser` / `c.ParamsParser` | `c.Bind().Query` / `c.Bind().URI` |
| Struct tag for path params | `params:` | `uri:` |
| Typed query helper | `c.QueryInt("limit", 20)` | `fiber.Query[int](c, "limit", 20)` |
| Go-standard request context | `c.UserContext()` | `c.Context()` |
| Raw fasthttp context | `c.Context()` (returns `*fasthttp.RequestCtx`) | `c.RequestCtx()` |
| Request id from context | `c.Locals("requestid")` | `requestid.FromContext(c)` |
| Static files / sub-app mount | `app.Static(...)` / `app.Mount(...)` | `static.New(...)` / `app.Use(...)` |

`fiber migrate --to v3` exists for a dedicated upgrade task; never fold a framework-major bump into a feature task.

**The v2 bug this corrects:** on Fiber v2, `c.Context()` returns the pooled `*fasthttp.RequestCtx`, not the request-scoped `context.Context` — passing it where a `context.Context` is expected either fails to compile or silently drops whatever middleware put into the real context (auth claims, request id, trace span). Use `c.UserContext()` on v2.

## Rules

- **Thin handlers:** parse/validate input → call the application service → map result to response DTO. No business logic, no SQL, no cross-entity rules in the handler.
- **Explicit DTO structs** aligned with domain types — never `map[string]any`.
- **Validate and bound all input at the boundary:** lengths, ranges, enum values, UUID parsing (`go-playground/validator` v10 if the repo already uses it; v3 has a `StructValidator` hook). Reject early with 4xx and a field-specific message in the repo's one error shape (see api-design-conventions).
- **Map domain errors to status in ONE place** (a shared `ErrorHandler` / mapper), not per handler, so the mapping can't drift. Show it mapping `errors.Is`/`errors.As` against domain sentinel errors to status + the error body.
- **New endpoints get the SAME middleware chain** (auth, logging, request-id) as their neighbors — copy the adjacent route's wiring, don't invent one.
- **Zero-allocation rule (Fiber-specific):** values Fiber hands you from `c.Params`/`c.Query`/`c.Body`/`c.Get` are only valid for the lifetime of the handler call — Fiber reuses the underlying buffer across requests. `strings.Clone` (or otherwise copy) anything you store in a struct that outlives the request, send to a goroutine, or put in a cache, unless the app is configured with `Immutable: true`.
- **Bound the request body:** `fiber.Config{BodyLimit: ...}` (v2/v3 default 4 MB) or `http.MaxBytesReader` on net/http — don't rely on the default alone for upload endpoints.

## net/http (Go ≥1.22, when the repo has no router)

```go
mux.HandleFunc("POST /tasks/{id}/children", h.CreateChild)
id := r.PathValue("id")
r.Body = http.MaxBytesReader(w, r.Body, maxBody)
```

## Worked Example

```go
func (h *TaskHandler) Create(c fiber.Ctx) error {
    var req createTaskRequest
    if err := c.Bind().Body(&req); err != nil {
        return fiber.NewError(fiber.StatusBadRequest, "invalid body")
    }
    if err := req.validate(); err != nil {
        return fiber.NewError(fiber.StatusBadRequest, err.Error())
    }
    task, err := h.svc.Create(c.Context(), req.Title)
    if err != nil {
        return err
    }
    return c.Status(fiber.StatusCreated).JSON(taskResponseFrom(task))
}
```

The title-length rule lives in the service/domain, not the handler. The central error middleware maps `domain.ErrInvalidTitle → 400`, `domain.ErrConflict → 409` — every handler benefits.

## Handler test in-process (no network)

```go
req := httptest.NewRequest(http.MethodPost, "/tasks", strings.NewReader(body))
req.Header.Set("Content-Type", "application/json")
resp, err := app.Test(req)       // v2: app.Test(req, -1)
// v3:  app.Test(req, fiber.TestConfig{Timeout: 0})
```
Assert status code and decoded body — this is still a unit test; it does not replace running the real service once (backend-runtime-check).

## Common Mistakes

- Business logic or SQL in the handler.
- `map[string]any` request/response instead of DTOs.
- Each handler mapping its own errors to codes → drift.
- A new route missing the auth middleware its neighbors have.
- 500 for a validation failure.
- Storing a value read from `c.Params`/`c.Query`/`c.Body` past the handler without copying it first.
- Passing v2's `c.Context()` where the request's `context.Context` is needed.

## Red Flags

- A handler longer than ~30 lines.
- `pgx`/repository calls inside a handler.
- A route registered without the neighbor's middleware chain.
- A struct field or goroutine capturing a byte slice straight from `c.Body()`/`c.Params()`.
