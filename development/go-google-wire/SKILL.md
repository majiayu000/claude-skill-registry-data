---
name: go-google-wire
description: "Compile-time dependency injection with google/wire. Covers provider sets, injectors, and code generation."
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Wed, 06 May 2026 06:50:00 GMT
---

## Core Principles

Wire is a **code generator** that automates the "manual" dependency injection you would otherwise write in `main()`. It has **no runtime overhead** and **no reflection**.

### Workflow
1. Write **Providers** (functions that return a value and its dependencies).
2. Group them into **Provider Sets**.
3. Create an **Injector** file with a `//go:build wireinject` tag.
4. Run `wire` to generate `wire_gen.go`.

## Best Practices

1. **Commit `wire_gen.go`** — Treat it as a standard source file. It must be in sync with your providers for the code to compile.
2. **Use Build Tags** — Always put `//go:build wireinject` at the top of your injector files (e.g., `wire.go`) to prevent them from being included in the final binary.
3. **Explicit Interface Binding** — Use `wire.Bind` to tell Wire which concrete type satisfies an interface. Wire does not perform implicit interface satisfaction.
4. **Cleanup Functions** — Providers can return a cleanup function (e.g., `func()`) which Wire will automatically chain in the correct reverse order.
5. **Named Types for Duplicates** — If you have two dependencies of the same type (e.g., two `*sql.DB` connections), wrap them in distinct named types (e.g., `type PrimaryDB *sql.DB`).

## Code Example: Provider and Set

```go
// infra/db.go
func NewDB(cfg *Config) (*sql.DB, func(), error) {
    db, _ := sql.Open("postgres", cfg.DSN)
    cleanup := func() { db.Close() }
    return db, cleanup, nil
}

var Set = wire.NewSet(NewDB, NewConfig)
```

## Code Example: Injector (`wire.go`)

```go
//go:build wireinject

package main

import "github.com/google/wire"

func InitializeApp() (*App, func(), error) {
    wire.Build(infra.Set, service.Set, NewApp)
    return nil, nil, nil
}
```

## Running Wire

```bash
go install github.com/google/wire/cmd/wire@latest
wire ./...
```

## Why Wire?

- **Type Safety**: The compiler catches missing or circular dependencies.
- **Performance**: Zero runtime overhead.
- **Testability**: No global state or magic containers; just plain Go functions.
- **Maintainability**: The generated `wire_gen.go` shows exactly how your application is wired.

## Anti-patterns

- ❌ **Editing `wire_gen.go`** — Your changes will be overwritten. Edit the providers or the injector instead.
- ❌ **Missing Build Tag** — Forgetting `//go:build wireinject` causes "duplicate function" errors during `go build`.
- ❌ **Fat Injectors** — Putting dozens of providers directly in `wire.Build`. Use `wire.NewSet` to group them by package/layer.
- ❌ **Implicit Interfaces** — Hoping Wire will guess which struct implements an interface. Use `wire.Bind`.
- ❌ **Circular Dependencies** — Wire will error out, but this usually indicates a deeper design flaw that needs refactoring.
