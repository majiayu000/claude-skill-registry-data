---
name: rust-backend-axum
description: Build production-ready Rust backend APIs with Axum framework. Covers router composition, state management, extractors, middleware (auth, tracing), error handling with IntoResponse, and graceful shutdown. Use when building Rust web services, REST APIs, or when working with Axum, Tower middleware, or async Rust backends.
---

<objective>
Build production-ready Rust backend APIs using Axum 0.7+ framework with Tower middleware integration. This skill provides patterns for modular router design, type-safe state management, request extraction, authentication middleware, custom error responses, and graceful shutdown.
</objective>

<essential_principles>
**1. Extractors Order Matters**

Body-consuming extractors (Json, Form, Bytes) must come LAST in handler parameters.

```rust
// CORRECT: State and Path before Json
async fn handler(
    State(state): State<AppState>,
    Path(id): Path<Uuid>,
    Json(body): Json<CreateRequest>,
) -> impl IntoResponse { }
```

**2. State Must Be Clone**

AppState passed to .with_state() must implement Clone. Use Arc for expensive-to-clone fields.

```rust
#[derive(Clone)]
struct AppState {
    db: sqlx::PgPool,          // PgPool is cheap to clone
    config: Arc<Config>,        // Arc for expensive data
}
```

**3. route_layer vs layer**

- route_layer() - Applies only to routes defined BEFORE it
- layer() - Applies to ALL routes
</essential_principles>

<quick_start>
**Minimal Axum Application**

```rust
use axum::{routing::get, Router};
use std::sync::Arc;

#[derive(Clone)]
struct AppState {
    db: sqlx::PgPool,
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let db = sqlx::PgPool::connect(&std::env::var("DATABASE_URL")?).await?;
    let state = AppState { db };

    let app = Router::new()
        .route("/health", get(|| async { "ok" }))
        .with_state(state);

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await?;
    axum::serve(listener, app).await?;
    Ok(())
}
```
</quick_start>

<patterns>
<pattern name="modular_router">
**Modular Router Composition**

```rust
pub fn create_router(state: AppState) -> Router {
    Router::new()
        .nest("/api/v1", api_routes())
        .route("/health", axum::routing::get(health))
        .with_state(state)
}

fn api_routes() -> Router<AppState> {
    Router::new()
        .nest("/users", users::routes())
        .nest("/items", items::routes())
}
```
</pattern>

<pattern name="auth_middleware">
**Authentication Middleware with Extension**

```rust
use axum::{
    extract::{Request, Extension},
    middleware::Next,
    http::{header, StatusCode},
};

pub async fn auth_middleware(
    mut req: Request,
    next: Next,
) -> Result<Response, StatusCode> {
    let auth_header = req.headers()
        .get(header::AUTHORIZATION)
        .and_then(|h| h.to_str().ok())
        .and_then(|h| h.strip_prefix("Bearer "));

    let token = auth_header.ok_or(StatusCode::UNAUTHORIZED)?;
    let user = validate_jwt(token).await.map_err(|_| StatusCode::UNAUTHORIZED)?;

    req.extensions_mut().insert(user);
    Ok(next.run(req).await)
}

// Apply to routes
pub fn protected_routes() -> Router<AppState> {
    Router::new()
        .route("/profile", get(protected_handler))
        .route_layer(middleware::from_fn(auth_middleware))
}
```
</pattern>

<pattern name="middleware_stack">
**Tower Middleware Stack**

```rust
use tower::ServiceBuilder;
use tower_http::{trace::TraceLayer, timeout::TimeoutLayer, compression::CompressionLayer};

let app = Router::new()
    .nest("/api", api_routes())
    .with_state(state)
    .layer(
        ServiceBuilder::new()
            .layer(TraceLayer::new_for_http())
            .layer(TimeoutLayer::new(Duration::from_secs(30)))
            .layer(CompressionLayer::new())
    );
```
</pattern>
</patterns>

<success_criteria>
- [ ] Router compiles with all routes registered
- [ ] State is Clone and contains Arc for expensive fields
- [ ] Extractors are ordered correctly (body consumers last)
- [ ] Error type implements IntoResponse
- [ ] Auth middleware uses Extension for user propagation
- [ ] Graceful shutdown handles SIGTERM/SIGINT
- [ ] cargo clippy passes without warnings
</success_criteria>
