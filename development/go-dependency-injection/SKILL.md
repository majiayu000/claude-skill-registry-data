---
name: go-dependency-injection
description: "Dependency injection (DI) patterns in Golang. Covers manual constructor injection and common DI libraries like wire, dig, fx, and do."
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Wed, 06 May 2026 06:00:00 GMT
---

## Core Principles

1. **Explicit Injection** — Dependencies MUST be passed to a component (via constructor or fields), never pulled from global state or created internally.
2. **Accept Interfaces, Return Structs** — Services should depend on interfaces to allow for mocking and loose coupling.
3. **Composition Root** — All wiring should happen in a single place, typically in `main()` or an `App` constructor.
4. **No Service Locator** — Do not pass the DI container into your services. Services should only know about their direct dependencies.
5. **Simple First** — Use manual constructor injection for small projects. Only reach for a DI library when the dependency graph becomes unmanageable (typically 15+ services).

## Manual Dependency Injection

This is the idiomatic Go way for most small-to-medium projects.

```go
type Service struct {
    repo Repository
}

func NewService(repo Repository) *Service {
    return &Service{repo: repo}
}

func main() {
    db := NewDB()
    repo := NewRepository(db)
    svc := NewService(repo)
    // ...
}
```

## DI Library Comparison

| Library | Type | Features |
| --- | --- | --- |
| **Manual** | N/A | Simple, explicit, no magic. Best for < 15 services. |
| **google/wire** | Compile-time | Code generation, type-safe, no runtime overhead. |
| **uber-go/fx** | Runtime | Reflection-based, built-in lifecycle management (start/stop). |
| **samber/do** | Runtime | Generics-based, no code generation, easy to use, supports lazy loading. |

## Why use DI?

- **Testability**: Easily swap real implementations for mocks in unit tests.
- **Loose Coupling**: Components don't need to know how their dependencies are created.
- **Lifecycle Management**: Centralized control over service startup and shutdown order.
- **Maintainability**: Clear visibility into what a service needs to function.

## Anti-patterns

- ❌ **Global Variables** — Using `var DB *sql.DB` at the package level.
- ❌ **`init()` for Service Setup** — Hard to test and can't return errors.
- ❌ **Container Passing** — Passing an `fx.App` or `do.Injector` into a service's methods.
- ❌ **Hardcoded Dependencies** — `NewService` calling `sql.Open` internally.
- ❌ **Premature Abstraction** — Creating interfaces before you have a second implementation or a test requirement.
