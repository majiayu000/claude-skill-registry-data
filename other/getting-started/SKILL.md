---
name: getting-started
description: Sets up injectable in a new Rust project from scratch. Use when adding injectable to a project for the first time, creating a first injectable type, or building a minimal working example.
---

# Getting Started with injectable

Targets `injectable` `0.2.x` on Rust `1.86+`.

## 1. Add dependency

```toml
[dependencies]
injectable  = { version = "0.2", features = ["axum"] }  # omit axum if not needed
tokio       = { version = "1",   features = ["full"] }
async-trait = "0.1"
```

## 2. Minimal example (3-step pattern)

```rust
use injectable::prelude::*;

// Step 1: Annotate types
#[injectable]
#[derive(Default, Clone)]
struct Database;

#[injectable]
struct UserService {
    db: Inject<Database>,   // Inject<T> fields are auto-wired
}

// Step 2: Build container
#[tokio::main]
async fn main() {
    let container = Container::builder()
        .build()
        .await
        .expect("container should build");

    // Step 3: Resolve
    let svc = container.resolve::<UserService>().await.unwrap();
    println!("UserService resolved!");
}
```

## 3. Add a service with dependencies

```rust
#[injectable]
struct OrderService {
    db:    Inject<Database>,
    users: Inject<UserService>,
}
// No registration needed — injectable finds it automatically.
```

## 4. Add an external type (e.g., DB pool)

```rust
#[injectable(factory)]
async fn make_pool(cfg: Inject<AppConfig>) -> Result<Pool<Sqlite>, sqlx::Error> {
    sqlx::SqlitePool::connect(&cfg.db_url).await
}

#[injectable]
struct Repository {
    #[injectable(inject(use_factory_async = self::make_pool))]
    pool: Pool<Sqlite>,
}
```

## 5. Common next steps

- Add lifecycle hooks → see `lifecycle-hooks` skill
- Add Axum integration → see `axum-integration` skill
- Inject database pool → see `sqlx-sqlite` skill
- Read env vars at startup → see `config-injection` skill
- Debug errors → see `troubleshooting` skill

See [guides/01-getting-started.md](../../guides/01-getting-started.md),
[guides/README.md](../../guides/README.md), and [README.md](../../README.md).
