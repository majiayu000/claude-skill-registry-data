---
name: dependency-graph
description: Validates the dependency graph at container build time to catch circular dependencies, missing registrations, and scope mismatches. Use when debugging GraphValidationFailed errors or validating a complex service graph.
---

# Dependency Graph

The graph is validated automatically at `Container::builder().build()`.

## Error types

```rust
match container_result {
    Err(InjectableError::GraphValidationFailed { errors }) => {
        for e in &errors {
            eprintln!("Graph error: {e}");
        }
    }
    Err(e) => eprintln!("Build error: {e}"),
    Ok(c) => { /* use container */ }
}
```

## Common errors and fixes

**Circular dependency**
```
`UserService` → `OrderService` → `UserService` (cycle)
```
Fix: introduce an interface layer or refactor the dependency.

**Missing registration**
```
`UserService` depends on `EmailClient`, which is not registered
```
Fix: add `#[injectable]` to `EmailClient` or register via `DynProvider`.

**Scope mismatch**
```
Singleton `UserService` cannot depend on Transient `RequestContext`
```
Fix: make `RequestContext` singleton, or make `UserService` transient.

## Inspect registered types

```rust
let container = Container::builder().build().await?;
let types = container.registered_types();
println!("Registered: {:?}", types);
// ["Database", "UserService", "OrderService", …]
```

## Use container! macro for compile-time validation

```rust
use injectable::container;

container! {
    Database,
    Cache { scope: "transient" },
    UserService { deps: [Database, Cache] },
}
// Compile error if circular deps, scope mismatches, or missing deps.
```

## Check specific type is registered

```rust
assert!(container.registered_types().contains(&"Database"));

// Non-failing check:
let result: Option<Database> = container.try_resolve().await?;
if result.is_none() {
    println!("Database not registered");
}
```

See [guides/12-dependency-graph.md](../../guides/12-dependency-graph.md).
