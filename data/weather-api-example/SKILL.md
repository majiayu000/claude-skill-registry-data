---
name: weather-api-example
description: Reference implementation of a weather API using injectable with Axum, SQLite caching, and reqwest HTTP client. Use when building a similar service or as a reference for factory patterns with external types.
---

# Weather API — Complete Example

Fetches weather from Open-Meteo, caches results in SQLite.
Source: `examples/09_weather_api.rs` and `examples/10_weather_users_api.rs`.

Run:
```bash
cargo run --example 09_weather_api --features axum
cargo run --example 10_weather_users_api --features axum
```

## Architecture

```
AppConfig (#[injectable(ctor)] reads env)
    ↓
make_pool (#[injectable(factory)])   make_http_client (#[injectable(factory)])
    ↓                               ↓
WeatherService (#[injectable] ← pool, client)
    ↓
UserService (#[injectable] ← pool, Arc<WeatherService>)
```

## Pool factory with sqlite::memory: note

```rust
#[injectable(factory)]
async fn make_pool(cfg: Inject<AppConfig>) -> Result<Pool<Sqlite>, InjectableError> {
    sqlx::sqlite::SqlitePoolOptions::new()
        .max_connections(1)        // REQUIRED for sqlite::memory:
        .idle_timeout(None)        // prevent connection recycling
        .max_lifetime(None)
        .connect(&cfg.database_url)
        .await
        .map_err(|e| InjectableError::ConstructionFailed {
            type_name: "SqlitePool",
            reason: e.to_string(),
        })
}
```

## HTTP client factory

```rust
async fn make_http_client(_ctx: &ResolveContext)
    -> Result<reqwest::Client, InjectableError>
{
    reqwest::Client::builder()
        .timeout(std::time::Duration::from_secs(10))
        .user_agent("injectable-example/1.0")
        .build()
        .map_err(|e| InjectableError::ConstructionFailed {
            type_name: "reqwest::Client",
            reason: e.to_string(),
        })
}
```

## Key patterns

| Pattern | Where used |
|---|---|
| `#[injectable(factory)]` for pool | `make_pool` |
| `use_factory_async` field | `pool` on WeatherService |
| `use_factory_sync` field | `client` on WeatherService (sync factory) |
| `Arc<WeatherService>` dep | `weather_service` field on UserService |
| `#[injectable(post_construct)]` migration | WeatherService, UserService |
| `#[injectable(pre_destruct)]` close | Pool close |
| Custom AppState | Implements InjectableState |

See full sources in `examples/`.
