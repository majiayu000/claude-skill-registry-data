---
name: multi-service-graph
description: Wires a multi-level service dependency graph where services depend on each other. Use when building complex service graphs with 3+ layers of dependencies or when multiple services share the same dependency.
---

# Multi-Service Dependency Graph

## Example: 4-level graph

```
AppConfig (level 0)
    ↓ make_db_pool
AuthService   (level 1) ← pool
UrlService    (level 1) ← pool, Arc<AppConfig>
AnalyticsService (level 2) ← pool, Arc<UrlService>
RedirectService  (level 3) ← Arc<UrlService>, Arc<AnalyticsService>
```

```rust
use injectable::prelude::*;

#[injectable]
pub struct AuthService {
    #[injectable(inject(use_factory_async = crate::make_db_pool))]
    pool: Pool<Sqlite>,
}

#[injectable]
pub struct UrlService {
    #[injectable(inject(use_factory_async = crate::make_db_pool))]
    pool:   Pool<Sqlite>,
    #[injectable(inject)]
    config: Arc<AppConfig>,     // depends on AppConfig
}

#[injectable]
pub struct AnalyticsService {
    #[injectable(inject(use_factory_async = crate::make_db_pool))]
    pool:    Pool<Sqlite>,
    #[injectable(inject)]
    url_svc: Arc<UrlService>,   // depends on UrlService
}

#[injectable]
pub struct RedirectService {
    #[injectable(inject)]
    url_svc:   Arc<UrlService>,       // shared reference
    #[injectable(inject)]
    analytics: Arc<AnalyticsService>, // depends on AnalyticsService
}
```

## Key points

- `Arc<T>` fields (with `#[injectable(inject)]`) share the singleton — `url_svc` in both
  `AnalyticsService` and `RedirectService` point to the **same** `Arc<UrlService>`.
- The factory `make_db_pool` is called once per service type (each service
  gets its own pool by default).
- Injectable resolves the full graph when the first type is extracted; singleton
  cache prevents redundant construction.

## Warm-up

```rust
let ctx = container.context();
// Extracting the deepest level warms up the entire chain:
ctx.extract::<Inject<RedirectService>>().await?;
// ↑ also initializes UrlService, AnalyticsService, AppConfig
```

## Verify shared singletons

```rust
let analytics: Inject<AnalyticsService> = ctx.extract().await?;
let redirect:  Inject<RedirectService>  = ctx.extract().await?;

// Both hold the same UrlService instance
assert!(Arc::ptr_eq(&analytics.url_svc, &redirect.url_svc));
```
