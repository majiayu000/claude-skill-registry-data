---
name: Pumped-Go
description: Auto-activating guidance for pumped-go ensuring production-ready, type-safe Go applications
when_to_use: automatically activates when go.mod contains github.com/pumped-fn/pumped-go dependency
version: 1.0.0
---

# Pumped-Go Skill

## Overview

Build observable, production-ready Go applications with explicit dependencies and lifecycle management.

**Core principle:** Long-lived resources become executors, short-span operations become flows, with proper lifecycle management and testability.

**Auto-activates when:** go.mod contains `github.com/pumped-fn/pumped-go`

## Decision Tree

```
What am I building?
        ↓
    ┌───────┴───────────────┐
    ↓                       ↓
Long-lived resource?    Short-span operation?
(DB, HTTP client,       (request handling,
 service, handler)       business logic)
    ↓                       ↓
EXECUTOR                 FLOW
(package-level var)   (Flow1, Flow2, etc.)
    ↓                       ↓
Provide (no deps) or    Execute with Exec()
Derive1-N (with deps)   or Exec1-N()
    ↓                       ↓
Controllers for deps    Sub-flows for composition
Handle all errors       Tag-based data flow
OnCleanup for cleanup   Error handling
    ↓                       ↓
Testing:                Testing:
WithPreset()            Execution contexts
Table-driven tests      Mock executors
                            ↓
                    Pure transformation?
                    No side effects?
                            ↓
                    PLAIN FUNCTION
                    (regular Go func)
                            ↓
                    Testing: Unit tests
```

## Quick API Reference

### Package-Level Executor Declaration

```go
package graph

import pumped "github.com/pumped-fn/pumped-go"

var (
    // No dependencies - use Provide
    Config = pumped.Provide(func(ctx *pumped.ResolveCtx) (*ConfigType, error) {
        return &ConfigType{
            DBHost: "localhost",
            DBPort: 5432,
        }, nil
    })

    // With 1 dependency - use Derive1
    DB = pumped.Derive1(
        Config,
        func(ctx *pumped.ResolveCtx, cfgCtrl *pumped.Controller[*ConfigType]) (*sql.DB, error) {
            cfg, err := cfgCtrl.Get()
            if err != nil {
                return nil, err
            }

            db, err := sql.Open("postgres", cfg.ConnectionString())
            if err != nil {
                return nil, err
            }

            // Cleanup registration
            ctx.OnCleanup(func() error {
                return db.Close()
            })

            return db, nil
        },
    )

    // With 2 dependencies - use Derive2
    UserRepo = pumped.Derive2(
        DB,
        Logger,
        func(ctx *pumped.ResolveCtx,
            dbCtrl *pumped.Controller[*sql.DB],
            logCtrl *pumped.Controller[*Logger]) (*UserRepository, error) {
            db, err := dbCtrl.Get()
            if err != nil {
                return nil, err
            }
            log, err := logCtrl.Get()
            if err != nil {
                return nil, err
            }
            return NewUserRepository(db, log), nil
        },
    )

    // Reactive dependency - re-resolves when Config changes
    CachedService = pumped.Derive1(
        Config.Reactive(),  // Note: .Reactive() method
        func(ctx *pumped.ResolveCtx, cfgCtrl *pumped.Controller[*ConfigType]) (*Service, error) {
            // This re-resolves when Config is updated
            cfg, err := cfgCtrl.Get()
            if err != nil {
                return nil, err
            }
            return NewService(cfg.CacheSize), nil
        },
    )
)
```

### Flow Execution

```go
// Define flow with dependencies
var ProcessOrderFlow = pumped.Flow2(
    UserRepo,
    PaymentGateway,
    func(execCtx *pumped.ExecutionCtx,
        userRepoCtrl *pumped.Controller[*UserRepository],
        paymentCtrl *pumped.Controller[*PaymentGateway]) (*Order, error) {

        userRepo, err := userRepoCtrl.Get()
        if err != nil {
            return nil, err
        }
        payment, err := paymentCtrl.Get()
        if err != nil {
            return nil, err
        }

        // Set data in execution context
        execCtx.Set(pumped.Input(), orderData)

        // Execute sub-flow
        user, _, err := pumped.Exec1(execCtx, FetchUserFlow)
        if err != nil {
            return nil, fmt.Errorf("fetch user failed: %w", err)
        }

        // Business logic...
        return order, nil
    },
    pumped.WithFlowTag(pumped.FlowName(), "processOrder"),
)

// Execute flow from main/handler
result, execNode, err := pumped.Exec(scope, ctx, ProcessOrderFlow)
if err != nil {
    // Handle error
}
```

### Scope & Lifecycle

```go
func main() {
    // Create scope
    scope := pumped.NewScope(
        pumped.WithExtension(extensions.NewLoggingExtension()),
    )
    defer scope.Dispose() // CRITICAL: Always dispose

    // Resolve executors
    db, err := pumped.Resolve(scope, DB)
    if err != nil {
        log.Fatalf("failed to resolve DB: %v", err)
    }

    // Graceful shutdown
    sigCh := make(chan os.Signal, 1)
    signal.Notify(sigCh, os.Interrupt, syscall.SIGTERM)
    <-sigCh

    log.Println("Shutting down...")
    scope.Dispose() // Runs all OnCleanup functions
}
```

## 1. Executors (Long-Lived Resources)

**What:** Resources that live for the application's lifetime (or significant portion)

**Examples:** Database connections, HTTP clients, repositories, services, handlers, schedulers

**Key characteristics:**
- Declared as package-level `var`
- Managed by scope (resolved once, cached, cleaned up on dispose)
- Dependencies via controllers
- Lifecycle via `ctx.OnCleanup()`
- Error handling at every step

### Package-Level Var Pattern

**✅ GOOD: Package-level executor declaration**

```go
package graph

var (
    // Group related executors in a single var block
    Config = pumped.Provide(func(ctx *pumped.ResolveCtx) (*Config, error) {
        return DefaultConfig(), nil
    })

    Logger = pumped.Derive1(
        Config.Reactive(),
        func(ctx *pumped.ResolveCtx, cfgCtrl *pumped.Controller[*Config]) (*Logger, error) {
            cfg, err := cfgCtrl.Get()
            if err != nil {
                return nil, err
            }
            return NewLogger(cfg.LogLevel), nil
        },
    )

    DB = pumped.Derive1(
        Config,
        func(ctx *pumped.ResolveCtx, cfgCtrl *pumped.Controller[*Config]) (*sql.DB, error) {
            cfg, err := cfgCtrl.Get()
            if err != nil {
                return nil, err
            }

            db, err := sql.Open("postgres", cfg.DBConnectionString())
            if err != nil {
                return nil, fmt.Errorf("failed to open database: %w", err)
            }

            // CRITICAL: Register cleanup
            ctx.OnCleanup(func() error {
                log.Println("Closing database connection")
                return db.Close()
            })

            return db, nil
        },
    )

    UserRepo = pumped.Derive1(
        DB,
        func(ctx *pumped.ResolveCtx, dbCtrl *pumped.Controller[*sql.DB]) (*UserRepository, error) {
            db, err := dbCtrl.Get()
            if err != nil {
                return nil, err
            }
            return NewUserRepository(db), nil
        },
    )
)
```

**Why package-level vars:**
- Executors are their own keys (no separate ID needed)
- Can reference each other (UserRepo depends on DB)
- Discoverable and testable
- Go idiom for singleton-like resources

**❌ BAD: Local executor variables**

```go
func main() {
    // Don't create executors locally - they should be package-level
    config := pumped.Provide(func(ctx *pumped.ResolveCtx) (*Config, error) {
        return DefaultConfig(), nil
    })
}
```

### Provide vs Derive1-N

**Provide:** No dependencies

```go
var Config = pumped.Provide(func(ctx *pumped.ResolveCtx) (*Config, error) {
    return &Config{
        DBHost: os.Getenv("DB_HOST"),
        DBPort: 5432,
    }, nil
})
```

**Derive1:** One dependency

```go
var DB = pumped.Derive1(
    Config,  // Dependency (default: static mode)
    func(ctx *pumped.ResolveCtx, cfgCtrl *pumped.Controller[*Config]) (*sql.DB, error) {
        cfg, err := cfgCtrl.Get()  // MUST handle error
        if err != nil {
            return nil, err
        }
        // Use cfg to create DB
        return sql.Open("postgres", cfg.ConnectionString())
    },
)
```

