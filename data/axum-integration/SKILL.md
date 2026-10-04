---
name: axum-integration
description: Wires injectable with Axum handlers using Inject<T> as an extractor. Use when adding dependency injection to Axum routes, setting up AxumState or custom InjectableState, or getting handler extraction errors.
---

# Axum Integration

## Setup

```rust
use injectable::{prelude::*, axum::AxumState};
use axum::{routing::get, Router};

#[tokio::main]
async fn main() {
    let container = Container::builder().build().await.unwrap();
    let state = AxumState::new(container);

    let app = Router::new()
        .route("/users", get(list_users))
        .with_state(state);

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await.unwrap();
    axum::serve(listener, app).await.unwrap();
}
```

## Handlers

```rust
use injectable::prelude::*;

// Inject<T> works like any Axum extractor
async fn list_users(
    Inject(svc): Inject<UserService>,          // destructure to get Arc<UserService>
    db: Inject<Database>,                       // or keep as Inject<T>
) -> axum::Json<Vec<User>> {
    axum::Json(svc.list().await.unwrap())
}

// Mix with other extractors
async fn create_user(
    Inject(svc): Inject<UserService>,
    axum::Json(body): axum::Json<CreateUserBody>,
) -> impl axum::response::IntoResponse { /* … */ }
```

## Custom state

```rust
use injectable::axum::InjectableState;

#[derive(Clone)]
struct AppState {
    container: Arc<Container>,
    version:   &'static str,
}

impl InjectableState for AppState {
    fn resolve_context(&self) -> &ResolveContext {
        self.container.context()
    }
}

// Use AppState instead of AxumState:
let app = Router::new()
    .route("/", get(handler))
    .with_state(AppState { container: Arc::new(container), version: "1.0" });
```

## Custom auth extractor

```rust
use axum::{async_trait, extract::FromRequestParts, http::request::Parts};

struct AuthUser { email: String }

#[async_trait]
impl FromRequestParts<AppState> for AuthUser {
    type Rejection = StatusCode;

    async fn from_request_parts(parts: &mut Parts, state: &AppState) -> Result<Self, StatusCode> {
        let api_key = parts.headers.get("x-api-key")
            .and_then(|v| v.to_str().ok())
            .ok_or(StatusCode::UNAUTHORIZED)?;

        let auth: Inject<AuthService> = Inject::extract(state.resolve_context())
            .await.map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;

        auth.validate(api_key).await
            .map(|email| AuthUser { email })
            .ok_or(StatusCode::UNAUTHORIZED)
    }
}
```

See [guides/07-axum-basics.md](../../guides/07-axum-basics.md) and [guides/08-axum-custom-state.md](../../guides/08-axum-custom-state.md).
