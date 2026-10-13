---
name: go-hexagonal-architecture
description: >
  Use this when designing the internal package layout of a Go microservice,
  defining port interfaces for repositories/messaging/external integrations,
  implementing PostgreSQL/NATS/third-party adapters, wiring application services
  with DI, or reviewing service structure for domain isolation. Covers cmd/,
  internal/domain/, internal/application/, internal/ports/, internal/adapters/
  layout and DI wiring.
  Triggers: hexagonal, ports and adapters, internal/domain, internal/ports, internal/adapters, DI wiring, package layout.
---



# Go Hexagonal Architecture

Standardizes the internal package layout for every microservice using hexagonal (ports and adapters) architecture. Domain logic stays isolated from infrastructure; all external dependencies flow through port interfaces.

## When to Activate
- When designing the internal package structure of a Go microservice
- When defining port interfaces for repositories, messaging, or external integrations
- When implementing adapters for PostgreSQL, NATS, or third-party services
- When wiring application services with dependency injection
- When reviewing service structure for proper domain isolation
- Used by: component-designer, simulated-senior-developer, simulated-tech-lead

## Package Structure

Every microservice follows this canonical layout. Replace `<service-name>` and `<entity>` with your domain (e.g., `order-service`/`order`, `patient-service`/`patient`, `account-service`/`account`):

### Domain Service Layout (NATS-primary inbound)

For all domain services, the primary inbound adapter is NATS (subscriptions
for events, request-reply handlers for queries). HTTP inbound adapters are
NOT used for inter-service communication. Only the API Gateway has HTTP
inbound adapters for business endpoints.

```
services/<service-name>/
├── cmd/
│   └── server/
│       └── main.go              # Wiring, config, graceful shutdown
├── internal/
│   ├── domain/
│   │   ├── model/
│   │   │   ├── <entity>.go      # Domain entities, value objects
│   │   │   └── rule.go
│   │   ├── event/
│   │   │   └── <entity>_events.go # Domain events
│   │   └── service/
│   │       └── <entity>_svc.go  # Domain services (pure logic, no I/O)
│   ├── application/
│   │   ├── command/
│   │   │   └── create_<entity>.go # Command handlers (use-case orchestration)
│   │   ├── query/
│   │   │   └── get_<entity>.go    # Query handlers
│   │   └── dto/
│   │       └── <entity>_dto.go    # Input/output DTOs for the application layer
│   ├── ports/
│   │   ├── inbound/
│   │   │   └── <entity>_api.go    # Inbound port interfaces
│   │   └── outbound/
│   │       ├── <entity>_repo.go   # Repository port
│   │       ├── event_pub.go       # Messaging port (NATS publish)
│   │       └── service_query.go   # Inter-service query port (NATS request-reply)
│   └── adapters/
│       ├── inbound/
│       │   └── nats/
│       │       ├── subscriber.go  # NATS event subscriber adapter
│       │       └── responder.go   # NATS request-reply responder adapter
│       └── outbound/
│           ├── dal/
│           │   └── client.go         # DAL client adapter (NATS→DAL for all DB ops)
│           ├── cache/
│           │   └── l1_cache.go       # freecache L1 adapter
│           ├── nats/
│           │   ├── event_pub.go     # NATS publisher adapter
│           │   └── requester.go     # NATS request-reply client adapter
│           └── email/
│               └── notifier.go      # Email adapter (via NATS to notification service)
├── migrations/
│   ├── 000001_create_<entities>.up.sql
│   └── 000001_create_<entities>.down.sql
└── config/
    └── config.go                  # Service-specific config struct
```

### API Gateway Layout (HTTP-primary inbound)

Only the API Gateway has HTTP inbound adapters for business endpoints.
It translates HTTP requests into NATS request-reply calls to domain services.

```
services/api-gateway/
├── cmd/server/main.go
├── internal/
│   ├── adapters/
│   │   ├── inbound/
│   │   │   └── http/
│   │   │       └── handler.go     # HTTP adapter (external client endpoints)
│   │   └── outbound/
│   │       └── nats/
│   │           └── requester.go   # NATS request-reply to domain services
│   ├── ports/
│   │   ├── inbound/
│   │   │   └── gateway_api.go     # HTTP inbound port
│   │   └── outbound/
│   │       └── service_client.go  # Inter-service query port (NATS)
│   └── middleware/                 # Auth, rate limit, tenant extraction
└── config/config.go
```

### Data Access Layer (DAL) Service Layout (PostgreSQL-primary)

The DAL service is the SOLE PostgreSQL client. It receives NATS requests from
entity services, compiles QueryStruct → SQL, executes queries, resolves
cross-joins, encodes MsgPack, and manages L2 Dragonfly cache.

