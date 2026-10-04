---
name: dyn-provider
description: Registers external types with DynProvider (sync, async, with-context, from-value). Every registration requires a token string. Use "" for unnamed/default providers. Use distinct tokens for multiple providers of the same type (e.g., "primary"/"replica" pools).
---

# DynProvider

## Four constructors + token

Every `.register(token, DynProvider::…)` call requires a token.
Use `""` (or `DEFAULT_TOKEN`) for the single, unnamed provider of a type.

```rust
use injectable::prelude::*;

Container::builder()

    // 1. Sync, no deps — default token
    .register("", DynProvider::sync(|| {
        Ok(reqwest::Client::new())
    }))

    // 2. Async, no deps — default token
    .register("", DynProvider::new(|| async {
        Ok(sqlx::SqlitePool::connect("sqlite:./app.db").await?)
    }))

    // 3. Async, reads other resolved types via FactoryCtx — default token
    .register("", DynProvider::with_ctx(|ctx| async move {
        let cfg: Inject<AppConfig> = ctx.extract().await?;
        Ok(sqlx::SqlitePool::connect(&cfg.db_url).await?)
    }))

    // 4. Pre-built value (useful in tests) — default token
    .register("", DynProvider::from_value(MockDatabase::default()))

    .build().await?;
```

## Multiple providers of the same type

```rust
Container::builder()
    .register("primary",   DynProvider::new(|| async { Ok(primary_pool().await?) }))
    .register("replica",   DynProvider::new(|| async { Ok(replica_pool().await?) }))
    .register("analytics", DynProvider::new(|| async { Ok(analytics_pool().await?) }))
    .build().await?;

// Resolve by token
let primary:   Pool = container.resolve_external_with_token("primary").await?;
let replica:   Pool = container.resolve_external_with_token("replica").await?;
let analytics: Pool = container.resolve_external_with_token("analytics").await?;
```

## FactoryCtx (scope-safe context in with_ctx)

```rust
DynProvider::with_ctx(|ctx| async move {
    let cfg: Inject<AppConfig> = ctx.extract().await?;
    let db:  Arc<Database>     = ctx.extract().await?;

    // Resolve named pool registered elsewhere
    let primary: Pool = ctx.resolve_external_with_token("primary").await?;

    Ok(MyService::new(cfg, db, primary))
})
```

## Resolving registered types

```rust
container.resolve_external::<T>().await?                     // default token ("")
container.resolve_external_with_token::<T>("token").await?   // named token
```

## Consuming via constructor / field

```rust
#[injectable(factory)]
async fn make_db_pool(cfg: Inject<AppConfig>) -> Result<sqlx::SqlitePool, sqlx::Error> {
    sqlx::SqlitePool::connect(&cfg.db_url).await
}

#[injectable]
impl UserService {
    #[injectable(ctor)]
    async fn new(
        #[injectable(inject(use_factory_async = self::make_db_pool))] pool: sqlx::SqlitePool,
    ) -> Self { Self { pool } }
}
```

See [guides/04-external-types.md](../../guides/04-external-types.md) and
[guides/11-token-based-providers.md](../../guides/11-token-based-providers.md).
