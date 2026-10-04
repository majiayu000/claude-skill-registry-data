---
name: external-types
description: Injects external/third-party types (sqlx::SqlitePool, reqwest::Client, redis::Client) that cannot be annotated with #[injectable]. Use when wiring types from dependencies you don't control.
---

# External Types

Three approaches — see [3-ways-to-inject-external-types.md](../../guides/3-ways-to-inject-external-types.md).

## Way 1 — `#[injectable(factory)]` + `use_factory_async`

Best when the external type is only used by one service and needs async setup,
such as opening a `sqlx::SqlitePool`.

```rust
use injectable::prelude::*;
use sqlx::{Pool, Sqlite};

#[injectable(factory)]
async fn make_db_pool(cfg: Inject<AppConfig>) -> Result<Pool<Sqlite>, sqlx::Error> {
    sqlx::sqlite::SqlitePoolOptions::new()
        .max_connections(5)
        .connect(&cfg.database_url)
        .await
}

#[injectable]
struct Database {
    #[injectable(inject(use_factory_async = self::make_db_pool))]
    pool: Pool<Sqlite>,
}
```

What this macro pair does:

- `#[injectable(factory)]` lets the factory depend on injectable inputs like
  `Inject<AppConfig>`.
- `#[injectable(inject(use_factory_async = self::make_db_pool))]` tells the
  generated provider to await that factory for the field.
- The service receives a concrete pool value, not `Inject<Pool<Sqlite>>`.

Implementation steps:

1. Define `make_db_pool` next to the service.
2. Put async connection logic in the factory.
3. Annotate the field or constructor parameter with `use_factory_async`.
4. Add `#[injectable(post_construct)]` if the service should run migrations.

## Way 2 — `use_factory_sync` (no await needed)

```rust
fn make_client(_ctx: &ResolveContext) -> reqwest::Client {
    reqwest::Client::builder().timeout(std::time::Duration::from_secs(10)).build().unwrap()
}

#[injectable]
struct ApiService {
    #[injectable(inject(use_factory_sync = self::make_client))]
    client: reqwest::Client,
}
```

## Way 3 — `DynProvider` (shared across many services)

Best when multiple services need the same external type instance.

```rust
let container = Container::builder()
    // Async, no deps
    .register(DynProvider::new(|| async {
        Ok(sqlx::SqlitePool::connect("sqlite:./app.db").await?)
    }))
    // Sync, no deps
    .register(DynProvider::sync(|| {
        Ok(reqwest::Client::new())
    }))
    // Async, reads another resolved type
    .register(DynProvider::with_ctx(|ctx| async move {
        let cfg: Inject<AppConfig> = ctx.extract().await?;
        Ok(sqlx::SqlitePool::connect(&cfg.db_url).await?)
    }))
    .build().await?;

// Consume at the container boundary:
let pool: sqlx::SqlitePool = container.resolve_external().await?;
```

Important: external types registered only through `DynProvider` are not
`Injectable`, so `#[injectable(inject)] pool: Arc<sqlx::SqlitePool>` is not the
recommended pattern. If you want a service field or constructor parameter to
receive the pool directly, wrap the pool in your own `#[injectable]` type or
use `#[injectable(inject(use_factory_async = self::make_db_pool))]`.

## Pre-built instances (testing)

```rust
let mock_pool = sqlx::SqlitePool::connect("sqlite::memory:").await?;
let container = Container::builder()
    .register(DynProvider::from_value(mock_pool))
    .build().await?;
```

See [guides/04-external-types.md](../../guides/04-external-types.md),
[guides/03-constructor-injection.md](../../guides/03-constructor-injection.md),
and [skills/sqlx-sqlite](../sqlx-sqlite/SKILL.md).
