---
name: post-construct-migrations
description: Runs database migrations automatically in a #[injectable(post_construct)] hook when a service is first resolved. Use when a service owns its schema and should self-migrate on startup.
---

# Database Migrations in post_construct

## Pattern

```rust
use injectable::prelude::*;
use sqlx::{Pool, Sqlite};

#[injectable(factory)]
async fn make_pool(cfg: Inject<AppConfig>) -> Result<Pool<Sqlite>, sqlx::Error> {
    sqlx::sqlite::SqlitePoolOptions::new()
        .max_connections(1)
        .idle_timeout(None)
        .max_lifetime(None)
        .connect(&cfg.database_url).await
}

#[injectable]
pub struct UserRepository {
    #[injectable(inject(use_factory_async = self::make_pool))]
    pool: Pool<Sqlite>,
}

#[injectable]
impl UserRepository {
    #[injectable(post_construct)]
    async fn migrate(&self) -> Result<(), sqlx::Error> {
        sqlx::query(
            "CREATE TABLE IF NOT EXISTS users (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                email      TEXT    NOT NULL UNIQUE,
                name       TEXT    NOT NULL,
                created_at TEXT    NOT NULL DEFAULT (datetime('now'))
            )",
        )
        .execute(&self.pool)
        .await?;
        println!("[UserRepository] Schema ready");
        Ok(())
    }

    #[injectable(pre_destruct)]
    async fn shutdown(&self) {
        self.pool.close().await;
    }
}
```

## Multiple services migrate their own tables

```rust
#[injectable]
impl OrderRepository {
    #[injectable(post_construct)]
    async fn migrate(&self) -> Result<(), sqlx::Error> {
        sqlx::query("CREATE TABLE IF NOT EXISTS orders ( … )").execute(&self.pool).await?;
        Ok(())
    }
}
```

## Triggering migrations

Migrations run automatically when the service is first resolved. To run eagerly
at startup:

```rust
let container = Container::builder().build().await?;
let ctx = container.context();

// Warm up all repos — triggers their migrations
ctx.extract::<Inject<UserRepository>>().await?;
ctx.extract::<Inject<OrderRepository>>().await?;

println!("All schemas ready");
```

## Using sqlx migrate! macro (alternative)

```rust
#[injectable(post_construct)]
async fn migrate(&self) -> Result<(), sqlx::migrate::MigrateError> {
    sqlx::migrate!("./migrations").run(&self.pool).await
}
```

Requires migration files in `./migrations/*.sql`.
