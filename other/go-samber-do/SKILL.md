---
name: go-samber-do
description: "Dependency injection for Go using samber/do. Covers type-safe, generics-based DI without reflection."
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Wed, 06 May 2026 07:20:00 GMT
---

## Core Philosophy

`samber/do` is a dependency injection library built on **Go Generics** (1.18+). It provides a type-safe way to manage your application's service graph without the overhead of reflection (`dig`) or the complexity of code generation (`wire`).

- **Type-safe**: Leverages generics for compile-time type checking.
- **No Reflection**: Faster startup and more predictable behavior.
- **Lifecycle Support**: Built-in support for health checks and graceful shutdown.
- **Service Types**: Lazy (default), Eager, Transient, and Value services.

## Basic Usage

### The Injector (Container)
```go
import "github.com/samber/do/v2"

injector := do.New()
```

### Providing Services
Follow "Accept Interfaces, Return Structs":
```go
// Lazy service (created only when first invoked)
do.Provide(injector, func(i do.Injector) (Database, error) {
    return &PostgreSQLDatabase{DSN: "..." }, nil
})

// Eager service (created immediately)
do.Provide(injector, do.Eager(func(i do.Injector) (*Config, error) {
    return &Config{ Port: 8080 }, nil
}))

// Value (pre-created instance)
do.ProvideValue(injector, os.Stdout)
```

### Invoking Services
```go
// With error handling
db, err := do.Invoke[Database](injector)

// Panics on error (useful for initialization)
db := do.MustInvoke[Database](injector)
```

## Service Lifecycles

### Transient Services
New instance is created every time it's invoked:
```go
do.ProvideTransient(injector, func(i do.Injector) (*Logger, error) {
    return &Logger{}, nil
})
```

### Shutdown
```go
// Close all services in the correct reverse order
err := injector.Shutdown()
```

## Why use `do`?

- **Generics First**: Designed specifically for modern Go.
- **Minimalistic**: Extremely lightweight with a small API surface.
- **Testable**: Easily swap implementations for testing by using `do.Override`.
- **Modular**: Use `do.Package` to group related service registrations together.

## Best Practices

1. **Composition Root** — Keep the injector in `main()` or your app's entry point.
2. **Implicit Aliasing** — Use `do.InvokeAs[Interface](i)` to fetch a concrete implementation as an interface.
3. **Named Services** — Use `ProvideNamed` when you have multiple instances of the same type (e.g., two different caches).
4. **Health Checks** — Implement health check methods in your services and register them with `do.HealthCheck`.
5. **Shallow Trees** — Try to keep your dependency chains simple (3-4 levels max).

## Anti-patterns

- ❌ **Container Injection** — Don't pass `do.Injector` into your business logic. Only use it in constructor functions.
- ❌ **Global State** — Avoid using a global `do.Injector`. Pass it around during initialization instead.
- ❌ **Silent Failures** — Always check errors returned by `do.Invoke` unless you are at the application startup where a panic is acceptable.
- ❌ **Using v1** — Always use `github.com/samber/do/v2` for the best performance and features.
