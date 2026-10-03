---
name: lca
description: >
  Layered Composition Architecture patterns. Use when designing system
  boundaries, state flow, lifecycle management, configuration, or module structure.
  Includes Infrastructure pattern for shared dependencies and Handler() factory
  for domain system handler creation.
  Triggers: System interface, New* constructor, Start() method, Cold Start,
  Hot Start, Runtime struct, Domain struct, Infrastructure, Handler() factory,
  lifecycle coordinator, OnStartup, OnShutdown, config.go, Finalize(),
  validate(), loadDefaults(), loadEnv().
  File patterns: internal/config/*.go, pkg/lifecycle/*.go, pkg/runtime/*.go,
  internal/*/system.go, cmd/server/*.go
---

# Layered Composition Architecture (LCA)

## When This Skill Applies

- Designing new systems or domains
- Implementing lifecycle management
- Creating configuration structures
- Understanding dependency flow
- Building runtime/domain separation
- Creating Infrastructure for shared dependencies
- Understanding Handler() factory pattern

## Principles

### 1. State Flows Down, Never Up

State flows through method calls (parameters), not through object initialization.

**Anti-Pattern** (Reaching Up):
```go
type Handler struct {
    service *Service  // Storing reference to parent
}

func (h *Handler) Process() {
    sys := h.service.Providers()  // Reaching up to parent state
}
```

**Correct Pattern** (State Flows Down):
```go
func HandleCreate(w http.ResponseWriter, r *http.Request, system providers.System, logger *slog.Logger) {
    // State injected at call site, flows DOWN
}
```

### 2. Systems, Not Services/Models

**Terminology**:
- **System**: A cohesive unit that owns both state and processes
- **State**: Structures that define data
- **Process**: Methods that operate on state
- **Interface**: Contract between systems

**Package Organization**:
- **cmd/server**: The process (composition root, entry point)
- **pkg/**: Public API (shared infrastructure, reusable toolkit)
- **internal/**: Private API (domain systems, business logic)

### 3. Cold Start vs Hot Start

**Cold Start** (State Initialization):
- `New*()` constructor functions
- Builds entire dependency graph
- All configurations → State objects
- All systems created but dormant
- No processes running
- Returns ready-to-start system

**Hot Start** (Process Activation):
- `Start()` methods
- State objects → Running processes
- Cascade start through dependency graph
- Context boundaries for lifecycle management
- System becomes interactable

```go
svc, err := NewService(cfg)  // Cold Start - Build state graph
if err := svc.Start(); err != nil {  // Hot Start - Activate processes
    log.Fatal(err)
}
```

### 4. System Interface Contract

Every system provides:

1. **Internal State** (private) - Only accessible within the system
2. **Internal Processes** (private) - Implementation details
3. **Getter Methods** (public) - Immutable access to state
4. **Commands** (public) - Write operations from owner
5. **Events** (public, optional) - Notifications to owner

### 5. Infrastructure Pattern

Infrastructure holds core systems required by all modules:

```go
// pkg/runtime/infrastructure.go
type Infrastructure struct {
    Lifecycle *lifecycle.Coordinator
    Logger    *slog.Logger
    Database  database.System
    Storage   storage.System
}

func New(cfg *config.Config) (*Infrastructure, error) {
    lc := lifecycle.New()
    logger := newLogger(&cfg.Logging)

    db, err := database.New(&cfg.Database, logger)
    if err != nil {
        return nil, fmt.Errorf("database init failed: %w", err)
    }

    store, err := storage.New(&cfg.Storage, logger)
    if err != nil {
        return nil, fmt.Errorf("storage init failed: %w", err)
    }

    return &Infrastructure{
        Lifecycle: lc,
        Logger:    logger,
        Database:  db,
        Storage:   store,
    }, nil
}

func (i *Infrastructure) Start() error {
    if err := i.Database.Start(i.Lifecycle); err != nil {
        return fmt.Errorf("database start failed: %w", err)
    }
    if err := i.Storage.Start(i.Lifecycle); err != nil {
        return fmt.Errorf("storage start failed: %w", err)
    }
    return nil
}
```

### 6. Runtime/Domain Separation

| Category | Characteristics | Examples |
|----------|----------------|----------|
| **Runtime Systems** | Long-running, lifecycle-managed, application-scoped | Database, Storage |
| **Domain Systems** | Stateless, request-scoped behavior, no lifecycle | Providers, Agents |

**Module Runtime** embeds Infrastructure and adds module-specific config:

```go
// internal/api/runtime.go
type Runtime struct {
    *runtime.Infrastructure
    Pagination pagination.Config
}

func NewRuntime(cfg *config.Config, infra *runtime.Infrastructure) *Runtime {
    return &Runtime{
        Infrastructure: &runtime.Infrastructure{
            Lifecycle: infra.Lifecycle,
            Logger:    infra.Logger.With("module", "api"),
            Database:  infra.Database,
            Storage:   infra.Storage,
        },
        Pagination: cfg.API.Pagination,
    }
}
```

### 7. Handler() Factory Pattern

Domain systems expose a `Handler()` method that creates handlers with the system's dependencies:

```go
// internal/providers/system.go
type System interface {
    Handler() *Handler

    List(ctx context.Context, page pagination.PageRequest, filters Filters) (*pagination.PageResult[Provider], error)
    Find(ctx context.Context, id uuid.UUID) (*Provider, error)
    Create(ctx context.Context, cmd CreateCommand) (*Provider, error)
    Update(ctx context.Context, id uuid.UUID, cmd UpdateCommand) (*Provider, error)
    Delete(ctx context.Context, id uuid.UUID) error
}

// internal/providers/repository.go
func (r *repo) Handler() *Handler {
    return NewHandler(r, r.logger, r.pagination)
}
```

**Domain Initialization** creates systems with Handler() factory:
```go
// internal/api/domain.go
type Domain struct {
    Providers providers.System
    Agents    agents.System
}

func NewDomain(runtime *Runtime) *Domain {
    return &Domain{
        Providers: providers.New(runtime.Database.Connection(), runtime.Logger, runtime.Pagination),
        Agents:    agents.New(runtime.Database.Connection(), runtime.Logger, runtime.Pagination),
    }
}
```

**Route Registration** uses Handler() to get handlers:
```go
// internal/api/routes.go
func registerRoutes(mux *http.ServeMux, spec *openapi.Spec, domain *Domain, cfg *config.Config) {
    routes.Register(mux, cfg.API.BasePath, spec,
        domain.Providers.Handler().Routes(),
        domain.Agents.Handler().Routes(),
    )
}
```

### 8. Module Architecture

Modules are self-contained HTTP sub-applications with their own runtime and domain.

**Principle: Domains Are Private to Modules**

Each module owns its Domain exclusively. Domains never cross module boundaries:

```go
// internal/api/domain.go - PRIVATE to api module
type Domain struct {
    Providers providers.System
    Agents    agents.System
    Documents documents.System
}

// The Domain struct is unexported or internal to the module.
// Other modules cannot access or share these systems.
```

**Principle: Config Flows Down to Modules**

Root configuration is passed to `NewModule()`. Modules extract what they need:

```go
// cmd/server/modules.go
apiModule, err := api.NewModule(cfg, &runtime.Infrastructure)

// internal/api/api.go
func NewModule(cfg *config.Config, infra *runtime.Infrastructure) (*module.Module, error) {
    // Extract module-specific config
    pagination := cfg.API.Pagination
    corsConfig := cfg.API.CORS

    // Access global config when needed
    version := cfg.Version
    domain := cfg.Domain
}
```

**Principle: Runtimes Reference Shared Infrastructure**

Child runtimes embed or reference parent infrastructure rather than duplicating fields:

```go
// pkg/runtime/infrastructure.go - Shared across modules
type Infrastructure struct {
    Logger    *slog.Logger
    Database  database.System
    Storage   storage.System
    Lifecycle *lifecycle.Coordinator
}

// internal/api/runtime.go - Module-specific runtime
type apiRuntime struct {
    *runtime.Infrastructure  // Embed shared infrastructure
    Pagination pagination.Config  // Add module-specific fields
}

func newRuntime(cfg *config.Config, infra *runtime.Infrastructure) *apiRuntime {
    return &apiRuntime{
        Infrastructure: infra,
        Pagination:     cfg.API.Pagination,
    }
}
```

This pattern:
- Avoids duplicating fields across runtimes
- Establishes clear dependency direction (child → parent)
- Keeps module-specific configuration isolated

### 9. Lifecycle Coordinator

```go
type Coordinator struct {
    ctx        context.Context
    cancel     context.CancelFunc
    startupWg  sync.WaitGroup
    shutdownWg sync.WaitGroup
    ready      bool
}

func (c *Coordinator) OnStartup(fn func())   // Register startup tasks
func (c *Coordinator) OnShutdown(fn func())  // Register cleanup tasks
func (c *Coordinator) WaitForStartup()       // Block until ready
func (c *Coordinator) Ready() bool           // Check readiness
```

**Usage Pattern**:
- **OnStartup**: Tasks that must complete for service readiness (e.g., database ping)
- **OnShutdown**: Cleanup tasks triggered on context cancellation (e.g., close connections)

### 10. Configuration Pattern

**Precedence** (highest to lowest):
```
Environment Variables
    ↓ replaces (not merges)
config.{env}.toml (overlay)
    ↓ replaces (not merges)
config.toml (base)
```

**Finalize Pattern**:
```go
type Config struct {
    Server   ServerConfig   `toml:"server"`
    Database DatabaseConfig `toml:"database"`
}

func (c *Config) Finalize() error {
    c.loadDefaults()  // Apply defaults for zero-value fields
    c.loadEnv()       // Map SECTION_FIELD environment variables
    return c.validate()  // Validate field constraints
}
```

**Section Config**:
```go
type ServerConfig struct {
    Host string `toml:"host"`
    Port int    `toml:"port"`
}

func (c *ServerConfig) loadDefaults() {
    if c.Host == "" { c.Host = "0.0.0.0" }
    if c.Port == 0 { c.Port = 8080 }
}

func (c *ServerConfig) loadEnv() {
    if v := os.Getenv("SERVER_HOST"); v != "" { c.Host = v }
    if v := os.Getenv("SERVER_PORT"); v != "" {
        if port, err := strconv.Atoi(v); err == nil { c.Port = port }
    }
}

func (c *ServerConfig) validate() error {
    if c.Port < 1 || c.Port > 65535 {
        return errors.New("port must be between 1 and 65535")
    }
    return nil
}
```

## Anti-Patterns

### Reaching Up for State

```go
// Bad: Handler reaches up to get dependencies
type Handler struct {
    app *Application
}

func (h *Handler) Process() {
    db := h.app.Database()  // Reaching up
}

// Good: Dependencies injected at call site
func HandleProcess(db database.System) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        // db available directly
    }
}
```

### Merged Configuration

```go
// Bad: Merging arrays from multiple sources
defaults := []string{"a", "b"}
overrides := []string{"c"}
result := append(defaults, overrides...)  // ["a", "b", "c"]

// Good: Complete replacement at each level
result := overrides  // ["c"] - override replaces entirely
```