**Derive2, Derive3, ... DeriveN:** Multiple dependencies

```go
var UserService = pumped.Derive3(
    DB,
    Logger,
    Cache,
    func(ctx *pumped.ResolveCtx,
        dbCtrl *pumped.Controller[*sql.DB],
        logCtrl *pumped.Controller[*Logger],
        cacheCtrl *pumped.Controller[*Cache]) (*UserService, error) {

        db, err := dbCtrl.Get()
        if err != nil {
            return nil, err
        }
        log, err := logCtrl.Get()
        if err != nil {
            return nil, err
        }
        cache, err := cacheCtrl.Get()
        if err != nil {
            return nil, err
        }

        return NewUserService(db, log, cache), nil
    },
)
```

### Controller Pattern

**All dependencies are passed as `*Controller[T]`** - you must call `.Get()` to access the value.

```go
// ✅ GOOD: Proper controller usage with error handling
var Service = pumped.Derive1(
    DB,
    func(ctx *pumped.ResolveCtx, dbCtrl *pumped.Controller[*sql.DB]) (*Service, error) {
        db, err := dbCtrl.Get()  // Get the value
        if err != nil {
            return nil, fmt.Errorf("failed to get DB: %w", err)
        }

        return NewService(db), nil
    },
)

// ❌ BAD: Forgetting to call .Get()
var Service = pumped.Derive1(
    DB,
    func(ctx *pumped.ResolveCtx, dbCtrl *pumped.Controller[*sql.DB]) (*Service, error) {
        return NewService(dbCtrl)  // Wrong! dbCtrl is not *sql.DB
    },
)

// ❌ BAD: Ignoring errors
var Service = pumped.Derive1(
    DB,
    func(ctx *pumped.ResolveCtx, dbCtrl *pumped.Controller[*sql.DB]) (*Service, error) {
        db, _ := dbCtrl.Get()  // Never ignore errors!
        return NewService(db), nil
    },
)
```

**Why controllers:**
- Enables reactive dependencies (update propagation)
- Provides lifecycle control (reload, update, release)
- Lazy resolution support
- Consistent API across all dependency types

### Static vs Reactive Dependencies

**Static (default):** Resolve once, cache forever

```go
var Service = pumped.Derive1(
    Config,  // Static dependency (default)
    func(ctx *pumped.ResolveCtx, cfgCtrl *pumped.Controller[*Config]) (*Service, error) {
        // This only runs once, even if Config changes
        cfg, err := cfgCtrl.Get()
        if err != nil {
            return nil, err
        }
        return NewService(cfg.MaxConnections), nil
    },
)
```

**Reactive:** Re-resolve when dependency changes

```go
var Service = pumped.Derive1(
    Config.Reactive(),  // Reactive dependency
    func(ctx *pumped.ResolveCtx, cfgCtrl *pumped.Controller[*Config]) (*Service, error) {
        // This re-runs when Config is updated via Accessor.Update()
        cfg, err := cfgCtrl.Get()
        if err != nil {
            return nil, err
        }
        return NewService(cfg.MaxConnections), nil
    },
)
```

**When to use reactive:**
- Configuration-driven resources that should reload
- Services that depend on runtime-updatable settings
- Caches with dynamic size limits

**Note:** Reactivity requires explicit updates via `Accessor`:

```go
configAcc := pumped.Accessor(scope, Config)
err := configAcc.Update(newConfig)  // Triggers re-resolution of reactive dependents
```

### Lifecycle Management with OnCleanup

**CRITICAL:** Always register cleanup for resources that need it.

```go
// ✅ GOOD: Proper cleanup registration
var DB = pumped.Derive1(
    Config,
    func(ctx *pumped.ResolveCtx, cfgCtrl *pumped.Controller[*Config]) (*sql.DB, error) {
        cfg, err := cfgCtrl.Get()
        if err != nil {
            return nil, err
        }

        db, err := sql.Open("postgres", cfg.ConnectionString())
        if err != nil {
            return nil, err
        }

        // Register cleanup - runs when scope.Dispose() is called
        ctx.OnCleanup(func() error {
            log.Println("Closing database connection")
            return db.Close()
        })

        return db, nil
    },
)

// ✅ GOOD: Goroutine cleanup
var Scheduler = pumped.Derive1(
    Logger,
    func(ctx *pumped.ResolveCtx, logCtrl *pumped.Controller[*Logger]) (*Scheduler, error) {
        log, err := logCtrl.Get()
        if err != nil {
            return nil, err
        }

        sched := NewScheduler(log)
        sched.Start()  // Starts background goroutine

        ctx.OnCleanup(func() error {
            log.Info("Stopping scheduler")
            sched.Stop()  // MUST stop goroutine
            return nil
        })

        return sched, nil
    },
)

// ❌ BAD: Missing cleanup for database
var DB = pumped.Derive1(
    Config,
    func(ctx *pumped.ResolveCtx, cfgCtrl *pumped.Controller[*Config]) (*sql.DB, error) {
        cfg, err := cfgCtrl.Get()
        if err != nil {
            return nil, err
        }
        return sql.Open("postgres", cfg.ConnectionString())
        // Missing: ctx.OnCleanup() - connection leak!
    },
)

// ❌ BAD: Missing cleanup for goroutine
var Scheduler = pumped.Derive1(
    Logger,
    func(ctx *pumped.ResolveCtx, logCtrl *pumped.Controller[*Logger]) (*Scheduler, error) {
        log, err := logCtrl.Get()
        if err != nil {
            return nil, err
        }
        sched := NewScheduler(log)
        sched.Start()  // Starts goroutine but never stopped - goroutine leak!
        return sched, nil
    },
)
```

**Cleanup order:** Reverse resolution order (dependencies cleaned up before dependents)

### Error Handling

**Every `.Get()` call returns `(T, error)` - ALWAYS handle errors.**

```go
// ✅ GOOD: Comprehensive error handling
var Service = pumped.Derive2(
    DB,
    Cache,
    func(ctx *pumped.ResolveCtx,
        dbCtrl *pumped.Controller[*sql.DB],
        cacheCtrl *pumped.Controller[*Cache]) (*Service, error) {

        db, err := dbCtrl.Get()
        if err != nil {
            return nil, fmt.Errorf("failed to get database: %w", err)
        }

        cache, err := cacheCtrl.Get()
        if err != nil {
            return nil, fmt.Errorf("failed to get cache: %w", err)
        }

        service, err := NewService(db, cache)
        if err != nil {
            return nil, fmt.Errorf("failed to create service: %w", err)
        }

        return service, nil
    },
)

// ❌ BAD: Ignoring errors
var Service = pumped.Derive1(
    DB,
    func(ctx *pumped.ResolveCtx, dbCtrl *pumped.Controller[*sql.DB]) (*Service, error) {
        db, _ := dbCtrl.Get()  // NEVER do this
        return NewService(db), nil
    },
)

// ❌ BAD: Not wrapping errors
var Service = pumped.Derive1(
    DB,
    func(ctx *pumped.ResolveCtx, dbCtrl *pumped.Controller[*sql.DB]) (*Service, error) {
        db, err := dbCtrl.Get()
        if err != nil {
            return nil, err  // Should wrap: fmt.Errorf("context: %w", err)
        }
        return NewService(db), nil
    },
)
```

## 2. Flows (Short-Span Operations)

**What:** Operations with defined beginning and end (request handling, business logic, transactions)

**When to use:**
- ✅ Request/response cycles
- ✅ Business operations with multiple steps
- ✅ Operations that need execution tracing
- ✅ Operations that compose sub-operations
- ✅ Operations that need tag-based data flow

**When NOT to use:**
- ❌ Pure transformations (use plain functions)
- ❌ Single method calls (use executors directly)
- ❌ Long-running background jobs (use executors with goroutines)

### ❌ Common Mistake: Nil Executor References

**CRITICAL:** Flow dependencies MUST be direct executor references, never nil.

