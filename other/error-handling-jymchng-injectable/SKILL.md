---
name: error-handling
description: Handles InjectableError variants — MissingDependency, ConstructionFailed, GraphValidationFailed, LifecycleHookFailed, ShutdownFailed. Use when matching on resolution errors or propagating injection failures.
---

# Error Handling

## InjectableError variants

```rust
use injectable::{prelude::*, InjectableError};

match container.resolve::<UserService>().await {
    Ok(svc) => { /* use svc */ }
    Err(InjectableError::MissingDependency { type_name }) => {
        eprintln!("Not registered: {type_name}");
    }
    Err(InjectableError::ConstructionFailed { type_name, reason }) => {
        eprintln!("Build failed for {type_name}: {reason}");
    }
    Err(InjectableError::GraphValidationFailed { errors }) => {
        for e in &errors { eprintln!("Graph: {e}"); }
    }
    Err(InjectableError::LifecycleHookFailed { type_name, hook, reason }) => {
        eprintln!("{hook} on {type_name} failed: {reason}");
    }
    Err(InjectableError::ShutdownFailed { errors }) => {
        for e in &errors { eprintln!("Shutdown: {e}"); }
    }
    Err(e) => eprintln!("Other: {e}"),
}
```

## Non-failing resolution

```rust
// Returns None instead of MissingDependency
let svc: Option<UserService> = container.try_resolve().await?;
let ext: Option<SqlitePool>  = container.try_resolve_external().await?;
```

## Errors in constructors

```rust
#[injectable]
impl ValidatedConfig {
    #[injectable(ctor)]
    fn new() -> Result<Self, Box<dyn std::error::Error + Send + Sync>> {
        let key = std::env::var("API_KEY")
            .map_err(|_| "API_KEY required")?;
        Ok(Self { key })
    }
}
// ConstructionFailed if env var missing
```

## Errors in lifecycle hooks

```rust
#[injectable(post_construct)]
async fn migrate(&self) -> Result<(), sqlx::Error> {
    sqlx::query("CREATE TABLE …").execute(&self.pool).await?;
    Ok(())
}
// LifecycleHookFailed if migration fails
```

## Propagating with anyhow

```rust
use anyhow::Context;

async fn start() -> anyhow::Result<()> {
    let container = Container::builder()
        .build().await
        .context("failed to build DI container")?;

    let svc = container
        .context().extract::<Inject<UserService>>().await
        .context("failed to resolve UserService")?;

    Ok(())
}
```

## InjectableResult alias

```rust
use injectable::InjectableResult;

async fn resolve_services(ctx: &ResolveContext) -> InjectableResult<Vec<Inject<Service>>> {
    let a: Inject<ServiceA> = ctx.extract().await?;
    let b: Inject<ServiceB> = ctx.extract().await?;
    Ok(vec![/* … */])
}
```
