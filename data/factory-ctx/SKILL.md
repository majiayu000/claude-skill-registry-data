---
name: factory-ctx
description: Uses FactoryCtx inside DynProvider::with_ctx closures for scope-safe resolution. Use when a DynProvider factory needs to resolve other injectable or external types without bypassing the singleton cache.
---

# FactoryCtx

`FactoryCtx` is the context passed to `DynProvider::with_ctx` closures.
It exposes only scope-safe operations.

## Methods

```rust
// extract::<T>() — full Extract machinery, respects singleton/transient scope
let cfg:  Inject<AppConfig>   = ctx.extract().await?;
let db:   Arc<Database>       = ctx.extract().await?;
let opt:  Option<Inject<Cache>> = ctx.extract().await?;

// resolve_external::<T>() — for DynProvider-registered types only
let pool: sqlx::SqlitePool    = ctx.resolve_external().await?;
```

## Example

```rust
use injectable::prelude::*;

let container = Container::builder()
    .register(DynProvider::with_ctx(|ctx| async move {
        // Resolve AppConfig (singleton) via FactoryCtx
        let cfg: Inject<AppConfig> = ctx.extract().await?;

        // Build a pool using the config
        let pool = sqlx::SqlitePool::connect(&cfg.db_url).await
            .map_err(|e| InjectableError::ConstructionFailed {
                type_name: "SqlitePool",
                reason: e.to_string(),
            })?;

        Ok(pool)
    }))
    .build().await?;
```

## Why not use ctx.resolve() directly?

`ResolveContext::resolve()` is `pub(crate)` — it bypasses the singleton cache
and creates a fresh instance every call. `FactoryCtx::extract()` goes through
the proper `Extract` machinery:

- `Inject<T>` → finds `InjectableArcFactory` → uses singleton cache ✓
- `Arc<T: Injectable>` → `Extract for Arc<T>` → singleton cache ✓
- Transient types → fresh instance per call ✓

## With scope-awareness

```rust
DynProvider::with_ctx(|ctx| async move {
    // Two extractions of a singleton return the same Arc:
    let a: Inject<AppConfig> = ctx.extract().await?;
    let b: Inject<AppConfig> = ctx.extract().await?;
    assert!(Arc::ptr_eq(&a.0, &b.0));   // same instance

    // Two extractions of a transient return different instances:
    let x: Inject<RequestLogger> = ctx.extract().await?;
    let y: Inject<RequestLogger> = ctx.extract().await?;
    assert!(!Arc::ptr_eq(&x.0, &y.0));  // different instances

    Ok(MyExternalService::new(a, x))
})
```