```go
// ❌ WRONG: Nil executor placeholders
var MyFlow = pumped.Flow2(
    nil, // UserRepo - will be set later    ❌ THIS WILL FAIL
    nil, // Logger - will be set later      ❌ THIS WILL FAIL
    func(execCtx *pumped.ExecutionCtx,
        userRepoCtrl *pumped.Controller[*UserRepository],
        logCtrl *pumped.Controller[*Logger]) (*Result, error) {
        // This will never work - executors are nil!
    },
    pumped.WithFlowTag(pumped.FlowName(), "myFlow"),
)

// ✅ CORRECT: Direct executor references
var (
    // Declare executors first
    UserRepo = pumped.Derive1(DB, func(...) (*UserRepository, error) { ... })
    Logger = pumped.Provide(func(...) (*Logger, error) { ... })

    // Flows reference executors directly
    MyFlow = pumped.Flow2(
        UserRepo,  // ✅ Direct reference to package-level var
        Logger,    // ✅ Direct reference to package-level var
        func(execCtx *pumped.ExecutionCtx,
            userRepoCtrl *pumped.Controller[*UserRepository],
            logCtrl *pumped.Controller[*Logger]) (*Result, error) {

            // Now Get() works correctly
            userRepo, err := userRepoCtrl.Get()
            if err != nil {
                return nil, err
            }
            // ...
        },
        pumped.WithFlowTag(pumped.FlowName(), "myFlow"),
    )
)
```

**Why this works:** Executors are package-level variables, so they're available when flows are declared. No separate "initialization" step is needed.

**Common confusion:** Coming from other frameworks where dependencies are "injected later". In pumped-go, executors are their own keys and can be referenced immediately.

### Flow vs Direct Call Decision

```
Need execution tracing/debugging? ───────YES────→ Use Flow
         │
         NO
         ↓
Multiple steps with branching logic? ────YES────→ Use Flow
         │
         NO
         ↓
Compose sub-operations? ─────────────────YES────→ Use Flow
         │
         NO
         ↓
Single service method call? ─────────────YES────→ Direct call
```

**Examples:**

✅ **Use Flow:**
- Process campaign: Fetch jobs → Send emails → Update stats → Log results
- Schedule campaign: Validate input → Check time → Create jobs → Update status
- User registration: Validate → Check duplicates → Create user → Send welcome email

❌ **Don't Use Flow:**
- Get user by ID (single repo call)
- Increment counter (single atomic operation)
- Format string (pure transformation)

### Basic Flow Definition

```go
// Flow with no dependencies
var SimpleFlow = pumped.Flow0(
    func(execCtx *pumped.ExecutionCtx) (string, error) {
        return "result", nil
    },
    pumped.WithFlowTag(pumped.FlowName(), "simpleFlow"),
)

// Flow with 1 dependency
var FetchUserFlow = pumped.Flow1(
    UserRepo,
    func(execCtx *pumped.ExecutionCtx,
        userRepoCtrl *pumped.Controller[*UserRepository]) (*User, error) {

        repo, err := userRepoCtrl.Get()
        if err != nil {
            return nil, err
        }

        // Access Go context (for cancellation, deadlines, values)
        ctx := execCtx.Context()

        // Get input from execution context
        userIDRaw, ok := execCtx.Get(pumped.Input())
        if !ok {
            return nil, fmt.Errorf("user ID not found in context")
        }
        userID := userIDRaw.(string)

        user, err := repo.FindByID(ctx, userID)
        if err != nil {
            return nil, fmt.Errorf("failed to fetch user: %w", err)
        }

        return user, nil
    },
    pumped.WithFlowTag(pumped.FlowName(), "fetchUser"),
)

// Flow with multiple dependencies
var ProcessOrderFlow = pumped.Flow3(
    UserRepo,
    PaymentGateway,
    Logger,
    func(execCtx *pumped.ExecutionCtx,
        userRepoCtrl *pumped.Controller[*UserRepository],
        paymentCtrl *pumped.Controller[*PaymentGateway],
        logCtrl *pumped.Controller[*Logger]) (*Order, error) {

        // Get all dependencies
        userRepo, err := userRepoCtrl.Get()
        if err != nil {
            return nil, err
        }
        payment, err := paymentCtrl.Get()
        if err != nil {
            return nil, err
        }
        log, err := logCtrl.Get()
        if err != nil {
            return nil, err
        }

        // Business logic...
        log.Info("Processing order")
        return processOrder(execCtx.Context(), userRepo, payment)
    },
    pumped.WithFlowTag(pumped.FlowName(), "processOrder"),
)
```

### Executing Flows

**From main or HTTP handlers:**

```go
func main() {
    scope := pumped.NewScope()
    defer scope.Dispose()

    ctx := context.Background()

    // Execute flow
    result, execNode, err := pumped.Exec(scope, ctx, FetchUserFlow)
    if err != nil {
        log.Fatalf("flow execution failed: %v", err)
    }

    // Access execution metadata
    if name, ok := execNode.Get(pumped.FlowName()); ok {
        log.Printf("Flow name: %s", name)
    }

    // Access execution tree
    tree := scope.GetExecutionTree()
    roots := tree.GetRoots()
    // Analyze execution tree for debugging/tracing
}

// HTTP handler example
func (h *Handler) HandleRequest(w http.ResponseWriter, r *http.Request) {
    result, _, err := pumped.Exec(h.scope, r.Context(), ProcessOrderFlow)
    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }
    json.NewEncoder(w).Encode(result)
}
```

### Sub-Flow Composition

**Execute child flows with `Exec1`, `Exec2`, etc.**

```go
var ParentFlow = pumped.Flow2(
    UserRepo,
    OrderRepo,
    func(execCtx *pumped.ExecutionCtx,
        userRepoCtrl *pumped.Controller[*UserRepository],
        orderRepoCtrl *pumped.Controller[*OrderRepository]) (string, error) {

        // Set data for child flows
        execCtx.Set(pumped.Input(), "user-123")

        // Execute sub-flow (inherits scope from execCtx)
        user, userCtx, err := pumped.Exec1(execCtx, FetchUserFlow)
        if err != nil {
            return "", fmt.Errorf("fetch user failed: %w", err)
        }

        // Execute another sub-flow (can use parent or sibling context)
        orders, _, err := pumped.Exec1(userCtx, FetchOrdersFlow)
        if err != nil {
            return "", fmt.Errorf("fetch orders failed: %w", err)
        }

        result := fmt.Sprintf("User %s has %d orders", user.Name, len(orders))
        return result, nil
    },
    pumped.WithFlowTag(pumped.FlowName(), "parentFlow"),
)
```

**Execution context tree:**
- `Exec1(execCtx, flow)` - Execute with current context as parent
- Child contexts inherit scope
- Tag lookups traverse upward (child → parent → scope)

### Tag-Based Data Flow

**Execution contexts support tag-based data storage and lookup:**

```go
var ParentFlow = pumped.Flow0(
    func(execCtx *pumped.ExecutionCtx) (string, error) {
        // Set data in current context
        execCtx.Set(pumped.Input(), "user-123")
        execCtx.Set(customTag, "custom-value")

        // Child flows can access this data
        result, _, err := pumped.Exec1(execCtx, ChildFlow)
        return result, err
    },
)

var ChildFlow = pumped.Flow0(
    func(execCtx *pumped.ExecutionCtx) (string, error) {
        // Get from current context only
        val, ok := execCtx.Get(pumped.Input())

        // Get from parent contexts (traverses upward)
        val, ok := execCtx.GetFromParent(pumped.Input())

        // Get from scope tags
        val, ok := execCtx.GetFromScope(customScopeTag)

        // Lookup: Try current, then parents, then scope
        val, ok := execCtx.Lookup(pumped.Input())  // Most common pattern
        if !ok {
            return "", fmt.Errorf("required data not found")
        }

        userID := val.(string)
        return fmt.Sprintf("Processing user: %s", userID), nil
    },
)
```

**Common tags:**
- `pumped.Input()` - Input data for flows
- `pumped.FlowName()` - Flow identification
- `pumped.Status()` - Execution status
- Custom tags - Create with `pumped.NewTag[T]()`

## 3. Production Lifecycle Management

**Critical for production:** Proper initialization, graceful shutdown, and resource cleanup.

### Scope Management

```go
func main() {
    // Create scope with extensions
    scope := pumped.NewScope(
        pumped.WithExtension(extensions.NewLoggingExtension()),
        // Add other extensions (metrics, tracing, etc.)
    )

    // CRITICAL: Always dispose (runs OnCleanup functions)
    defer scope.Dispose()

    // Resolve executors
    logger, err := pumped.Resolve(scope, Logger)
    if err != nil {
        log.Fatalf("failed to resolve logger: %v", err)
    }

    // Start application...
}
```

