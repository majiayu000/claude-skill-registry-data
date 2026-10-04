---
name: go-web-ddd-framework
description: "Use when building Go Web projects with DDD and Clean Architecture on the github.com/go-jimu/template ecosystem. Covers: project bootstrapping with gonew, layer isolation (domain/application/infrastructure), Aggregate Roots with validation and events, Value Objects, CQRS (Commands + Queries), Domain Events via Mediator, Repository pattern with XORM, ConnectRPC API layer, fx dependency injection wiring, error handling with oops, and testing strategy. Use when: (1) creating a new Go DDD project from scratch, (2) adding a new bounded context/domain module, (3) defining entities, VOs, or repositories, (4) implementing CQRS handlers, (5) wiring fx modules, (6) writing proto/ConnectRPC APIs."
metadata:
  version: 1.0
---

# Go-Jimu DDD Framework — Production Guide

Based on `github.com/go-jimu/template`. All code examples are from the actual codebase.

## Quick Start — Bootstrap a New Project

```bash
# 1. Create project from template
go install golang.org/x/tools/cmd/gonew@latest
gonew github.com/go-jimu/template <your-module-path>
cd <your-project>

# 2. Install dev tools (buf, grpcurl, protoc-gen-go, protoc-gen-connect-go)
make tools

# 3. Generate protobuf code
buf generate

# 4. Setup database
mysql -u root -p < scripts/sql/init.sql

# 5. Configure (edit configs/default.yml or use env vars)
# MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE

# 6. Run
make server        # go run cmd/main.go
make unittest      # go test -race with coverage
```

## Architecture — Directory Structure

```text
cmd/
  main.go                        # fx.App entry — wires all modules
  client/                        # Example ConnectRPC client
configs/
  default.yml                    # YAML config with ${ENV_VAR:default} support
internal/
  business/                      # DDD Bounded Contexts
    <module>/
      domain/                    # PURE layer: entities, VOs, repo interfaces, events
        <entity>.go              # Aggregate root with validation
        event.go                 # Domain event definitions
        repository.go            # Repository interface (operates on aggregates only)
      application/               # USE CASE layer: commands, queries, event handlers, DTOs
        application.go           # Application service — implements ConnectRPC handler
        command.go               # Write-side command handlers
        query.go                 # Read-side query handlers + QueryRepository interface
        handler.go               # Domain event handlers
        dto.go                   # Request/Response DTOs
        assembler.go             # Domain Entity -> Proto response conversion
      infrastructure/            # ADAPTER layer: repo impls, DB models, converters
        <entity>.go              # Repository implementation (XORM)
        do.go                    # Data Objects (DB table mapping)
        converter.go             # Entity <-> DO <-> DTO converters
      <module>.go                # fx.Module — wires all layers together
  pkg/                           # Shared infrastructure
    connectrpc/                  # ConnectRPC server + interceptors
    database/                    # XORM driver + custom column types
    eventbus/                    # Mediator factory
    httpsrv/                     # Chi HTTP router
    grpcsrv/                     # gRPC server
    validator/                   # go-playground/validator wrapper
    module.go                    # fx.Module for all infrastructure
pkg/gen/                         # Generated ConnectRPC/Protobuf code (DO NOT EDIT)
proto/                           # .proto API definitions
scripts/sql/                     # Database init scripts
```

## Technology Stack

| Concern | Library | Import |
|---|---|---|
| DI | Uber fx | `go.uber.org/fx` |
| RPC/HTTP | ConnectRPC | `connectrpc.com/connect` |
| Router | Chi v5 | `github.com/go-chi/chi/v5` |
| ORM | XORM | `xorm.io/xorm` |
| Validation | go-playground | `github.com/go-playground/validator/v10` |
| Logging | slog (stdlib) | `log/slog` + `github.com/go-jimu/components/sloghelper` |
| Errors | oops | `github.com/samber/oops` |
| Events | Mediator | `github.com/go-jimu/components/mediator` |
| Protobuf | Buf | `buf generate` |
| Copier | jinzhu/copier | `github.com/jinzhu/copier` |

**Do NOT introduce alternatives** (no GORM, no Gin, no standard net/http mux).

## Domain Layer — Pure Business Logic

### Aggregate Root

Public exported fields with `validate` tags. Contains `mediator.EventCollection` for domain events.

