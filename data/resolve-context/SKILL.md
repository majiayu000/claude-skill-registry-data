---
name: resolve-context
description: Uses ResolveContext to extract services inside factory closures or custom extractors. Use when needing to resolve types inside DynProvider::with_ctx or Axum FromRequestParts implementations.
---

# ResolveContext

`ResolveContext` is the framework's resolution engine. Direct user access is
restricted to scope-safe operations.

## Safe API

```rust
// ctx.extract::<T>() — scope-safe, goes through Extract machinery
let cfg: Inject<AppConfig>    = ctx.extract().await?;
let db:  Arc<Database>        = ctx.extract().await?;
let opt: Option<Inject<Cache>> = ctx.extract().await?;

// ctx.resolve_external::<T>() — for DynProvider-registered types
let pool: sqlx::SqlitePool = ctx.resolve_external().await?;
```

## In DynProvider::with_ctx (use FactoryCtx)

```rust
DynProvider::with_ctx(|ctx| async move {
    // ctx is FactoryCtx — exposes extract() and resolve_external()
    let cfg: Inject<AppConfig>    = ctx.extract().await?;
    let pool: sqlx::SqlitePool    = ctx.resolve_external().await?;
    Ok(MyService::new(cfg, pool))
})
```

## In custom Axum extractors

```rust
use axum::{async_trait, extract::FromRequestParts, http::request::Parts};
use injectable::axum::InjectableState;

struct AuthUser { email: String }

#[async_trait]
impl FromRequestParts<AppState> for AuthUser {
    type Rejection = StatusCode;

    async fn from_request_parts(parts: &mut Parts, state: &AppState) -> Result<Self, StatusCode> {
        let ctx = state.resolve_context();
        let auth: Inject<AuthService> = Inject::extract(ctx)
            .await.map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;

        let api_key = parts.headers.get("x-api-key")
            .and_then(|v| v.to_str().ok())
            .ok_or(StatusCode::UNAUTHORIZED)?;

        auth.validate(api_key).await
            .map(|email| AuthUser { email })
            .ok_or(StatusCode::UNAUTHORIZED)
    }
}
```

## What is intentionally private

`ctx.resolve::<T>()` and `ctx.resolve_singleton_arc::<T>()` are `pub(crate)`.
They bypass the singleton cache and can violate scope semantics. Use `ctx.extract()`
instead — it goes through the full Extract machinery and respects all scopes.
