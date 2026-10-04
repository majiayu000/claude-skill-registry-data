---
name: optional-dependencies
description: Injects optional dependencies using Option<Inject<T>>. Use when a service should work with or without a backend (metrics, telemetry, feature flags) that may not always be registered.
---

# Optional Dependencies

`Option<Inject<T>>` resolves to `Some` when T is available, `None` otherwise.

## Field pattern

```rust
use injectable::prelude::*;

#[injectable]
struct Analytics {
    db: Inject<Database>,
    #[injectable(inject)]
    metrics: Option<Inject<MetricsBackend>>,   // None if not registered
}

impl Analytics {
    pub fn record(&self, event: &str) {
        if let Some(m) = &self.metrics {
            m.emit(event);
        }
    }
}
```

## Registering the optional dep

```rust
// Production: register it
let container = Container::builder()
    .register(DynProvider::sync(|| Ok(PrometheusMetrics::new())))
    .build().await?;

// Test/dev: omit it — Analytics still resolves with metrics = None
let container = Container::builder().build().await?;
```

## Manual extraction

```rust
let ctx = container.context();
let maybe: Option<Inject<MetricsBackend>> = ctx.extract().await?;
if let Some(m) = maybe {
    m.flush().await;
}
```

## try_resolve — check without fail

```rust
// Returns Ok(None) instead of Err(MissingDependency)
let svc: Option<UserService> = container.try_resolve().await?;
let ext: Option<reqwest::Client> = container.try_resolve_external().await?;
```

See [guides/14-optional-deps.md](../../guides/14-optional-deps.md).