```go
// internal/business/<module>/domain/<entity>.go
type User struct {
    ID             string `validate:"required"`
    Name           string `validate:"required"`
    Email          string `validate:"required,email"`
    HashedPassword []byte `copier:"Password"`
    Events         mediator.EventCollection
    Version        int       // 0 = new (INSERT), >0 = existing (UPDATE)
    Dirty          int32     // Change tracking flag
    Deleted        bool      // Soft delete flag
    CreatedAt      time.Time
    UpdatedAt      time.Time
}
```

**Factory method** — validates, generates ID (UUID v7), raises domain event:

```go
func NewUser(name, password, email string) (*User, error) {
    user := &User{
        ID:     uuid.Must(uuid.NewV7()).String(),
        Name:   name,
        Email:  email,
        Events: mediator.NewEventCollection(),
    }
    if err := user.genPassword(password); err != nil {
        return nil, err
    }
    if err := user.Validate(); err != nil {
        return nil, err
    }
    user.Events.Add(EventUserCreated{ID: user.ID, Name: name, Email: email})
    return user, nil
}

func (u *User) Validate() error {
    return validator.Validate(u)
}
```

**Business methods** — state changes happen via methods, mark dirty:

```go
func (u *User) ChangePassword(old, new string) error {
    if err := bcrypt.CompareHashAndPassword(u.HashedPassword, []byte(old)); err != nil {
        return err
    }
    if err := u.genPassword(new); err != nil {
        return err
    }
    atomic.CompareAndSwapInt32(&u.Dirty, 0, 1)
    return nil
}
```

### Domain Events

```go
// internal/business/<module>/domain/event.go
type EventUserCreated struct {
    ID    string
    Name  string
    Email string
}

const EKUserCreated = mediator.EventKind("user.created")

func (uc EventUserCreated) Kind() mediator.EventKind {
    return EKUserCreated
}
```

### Repository Interface

Defined in domain, operates on aggregate roots only. Separate write and read interfaces for CQRS.

```go
// internal/business/<module>/domain/repository.go
type Repository interface {
    Get(context.Context, string) (*User, error)
    Save(context.Context, *User) error
}
```

## Application Layer — Use Cases & CQRS

### Application Service

Groups Commands + Queries. Implements the ConnectRPC handler interface. Subscribes event handlers to mediator.

```go
// internal/business/<module>/application/application.go
type Application struct {
    repo     domain.Repository
    Queries  *Queries
    Commands *Commands
    handlers []mediator.EventHandler
}

func NewApplication(ev mediator.Mediator, repo domain.Repository, read QueryRepository) userv1connect.UserAPIHandler {
    app := &Application{
        repo: repo,
        Queries:  &Queries{FindUserList: NewFindUserListHandler(read)},
        Commands: &Commands{ChangePassword: NewCommandChangePasswordHandler(repo)},
        handlers: []mediator.EventHandler{NewUserCreatedHandler()},
    }
    for _, hdl := range app.handlers {
        ev.Subscribe(hdl) // Auto-subscribe domain event handlers
    }
    return app
}

// ConnectRPC handler method
func (app *Application) Get(ctx context.Context, req *connect.Request[userv1.GetRequest]) (*connect.Response[userv1.GetResponse], error) {
    logger := sloghelper.FromContext(ctx).With(slog.String("user_id", req.Msg.GetId()))
    entity, err := app.repo.Get(ctx, req.Msg.GetId())
    if err != nil {
        return nil, connect.NewError(connect.CodeNotFound, err)
    }
    return connect.NewResponse(assembleDomainUser(entity)), nil
}
```

### Command Handler (Write Path)

`API -> Application -> Domain/Aggregate -> Repository -> Raise Events`

```go
// internal/business/<module>/application/command.go
type CommandChangePasswordHandler struct {
    repo domain.Repository
}

func (h *CommandChangePasswordHandler) Handle(ctx context.Context, logger *slog.Logger, cmd *CommandChangePassword) error {
    entity, err := h.repo.Get(ctx, cmd.ID)
    if err != nil {
        return err
    }
    if err = entity.ChangePassword(cmd.OldPassword, cmd.NewPassword); err != nil {
        return err
    }
    if err = h.repo.Save(ctx, entity); err != nil {
        return err
    }
    entity.Events.Raise(mediator.Default()) // Dispatch domain events AFTER persistence
    return nil
}
```

### Query Handler (Read Path)