```
services/data-access-layer/
├── cmd/server/main.go              # pgxpool + Dragonfly + NATS + OTel wiring
├── internal/
│   ├── domain/
│   │   └── querybuilder/
│   │       ├── types.go            # QueryStruct, Pagination, CompiledQuery
│   │       └── compiler.go         # Compile(), EnforcePagination()
│   ├── application/
│   │   ├── handler_get.go          # GET-by-ID: L2 check → SQL → encode
│   │   ├── handler_list.go         # List: compile → execute → cross-join → encode
│   │   ├── handler_analytics.go    # Analytics: force_duckdb → execute → encode
│   │   ├── handler_create.go       # Insert → invalidate L2 → publish event
│   │   ├── handler_update.go       # Update (optimistic lock) → invalidate
│   │   ├── handler_delete.go       # Soft delete → invalidate
│   │   └── handler_batch.go        # Transactional batch operations
│   ├── ports/
│   │   ├── inbound/
│   │   │   └── dal_handler.go      # NATS request handler interface
│   │   └── outbound/
│   │       ├── pool_manager.go     # pgxpool PoolManager interface
│   │       ├── cache.go            # L2 Dragonfly cache interface
│   │       └── event_pub.go        # Cache invalidation event publisher
│   └── adapters/
│       ├── inbound/
│       │   └── nats/
│       │       └── subscriber.go   # NATS QueueSubscribe for DAL requests
│       └── outbound/
│           ├── postgres/
│           │   ├── pool_manager.go # pgxpool shared pool per app-database
│           │   ├── schema.go       # AcquireForTenant, sanitizeSchema
│           │   ├── executor.go     # SQL execution, scanToMaps
│           │   └── analytics.go    # DuckDB session setup
│           ├── dragonfly/
│           │   └── cache.go        # Dragonfly L2 cache adapter (go-redis)
│           ├── crossjoin/
│           │   └── resolver.go     # EntityResolver, ResolveCrossJoins worker pool
│           └── encoding/
│               └── columnar.go     # EncodeColumnar, DecodeColumnar MsgPack
├── migrations/                     # DAL owns ALL migrations for all entity tables
└── config/config.go                # PostgreSQL DSN, Dragonfly URL, NATS URL
```

**DAL is the ONLY service with `adapters/outbound/postgres/`.** Entity services
have `adapters/outbound/dal/` (NATS client) instead.

### Package Rules

| Rule | Rationale |
|------|-----------|
| `domain/` imports NOTHING outside `domain/` | Domain must be pure, testable without infrastructure |
| `application/` imports `domain/` and `ports/` only | Orchestrates use cases via port interfaces |
| `ports/` imports `domain/` types only | Interfaces reference domain models, not adapter types |
| `adapters/` imports `ports/`, `domain/`, and external libs | Adapters implement ports with real infrastructure |
| `cmd/` wires everything together | The composition root, no business logic |

## Port Interface Design

### Repository Port

```go
// internal/ports/outbound/<entity>_repo.go
package outbound

import (
	"context"

	"github.com/yourorg/<service-name>/pkg/dal"
)

// OrderQuerier defines data access operations routed through DAL.
// Every method ultimately sends a NATS request to the data-access-layer service.
type OrderQuerier interface {
	GetByID(ctx context.Context, id string) ([]byte, error)
	List(ctx context.Context, qs dal.QueryStruct) ([]byte, error)
	Create(ctx context.Context, data map[string]any) ([]byte, error)
	Update(ctx context.Context, id string, data map[string]any, version int) error
	Delete(ctx context.Context, id string) error
}
```

### Messaging Port (NATS Publish)

```go
// internal/ports/outbound/event_pub.go
package outbound

import "context"

// EventPublisher abstracts the messaging infrastructure.
// Implementations target NATS JetStream in this project.
type EventPublisher interface {
	Publish(ctx context.Context, subject string, payload []byte) error
	PublishAsync(ctx context.Context, subject string, payload []byte) error
}
```

### Inter-Service Query Port (NATS Request-Reply)

```go
// internal/ports/outbound/service_query.go
package outbound

import "context"

// ServiceQuerier abstracts NATS request-reply calls to other services.
// This replaces HTTP clients and gRPC stubs for inter-service queries.
type ServiceQuerier interface {
	Query(ctx context.Context, subject string, request []byte) ([]byte, error)
}
```

### External Service Port (via NATS)

```go
// internal/ports/outbound/notification.go
package outbound

import (
	"context"

	"github.com/google/uuid"
)

// Notifier abstracts notification delivery via NATS to the notification service.
// No direct HTTP calls to other services -- communication goes through NATS.
type Notifier interface {
	SendEntityCreated(ctx context.Context, tenantID uuid.UUID, entityID uuid.UUID) error
	SendDeadlineApproaching(ctx context.Context, tenantID uuid.UUID, entityID uuid.UUID) error
}
```

## Adapter Implementation

Adapters implement port interfaces with real infrastructure dependencies.

```go
// internal/adapters/outbound/dal/client.go
package dal

import (
	"github.com/coocood/freecache"
	"github.com/yourorg/<service-name>/internal/ports/outbound"
	"github.com/yourorg/<service-name>/pkg/dal"
)

// Compile-time interface check.
var _ outbound.OrderQuerier = (*OrderDALClient)(nil)

// OrderDALClient implements OrderQuerier via NATS request-reply to DAL.
type OrderDALClient struct {
	dalClient dal.Client    // pkg/dal NATS client
	l1Cache   *freecache.Cache
}
```

