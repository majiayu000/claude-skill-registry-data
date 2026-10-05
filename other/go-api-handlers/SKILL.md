---
name: go-api-handlers
description: Write or modify Gin HTTP handlers in the clean-arch API layer (internal/infrastructure/api/*_api.go). Use when adding a new endpoint/route, creating a new *_api.go file for a feature, or wiring a handler to a usecase. Enforces request parsing, error wrapping via HandleErr, response shaping, and the conventions below.
---

# Go API Handlers (Gin)

Authoritative style for the handler layer (`internal/infrastructure/api/*_api.go`) on the
clean-architecture path. Follow it exactly — these rules override generic Gin habits.
Existing handlers may predate this style; when you touch one, bring it into compliance.

## When to use

- Adding a new endpoint to an existing `*_api.go` file.
- Creating a new `*_api.go` file for a new clean-arch feature.
- Reviewing handler code for style compliance.

## Non-negotiable rules

**Structure**
- One file per feature: `internal/infrastructure/api/{feature}_api.go`, `package api`.
- Define a narrow `{Feature}Usecase` interface **in the handler file itself**, listing only
  the methods this handler calls. Never import the concrete `usecase.Xxx` struct — depend on
  the interface you declared.
- Handler struct holds the usecase interface as its only field:
  `{Feature}Handler struct { usecase {Feature}Usecase }`.
- Constructor `New{Feature}V2Handlers(r *gin.Engine, srv {Feature}Usecase)` builds the
  handler, opens `r.Group("/v2/{feature}")`, and registers every route. Wire the call into
  `internal/bootstrap/{feature}/setup.go`.
- Each route is a method returning `gin.HandlerFunc`; all logic lives in the returned
  closure, not the method body.

**Handler body**
- First line of every closure: `ctx := c.Request.Context()`.
- The handler has **zero business logic** — only: parse input → call usecase → shape
  response. Anything else belongs in the usecase.
- Path params: `id, err := uuid.Parse(c.Param("id"))`; wrap with
  `domain.WrapInvalidInput(err, "id must be valid")`.
- Optional query params (e.g. dates): guard on empty string before parsing, so an absent
  param leaves the zero value instead of erroring.
- JSON body: bind straight into the domain type — `c.ShouldBindJSON(&movement)` — wrapped
  with `domain.WrapInvalidInput(err, "invalid json body")`. Don't invent a separate request
  DTO unless the domain type genuinely can't represent the wire shape.
- Multi-field/derived input (e.g. building a `domain.Period` from `from`/`to` query params)
  goes in a private `h.parseX(c *gin.Context) (domain.X, error)` helper using the same wrap
  pattern, called from the route method.

**Error handling**
- Every error from parsing or from the usecase goes straight through
  `HandleErr(c, ctx, err)` followed by a bare `return`. Never hand-build a JSON error body
  in a handler — `HandleErr` / `toAPIError` in `errors_handler.go` own that mapping.
- If `toAPIError` has no case yet for a new domain/usecase sentinel error, add the case
  there. Don't special-case the error in the handler instead.

**Response shaping**
- If an `output.ToXOutput` mapper exists for the domain type, use it — don't return the raw
  domain struct when a mapper is available. If no mapper exists yet for the resource,
  returning the domain/usecase result struct directly is acceptable existing precedent
  (e.g. `statement_api.go`, `user_api.go`).
- Status code follows the outcome, not just the HTTP verb:
  - Created a new resource → `http.StatusCreated` + body.
  - Returns the affected resource (update, pay, revert, recalculate-with-result, etc.) →
    `http.StatusOK` + body.
  - No resource returned (delete, recalculate-without-result, etc.) →
    `c.Status(http.StatusNoContent)`, no body.
- A list endpoint that combines multiple slices gets a named local response struct (see
  `PeriodMovementsResponse` in `movement_api.go`) — never a bare `gin.H{}` or unnamed map.

## Canonical template

Copy this and adapt — it already encodes every rule above (JSON body + 201, path param +
optional query param + 200, derived input via helper, and 204-no-body).

```go
package api

import (
	"context"
	"net/http"
	"time"

	"personal-finance/internal/domain"
	"personal-finance/internal/domain/output"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
)

type (
	WidgetUsecase interface {
		Add(ctx context.Context, widget domain.Widget) (domain.Widget, error)
		Pay(ctx context.Context, id uuid.UUID, date time.Time) (domain.Widget, error)
		DeleteOne(ctx context.Context, id uuid.UUID) error
	}

	WidgetHandler struct {
		usecase WidgetUsecase
	}
)

func NewWidgetV2Handlers(r *gin.Engine, srv WidgetUsecase) {
	handler := WidgetHandler{usecase: srv}

	group := r.Group("/v2/widgets")
	group.POST("/", handler.Add())
	group.POST("/:id/pay", handler.Pay())
	group.DELETE("/:id", handler.DeleteOne())
}

// Add: JSON body bound straight into the domain type, 201 + mapped output.
func (h WidgetHandler) Add() gin.HandlerFunc {
	return func(c *gin.Context) {
		ctx := c.Request.Context()
		var widget domain.Widget
		if err := c.ShouldBindJSON(&widget); err != nil {
			HandleErr(c, ctx, domain.WrapInvalidInput(err, "invalid json body"))
			return
		}

		saved, err := h.usecase.Add(ctx, widget)
		if err != nil {
			HandleErr(c, ctx, err)
			return
		}

		c.JSON(http.StatusCreated, output.ToWidgetOutput(saved))
	}
}

// Pay: path param + optional query param, returns the affected resource -> 200.
func (h WidgetHandler) Pay() gin.HandlerFunc {
	return func(c *gin.Context) {
		ctx := c.Request.Context()

		id, err := uuid.Parse(c.Param("id"))
		if err != nil {
			HandleErr(c, ctx, domain.WrapInvalidInput(err, "id must be valid"))
			return
		}

		var date time.Time
		if dateString := c.Query("date"); dateString != "" {
			date, err = time.Parse("2006-01-02", dateString)
			if err != nil {
				HandleErr(c, ctx, domain.WrapInvalidInput(err, "invalid date format"))
				return
			}
		}

		paid, err := h.usecase.Pay(ctx, id, date)
		if err != nil {
			HandleErr(c, ctx, err)
			return
		}

		c.JSON(http.StatusOK, output.ToWidgetOutput(paid))
	}
}

// DeleteOne: no resource returned -> 204, no body.
func (h WidgetHandler) DeleteOne() gin.HandlerFunc {
	return func(c *gin.Context) {
		ctx := c.Request.Context()

		id, err := uuid.Parse(c.Param("id"))
		if err != nil {
			HandleErr(c, ctx, domain.WrapInvalidInput(err, "id must be valid"))
			return
		}

		if err := h.usecase.DeleteOne(ctx, id); err != nil {
			HandleErr(c, ctx, err)
			return
		}

		c.Status(http.StatusNoContent)
	}
}
```

Derived/multi-field input helper (mirrors `parsePeriod` in `movement_api.go`):

```go
func (h WidgetHandler) parseFilter(c *gin.Context) (domain.WidgetFilter, error) {
	var filter domain.WidgetFilter

	if fromString := c.Query("from"); fromString != "" {
		from, err := time.Parse("2006-01-02", fromString)
		if err != nil {
			return domain.WidgetFilter{}, domain.WrapInvalidInput(err, "invalid from date format")
		}
		filter.From = from
	}

	if err := filter.Validate(); err != nil {
		return domain.WidgetFilter{}, domain.WrapInvalidInput(err, "invalid filter")
	}

	return filter, nil
}
```

## Anti-patterns (reject these)

| Don't | Do |
|---|---|
| Importing `usecase.Xxx` concrete struct in the handler file | Declare a narrow `XxxUsecase` interface in the handler file, with only the methods used |
| Business logic (loops, conditionals beyond input parsing, calls to repository/external API) in the handler | Push it into the usecase; handler only parses, calls, and shapes the response |
| Hand-rolled `c.JSON(code, gin.H{"error": ...})` on failure | `HandleErr(c, ctx, err)` then `return` — let `errors_handler.go` map the status code |
| Parsing an optional query param without checking for `""` first | Guard on empty string; only parse (and only error) when the param is present |
| Returning the raw domain struct when an `output.ToXOutput` mapper already exists for it | Use the existing mapper |
| `c.JSON(http.StatusOK, ...)` for an endpoint that creates a resource | `http.StatusCreated` for creation, `http.StatusNoContent` when nothing is returned |
| Registering routes/wiring the usecase outside `New{Feature}V2Handlers` + `bootstrap/{feature}/setup.go` | Keep route registration in the constructor; keep DI wiring in `setup.go` |

## Run & verify

```bash
go build ./...                                    # compiles
make linter                                        # golangci-lint
go test ./internal/infrastructure/api/...          # handler tests
```

Use the `go-unit-tests` skill for the handler's test file (table-driven, AAA, testify). Run
the package's tests and confirm they pass before reporting done.
