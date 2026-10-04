---
name: scoping
description: Controls injectable type scopes (Singleton, Transient, RequestScoped). Use when a type should be recreated per resolution, shared across the whole app, or isolated per HTTP request.
---

# Scoping

## Scope types

| Scope | Behaviour | Use when |
|---|---|---|
| `Singleton` | One instance per container (default) | Shared state, DB pools, caches |
| `Transient` | Fresh instance every resolution | Loggers with request IDs, counters |
| `RequestScoped` | One instance per HTTP request | Per-request transactions |

## Setting scope

```rust
use injectable::prelude::*;

#[injectable]                           // Singleton (default)
struct SharedCache { db: Inject<Database> }

#[injectable(scope = Transient)]        // Fresh each time
struct RequestLogger { request_id: u32 }

#[injectable(scope = RequestScoped)]    // One per HTTP request
struct Transaction { pool: Pool<Sqlite> }
```

## Constructor injection with scope

```rust
#[injectable(scope = Transient)]
impl RequestLogger {
    #[injectable(ctor)]
    fn new() -> Self {
        Self { request_id: rand::random() }
    }
}
```

## Verifying singleton semantics

```rust
let ctx = container.context();
let a: Arc<SharedCache> = ctx.extract().await?;
let b: Arc<SharedCache> = ctx.extract().await?;
assert!(Arc::ptr_eq(&a, &b));   // same instance

// OR use ptr_eq helper:
let a: Inject<SharedCache> = ctx.extract().await?;
let b: Inject<SharedCache> = ctx.extract().await?;
assert!(a.ptr_eq(&b));
```

## Transient via Arc<T> field

```rust
// Arc<T> field of a singleton always returns the same Arc (T's own scope is respected).
#[injectable]
struct Service {
    #[injectable(inject)]
    cache: Arc<SharedCache>,    // Arc points to the SAME singleton
}
```

## RequestScoped with Axum

```rust
// RequestScoped types get a fresh instance per HTTP request.
// The Axum FromRequestParts impl creates a per-request ResolveContext automatically.
async fn handler(
    Inject(tx): Inject<Transaction>,   // fresh Transaction for this request
) -> impl IntoResponse { /* … */ }
```

See [guides/06-inject-wrapper.md](../../guides/06-inject-wrapper.md).
