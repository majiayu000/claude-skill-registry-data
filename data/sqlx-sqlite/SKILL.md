---
name: sqlx-sqlite
description: Injects an sqlx::SqlitePool into services using injectable. Use when setting up a SQLite database connection pool, running migrations in post_construct, or sharing a pool across multiple services.
---

# SQLite with sqlx

Use `#[injectable(inject(use_factory_async = self::make_db_pool))]` when a
service needs a `sqlx` pool created asynchronously from injectable config.

## Pool factory

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
```

Purpose:

- Open the database pool with async I/O before the service is used.
- Keep connection details in one place instead of duplicating setup logic across
  services.
- Let the service keep a plain `Pool<Sqlite>` field while DI handles creation.

## Service with pool + migration

```rust
#[injectable]
struct Database {
    #[injectable(inject(use_factory_async = self::make_db_pool))]
    pool: Pool<Sqlite>,
}

#[injectable]
impl Database {
    #[injectable(post_construct)]
    async fn migrate(&self) -> Result<(), sqlx::Error> {
        sqlx::query(
            "CREATE TABLE IF NOT EXISTS users (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                email      TEXT    NOT NULL UNIQUE,
                created_at TEXT    NOT NULL DEFAULT (datetime('now'))
            )",
        )
        .execute(&self.pool)
        .await?;
        Ok(())
    }

    #[injectable(pre_destruct)]
    async fn close(&self) {
        self.pool.close().await;
    }
}
```

Implementation steps:

1. Add a `#[injectable(factory)] async fn make_db_pool(...)`.
2. Read `Inject<AppConfig>` or other injectable dependencies in the factory.
3. Annotate the field or constructor parameter with
   `#[injectable(inject(use_factory_async = self::make_db_pool))]`.
4. Use `#[injectable(post_construct)]` for migrations or warm-up queries.
5. Use `#[injectable(pre_destruct)]` to close the pool cleanly on shutdown.

## Sharing pool across services

```rust
// If multiple services each use use_factory_async directly, each service gets
// its own Pool instance. For sqlite::memory:, that means separate in-memory
// databases. Use a single-connection pool if you intentionally keep one pool
// per service.
#[injectable(factory)]
async fn make_shared_pool(cfg: Inject<AppConfig>) -> Result<Pool<Sqlite>, sqlx::Error> {
    sqlx::sqlite::SqlitePoolOptions::new()
        .max_connections(1)          // required for sqlite::memory:
        .idle_timeout(None)
        .max_lifetime(None)
        .connect(&cfg.database_url)
        .await
}
```

`#[injectable(inject(use_factory_async = make_db_pool))]` is not a cross-service
singleton by itself. The factory runs once per construction of the owning
service type. Since services are singleton by default, that usually means one
pool per service, not one pool for the entire application.

## One pool shared by many services

Wrap the external pool in your own singleton `#[injectable]` type, then inject
that wrapper everywhere else:

```rust
use injectable::prelude::*;
use sqlx::{Pool, Sqlite};

#[injectable(factory)]
async fn make_db_pool(cfg: Inject<AppConfig>) -> Result<Pool<Sqlite>, sqlx::Error> {
    println!("  [DB] Connecting to {}", cfg.database_url);
    sqlx::sqlite::SqlitePoolOptions::new()
        .max_connections(1)
        .idle_timeout(None)
        .max_lifetime(None)
        .connect(&cfg.database_url)
        .await
}

#[injectable]
pub struct DbPool {
    #[injectable(inject(use_factory_async = make_db_pool))]
    pub pool: Pool<Sqlite>,
}

#[injectable]
pub struct AuthService {
    db: Inject<DbPool>,
}

#[injectable]
pub struct UserService {
    db: Inject<DbPool>,
}
```

Why this works:

- `DbPool` is singleton by default.
- Its `pool` field is built once when `DbPool` is first constructed.
- `AuthService` and `UserService` both resolve the same `Arc<DbPool>`.
- `make_db_pool` therefore runs exactly once for the shared wrapper.

## `Inject<DbPool>` vs `Arc<DbPool>`

If you prefer `Arc<DbPool>` instead of `Inject<DbPool>`, that works too:

```rust
#[injectable]
pub struct AuthService {
    #[injectable(inject)]
    db: Arc<DbPool>,
}

#[injectable]
pub struct UserService {
    #[injectable(inject)]
    db: Arc<DbPool>,
}
```

These two forms use the same singleton cache path:

- `Inject<DbPool>` auto-injects and is the most idiomatic injectable field type.
- `Arc<DbPool>` requires `#[injectable(inject)]`.
- Both point to the same shared singleton instance of `DbPool`.

Choose `Inject<DbPool>` when you want the standard injectable wrapper API.
Choose `Arc<DbPool>` when the service should store a plain `Arc` field.

## Config

```rust
#[injectable]
impl AppConfig {
    #[injectable(ctor)]
    fn new() -> Self {
        Self {
            database_url: std::env::var("DATABASE_URL")
                .unwrap_or_else(|_| "sqlite::memory:".into()),
        }
    }
}
```

## Querying

```rust
pub async fn find_user(&self, id: i64) -> Result<User, sqlx::Error> {
    sqlx::query_as::<_, User>("SELECT id, email FROM users WHERE id = ?")
        .bind(id)
        .fetch_one(&self.pool)
        .await
}
```

Related async-init macros to audit alongside this pattern:

- `#[injectable(factory)]` for async pool creation
- `#[injectable(inject(use_factory_async = ...))]` for injection
- `#[injectable(post_construct)]` for migrations and warm-up
