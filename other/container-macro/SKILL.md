---
name: container-macro
description: Uses container!{} macro for compile-time DI graph validation and container construction. Use when wanting compile-time circular dependency detection, explicit registration declarations, or strict DI setup validation.
---

# container! Macro

The `container!` macro provides compile-time dependency graph validation and emits `compile_error!()` for issues like circular dependencies, scope mismatches, and missing dependencies.

## Basic usage

```rust
use injectable::prelude::*;

container! {
    // Leaf type — singleton by default
    Database,

    // With explicit scope
    Cache { scope: "transient" },

    // With dependencies (registered elsewhere)
    UserService { deps: [Database, Cache] },
}
```

## Compile-time checks

The macro validates at compile time:
- **Circular dependencies**: detected via DFS with full cycle path
- **Scope mismatches**: singleton depending on transient is rejected
- **Missing dependencies**: unregistered dependencies are caught
- **Duplicate registrations**: duplicate type names are caught

## When to use vs Container::builder()

| Approach | Use when |
|---|---|
| `Container::builder()` | Runtime construction, dynamic registration |
| `container! {}` | Compile-time validation, strict DI setup |

```rust
// Runtime approach (no compile-time validation)
let container = Container::builder()
    .register(DynProvider::sync(|| Ok(HttpClient::new())))
    .build()
    .await?;

// Compile-time approach (validates graph at compile time)
container! {
    Database,
    HttpClient,
    UserService { deps: [Database, HttpClient] },
}
```

## With scopes

```rust
container! {
    // Singleton (default)
    Database,

    // Transient — fresh instance each resolution
    RequestId { scope: "transient" },

    // Singleton depending on transient (REJECTED at compile time)
    // UserService { deps: [RequestId] }, // ERROR: singleton depends on transient
}
```

## Limitations

- The `container!` macro validates the *declared* graph, not all injectable types
- Types using `#[injectable]` derive are auto-registered via `inventory` and must still be validated
- Use `Container::builder().build()` for full validation including auto-registered types

For most cases, `Container::builder().build()` is sufficient as it also validates the full graph at startup time.
