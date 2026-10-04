---
name: container-inspection
description: Inspects what types are registered in the container and checks for optional registrations. Use when debugging missing types, writing health checks, or verifying test setup.
---

# Container Inspection

## List registered types

```rust
use injectable::prelude::*;

let container = Container::builder().build().await?;

let types: Vec<&'static str> = container.registered_types();
println!("Registered: {types:?}");
// ["AppConfig", "Database", "UserService", "AuthService", …]

// Assert a type is registered:
assert!(types.contains(&"Database"), "Database must be registered");
```

## try_resolve — non-failing resolution

```rust
// Returns Ok(None) instead of Err(MissingDependency)
let svc: Option<UserService> = container.try_resolve().await?;
match svc {
    Some(s) => println!("UserService resolved"),
    None    => println!("UserService not registered"),
}

// For external types:
let pool: Option<sqlx::SqlitePool> = container.try_resolve_external().await?;
```

## Check at startup

```rust
#[tokio::main]
async fn main() {
    let container = Container::builder().build().await.unwrap();

    // Verify critical services are present
    let types = container.registered_types();
    for required in &["Database", "UserService", "AuthService"] {
        assert!(types.contains(required), "{required} not registered");
    }

    println!("✓ All required services registered");
}
```

## Health check endpoint

```rust
async fn health(State(state): State<AxumState>) -> axum::Json<HealthResponse> {
    axum::Json(HealthResponse {
        status: "ok",
        registered_services: state.container().registered_types(),
    })
}
```

## Debug registration issues

```rust
// If a type is missing, check:
// 1. Does it have #[injectable]?
// 2. Is the crate that defines it linked to the binary?
//    (inventory collects types at link time)
// 3. For external types: is DynProvider registered?

let result = container.try_resolve::<MissingService>().await.unwrap();
if result.is_none() {
    eprintln!("MissingService not found. Registered: {:?}", container.registered_types());
}
```