### Graceful Shutdown Pattern

```go
func main() {
    scope := pumped.NewScope()
    defer scope.Dispose()

    // Resolve components
    logger, _ := pumped.Resolve(scope, Logger)
    server, _ := pumped.Resolve(scope, HTTPServer)

    // Start server in goroutine
    go func() {
        logger.Info("Server starting on :8080")
        if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
            logger.Error("server error: %v", err)
            os.Exit(1)
        }
    }()

    // Wait for shutdown signal
    sigCh := make(chan os.Signal, 1)
    signal.Notify(sigCh, os.Interrupt, syscall.SIGTERM)
    <-sigCh

    logger.Info("Shutting down gracefully...")

    // Graceful shutdown with timeout
    shutdownCtx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()

    if err := server.Shutdown(shutdownCtx); err != nil {
        logger.Error("server shutdown error: %v", err)
    }

    // scope.Dispose() runs via defer
    // Order: Reverse of resolution (server stops before DB closes)
    logger.Info("Shutdown complete")
}
```

### Cleanup Ordering

**Cleanup runs in reverse resolution order:**

1. Last resolved executor cleaned up first
2. Dependencies cleaned up after dependents
3. Example: HTTP handlers → Services → Repositories → Database

```go
// Resolution order:
// 1. Config
// 2. DB (depends on Config)
// 3. UserRepo (depends on DB)
// 4. UserService (depends on UserRepo)

// Cleanup order (automatic):
// 1. UserService cleanup
// 2. UserRepo cleanup
// 3. DB cleanup (db.Close())
// 4. Config cleanup (if any)
```

**This ensures:** Handlers stop before services, services release before repos, repos close before DB.

### Background Goroutine Management

**ALWAYS stop goroutines in OnCleanup:**

```go
// ✅ GOOD: Goroutine with cleanup
var Scheduler = pumped.Derive1(
    Logger,
    func(ctx *pumped.ResolveCtx, logCtrl *pumped.Controller[*Logger]) (*Scheduler, error) {
        log, err := logCtrl.Get()
        if err != nil {
            return nil, err
        }

        sched := &Scheduler{
            logger: log,
            stopCh: make(chan struct{}),
        }

        // Start background goroutine
        go sched.run()

        // CRITICAL: Register cleanup
        ctx.OnCleanup(func() error {
            log.Info("Stopping scheduler")
            close(sched.stopCh)  // Signal goroutine to stop
            return nil
        })

        return sched, nil
    },
)

type Scheduler struct {
    logger *Logger
    stopCh chan struct{}
}

func (s *Scheduler) run() {
    ticker := time.NewTicker(5 * time.Second)
    defer ticker.Stop()

    for {
        select {
        case <-ticker.C:
            s.logger.Info("Scheduler tick")
            // Do work...
        case <-s.stopCh:
            s.logger.Info("Scheduler stopped")
            return  // Exit goroutine
        }
    }
}
```

## 4. Interaction Points

**Where external world meets your application**

### HTTP Handlers

```go
// Handler as executor (receives dependencies)
var UserHandler = pumped.Derive2(
    UserRepo,
    Logger,
    func(ctx *pumped.ResolveCtx,
        userRepoCtrl *pumped.Controller[*UserRepository],
        logCtrl *pumped.Controller[*Logger]) (*UserHandler, error) {

        userRepo, err := userRepoCtrl.Get()
        if err != nil {
            return nil, err
        }
        log, err := logCtrl.Get()
        if err != nil {
            return nil, err
        }

        return &UserHandler{
            userRepo: userRepo,
            logger:   log,
        }, nil
    },
)

type UserHandler struct {
    userRepo *UserRepository
    logger   *Logger
}

func (h *UserHandler) GetUser(w http.ResponseWriter, r *http.Request) {
    userID := r.PathValue("id")

    user, err := h.userRepo.FindByID(r.Context(), userID)
    if err != nil {
        h.logger.Error("failed to fetch user: %v", err)
        http.Error(w, "User not found", http.StatusNotFound)
        return
    }

    json.NewEncoder(w).Encode(user)
}

// Main function
func main() {
    scope := pumped.NewScope()
    defer scope.Dispose()

    userHandler, err := pumped.Resolve(scope, UserHandler)
    if err != nil {
        log.Fatalf("failed to resolve handler: %v", err)
    }

    mux := http.NewServeMux()
    mux.HandleFunc("GET /users/{id}", userHandler.GetUser)

    server := &http.Server{
        Addr:    ":8080",
        Handler: mux,
    }

    // Start and shutdown as shown in Lifecycle section
}
```

**Executing Flows in Handlers:**

Handlers should use flows for multi-step operations to enable execution tracing and observability.

```go
// Define custom tags for flow input (in flows/ or graph.go)
var (
    OrderIDTag = pumped.NewTag[string]("order.id")
    OrderItemsTag = pumped.NewTag[[]OrderItem]("order.items")
)

// Define flow with dependencies
var ProcessOrderFlow = pumped.Flow3(
    OrderRepo,
    InventoryService,
    PaymentService,
    func(execCtx *pumped.ExecutionCtx,
        orderRepoCtrl *pumped.Controller[*OrderRepository],
        inventoryCtrl *pumped.Controller[*InventoryService],
        paymentCtrl *pumped.Controller[*PaymentService]) (*Order, error) {

        // Get dependencies
        orderRepo, err := orderRepoCtrl.Get()
        if err != nil {
            return nil, err
        }
        inventory, err := inventoryCtrl.Get()
        if err != nil {
            return nil, err
        }
        payment, err := paymentCtrl.Get()
        if err != nil {
            return nil, err
        }

        // Get input from execution context
        orderID, ok := execCtx.Lookup(OrderIDTag)
        if !ok {
            return nil, fmt.Errorf("order ID not found")
        }
        items, ok := execCtx.Lookup(OrderItemsTag)
        if !ok {
            return nil, fmt.Errorf("order items not found")
        }

        // Multi-step business logic
        // Step 1: Check inventory
        available, err := inventory.CheckStock(execCtx.Context(), items.([]OrderItem))
        if err != nil {
            return nil, fmt.Errorf("inventory check failed: %w", err)
        }
        if !available {
            return nil, fmt.Errorf("insufficient stock")
        }

        // Step 2: Process payment
        charged, err := payment.Charge(execCtx.Context(), calculateTotal(items.([]OrderItem)))
        if err != nil {
            return nil, fmt.Errorf("payment failed: %w", err)
        }

        // Step 3: Create order
        order, err := orderRepo.Create(execCtx.Context(), orderID.(string), items.([]OrderItem), charged)
        if err != nil {
            return nil, fmt.Errorf("order creation failed: %w", err)
        }

        return order, nil
    },
    pumped.WithFlowTag(pumped.FlowName(), "processOrder"),
)

// Handler with scope
type OrderHandler struct {
    scope *pumped.Scope
}

func (h *OrderHandler) ProcessOrder(w http.ResponseWriter, r *http.Request) {
    var input ProcessOrderInput
    if err := json.NewDecoder(r.Body).Decode(&input); err != nil {
        http.Error(w, "Invalid input", http.StatusBadRequest)
        return
    }

    // Validate input
    if len(input.Items) == 0 {
        http.Error(w, "No items in order", http.StatusBadRequest)
        return
    }

    // Set input tags in scope
    h.scope.SetTag(OrderIDTag, input.OrderID)
    h.scope.SetTag(OrderItemsTag, input.Items)

    // Execute flow
    order, execNode, err := pumped.Exec(h.scope, r.Context(), ProcessOrderFlow)
    if err != nil {
        // Log error with execution context
        log.Printf("Flow execution failed: %v", err)
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }

    // Access execution metadata for logging/tracing
    if flowName, ok := execNode.Get(pumped.FlowName()); ok {
        log.Printf("Successfully executed flow: %s", flowName)
    }

    // Can access execution tree for debugging
    tree := h.scope.GetExecutionTree()
    roots := tree.GetRoots()
    log.Printf("Execution tree has %d root nodes", len(roots))

    w.WriteHeader(http.StatusCreated)
    json.NewEncoder(w).Encode(order)
}
```

**Why use flows in handlers:**
- ✅ Execution tracing - see exactly what happened in request
- ✅ Execution tree - visualize operation flow for debugging
- ✅ Tag-based input - clean data passing without global state
- ✅ Observable - extensions can hook into flow lifecycle
- ✅ Testable - mock executors, verify flow logic independently

