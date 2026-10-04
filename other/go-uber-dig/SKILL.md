---
name: go-uber-dig
description: "Dependency injection for Go using uber-go/dig. Covers reflection-based wiring, parameter/result objects, and named dependencies."
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Wed, 06 May 2026 07:00:00 GMT
---

## Core Concepts

Uber Dig is a **reflection-based** dependency injection toolkit. Unlike `wire`, it resolves dependencies at **runtime**. It is the underlying engine for the `uber-go/fx` framework.

### Key Primitives
- **`Provide`**: Registers a constructor function in the container.
- **`Invoke`**: Runs a function, automatically providing its arguments from the container.
- **`dig.In`**: A struct embed used to define multiple input dependencies.
- **`dig.Out`**: A struct embed used to return multiple dependencies from a single provider.

## Best Practices

1. **Composition Root** — Keep the container (`dig.New()`) in your `main()` or application entry point. Never pass the container into your services (Service Locator anti-pattern).
2. **Lazy and Memoized** — Providers in Dig are lazy (only called if needed) and memoized (called only once per container).
3. **Use Structs for Many Deps** — When a constructor has more than 3 dependencies, use a struct that embeds `dig.In`. This makes the code more maintainable and avoids long parameter lists.
4. **Named Dependencies** — Use the `name` tag to disambiguate multiple instances of the same type (e.g., a primary and a replica database).
5. **Value Groups** — Use the `group` tag to collect multiple implementations of an interface into a single slice (e.g., collecting all `http.Handler`s for a router).

## Parameter Object Example (`dig.In`)

```go
type ServerParams struct {
    dig.In
    
    Logger *log.Logger
    Config *Config
    DB     *sql.DB `name:"primary"`
    Auth   AuthService `optional:"true"`
}

func NewServer(p ServerParams) *http.Server {
    // ...
}
```

## Result Object Example (`dig.Out`)

```go
type DBResult struct {
    dig.Out
    
    Primary *sql.DB `name:"primary"`
    Replica *sql.DB `name:"replica"`
}

func NewDatabases(cfg *Config) (DBResult, error) {
    // ...
}
```

## Basic Setup

```go
func main() {
    c := dig.New()
    
    c.Provide(NewConfig)
    c.Provide(NewLogger)
    c.Provide(NewDatabases)
    c.Provide(NewServer)
    
    if err := c.Invoke(func(srv *http.Server) {
        srv.ListenAndServe()
    }); err != nil {
        log.Fatal(err)
    }
}
```

## Why Dig?

- **Simplicity**: No code generation required.
- **Flexibility**: Great for dynamic graphs and plugin-based architectures.
- **Integration**: Works seamlessly with `uber-go/fx` for full application lifecycle management.

## Anti-patterns

- ❌ **Container Injection** — Passing `*dig.Container` to a service.
- ❌ **Silent Failures** — Ignoring errors returned by `c.Provide`.
- ❌ **Duplicate Types without Names** — Providing two `*sql.DB` objects without using `name` tags.
- ❌ **Overuse of `optional:"true"`** — Can lead to `nil` pointer panics if not handled carefully.
- ❌ **Circular Dependencies** — Dig will error at runtime; indicates a need for refactoring.
