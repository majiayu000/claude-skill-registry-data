---
name: config-injection
description: Injects application configuration from environment variables or config files using #[injectable(ctor)]. Use when services need database URLs, API keys, ports, or other startup configuration.
---

# Configuration Injection

## Env var pattern

```rust
use injectable::prelude::*;

#[derive(Debug, Clone)]
struct AppConfig {
    pub database_url: String,
    pub port:         u16,
    pub api_key:      String,
}

#[injectable]
impl AppConfig {
    #[injectable(ctor)]
    fn new() -> Result<Self, Box<dyn std::error::Error + Send + Sync>> {
        Ok(Self {
            database_url: std::env::var("DATABASE_URL")
                .unwrap_or_else(|_| "sqlite::memory:".into()),
            port: std::env::var("PORT")
                .ok().and_then(|p| p.parse().ok()).unwrap_or(3000),
            api_key: std::env::var("API_KEY")
                .map_err(|_| "API_KEY env var required")?,
        })
    }
}
```

## Consuming config in other services

```rust
#[injectable(factory)]
async fn make_pool(cfg: Inject<AppConfig>) -> Result<sqlx::SqlitePool, sqlx::Error> {
    sqlx::SqlitePool::connect(&cfg.database_url).await
}

#[injectable]
struct Database {
    #[injectable(inject(use_factory_async = self::make_pool))]
    pool: sqlx::SqlitePool,
}

// Or via constructor:
#[injectable]
impl ApiClient {
    #[injectable(ctor)]
    fn new(cfg: Inject<AppConfig>) -> Self {
        Self {
            base_url: format!("https://api.example.com"),
            api_key:  cfg.api_key.clone(),
        }
    }
}
```

## Config as singleton

AppConfig is singleton by default — all services share the same config instance.

```rust
let ctx = container.context();
let cfg: Inject<AppConfig> = ctx.extract().await?;
println!("Port: {}", cfg.port);
```

## Testing with custom config

```rust
// Override via environment before building:
std::env::set_var("DATABASE_URL", "sqlite::memory:");
std::env::set_var("API_KEY", "test-key");

let container = Container::builder().build().await.unwrap();
```

See [guides/11-config-from-env.md](../../guides/11-config-from-env.md).