**When NOT to use flows in handlers:**
- ❌ Simple CRUD operations (single repo call)
- ❌ Direct data fetching (no business logic)
- ❌ Trivial transformations

**Complete Handler Example with Flows:**

```go
// graph.go - Define everything
var (
    // Executors
    UserRepo = pumped.Derive1(DB, func(...) (*UserRepository, error) { ... })
    EmailService = pumped.Derive1(SMTP, func(...) (*EmailService, error) { ... })

    // Tags
    UserEmailTag = pumped.NewTag[string]("user.email")
    UserNameTag = pumped.NewTag[string]("user.name")

    // Flow
    RegisterUserFlow = pumped.Flow2(
        UserRepo,
        EmailService,
        func(execCtx *pumped.ExecutionCtx,
            userRepoCtrl *pumped.Controller[*UserRepository],
            emailCtrl *pumped.Controller[*EmailService]) (*User, error) {

            userRepo, err := userRepoCtrl.Get()
            if err != nil {
                return nil, err
            }
            email, err := emailCtrl.Get()
            if err != nil {
                return nil, err
            }

            // Get input
            emailAddr, _ := execCtx.Lookup(UserEmailTag)
            name, _ := execCtx.Lookup(UserNameTag)

            // Check duplicates
            existing, err := userRepo.FindByEmail(execCtx.Context(), emailAddr.(string))
            if err == nil && existing != nil {
                return nil, fmt.Errorf("email already registered")
            }

            // Create user
            user, err := userRepo.Create(execCtx.Context(), emailAddr.(string), name.(string))
            if err != nil {
                return nil, fmt.Errorf("failed to create user: %w", err)
            }

            // Send welcome email
            err = email.SendWelcome(execCtx.Context(), user.Email)
            if err != nil {
                // Non-fatal, log but don't fail
                log.Printf("Failed to send welcome email: %v", err)
            }

            return user, nil
        },
        pumped.WithFlowTag(pumped.FlowName(), "registerUser"),
    )

    // Handler as executor
    UserHandler = pumped.Provide(func(ctx *pumped.ResolveCtx) (*UserHandlerImpl, error) {
        return &UserHandlerImpl{}, nil
    })
)

// Handler implementation
type UserHandlerImpl struct {
    scope *pumped.Scope
}

func (h *UserHandlerImpl) Register(w http.ResponseWriter, r *http.Request) {
    var input RegisterInput
    if err := json.NewDecoder(r.Body).Decode(&input); err != nil {
        http.Error(w, "Invalid input", http.StatusBadRequest)
        return
    }

    // Set input tags
    h.scope.SetTag(UserEmailTag, input.Email)
    h.scope.SetTag(UserNameTag, input.Name)

    // Execute flow
    user, _, err := pumped.Exec(h.scope, r.Context(), RegisterUserFlow)
    if err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }

    w.WriteHeader(http.StatusCreated)
    json.NewEncoder(w).Encode(user)
}

// main.go - Wire everything together
func main() {
    scope := pumped.NewScope()
    defer scope.Dispose()

    userHandler, err := pumped.Resolve(scope, UserHandler)
    if err != nil {
        log.Fatalf("failed to resolve handler: %v", err)
    }

    // Pass scope to handler
    userHandler.scope = scope

    mux := http.NewServeMux()
    mux.HandleFunc("POST /users/register", userHandler.Register)

    server := &http.Server{Addr: ":8080", Handler: mux}

    go func() {
        if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
            log.Fatalf("server error: %v", err)
        }
    }()

    // Graceful shutdown...
}
```

### CLI Commands

```go
func main() {
    scope := pumped.NewScope()
    defer scope.Dispose()

    taskService, err := pumped.Resolve(scope, TaskService)
    if err != nil {
        log.Fatalf("failed to resolve service: %v", err)
    }

    app := &cli.App{
        Commands: []*cli.Command{
            {
                Name:  "add",
                Usage: "Add a new task",
                Action: func(c *cli.Context) error {
                    task := &Task{
                        Title: c.Args().First(),
                    }
                    return taskService.Create(c.Context, task)
                },
            },
            {
                Name:  "list",
                Usage: "List all tasks",
                Action: func(c *cli.Context) error {
                    tasks, err := taskService.List(c.Context)
                    if err != nil {
                        return err
                    }
                    for _, task := range tasks {
                        fmt.Printf("- %s\n", task.Title)
                    }
                    return nil
                },
            },
        },
    }

    if err := app.Run(os.Args); err != nil {
        log.Fatal(err)
    }
}
```

## 5. Testing Strategies

### Testing Executors with WithPreset

**Replace executors with mocks/test implementations:**

```go
func TestGraph_UserService(t *testing.T) {
    // Create mock repository
    mockRepo := &MockUserRepository{
        users: map[string]*User{
            "user-1": {ID: "user-1", Name: "Alice"},
        },
    }

    // Create test scope with preset
    testScope := pumped.NewScope(
        pumped.WithPreset(UserRepo, mockRepo),
    )
    defer testScope.Dispose()

    // Resolve service (will get mock repo)
    service, err := pumped.Resolve(testScope, UserService)
    if err != nil {
        t.Fatalf("failed to resolve service: %v", err)
    }

    // Test service
    user, err := service.GetUser("user-1")
    if err != nil {
        t.Fatalf("failed to get user: %v", err)
    }

    if user.Name != "Alice" {
        t.Errorf("expected name Alice, got %s", user.Name)
    }
}
```

### Table-Driven Tests (Go Idiom)

```go
func TestGraph_AllComponentsResolve(t *testing.T) {
    testScope := pumped.NewScope(
        pumped.WithPreset(Config, &Config{DBPath: ":memory:"}),
    )
    defer testScope.Dispose()

    tests := []struct {
        name string
        fn   func() error
    }{
        {"Logger", func() error {
            _, err := pumped.Resolve(testScope, Logger)
            return err
        }},
        {"DB", func() error {
            _, err := pumped.Resolve(testScope, DB)
            return err
        }},
        {"UserRepo", func() error {
            _, err := pumped.Resolve(testScope, UserRepo)
            return err
        }},
        {"UserService", func() error {
            _, err := pumped.Resolve(testScope, UserService)
            return err
        }},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            if err := tt.fn(); err != nil {
                t.Errorf("failed to resolve %s: %v", tt.name, err)
            }
        })
    }
}
```

### Testing Reactivity

```go
func TestGraph_ConfigReactivity(t *testing.T) {
    initialConfig := &Config{LogLevel: "info"}

    testScope := pumped.NewScope(
        pumped.WithPreset(Config, initialConfig),
    )
    defer testScope.Dispose()

    // Resolve logger (reactive to Config)
    logger1, _ := pumped.Resolve(testScope, Logger)
    if logger1.Level != "info" {
        t.Errorf("expected info level, got %s", logger1.Level)
    }

    // Update config
    configAcc := pumped.Accessor(testScope, Config)
    newConfig := &Config{LogLevel: "debug"}
    err := configAcc.Update(newConfig)
    if err != nil {
        t.Fatalf("failed to update config: %v", err)
    }

    // Resolve logger again (should be new instance)
    logger2, _ := pumped.Resolve(testScope, Logger)
    if logger1 == logger2 {
        t.Error("expected logger to be re-initialized")
    }
    if logger2.Level != "debug" {
        t.Errorf("expected debug level, got %s", logger2.Level)
    }
}
```

### Testing Flows

```go
func TestFlow_FetchUser(t *testing.T) {
    mockRepo := &MockUserRepository{
        users: map[string]*User{
            "user-1": {ID: "user-1", Name: "Alice"},
        },
    }

    testScope := pumped.NewScope(
        pumped.WithPreset(UserRepo, mockRepo),
    )
    defer testScope.Dispose()

    ctx := context.Background()

    // Execute flow
    result, execNode, err := pumped.Exec(testScope, ctx, FetchUserFlow)
    if err != nil {
        t.Fatalf("flow execution failed: %v", err)
    }

    if result.Name != "Alice" {
        t.Errorf("expected Alice, got %s", result.Name)
    }

    // Verify execution metadata
    if name, ok := execNode.Get(pumped.FlowName()); ok {
        if name != "fetchUser" {
            t.Errorf("expected flow name fetchUser, got %s", name)
        }
    }
}
```

### Integration Tests

