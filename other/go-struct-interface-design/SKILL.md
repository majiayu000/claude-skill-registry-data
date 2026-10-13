---
name: go-struct-interface-design
description: >
  Use this when defining domain structs, designing repository/service/messaging
  interfaces, creating DTOs with validation/serialization tags, or reviewing
  struct/interface code for naming and convention compliance. Covers struct tag
  ordering (json/db/validate), constructor functions, godoc rules, accept-interfaces-return-structs,
  -er suffix, acronym casing, and no-stutter naming.
  Triggers: struct, interface, naming, godoc, struct tags, constructor, -er suffix, acronym casing.
---



# Go Struct & Interface Design

Standardizes how structs and interfaces are defined across all microservices. Enforces consistent naming, tagging, documentation, and multi-tenancy requirements.

## When to Activate
- When defining domain model structs or value objects
- When designing repository, service, or messaging interfaces
- When creating DTOs with validation and serialization tags
- When reviewing struct/interface code for naming and convention compliance
- Used by: component-designer, interface-designer, coding-guidelines-generator

## Struct Definition Conventions

### Tag Order

Always apply tags in this order: `json`, `db`, `validate`.

```go
// internal/domain/model/order.go
package model

import (
	"time"

	"github.com/google/uuid"
)

// Order represents a customer order within a tenant boundary.
type Order struct {
	ID          uuid.UUID `json:"id"          db:"id"          validate:"required"`
	TenantID    uuid.UUID `json:"tenant_id"   db:"tenant_id"   validate:"required"`
	CustomerID  uuid.UUID `json:"customer_id" db:"customer_id" validate:"required"`
	Description string    `json:"description" db:"description" validate:"max=10000"`
	Status      Status    `json:"status"      db:"status"      validate:"required,oneof=pending confirmed shipped delivered cancelled"`
	Priority    Priority  `json:"priority"    db:"priority"    validate:"required,oneof=low medium high critical"`
	AssigneeID  uuid.UUID `json:"assignee_id" db:"assignee_id"`
	CreatedAt   time.Time `json:"created_at"  db:"created_at"`
	UpdatedAt   time.Time `json:"updated_at"  db:"updated_at"`
}
```

### TenantID Requirement

Every struct that touches data MUST include `TenantID uuid.UUID`. This field is non-negotiable for multi-tenant isolation.

```go
// Every data-bearing struct includes TenantID.
type Product struct {
	ID       uuid.UUID `json:"id"        db:"id"`
	TenantID uuid.UUID `json:"tenant_id" db:"tenant_id" validate:"required"`
	Name     string    `json:"name"      db:"name"      validate:"required"`
	Type     string    `json:"type"      db:"type"      validate:"required"`
}
```

### Type Aliases for Enums

Use string-based types with constants for type safety.

```go
// Status represents the entity lifecycle state.
type Status string

const (
	StatusPending   Status = "pending"
	StatusConfirmed Status = "confirmed"
	StatusShipped   Status = "shipped"
	StatusDelivered Status = "delivered"
	StatusCancelled Status = "cancelled"
)

// IsTerminal reports whether the status is a final state.
func (s Status) IsTerminal() bool {
	return s == StatusDelivered || s == StatusCancelled
}
```

## Constructor Functions

Every exported struct with required fields gets a `NewXxx` constructor.

```go
// NewOrder creates an Order with generated ID and timestamps.
// It does not validate; call Validate() separately.
func NewOrder(tenantID uuid.UUID, customerID uuid.UUID, priority Priority) *Order {
	now := time.Now().UTC()
	return &Order{
		ID:         uuid.New(),
		TenantID:   tenantID,
		CustomerID: customerID,
		Priority:   priority,
		Status:     StatusPending,
		CreatedAt:  now,
		UpdatedAt:  now,
	}
}
```

Constructors return concrete types (pointers), not interfaces.

## Godoc Comment Conventions

Every exported type, function, and method MUST have a godoc comment starting with the identifier name.

```go
// OrderFilter defines query parameters for listing orders.
type OrderFilter struct {
	Status   *Status    `json:"status,omitempty"`
	Priority *Priority  `json:"priority,omitempty"`
	Since    *time.Time `json:"since,omitempty"`
	Limit    int        `json:"limit"    validate:"min=1,max=100"`
	Offset   int        `json:"offset"   validate:"min=0"`
}

// HasStatusFilter reports whether a status filter is set.
func (f OrderFilter) HasStatusFilter() bool {
	return f.Status != nil
}
```

## Interface Design Rules

### Accept Interfaces, Return Structs

Functions accept interface parameters for flexibility. They return concrete struct types for clarity.

```go
// CreateOrderHandler accepts an OrderRepository interface
// but returns a concrete *CreateOrderHandler.
type CreateOrderHandler struct {
	repo OrderRepository
}

func NewCreateOrderHandler(repo OrderRepository) *CreateOrderHandler {
	return &CreateOrderHandler{repo: repo}
}
```

### The -er Suffix Convention

Interfaces that describe a single behavior use the `-er` suffix.