Bypasses domain layer. Uses QueryRepository that returns DTOs directly.

```go
// internal/business/<module>/application/query.go
type QueryRepository interface {
    FindUserList(ctx context.Context, name string, limit, offset int) ([]*User, error)
    CountUserNumber(context.Context, string) (int, error)
}

type FindUserListHandler struct {
    readModel QueryRepository
}

func (h *FindUserListHandler) Handle(ctx context.Context, logger *slog.Logger, req *QueryFindUserListRequest) (*QueryFindUserListResponse, error) {
    total, _ := h.readModel.CountUserNumber(ctx, req.Name)
    users, _ := h.readModel.FindUserList(ctx, req.Name, req.PageSize, offset)
    return &QueryFindUserListResponse{Total: total, Users: users}, nil
}
```

### DTOs & Assemblers

```go
// application/dto.go — flat data carriers
type User struct {
    ID    string `json:"id"`
    Name  string `json:"name"`
    Email string `json:"email"`
}

type CommandChangePassword struct {
    ID          string `json:"_"`
    OldPassword string `json:"old_password"`
    NewPassword string `json:"new_password"`
}

// application/assembler.go — domain -> proto
func assembleDomainUser(entity *domain.User) *userv1.GetResponse {
    return &userv1.GetResponse{Id: entity.ID, Name: entity.Name, Email: entity.Email}
}
```

### Event Handler

```go
// internal/business/<module>/application/handler.go
type UserCreatedHandler struct{}

func (s UserCreatedHandler) Listening() []mediator.EventKind {
    return []mediator.EventKind{domain.EKUserCreated}
}

func (s UserCreatedHandler) Handle(ctx context.Context, ev mediator.Event) {
    // Side effects: send email, update cache, audit log, etc.
}
```

## Infrastructure Layer — Persistence

### Data Object (DO)

Separate struct mapped to DB table. Uses `xorm` tags and `copier` tags for field mapping.

```go
// internal/business/<module>/infrastructure/do.go
type UserDO struct {
    ID        string             `xorm:"id pk"`
    Name      string             `xorm:"name"`
    Password  []byte             `xorm:"password" copier:"HashedPassword"`
    Email     string             `xorm:"email"`
    Version   int                `xorm:"version"`
    CreatedAt database.Timestamp `xorm:"created_at"`
    UpdatedAt database.Timestamp `xorm:"updated_at"`
    DeletedAt database.Timestamp `xorm:"deleted_at"`
}

func (u UserDO) TableName() string { return "user" }
```

### Converters

Three conversion directions: Entity->DO, DO->Entity, DO->DTO. Use `jinzhu/copier`.

```go
// infrastructure/converter.go
func convertUserToDO(entity *domain.User) (*UserDO, error) {
    do := new(UserDO)
    if err := copier.Copy(do, entity); err != nil {
        return nil, oops.Wrap(err)
    }
    // Handle timestamps and soft delete
    return do, nil
}

func convertUserDO(do *UserDO) (*domain.User, error) {
    entity := new(domain.User)
    if err := copier.Copy(entity, do); err != nil {
        return nil, oops.Wrap(err)
    }
    entity.Events = mediator.NewEventCollection() // Always init EventCollection
    return entity, nil
}

func convertUserDOToDTO(do *UserDO) (*application.User, error) {
    dto := new(application.User)
    return dto, copier.Copy(dto, do)
}
```

### Repository Implementation

Write repo: `domain.Repository`. Read repo: `application.QueryRepository`.

```go
// infrastructure/<entity>.go
type userRepository struct {
    engine   *xorm.Engine
    mediator mediator.Mediator
}

var _ domain.Repository = (*userRepository)(nil) // Interface compliance check

func NewRepository(engine *xorm.Engine, mediator mediator.Mediator) domain.Repository {
    return &userRepository{engine: engine, mediator: mediator}
}

func (ur *userRepository) Save(ctx context.Context, user *domain.User) error {
    data, _ := convertUserToDO(user)
    if user.Version == 0 { // New entity — INSERT
        _, err := ur.engine.Context(ctx).Insert(data)
        return err
    }
    // Existing entity — UPDATE with soft delete guard
    _, err := ur.engine.Context(ctx).
        Cols("name", "password", "email", "updated_at", "deleted_at").
        Where("id = ? AND deleted_at = 0", user.ID).
        Update(data)
    return err
}
```