```go
func TestIntegration_HealthMonitor(t *testing.T) {
    if testing.Short() {
        t.Skip("skipping integration test in short mode")
    }

    // Use real implementations
    testScope := pumped.NewScope(
        pumped.WithPreset(Config, &Config{
            DBPath:   ":memory:",  // In-memory SQLite
            LogLevel: "info",
        }),
    )
    defer testScope.Dispose()

    // Resolve and test with real database
    db, err := pumped.Resolve(testScope, DB)
    if err != nil {
        t.Fatalf("failed to resolve DB: %v", err)
    }

    // Run migrations, seed data, etc.
    // Test actual database operations
}
```

## 6. Enforcement Rules

### Tier 1: Critical (MUST Follow for Production)

**Package-Level Executor Declaration**
- ✅ ALL executors MUST be package-level `var`
- ❌ NEVER create executors in functions
- **Why:** Executors are their own keys; local variables can't be referenced

**Error Handling**
- ✅ ALWAYS handle errors from `ctrl.Get()`
- ✅ ALWAYS wrap errors with context (`fmt.Errorf("context: %w", err)`)
- ❌ NEVER ignore errors (`_, _ := ctrl.Get()`)
- **Why:** Silent failures are production killers

**Lifecycle Management**
- ✅ ALWAYS call `scope.Dispose()` (use `defer`)
- ✅ ALWAYS register `ctx.OnCleanup()` for resources (DB, HTTP clients, goroutines)
- ❌ NEVER leak resources (connections, goroutines, file handles)
- **Why:** Resource leaks crash production systems

**Goroutine Safety**
- ✅ ALWAYS stop goroutines in `OnCleanup`
- ✅ ALWAYS use channels or context for goroutine signaling
- ❌ NEVER start goroutines without cleanup
- **Why:** Orphaned goroutines cause memory leaks and zombie behavior

### Tier 2: Important (Strong Recommendations)

**Dependency Modes**
- Use `.Reactive()` only for runtime-updatable dependencies
- Default to static dependencies (better performance)
- Document why reactive is needed

**Flow Usage**
- Use flows for multi-step operations with tracing needs
- Use plain functions for simple transformations
- Don't over-use flows for single method calls

**Testing**
- Test all executors resolve without errors
- Test reactivity when using `.Reactive()`
- Use table-driven tests (Go idiom)
- Separate unit tests from integration tests

**Code Organization**
- Group related executors in `graph.go` or `graph/` package
- Separate concerns: config → infra → repos → services → handlers
- Use meaningful executor variable names (e.g., `UserRepo`, not `UR`)

### Tier 3: Best Practices

**Naming Conventions**
- Executor variables: `PascalCase` (e.g., `UserService`, `DBExec`)
- Flow variables: `PascalCase` with `Flow` suffix (e.g., `ProcessOrderFlow`)
- Factory functions: Use controllers with meaningful parameter names

**Documentation**
- Comment executor groups explaining purpose
- Document reactive dependencies (why reactive vs static)
- Explain cleanup behavior for non-obvious resources

**Extensions**
- Use logging extension for production observability
- Add metrics extension for monitoring
- Consider tracing extension for distributed systems

**Graceful Shutdown**
- Always implement signal handling
- Use context timeouts for shutdown operations
- Log shutdown steps for debugging

## Common Patterns

### Repository Pattern with Executors

```go
var (
    DB = pumped.Derive1(
        Config,
        func(ctx *pumped.ResolveCtx, cfgCtrl *pumped.Controller[*Config]) (*sql.DB, error) {
            // Database setup...
        },
    )

    UserRepo = pumped.Derive1(
        DB,
        func(ctx *pumped.ResolveCtx, dbCtrl *pumped.Controller[*sql.DB]) (*UserRepository, error) {
            db, err := dbCtrl.Get()
            if err != nil {
                return nil, err
            }
            return NewUserRepository(db), nil
        },
    )

    PostRepo = pumped.Derive1(
        DB,
        func(ctx *pumped.ResolveCtx, dbCtrl *pumped.Controller[*sql.DB]) (*PostRepository, error) {
            db, err := dbCtrl.Get()
            if err != nil {
                return nil, err
            }
            return NewPostRepository(db), nil
        },
    )
)
```

### Service Layer Composition

```go
var (
    UserService = pumped.Derive2(
        UserRepo,
        Logger,
        func(ctx *pumped.ResolveCtx,
            userRepoCtrl *pumped.Controller[*UserRepository],
            logCtrl *pumped.Controller[*Logger]) (*UserService, error) {

            userRepo, err := userRepoCtrl.Get()
            if err != nil {
                return nil, err
            }
            log, err := logCtrl.Get()
            if err != nil {
                return nil, err
            }

            return NewUserService(userRepo, log), nil
        },
    )

    PostService = pumped.Derive3(
        PostRepo,
        UserService,  // Service depends on another service
        Logger,
        func(ctx *pumped.ResolveCtx,
            postRepoCtrl *pumped.Controller[*PostRepository],
            userServiceCtrl *pumped.Controller[*UserService],
            logCtrl *pumped.Controller[*Logger]) (*PostService, error) {

            postRepo, err := postRepoCtrl.Get()
            if err != nil {
                return nil, err
            }
            userService, err := userServiceCtrl.Get()
            if err != nil {
                return nil, err
            }
            log, err := logCtrl.Get()
            if err != nil {
                return nil, err
            }

            return NewPostService(postRepo, userService, log), nil
        },
    )
)
```

### Handler Dependency Injection

```go
var (
    UserHandler = pumped.Derive2(
        UserService,
        Logger,
        func(ctx *pumped.ResolveCtx,
            userServiceCtrl *pumped.Controller[*UserService],
            logCtrl *pumped.Controller[*Logger]) (*UserHandler, error) {

            userService, err := userServiceCtrl.Get()
            if err != nil {
                return nil, err
            }
            log, err := logCtrl.Get()
            if err != nil {
                return nil, err
            }

            return &UserHandler{
                userService: userService,
                logger:      log,
            }, nil
        },
    )
)

func main() {
    scope := pumped.NewScope()
    defer scope.Dispose()

    userHandler, _ := pumped.Resolve(scope, UserHandler)

    mux := http.NewServeMux()
    mux.HandleFunc("GET /users/{id}", userHandler.GetUser)
    mux.HandleFunc("POST /users", userHandler.CreateUser)

    // Server setup...
}
```

### Background Worker Lifecycle

```go
var Scheduler = pumped.Derive2(
    ServiceRepo,
    Logger,
    func(ctx *pumped.ResolveCtx,
        serviceRepoCtrl *pumped.Controller[ServiceRepo],
        logCtrl *pumped.Controller[*Logger]) (*Scheduler, error) {

        serviceRepo, err := serviceRepoCtrl.Get()
        if err != nil {
            return nil, err
        }
        log, err := logCtrl.Get()
        if err != nil {
            return nil, err
        }

        sched := NewScheduler(serviceRepo, log)
        sched.Start()  // Starts background goroutine

        ctx.OnCleanup(func() error {
            log.Info("Stopping scheduler")
            sched.Stop()  // Stops goroutine
            return nil
        })

        return sched, nil
    },
)

type Scheduler struct {
    serviceRepo ServiceRepo
    logger      *Logger
    ticker      *time.Ticker
    stopCh      chan struct{}
}

func (s *Scheduler) Start() {
    s.ticker = time.NewTicker(5 * time.Second)
    s.stopCh = make(chan struct{})

    go func() {
        for {
            select {
            case <-s.ticker.C:
                s.runHealthChecks()
            case <-s.stopCh:
                s.logger.Info("Scheduler stopped")
                return
            }
        }
    }()
}

func (s *Scheduler) Stop() {
    s.ticker.Stop()
    close(s.stopCh)
}
```

## Troubleshooting Common Issues

### Problem: Flows defined but not executing

**Symptom:** You created flows but they're never called, or handlers don't use them.

**Solution:** Flows must be explicitly executed with `pumped.Exec()`:

```go
// ❌ Wrong - Flow defined but never used
var MyFlow = pumped.Flow1(UserRepo, func(...) { ... })

func (h *Handler) DoWork(w http.ResponseWriter, r *http.Request) {
    // Handler calls services directly, flow is ignored
    result := h.service.DoWork()
}

// ✅ Correct - Execute flow from handler
func (h *Handler) DoWork(w http.ResponseWriter, r *http.Request) {
    result, _, err := pumped.Exec(h.scope, r.Context(), MyFlow)
    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }
    // Use result...
}
```

