---
name: prelude
description: Uses injectable::prelude::* for ergonomic imports. Use when starting a new file that uses injectable, or when figuring out what to import.
---

# injectable::prelude

Single import that brings in everything commonly needed:

```rust
use injectable::prelude::*;

// Now available:
// Macros:   #[injectable], #[injectable(ctor)], #[injectable(factory)],
//           #[injectable(post_construct)], #[injectable(pre_destruct)], bind!, container!
// Types:    Injectable, Inject, Extract, Container, DynProvider, FactoryCtx
//           InjectableError, InjectableResult, HookResult, ResolveContext
// Scopes:   Singleton, Transient, RequestScoped
// Std:      Arc (re-exported)
```

## Full example with only prelude

```rust
use injectable::prelude::*;

#[injectable]
#[derive(Default, Clone)]
struct Database;

#[injectable]
struct UserService {
    db: Inject<Database>,
}

#[tokio::main]
async fn main() {
    let container = Container::builder().build().await.unwrap();
    let ctx = container.context();
    let svc: Inject<UserService> = ctx.extract().await.unwrap();
}
```

## When to add extra imports

```rust
// Axum integration:
use injectable::axum::{AxumState, InjectableState, InjectableRejection};

// Manual Injectable impl (rare):
use injectable_rs_runtime::{Injectable, Provider};

// async_trait (for manual Provider impls):
use async_trait::async_trait;
```

## Cargo.toml

```toml
[dependencies]
injectable  = { version = "0.2", features = ["axum"] }
tokio       = { version = "1",   features = ["full"] }
async-trait = "0.1"
```

For repository-level context and guide navigation, see
[skills/README.md](../README.md) and [guides/README.md](../../guides/README.md).
