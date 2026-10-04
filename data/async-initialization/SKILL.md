---
name: async-initialization
description: Initializes services that require async work at startup — connecting to databases, loading config from remote, seeding caches. Use when #[injectable(ctor)] or #[injectable(post_construct)] need to .await async operations.
---

# Async Initialization

## Which async macro to use?

| Pattern | Best for | Example macro |
|---|---|---|
| Async constructor | The service itself owns the async setup | `#[injectable(ctor)] async fn new(...)` |
| Async external factory | A third-party type such as `sqlx::SqlitePool` must be created first | `#[injectable(inject(use_factory_async = self::make_db_pool))]` |
| Post-construction warm-up | The service exists, then needs migrations, cache loads, or probes | `#[injectable(post_construct)]` |

For async database pools, prefer a dedicated `#[injectable(factory)]` helper plus
`use_factory_async` instead of putting connection logic directly inside an
unrelated service constructor.

## Async constructor

```rust
use injectable::prelude::*;

#[derive(Clone)]
struct DbPool { inner: sqlx::SqlitePool }

#[injectable]
impl DbPool {
    #[injectable(ctor)]
    pub async fn new(cfg: Inject<AppConfig>) -> Result<Self, sqlx::Error> {
        let pool = sqlx::SqlitePool::connect(&cfg.db_url).await?;
        Ok(Self { inner: pool })
    }
}
```

## Async post_construct

```rust
#[injectable]
impl CacheService {
    #[injectable(ctor)]
    fn new(#[injectable(inject)] db: Arc<Database>) -> Self {
        Self { db, cache: DashMap::new() }
    }

    #[injectable(post_construct)]
    async fn warm_up(&self) -> HookResult {
        let items = self.db.load_hot_items().await
            .map_err(|e| Box::new(e) as Box<dyn std::error::Error + Send + Sync>)?;
        for item in items {
            self.cache.insert(item.id, item);
        }
        println!("[Cache] Loaded {} items", self.cache.len());
        Ok(())
    }
}
```

## Zero-arg async constructor

```rust
struct Clock { started: std::time::Instant }

#[injectable]
impl Clock {
    #[injectable(ctor)]
    pub async fn new() -> Self {
        // Simulate async init (e.g., NTP sync)
        tokio::time::sleep(std::time::Duration::from_millis(10)).await;
        Self { started: std::time::Instant::now() }
    }

    pub fn elapsed(&self) -> std::time::Duration {
        self.started.elapsed()
    }
}
```

## Eager warm-up ensures async init completes before serving

```rust
let container = Container::builder().build().await?;
let ctx = container.context();

// These calls trigger async constructors + post_construct hooks
ctx.extract::<Inject<DbPool>>().await?;
ctx.extract::<Inject<CacheService>>().await?;

println!("All services initialized — ready to serve");
// Start Axum server here…
```