### Problem: Nil pointer dereference in flow execution

**Symptom:** `panic: nil pointer dereference` when executing flow, or `nil executor` error.

**Cause:** Flow defined with nil executors instead of executor references.

**Solution:** Use direct executor references (see "Common Mistake: Nil Executor References" section):

```go
// ❌ Wrong
var MyFlow = pumped.Flow1(
    nil,  // ❌ This causes nil pointer errors
    func(...) { ... },
)

// ✅ Correct
var (
    UserRepo = pumped.Derive1(DB, func(...) (*UserRepository, error) { ... })

    MyFlow = pumped.Flow1(
        UserRepo,  // ✅ Direct reference to executor
        func(...) { ... },
    )
)
```

### Problem: Resource leaks on shutdown

**Symptom:** Database connections, goroutines, or file handles not cleaned up. Application hangs on shutdown.

**Cause:** Missing `OnCleanup()` registration or missing `scope.Dispose()`.

**Solution 1:** Register cleanup in executor:

```go
var DB = pumped.Derive1(Config, func(ctx *pumped.ResolveCtx, ...) (*sql.DB, error) {
    db, err := sql.Open(...)
    if err != nil {
        return nil, err
    }

    // ✅ Register cleanup
    ctx.OnCleanup(func() error {
        log.Println("Closing database connection")
        return db.Close()
    })

    return db, nil
})
```

**Solution 2:** Always dispose scope:

```go
func main() {
    scope := pumped.NewScope()
    defer scope.Dispose()  // ✅ CRITICAL - runs all OnCleanup functions

    // Application code...
}
```

**Solution 3:** Stop goroutines in cleanup:

```go
var Worker = pumped.Derive1(Logger, func(ctx *pumped.ResolveCtx, ...) (*Worker, error) {
    worker := NewWorker()
    worker.Start()  // Starts background goroutine

    // ✅ Register goroutine cleanup
    ctx.OnCleanup(func() error {
        log.Println("Stopping worker")
        worker.Stop()  // Must stop goroutine!
        return nil
    })

    return worker, nil
})
```

### Problem: Config changes don't propagate

**Symptom:** Updated config via `Accessor.Update()` but dependent services didn't reload.

**Cause:** Forgot `.Reactive()` on dependency declaration.

**Solution:** Use `.Reactive()` for dependencies that should reload:

```go
// ❌ Wrong - Static dependency (won't reload)
var Service = pumped.Derive1(
    Config,  // Static mode (default)
    func(...) { ... },
)

// ✅ Correct - Reactive dependency (reloads on config update)
var Service = pumped.Derive1(
    Config.Reactive(),  // ✅ Will re-resolve when Config updates
    func(ctx *pumped.ResolveCtx, cfgCtrl *pumped.Controller[*Config]) (*Service, error) {
        cfg, err := cfgCtrl.Get()
        if err != nil {
            return nil, err
        }
        return NewService(cfg.MaxConnections), nil
    },
)

// Update config (triggers reactive dependents)
configAcc := pumped.Accessor(scope, Config)
err := configAcc.Update(newConfig)
```

### Problem: Tests fail with "executor not found" or similar

**Symptom:** Tests can't resolve executors or get unexpected errors.

**Cause:** Test scope doesn't have required presets or wrong executor referenced.

**Solution:** Use `WithPreset()` to provide test implementations:

```go
func TestService(t *testing.T) {
    // Create mock
    mockRepo := &MockUserRepository{
        users: map[string]*User{
            "test-id": {ID: "test-id", Name: "Test User"},
        },
    }

    // Create test scope with preset
    testScope := pumped.NewScope(
        pumped.WithPreset(UserRepo, mockRepo),  // ✅ Provide mock
    )
    defer testScope.Dispose()

    // Resolve service (will get mock repo)
    service, err := pumped.Resolve(testScope, UserService)
    if err != nil {
        t.Fatalf("failed to resolve: %v", err)
    }

    // Test with mock...
}
```

### Problem: Executor resolution fails with dependency errors

**Symptom:** `failed to get <dependency>: ...` errors during executor resolution.

**Cause:** Dependency chain broken, or executor factory returns error.

**Solution:** Check entire dependency chain:

```go
// If UserService fails to resolve:
// 1. Check UserService factory
var UserService = pumped.Derive1(
    UserRepo,
    func(ctx *pumped.ResolveCtx, repoCtrl *pumped.Controller[*UserRepository]) (*UserService, error) {
        repo, err := repoCtrl.Get()  // ✅ Check this error
        if err != nil {
            return nil, fmt.Errorf("failed to get repo: %w", err)  // This tells you the issue
        }
        return NewUserService(repo), nil
    },
)

// 2. Check UserRepo factory
var UserRepo = pumped.Derive1(
    DB,
    func(ctx *pumped.ResolveCtx, dbCtrl *pumped.Controller[*sql.DB]) (*UserRepository, error) {
        db, err := dbCtrl.Get()  // ✅ Check this error
        if err != nil {
            return nil, fmt.Errorf("failed to get DB: %w", err)  // Propagates the issue
        }
        return NewUserRepository(db), nil
    },
)

// 3. Check DB factory (root cause might be here)
var DB = pumped.Derive1(
    Config,
    func(ctx *pumped.ResolveCtx, cfgCtrl *pumped.Controller[*Config]) (*sql.DB, error) {
        cfg, err := cfgCtrl.Get()
        if err != nil {
            return nil, fmt.Errorf("failed to get config: %w", err)
        }
        db, err := sql.Open("postgres", cfg.DSN)
        if err != nil {
            return nil, fmt.Errorf("failed to open DB: %w", err)  // ✅ Root cause
        }
        return db, nil
    },
)
```

**Debugging tip:** Errors propagate up the chain with context. Read the full error message to trace back to the root cause.

### Problem: Application hangs on shutdown

**Symptom:** Application doesn't exit cleanly when interrupted (Ctrl+C).

**Cause:** Missing signal handling or cleanup taking too long.

**Solution:** Implement proper graceful shutdown:

```go
func main() {
    scope := pumped.NewScope()
    defer scope.Dispose()

    // Setup signal handling
    sigCh := make(chan os.Signal, 1)
    signal.Notify(sigCh, os.Interrupt, syscall.SIGTERM)

    // Start server in goroutine
    go func() {
        if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
            log.Fatalf("server error: %v", err)
        }
    }()

    // Wait for signal
    <-sigCh
    log.Println("Shutting down...")

    // Shutdown server with timeout
    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()

    if err := server.Shutdown(ctx); err != nil {
        log.Printf("server shutdown error: %v", err)
    }

    // scope.Dispose() runs via defer (cleanup executors)
    log.Println("Shutdown complete")
}
```

## Coding Style

### Flat Structure Over Subfolders

**CRITICAL:** Keep project structure flat. Avoid overcomplicated nested folders.

**✅ CORRECT: Flat structure**
```
myapp/
├── main.go
├── graph.go          // All executors
├── graph_test.go
├── user.go           // User domain (repo + service)
├── user_test.go
├── order.go          // Order domain
├── order_test.go
└── worker.go         // Background workers
```

**❌ WRONG: Over-nested structure**
```
myapp/
├── cmd/
│   └── server/
│       └── main.go
├── internal/
│   ├── domain/
│   │   ├── user/
│   │   │   ├── repository/
│   │   │   │   └── postgres/
│   │   │   │       └── user_repository.go
│   │   │   └── service/
│   │   │       └── user_service.go
```

**Why flat structure:**
- Faster navigation (no deep nesting)
- Clearer dependencies (all in one file)
- Less boilerplate (no package-per-file overhead)
- Go idiom: organize by feature, not by layer

**When to create subdirectories:**
- Multiple related types need grouping (e.g., `models/` for 10+ domain models)
- Shared utilities used across features (e.g., `testutil/` for test helpers)
- Examples or docs (e.g., `examples/`, `docs/`)

**Rule of thumb:** If you can fit it in one file, keep it there. If a file grows beyond 500 lines, split by feature/domain, not by technical layer.

### Zero Comments Rule

**CRITICAL:** Code should be self-documenting. No comments needed.