## fx Wiring

### Module-level (`internal/business/<module>/<module>.go`)

```go
var Module = fx.Module(
    "domain.<module>",
    fx.Provide(infrastructure.NewQueryRepository),
    fx.Provide(application.NewApplication),
    fx.Provide(infrastructure.NewRepository),
    fx.Invoke(func(srv userv1connect.UserAPIHandler, c connectrpc.ConnectServer) {
        c.Register(userv1connect.NewUserAPIHandler(
            srv, connect.WithInterceptors(c.GetGlobalInterceptors()...)))
    }),
)
```

### App-level (`cmd/main.go`)

```go
app := fx.New(
    fx.Provide(parseOption),
    fx.Provide(sloghelper.NewLog),
    fx.Provide(eventbus.NewMediator),
    pkg.Module,        // Infrastructure: DB, HTTP, gRPC, ConnectRPC
    user.Module,       // Business modules
    // order.Module,
    fx.NopLogger,
)
```

## Proto & API Layer

```protobuf
// proto/<module>/v1/<module>_api.proto
syntax = "proto3";
package <module>.v1;
option go_package = "github.com/go-jimu/template/pkg/gen/<module>/v1;<module>pb";

service <Module>Service {
  rpc Get(GetRequest) returns (GetResponse) {}
}
```

Generate with `buf generate`. Code lands in `pkg/gen/<module>/v1/`.

## Error & Logging

| Layer | Pattern |
|---|---|
| Domain / Infrastructure | `return oops.With("key", val).Wrap(err)` — context only, **no logging** |
| Application | `logger.ErrorContext(ctx, "msg", sloghelper.Error(err)); return err` |
| API edge | `return nil, connect.NewError(connect.CodeNotFound, err)` |

Get logger from context: `sloghelper.FromContext(ctx)`.

## Configuration

`configs/default.yml` with environment variable override: `${ENV_VAR:default_value}`

```yaml
mysql:
  host: ${MYSQL_HOST:localhost}
  port: ${MYSQL_PORT:3306}
  user: ${MYSQL_USER:root}
  password: ${MYSQL_PASSWORD:jimu}
  database: ${MYSQL_DATABASE:jimu}
eventbus:
  concurrent: 10
  timeout: 10s
connect:
  addr: ":8080"
```

## Adding a New Domain Module

See `references/new-domain-guide.md` for a complete step-by-step walkthrough with file templates.

**Summary of steps:**

1. Define proto in `proto/<module>/v1/<module>_api.proto` -> `buf generate`
2. Create `internal/business/<module>/domain/` — entity, events, repository interface
3. Create `internal/business/<module>/application/` — application service, commands, queries, DTOs, assemblers, event handlers
4. Create `internal/business/<module>/infrastructure/` — DO, converters, repository impl
5. Create `internal/business/<module>/<module>.go` — fx.Module wiring
6. Add SQL table to `scripts/sql/init.sql`
7. Register module in `cmd/main.go`

## Architectural Red Lines

- Domain layer has **ZERO** imports from infrastructure or DB libraries
- Repositories operate on **Aggregate Roots only**, never sub-entities
- All state changes via **methods on the aggregate** (no direct field mutation from outside)
- Business logic lives in **domain**, not application layer
- Command handlers are **orchestration only**
- Query handlers **bypass domain**, map DB rows to DTOs directly
- Domain Events dispatched **after successful persistence**: `entity.Events.Raise(mediator.Default())`
- Cross-module communication via **domain events**, not direct service calls
- Interface compliance: `var _ domain.Repository = (*repoImpl)(nil)`
- Constructors return **interfaces**: `func NewRepository(...) domain.Repository`

## Quality Checklist

- [ ] Directory structure follows canonical layout
- [ ] Domain entity uses `validate` tags + `Validate()` in factory method
- [ ] `mediator.NewEventCollection()` initialized in factory AND converter
- [ ] Repository returns domain entities (not DOs)
- [ ] Write repo and read repo are separate (CQRS)
- [ ] DO struct has `TableName()` method
- [ ] Converters handle timestamps and soft delete correctly
- [ ] fx.Module in `<module>.go` provides all constructors and invokes registration
- [ ] `cmd/main.go` includes the new module
- [ ] Proto generated code is not manually edited
- [ ] Errors wrapped with `oops.With()` at each layer