```go
// Reader reads entity data from the store.
type Reader interface {
	FindByID(ctx context.Context, tenantID, id uuid.UUID) (*model.Order, error)
	FindByFilter(ctx context.Context, tenantID uuid.UUID, filter model.OrderFilter) ([]model.Order, error)
}

// Writer persists entity mutations.
type Writer interface {
	Create(ctx context.Context, order *model.Order) error
	Update(ctx context.Context, order *model.Order) error
	Delete(ctx context.Context, tenantID, id uuid.UUID) error
}

// OrderRepository composes Reader and Writer for full data access.
type OrderRepository interface {
	Reader
	Writer
}
```

### Keep Interfaces Small

Prefer composition of small interfaces over large monolithic ones.

| Interface Size | Guideline |
|----------------|-----------|
| 1-3 methods | Ideal single-responsibility interface |
| 4-6 methods | Acceptable if cohesive; consider splitting |
| 7+ methods | Split into composed interfaces |

### Interface Placement

Define interfaces where they are consumed, not where they are implemented.

```
ports/outbound/<entity>_repo.go   -- Repository interface (consumed by application/)
adapters/outbound/postgres/       -- Concrete implementation (implements the port)
```

## Naming Rules

### No Stuttering (package.PackageType)

```go
// GOOD
package order
type Service struct{}  // Used as order.Service

// BAD
package order
type OrderService struct{}  // Used as order.OrderService (stutters)
```

### Acronym Casing

Acronyms are all-caps in Go identifiers. Mixed-case acronyms are incorrect.

| Correct | Incorrect |
|---------|-----------|
| `ID` | `Id` |
| `HTTP` | `Http` |
| `URL` | `Url` |
| `TenantID` | `TenantId` |
| `APIURL` | `ApiUrl` |

```go
// GOOD
type Config struct {
	HTTPURL  string
	TenantID uuid.UUID
}

// BAD
type Config struct {
	HttpUrl  string
	TenantId uuid.UUID
}
```

### Method Signatures

All public methods that perform I/O accept `context.Context` as the first parameter.

```go
// GOOD: context.Context is the first parameter.
func (s *Service) GetOrder(ctx context.Context, tenantID, orderID uuid.UUID) (*Order, error)

// BAD: Missing context.
func (s *Service) GetOrder(tenantID, orderID uuid.UUID) (*Order, error)
```

## DTO Structs

DTOs live in `internal/application/dto/` and translate between API and domain.

```go
// internal/application/dto/order_dto.go
package dto

import (
	"github.com/google/uuid"
	"github.com/yourorg/<service-name>/internal/domain/model"
)

// CreateOrderRequest is the inbound DTO for order creation.
type CreateOrderRequest struct {
	CustomerID  uuid.UUID      `json:"customer_id" validate:"required"`
	Description string         `json:"description" validate:"max=10000"`
	Priority    model.Priority `json:"priority"    validate:"required,oneof=low medium high critical"`
}

// ToCommand converts the DTO to a domain command.
func (r CreateOrderRequest) ToCommand(tenantID uuid.UUID) model.CreateOrderCommand {
	return model.CreateOrderCommand{
		TenantID:    tenantID,
		CustomerID:  r.CustomerID,
		Description: r.Description,
		Priority:    r.Priority,
	}
}
```

## Examples

### GOOD
```go
// Correct: small interface, -er suffix, context.Context first, TenantID present.
package outbound

import (
	"context"

	"github.com/google/uuid"
	"github.com/yourorg/<service-name>/internal/domain/model"
)

// Finder retrieves entities from the data store.
type Finder interface {
	FindByID(ctx context.Context, tenantID, entityID uuid.UUID) (*model.Order, error)
}
```

### BAD
```go
// WRONG: Large interface, no -er suffix, missing context, missing TenantID,
// stuttering name, wrong acronym casing.
package order

type OrderDataAccess interface {
	GetOrderById(orderId string) (*OrderModel, error)
	SaveOrder(order *OrderModel) error
	DeleteOrder(orderId string) error
	ListAllOrders(page int) ([]*OrderModel, error)
	CountOrders() (int, error)
	SearchOrders(query string) ([]*OrderModel, error)
	ArchiveOrder(orderId string) error
}
```

## Common Mistakes

1. **Using `Id` instead of `ID`** -- Go convention requires all-caps acronyms. `TenantId`, `HttpUrl`, `ApiKey` are all incorrect. Use `TenantID`, `HTTPURL`, `APIKey`.

2. **Returning interfaces from constructors** -- `NewService()` must return `*Service`, not `ServiceInterface`. Returning interfaces hides the concrete type and prevents accessing non-interface methods.

3. **Defining interfaces at the implementation site** -- Interfaces belong where they are consumed (in `ports/`), not next to their implementation (in `adapters/`). This follows Go's implicit interface satisfaction model.

4. **Omitting TenantID from data structs** -- Every struct that represents persisted data or crosses a service boundary must carry `TenantID uuid.UUID`. Missing tenant context breaks multi-tenant isolation.

5. **Stuttering names** -- An `order.OrderService` stutters. Use `order.Service` so call sites read `order.Service`, not `order.OrderService`.