**✅ CORRECT: Self-documenting code**
```go
var UserRepo = pumped.Derive1(
    DB,
    func(ctx *pumped.ResolveCtx, dbCtrl *pumped.Controller[*sql.DB]) (*UserRepository, error) {
        db, err := dbCtrl.Get()
        if err != nil {
            return nil, fmt.Errorf("failed to get database: %w", err)
        }

        ctx.OnCleanup(func() error {
            return db.Close()
        })

        return &UserRepository{db: db}, nil
    },
)
```

**❌ WRONG: Over-commented code**
```go
// UserRepo is a repository for users
var UserRepo = pumped.Derive1(
    DB, // Database dependency
    func(ctx *pumped.ResolveCtx, dbCtrl *pumped.Controller[*sql.DB]) (*UserRepository, error) {
        // Get the database controller
        db, err := dbCtrl.Get()
        if err != nil {
            // Return error if we can't get the database
            return nil, fmt.Errorf("failed to get database: %w", err)
        }

        // Register cleanup handler
        ctx.OnCleanup(func() error {
            // Close the database connection
            return db.Close()
        })

        // Create and return repository
        return &UserRepository{db: db}, nil
    },
)
```

**Why zero comments:**
- Code explains itself through clear naming
- Error messages provide context
- Type signatures document expectations
- Tests show usage patterns

**Exceptions (rare):**
- Complex algorithms requiring explanation (document the "why", not the "what")
- Non-obvious performance optimizations
- Package-level godoc for exported APIs
- TODO markers for known issues

**Best practices:**
- Use descriptive variable names (`user` not `u`, `database` not `db` in contexts where clarity matters)
- Error messages should explain what failed (not code comments)
- Function names should describe what they do
- Type names should describe what they represent

## Configuration Patterns

### Dual-Mode Configuration

**CRITICAL:** Configuration should support both default values AND tag-based overrides via scope.

### Pattern 1: Default Configuration

**Every application needs sensible defaults.**

```go
var Config = pumped.Provide(func(ctx *pumped.ResolveCtx) (*Config, error) {
    return &Config{
        DBHost:     "localhost",
        DBPort:     5432,
        DBName:     "myapp",
        ServerPort: 8080,
        LogLevel:   "info",
    }, nil
})
```

### Pattern 2: Tag-Based Override

**Allow runtime configuration via scope tags.**

```go
var (
    // Define tags for configuration
    DBHostTag     = pumped.NewTag[string]("config.db.host")
    DBPortTag     = pumped.NewTag[int]("config.db.port")
    ServerPortTag = pumped.NewTag[int]("config.server.port")
)

var Config = pumped.Provide(func(ctx *pumped.ResolveCtx) (*Config, error) {
    cfg := &Config{
        DBHost:     "localhost",
        DBPort:     5432,
        DBName:     "myapp",
        ServerPort: 8080,
        LogLevel:   "info",
    }

    scope := ctx.Scope()

    if host, ok := scope.GetTag(DBHostTag); ok {
        cfg.DBHost = host
    }

    if port, ok := scope.GetTag(DBPortTag); ok {
        cfg.DBPort = port
    }

    if serverPort, ok := scope.GetTag(ServerPortTag); ok {
        cfg.ServerPort = serverPort
    }

    return cfg, nil
})
```

### Pattern 3: Usage in Main

**Set tags on scope creation for different environments.**

```go
func main() {
    scope := pumped.NewScope(
        pumped.WithTag(DBHostTag, os.Getenv("DB_HOST")),
        pumped.WithTag(DBPortTag, 5433),
        pumped.WithTag(ServerPortTag, 3000),
    )
    defer scope.Dispose()

    configCtrl := pumped.Controller(scope, Config)
    cfg, err := configCtrl.Get()
    if err != nil {
        log.Fatalf("failed to load config: %v", err)
    }

    log.Printf("Starting server on port %d", cfg.ServerPort)
}
```

### Pattern 4: Environment-Based Configuration

**Load from environment variables with defaults.**

```go
var Config = pumped.Provide(func(ctx *pumped.ResolveCtx) (*Config, error) {
    cfg := &Config{
        DBHost:     getEnv("DB_HOST", "localhost"),
        DBPort:     getEnvInt("DB_PORT", 5432),
        DBName:     getEnv("DB_NAME", "myapp"),
        ServerPort: getEnvInt("SERVER_PORT", 8080),
        LogLevel:   getEnv("LOG_LEVEL", "info"),
    }

    scope := ctx.Scope()

    if host, ok := scope.GetTag(DBHostTag); ok {
        cfg.DBHost = host
    }

    if port, ok := scope.GetTag(DBPortTag); ok {
        cfg.DBPort = port
    }

    return cfg, nil
})

func getEnv(key, defaultValue string) string {
    if value := os.Getenv(key); value != "" {
        return value
    }
    return defaultValue
}

func getEnvInt(key string, defaultValue int) int {
    if value := os.Getenv(key); value != "" {
        if i, err := strconv.Atoi(value); err == nil {
            return i
        }
    }
    return defaultValue
}
```

### Configuration Priority

**Order of precedence (highest to lowest):**

1. **Scope tags** - Highest priority, set at runtime
2. **Environment variables** - Middle priority, set at deployment
3. **Default values** - Lowest priority, hardcoded in Config executor

**Example:**
```go
// main.go
scope := pumped.NewScope(
    pumped.WithTag(ServerPortTag, 9000), // Highest priority
)

// Config executor checks:
// 1. Scope tag (9000) ✅ Used
// 2. Environment variable (8080) - Skipped
// 3. Default (8080) - Skipped
```

### Testing with Configuration

**Override config in tests using WithPreset.**

```go
func TestUserService(t *testing.T) {
    testConfig := &Config{
        DBHost: "localhost",
        DBPort: 5433,
        DBName: "testdb",
    }

    testScope := pumped.NewScope(
        pumped.WithPreset(Config, testConfig),
    )
    defer testScope.Dispose()

    serviceCtrl := pumped.Controller(testScope, UserService)
    service, err := serviceCtrl.Get()
    if err != nil {
        t.Fatalf("failed to get service: %v", err)
    }

}
```

### Configuration Best Practices

**✅ DO:**
- Provide sensible defaults for local development
- Use environment variables for deployment configuration
- Use scope tags for test-specific overrides
- Keep configuration struct simple (basic types)
- Document environment variables in README

**❌ DON'T:**
- Load configuration from files (use env vars or tags)
- Use global variables for configuration
- Parse flags in Config executor (do it in main, pass via tags)
- Make Config mutable (read-only after creation)
- Ignore errors from missing required configuration

### Configuration with Reactive Dependencies

**When configuration changes trigger re-resolution:**

```go
var (
    Config = pumped.Provide(func(ctx *pumped.ResolveCtx) (*Config, error) {
        scope := ctx.Scope()

        rateLimitTag := pumped.NewTag[int]("rateLimit")
        rateLimit := 100

        if limit, ok := scope.GetTag(rateLimitTag); ok {
            rateLimit = limit
        }

        return &Config{RateLimit: rateLimit}, nil
    })

    RateLimiter = pumped.Derive1(
        Config.Reactive(),
        func(ctx *pumped.ResolveCtx, cfgCtrl *pumped.Controller[*Config]) (*RateLimiter, error) {
            cfg, err := cfgCtrl.Get()
            if err != nil {
                return nil, err
            }

            return NewRateLimiter(cfg.RateLimit), nil
        },
    )
)
```

**When Config changes, RateLimiter automatically re-resolves with new rate limit.**

## Key Behaviors

- **Auto-activation:** Skill activates when `go.mod` contains `github.com/pumped-fn/pumped-go`
- **Example-driven:** Reference `examples/` directory for complete working examples
- **Production-focused:** Emphasize lifecycle management, error handling, graceful shutdown
- **Go-idiomatic:** Follow Go conventions (error handling, interfaces, table-driven tests)
- **Testing-friendly:** Use `WithPreset()` for mocking, support both unit and integration tests

## Remember

- Package-level `var` for all executors
- Controllers for all dependencies (`.Get()` with error handling)
- `OnCleanup()` for all resources that need cleanup
- `scope.Dispose()` for proper shutdown
- Flows for traced operations, plain functions for simple transformations
- `WithPreset()` for testing
- Graceful shutdown with signal handling
- **Flat project structure** (avoid overcomplicated folders)
- **Zero comments** (self-documenting code)
- **Dual-mode configuration** (defaults + tag-based overrides)
- Examples directory has production-ready patterns
