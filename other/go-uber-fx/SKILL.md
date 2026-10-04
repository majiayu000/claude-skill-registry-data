---
name: go-uber-fx
description: "Application framework and dependency injection with uber-go/fx. Covers lifecycle hooks, modules, and modular application design."
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Wed, 06 May 2026 06:55:00 GMT
---

## Core Concepts

Uber Fx is a **framework** built on top of the `dig` DI container. It provides:
- **Dependency Injection**: Automatic wiring of your application graph.
- **Lifecycle Management**: Hooks for starting and stopping your application safely.
- **Modularity**: A way to group related logic into reusable `fx.Module` units.
- **Signal Handling**: Automatic handling of termination signals (SIGINT, SIGTERM) for graceful shutdown.

## Best Practices

1. **Keep `main()` Thin** — Your `main()` function should ideally just be an `fx.New(...).Run()` call. Push all logic into providers and modules.
2. **Use Lifecycle Hooks** — Never start long-running processes (like HTTP servers) in a constructor. Use `lc.Append(fx.Hook{ OnStart: ..., OnStop: ... })` instead.
3. **Respect Contexts** — Both `OnStart` and `OnStop` receive a `context.Context`. Respect it for timeouts and cancellation.
4. **OnStart Should Not Block** — If you need to start a long-running process, spawn a goroutine inside `OnStart` and return immediately so the rest of the application can boot.
5. **Annotate for Interfaces** — Use `fx.As` to tell Fx that a concrete type should be provided as an interface.
6. **Group Related Providers** — Use `fx.Module` to group related services (e.g., a `DatabaseModule` containing connection pooling and repositories).

## Lifecycle Hook Example

```go
func NewServer(lc fx.Lifecycle, logger *log.Logger) *http.Server {
    srv := &http.Server{Addr: ":8080"}
    
    lc.Append(fx.Hook{
        OnStart: func(ctx context.Context) error {
            logger.Println("Starting server...")
            go srv.ListenAndServe() // Non-blocking!
            return nil
        },
        OnStop: func(ctx context.Context) error {
            logger.Println("Stopping server...")
            return srv.Shutdown(ctx)
        },
    })
    
    return srv
}
```

## Modular Design Example

```go
var DBModule = fx.Module("db",
    fx.Provide(NewDBConnection, NewUserRepository),
)

func main() {
    fx.New(
        DBModule,
        fx.Provide(NewServer, NewLogger),
        fx.Invoke(func(s *http.Server) {
            // This triggers the wiring of the server
        }),
    ).Run()
}
```

## Why Uber Fx?

- **Boilerplate Reduction**: No need to manually wire dozens of services.
- **Reliable Shutdown**: Ensures all resources (DB, files, sockets) are closed in the correct order.
- **Consistency**: Enforces a standard way to structure Go applications across a team.

## Anti-patterns

- ❌ **Blocking `OnStart`** — Prevents the application from completing its boot cycle.
- ❌ **Side Effects in Constructors** — Don't open connections or start timers in `NewXXX` functions; use lifecycle hooks.
- ❌ **Global `fx.App`** — Don't pass the app itself as a dependency.
- ❌ **Missing `fx.Invoke`** — If nothing "invokes" your dependency chain, Fx won't build it.
- ❌ **Ignoring `OnStop` Errors** — If a cleanup operation fails, you should log it or handle it; don't silently ignore it.
