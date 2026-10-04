---
name: lifecycle-hooks
description: Adds post_construct and pre_destruct lifecycle hooks to injectable types. Use when initializing resources after construction (DB migrations, connection warm-up) or cleaning up before shutdown (pool close, flush buffers).
---

# Lifecycle Hooks

## Hook summary

| Hook | Runs | Common use |
|---|---|---|
| `#[injectable(post_construct)]` | After construction | Migrations, warm-up, cache load |
| `#[injectable(pre_destruct)]` | During `container.shutdown()` | Close connections, flush, drain |

## With constructor injection (same impl block)

```rust
use injectable::prelude::*;

#[injectable]
impl Database {
    #[injectable(ctor)]
    async fn new(#[injectable(inject(use_factory_async = make_pool))] pool: Pool<Sqlite>) -> Self {
        Self { pool }
    }

    #[injectable(post_construct)]
    async fn migrate(&self) -> Result<(), sqlx::Error> {
        sqlx::query("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY)")
            .execute(&self.pool).await?;
        println!("[DB] Schema ready");
        Ok(())
    }

    #[injectable(pre_destruct)]
    async fn close(&self) {
        self.pool.close().await;
        println!("[DB] Pool closed");
    }
}
```

## With field injection (separate impl block)

```rust
#[injectable]
struct Cache { db: Inject<Database> }

#[injectable]          // no #[injectable(ctor)] — lifecycle hooks only
impl Cache {
    #[injectable(post_construct)]
    async fn warm_up(&self) -> HookResult {
        println!("[Cache] Warming up");
        Ok(())
    }
}
```

## Hook return types

```rust
// Returns () — always succeeds
#[injectable(post_construct)]
fn init(&self) { println!("initialized"); }

// Returns Result — errors become LifecycleHookFailed
#[injectable(post_construct)]
async fn connect(&self) -> Result<(), std::io::Error> {
    Ok(())
}
```

## Shutdown

```rust
let container = Container::builder().build().await?;
// … use container …
container.shutdown().await?;   // calls all #[injectable(pre_destruct)] hooks in reverse order
```

Hooks run in **reverse construction order** — the most-recently-constructed type is
destroyed first.

See [guides/05-lifecycle-hooks.md](../../guides/05-lifecycle-hooks.md).
