---
name: reqwest-client
description: Injects a reqwest::Client into services using injectable. Use when adding an HTTP client to a service, sharing one client across services, or configuring timeouts and headers at startup.
---

# reqwest::Client with injectable

## Simple factory (per-service)

```rust
use injectable::prelude::*;

fn make_http_client(_ctx: &ResolveContext) -> reqwest::Client {
    reqwest::Client::builder()
        .timeout(std::time::Duration::from_secs(30))
        .user_agent("my-app/1.0")
        .build()
        .expect("valid client config")
}

#[injectable]
struct WeatherService {
    #[injectable(inject(use_factory_sync = self::make_http_client))]
    client: reqwest::Client,
}
```

## Factory that reads config

```rust
#[injectable(factory)]
async fn make_client(cfg: Inject<AppConfig>) -> Result<reqwest::Client, reqwest::Error> {
    reqwest::Client::builder()
        .timeout(std::time::Duration::from_secs(cfg.http_timeout_secs))
        .build()
}

#[injectable]
struct ApiService {
    #[injectable(inject(use_factory_async = self::make_client))]
    client: reqwest::Client,
}
```

## Shared client via DynProvider

```rust
let container = Container::builder()
    .register(DynProvider::sync(|| {
        Ok(reqwest::Client::builder()
            .timeout(std::time::Duration::from_secs(30))
            .build()?)
    }))
    .build().await?;

// Consume in constructor:
#[injectable]
impl WeatherService {
    #[injectable(ctor)]
    fn new(#[injectable(inject)] client: Arc<reqwest::Client>) -> Self {
        Self { client }
    }
}
```

## Usage in service

```rust
pub async fn get_weather(&self, lat: f64, lon: f64) -> Result<WeatherInfo, reqwest::Error> {
    let url = format!(
        "https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m"
    );
    let resp: WeatherResponse = self.client.get(&url).send().await?.json().await?;
    Ok(resp.into())
}
```

## Cargo.toml

```toml
reqwest = { version = "0.12", features = ["json"] }
```
