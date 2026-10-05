---
name: go-usecases
description: Write or modify business logic in the clean-arch usecase layer (internal/usecase/*.go). Use when adding/editing a usecase method, defining a new Repository/Gateway/UseCase dependency interface, wiring a transaction, or wrapping errors from repositories/external calls. Enforces interface-at-point-of-use, transaction boundaries, and the error-wrapping conventions below.
---

# Go Usecases

Authoritative style for the business-logic layer (`internal/usecase/*.go`) on the
clean-architecture path. Follow it exactly — these rules override generic Go habits.
Existing usecases may predate this style (notably error-message language); when you touch
one, bring it into compliance.

## When to use

- Adding a method to an existing usecase struct.
- Creating a new `{feature}_usecase.go` for a new clean-arch feature.
- Adding a dependency (repository, sub-usecase, external gateway) to a usecase.
- Reviewing usecase code for style compliance.

## Non-negotiable rules

**Structure**
- One file per feature: `internal/usecase/{feature}_usecase.go`, `package usecase`.
- Define narrow dependency interfaces **in the same file as the usecase that consumes
  them** — never import a concrete repository/gateway struct:
  - `{Feature}Repository` — DB access methods this usecase needs.
  - `{Feature}Gateway` — third-party/external calls (e.g. `StripeSubscriptionGateway`,
    `MercadoPagoSubscriptionGateway`). The HTTP client implementation lives in the
    infrastructure layer — out of scope for this skill.
  - `{Feature}UseCase` — when this usecase needs another usecase's business logic, not just
    CRUD (e.g. `Movement` depends on `InvoiceUseCase` for
    `FindOrCreateInvoiceForMovement`). It's fine to hold both a repo and a usecase
    dependency for the same feature when you need plain CRUD *and* business logic (`Movement`
    holds both `invoiceRepo InvoiceRepository` and `invoiceUseCase InvoiceUseCase`).
  - List only the methods actually called — not the dependency's full interface.
- The usecase struct is named after the domain entity, no `Usecase` suffix (`Movement`,
  `Wallet`, `CreditCard`). Dependencies are unexported fields.
- Constructor `New{Entity}(deps...) {Entity}` returns the struct **by value**. Methods may
  use pointer or value receivers — pointer is more common for usecases with several
  dependencies/private helpers; match whatever the file already uses. If methods use
  pointer receivers, the caller in `bootstrap/{feature}/setup.go` must take the address
  (`&service`) when passing it into a handler constructor or another usecase's dependency
  slot, e.g. `movementService := usecase.NewMovement(...); api.NewMovementV2Handlers(r,
  &movementService)`.
- Repository methods that mutate state take `tx *gorm.DB`; read-only finds don't. Only pass
  a non-nil `tx` from inside a `txManager.WithTransaction` callback.

**Transactions**
- Multi-step writes that must be atomic go inside
  `u.txManager.WithTransaction(ctx, func(tx *gorm.DB) error { ... })`. Assign results to an
  outer-scoped variable and `return err` from the closure — never return early from the
  outer function from inside the closure.
- A single mutating repo call with no other side effects doesn't need a transaction; call
  the repo method directly (it opens its own local transaction if it needs one).

**Validation & cross-cutting checks**
- Optional cross-cutting validators (e.g. `limitsValidator PlanLimitsValidatorInterface`)
  can be `nil` (some wiring/tests omit them) — guard with `if u.limitsValidator != nil {
  ... }` before calling.
- Run input/business-rule validation **before** opening a transaction, so a rejected
  request never begins a DB transaction.

**Error handling** — three cases, pick the one that matches:
1. **Bubbling up a dependency's error with context** (repo, gateway, sub-usecase) →
   `fmt.Errorf("doing x: %w", err)`. English, lowercase, action-phrased. This is the
   dominant pattern in this package (~7x more common than `domain.Wrap*`) — don't translate
   new messages to Portuguese even though an older file does (`wallet_usecase.go`'s
   `"erro ao..."` strings predate this convention; don't copy them).
2. **Rejecting on a business rule the usecase itself checks** → return
   `domain.WrapInvalidInput(ErrXxx, "human message")` (or `WrapNotFound` / `WrapConflict` /
   etc.), wrapping a named sentinel. This makes `errors_handler.go`'s generic
   `domain.Is(err, domain.ErrInvalidInput)` case classify it correctly even before a
   dedicated case exists.
3. **A known business-rule violation with no dynamic error to wrap** → return the sentinel
   directly, e.g. `return ErrInsufficientBalance`.
- Sentinel errors live in `internal/usecase/usecase_errors.go` as one flat `var (...)`
  block — add new ones there, named `Err{Description}`. After adding one, add a matching
  `case domain.Is(err, usecase.ErrXxx):` in `errors_handler.go::toAPIError` (see the
  `go-api-handlers` skill) — otherwise it silently falls through to 500.
- For a one-off validation message that's truly local and never checked by callers,
  `domain.New("message")` inline is acceptable instead of a named sentinel (see
  `validateSubCategory` in `movement_usecase.go`).

**Business metrics (optional)**
- If a method performs a business-significant state change worth tracking as a KPI, emit
  it via `pkg/metrics.IncBusiness(ctx, "biz_x_total", 1, metrics.String("tag", value), ...)`
  right after the operation succeeds (see `Movement.Add`). This is opt-in — most methods
  don't need it.

## Canonical template

Condensed from `movement_usecase.go` / `wallet_usecase.go`: repo + sub-usecase dependency,
a transaction, all three error-wrap cases, and an optional limits validator.

```go
package usecase

import (
	"context"
	"fmt"

	"personal-finance/internal/domain"
	"personal-finance/internal/infrastructure/repository/transaction"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

type (
	WidgetRepository interface {
		Add(ctx context.Context, tx *gorm.DB, widget domain.Widget) (domain.Widget, error)
		FindByID(ctx context.Context, id uuid.UUID) (domain.Widget, error)
	}

	GadgetUseCase interface {
		Reserve(ctx context.Context, gadgetID uuid.UUID, amount float64) (domain.Gadget, error)
	}

	Widget struct {
		repo            WidgetRepository
		gadgetUseCase   GadgetUseCase
		txManager       transaction.Manager
		limitsValidator PlanLimitsValidatorInterface
	}
)

func NewWidget(
	repo WidgetRepository,
	gadgetUseCase GadgetUseCase,
	txManager transaction.Manager,
	limitsValidator PlanLimitsValidatorInterface,
) Widget {
	return Widget{
		repo:            repo,
		gadgetUseCase:   gadgetUseCase,
		txManager:       txManager,
		limitsValidator: limitsValidator,
	}
}

func (u *Widget) Add(ctx context.Context, widget domain.Widget) (domain.Widget, error) {
	if u.limitsValidator != nil {
		if err := u.limitsValidator.ValidateWidgetCreation(ctx); err != nil {
			return domain.Widget{}, err
		}
	}

	if widget.Amount <= 0 {
		return domain.Widget{}, domain.WrapInvalidInput(ErrInvalidWidgetAmount, "amount must be positive")
	}

	var result domain.Widget
	err := u.txManager.WithTransaction(ctx, func(tx *gorm.DB) error {
		gadget, err := u.gadgetUseCase.Reserve(ctx, *widget.GadgetID, widget.Amount)
		if err != nil {
			return fmt.Errorf("error reserving gadget: %w", err)
		}
		widget.GadgetSnapshot = gadget

		created, err := u.repo.Add(ctx, tx, widget)
		if err != nil {
			return fmt.Errorf("error adding widget: %w", err)
		}

		result = created
		return nil
	})
	if err != nil {
		return domain.Widget{}, err
	}

	return result, nil
}

func (u *Widget) FindByID(ctx context.Context, id uuid.UUID) (domain.Widget, error) {
	widget, err := u.repo.FindByID(ctx, id)
	if err != nil {
		return domain.Widget{}, fmt.Errorf("error finding widget: %w", err)
	}
	return widget, nil
}
```

New sentinel goes in `usecase_errors.go`:

```go
ErrInvalidWidgetAmount = errors.New("widget amount must be positive")
```

## Anti-patterns (reject these)

| Don't | Do |
|---|---|
| Importing the concrete repository/gateway struct in the usecase file | Declare a narrow `{Feature}Repository`/`{Feature}Gateway` interface in the usecase file, listing only the methods used |
| Swallowing or re-raising a dependency's error with no context | `fmt.Errorf("doing x: %w", err)` so the original error stays `errors.Is`-able |
| Translating new error messages to Portuguese because an old file does | Write new wrap/error messages in English, lowercase, action-phrased |
| Adding a new `usecase.ErrXxx` without a case in `errors_handler.go` | Add the sentinel to `usecase_errors.go` **and** the matching case in `toAPIError` in the same change |
| Validating input *inside* a `WithTransaction` closure when it could reject the request | Validate before opening the transaction — never open a DB transaction for a request you're about to reject |
| Calling `u.limitsValidator.Validate...()` without a nil check | `if u.limitsValidator != nil { ... }` — it's an optional cross-cutting dependency |
| Returning early from the outer function from inside a `WithTransaction` closure | Assign to an outer-scoped var, `return err` from the closure, check the transaction's returned error afterward |

## Run & verify

```bash
go build ./...
make linter
go test ./internal/usecase/...
```

Use the `go-unit-tests` skill for the usecase's test file (table-driven, AAA, testify; mock
the `{Feature}Repository` / `{Feature}Gateway` / `{Feature}UseCase` interfaces declared in
the file). Run the package's tests and confirm they pass before reporting done.