## Application Service Layer

Application services orchestrate use cases by composing domain logic with port calls.

```go
// internal/application/command/create_order.go
package command

import (
	"context"
	"github.com/vmihailenco/msgpack/v5"
	"fmt"

	"github.com/yourorg/<service-name>/internal/domain/model"
	"github.com/yourorg/<service-name>/internal/ports/outbound"
)

// CreateOrderHandler orchestrates order creation.
type CreateOrderHandler struct {
	repo      outbound.OrderRepository
	publisher outbound.EventPublisher
}

// NewCreateOrderHandler returns a handler wired to its ports.
func NewCreateOrderHandler(repo outbound.OrderRepository, pub outbound.EventPublisher) *CreateOrderHandler {
	return &CreateOrderHandler{repo: repo, publisher: pub}
}

// Handle executes the create-order use case.
func (h *CreateOrderHandler) Handle(ctx context.Context, cmd model.CreateOrderCommand) (*model.Order, error) {
	order := model.NewOrder(cmd)

	if err := h.repo.Create(ctx, order); err != nil {
		return nil, fmt.Errorf("creating order: %w", err)
	}

	payload, err := msgpack.Marshal(order)
	if err != nil {
		return nil, fmt.Errorf("marshalling order event: %w", err)
	}

	subject := fmt.Sprintf("tenant.%s.order.created", order.TenantID)
	if err := h.publisher.Publish(ctx, subject, payload); err != nil {
		return nil, fmt.Errorf("publishing order.created: %w", err)
	}

	return order, nil
}
```

## Composition Root (cmd/main.go)

```go
// cmd/server/main.go
package main

import (
	"context"
	"log"
	"os/signal"
	"syscall"
	"time"

	"github.com/coocood/freecache"
	dalclient "github.com/yourorg/<service-name>/internal/adapters/outbound/dal"
	natspub "github.com/yourorg/<service-name>/internal/adapters/outbound/nats"
	"github.com/yourorg/<service-name>/internal/application/command"
	"github.com/yourorg/<service-name>/pkg/dal"
)

func main() {
	ctx, stop := signal.NotifyContext(context.Background(), syscall.SIGINT, syscall.SIGTERM)
	defer stop()

	// L1 Cache (in-process, for GET-by-ID)
	l1Cache := freecache.NewCache(100 * 1024 * 1024) // 100MB

	// DAL client (all DB operations via NATS to data-access-layer)
	dc := dal.NewClient(nc, dal.WithTimeout(5*time.Second))
	defer dc.Close()

	repo := dalclient.NewOrderDALClient(dc, l1Cache)
	pub := natspub.NewPublisher( /* nats conn */ )
	handler := command.NewCreateOrderHandler(repo, pub)

	_ = handler // wire into NATS inbound adapters
	<-ctx.Done()
}
```

## Examples

### GOOD
```go
// Domain model depends on nothing external.
// internal/domain/model/order.go
package model

import (
	"time"

	"github.com/google/uuid"
)

// Order represents the core order entity.
type Order struct {
	ID         uuid.UUID
	TenantID   uuid.UUID
	CustomerID uuid.UUID
	Status     string
	CreatedAt  time.Time
	UpdatedAt  time.Time
}
```

### BAD
```go
// WRONG: Domain model imports infrastructure (pgx).
package model

import (
	"github.com/jackc/pgx/v5"
)

type Order struct {
	Row pgx.Row // Domain leaks infrastructure detail
}
```

### GOOD
```go
// Compile-time interface satisfaction check.
var _ outbound.OrderRepository = (*OrderRepo)(nil)
```

### BAD
```go
// WRONG: No compile-time check. A broken adapter is only caught at runtime.
type OrderRepo struct{}
// Missing: var _ outbound.OrderRepository = (*OrderRepo)(nil)
```

## Common Mistakes

1. **Domain imports infrastructure packages** -- The `domain/` package must never import `pgx`, `nats`, `net/http`, or any adapter library. If domain code needs I/O, define a port interface in `ports/outbound/` and inject the adapter.

2. **Business logic in adapters** -- Adapters (NATS subscribers, request-reply responders) should only translate between external formats and application-layer calls. Move validation, orchestration, and rules into `application/` or `domain/service/`.

3. **Skipping compile-time interface checks** -- Always add `var _ PortInterface = (*Adapter)(nil)` in every adapter file. Without this, interface drift goes undetected until runtime.

4. **Putting wiring logic in application services** -- Constructor calls, config parsing, and connection setup belong in `cmd/`. Application services receive fully constructed dependencies through their constructors.

5. **Missing TenantID in port method signatures** -- Every method that queries or mutates data must accept tenant context. A repository method without `tenantID` breaks tenant isolation.

6. **Using HTTP inbound adapters for inter-service communication** -- Domain services must NOT have HTTP inbound adapters for business endpoints. Only the API Gateway has HTTP inbound adapters. Domain services use NATS inbound adapters (subscriptions for events, responders for request-reply queries).

7. **Using pgxpool in entity services** -- Entity services communicate with DAL via NATS. Only the DAL service imports pgxpool.
