---
name: large-app-organization
description: Organizes a large application using injectable across multiple modules and crates. Use when the codebase grows beyond a single file, when splitting services into modules, or when structuring a workspace.
---

# Large App Organization

## Module structure

```
src/
├── main.rs
├── config.rs          (#[injectable] AppConfig)
├── db/
│   ├── mod.rs
│   ├── pool.rs        (make_db_pool #[injectable(factory)])
│   └── migrations.rs
├── services/
│   ├── auth.rs        (#[injectable] AuthService)
│   ├── users.rs       (#[injectable] UserService)
│   └── orders.rs      (#[injectable] OrderService)
└── api/
    ├── mod.rs
    └── handlers.rs    (Axum handlers)
```

## Services depend on each other

```rust
// services/auth.rs
#[injectable]
pub struct AuthService {
    #[injectable(inject(use_factory_async = crate::db::pool::make_db_pool))]
    pool: Pool<Sqlite>,
}

// services/users.rs
#[injectable]
pub struct UserService {
    #[injectable(inject(use_factory_async = crate::db::pool::make_db_pool))]
    pool: Pool<Sqlite>,
    #[injectable(inject)]
    auth: Arc<AuthService>,         // depends on AuthService
}

// services/orders.rs
#[injectable]
pub struct OrderService {
    #[injectable(inject)]
    users: Arc<UserService>,        // depends on UserService
    #[injectable(inject)]
    auth:  Arc<AuthService>,
}
```

## main.rs assembly

```rust
mod config; mod db; mod services; mod api;

#[tokio::main]
async fn main() {
    let container = Container::builder()
        .build().await.expect("DI container failed");

    // Warm up all singletons eagerly
    let ctx = container.context();
    ctx.extract::<Inject<services::auth::AuthService>>().await.expect("AuthService");
    ctx.extract::<Inject<services::users::UserService>>().await.expect("UserService");
    ctx.extract::<Inject<services::orders::OrderService>>().await.expect("OrderService");

    let state = AxumState::new(container);
    let app = api::router(state);
    axum::serve(listener, app).await.unwrap();
}
```

## Multi-crate workspace

```toml
# Cargo.toml (workspace)
[workspace]
members = ["app", "domain", "infra"]
```

Types in `domain` crate implement `#[injectable]`, types in `infra` crate
register external types via `DynProvider`. The `app` crate builds the container
and wires everything together.

See [guides/15-large-app-organization.md](../../guides/15-large-app-organization.md).
