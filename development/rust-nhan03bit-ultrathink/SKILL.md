---
name: rust
description: Rust ownership model, async programming with Tokio, web frameworks (Axum/Actix), error handling, and systems programming patterns
layer: domain
category: backend
triggers:
  - "rust"
  - "cargo"
  - "tokio"
  - "axum"
  - "actix"
  - "ownership"
  - "borrow checker"
  - "rust web"
inputs:
  - "Rust application requirements"
  - "Performance-critical system needs"
  - "Web service specifications"
outputs:
  - "Idiomatic Rust implementations"
  - "Async patterns with Tokio"
  - "Web framework configurations"
linksTo:
  - microservices
  - postgresql
  - redis
  - websockets
  - message-queues
linkedFrom:
  - error-handling
  - testing
preferredNextSkills:
  - postgresql
  - redis
  - microservices
fallbackSkills:
  - golang
  - nodejs
riskLevel: low
memoryReadPolicy: selective
memoryWritePolicy: none
sideEffects: []
---

# Rust Domain Skill

## Purpose

Provide expert-level guidance on Rust development, including the ownership system, async programming with Tokio, web framework patterns (Axum, Actix), error handling with `thiserror`/`anyhow`, and production-grade systems programming.

## Key Patterns

### 1. Ownership and Borrowing

```rust
// Ownership rules:
// 1. Each value has exactly one owner
// 2. When the owner goes out of scope, the value is dropped
// 3. You can have EITHER one mutable reference OR any number of immutable references

// Prefer borrowing over cloning
fn process_name(name: &str) -> String {
    // Takes a reference -- no ownership transfer
    name.to_uppercase()
}

// Use lifetimes when the compiler needs help
struct Config<'a> {
    database_url: &'a str,
    app_name: &'a str,
}

impl<'a> Config<'a> {
    fn connection_string(&self) -> String {
        format!("{}?app={}", self.database_url, self.app_name)
    }
}

// Interior mutability for shared mutable state
use std::sync::{Arc, RwLock};

#[derive(Clone)]
struct AppState {
    cache: Arc<RwLock<HashMap<String, CachedItem>>>,
    db: Arc<Pool<Postgres>>,
}

impl AppState {
    fn get_cached(&self, key: &str) -> Option<CachedItem> {
        self.cache.read().unwrap().get(key).cloned()
    }

    fn set_cached(&self, key: String, item: CachedItem) {
        self.cache.write().unwrap().insert(key, item);
    }
}
```

### 2. Error Handling

```rust
use thiserror::Error;

// Domain-specific errors with thiserror
#[derive(Error, Debug)]
pub enum AppError {
    #[error("resource not found: {resource} with id {id}")]
    NotFound { resource: String, id: String },

    #[error("unauthorized: {0}")]
    Unauthorized(String),

    #[error("validation failed: {0}")]
    Validation(String),

    #[error("database error")]
    Database(#[from] sqlx::Error),

    #[error("external service error")]
    ExternalService(#[from] reqwest::Error),

    #[error(transparent)]
    Internal(#[from] anyhow::Error),
}

// Map to HTTP responses (Axum)
impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, code, message) = match &self {
            AppError::NotFound { .. } => (StatusCode::NOT_FOUND, "NOT_FOUND", self.to_string()),
            AppError::Unauthorized(msg) => (StatusCode::UNAUTHORIZED, "UNAUTHORIZED", msg.clone()),
            AppError::Validation(msg) => (StatusCode::UNPROCESSABLE_ENTITY, "VALIDATION", msg.clone()),
            AppError::Database(_) => {
                tracing::error!(error = ?self, "database error");
                (StatusCode::INTERNAL_SERVER_ERROR, "INTERNAL", "internal error".into())
            }
            AppError::ExternalService(_) => {
                tracing::error!(error = ?self, "external service error");
                (StatusCode::BAD_GATEWAY, "BAD_GATEWAY", "upstream error".into())
            }
            AppError::Internal(_) => {
                tracing::error!(error = ?self, "internal error");
                (StatusCode::INTERNAL_SERVER_ERROR, "INTERNAL", "internal error".into())
            }
        };

        (status, Json(json!({ "error": { "code": code, "message": message } }))).into_response()
    }
}

// Use Result<T, AppError> throughout
type AppResult<T> = Result<T, AppError>;
```

### 3. Axum Web Framework

```rust
use axum::{
    extract::{Path, Query, State, Json},
    http::StatusCode,
    middleware,
    routing::{get, post, delete},
    Router,
};
use tower::ServiceBuilder;
use tower_http::{
    cors::CorsLayer,
    trace::TraceLayer,
    compression::CompressionLayer,
    timeout::TimeoutLayer,
};

pub fn create_router(state: AppState) -> Router {
    let api = Router::new()
        .route("/users", get(list_users).post(create_user))
        .route("/users/{id}", get(get_user).delete(delete_user))
        .layer(middleware::from_fn_with_state(state.clone(), auth_middleware));

    Router::new()
        .nest("/api/v1", api)
        .route("/health", get(health_check))
        .layer(
            ServiceBuilder::new()
                .layer(TraceLayer::new_for_http())
                .layer(CompressionLayer::new())
                .layer(TimeoutLayer::new(Duration::from_secs(30)))
                .layer(CorsLayer::permissive()),
        )
        .with_state(state)
}

// Handler with extractors
async fn list_users(
    State(state): State<AppState>,
    Query(params): Query<ListUsersParams>,
) -> AppResult<Json<PaginatedResponse<UserResponse>>> {
    let users = state.user_service.list(params.into()).await?;
    Ok(Json(users))
}

async fn create_user(
    State(state): State<AppState>,
    Json(body): Json<CreateUserRequest>,
) -> AppResult<(StatusCode, Json<UserResponse>)> {
    let user = state.user_service.create(body).await?;
    Ok((StatusCode::CREATED, Json(user)))
}

// Middleware
async fn auth_middleware(
    State(state): State<AppState>,
    mut req: Request,
    next: Next,
) -> Result<Response, AppError> {
    let token = req
        .headers()
        .get("Authorization")
        .and_then(|h| h.to_str().ok())
        .and_then(|h| h.strip_prefix("Bearer "))
        .ok_or_else(|| AppError::Unauthorized("missing token".into()))?;

    let claims = state.auth_service.verify(token).await?;
    req.extensions_mut().insert(claims);
    Ok(next.run(req).await)
}
```

### 4. Async with Tokio

```rust
use tokio::sync::{mpsc, Semaphore};
use tokio::time::{timeout, Duration};

// Bounded channel for backpressure
async fn process_events(mut rx: mpsc::Receiver<Event>) {
    while let Some(event) = rx.recv().await {
        if let Err(e) = handle_event(&event).await {
            tracing::error!(error = ?e, event = ?event, "failed to handle event");
        }
    }
}

// Semaphore for concurrency limiting
async fn fetch_all(urls: Vec<String>, max_concurrent: usize) -> Vec<Result<String, reqwest::Error>> {
    let semaphore = Arc::new(Semaphore::new(max_concurrent));
    let client = reqwest::Client::new();

    let tasks: Vec<_> = urls
        .into_iter()
        .map(|url| {
            let sem = semaphore.clone();
            let client = client.clone();
            tokio::spawn(async move {
                let _permit = sem.acquire().await.unwrap();
                client.get(&url).send().await?.text().await
            })
        })
        .collect();

    let mut results = Vec::with_capacity(tasks.len());
    for task in tasks {
        results.push(task.await.unwrap());
    }
    results
}

// Graceful shutdown
async fn run_server(listener: TcpListener, app: Router) {
    let (shutdown_tx, shutdown_rx) = tokio::sync::oneshot::channel::<()>();

    tokio::spawn(async move {
        let mut sigterm = tokio::signal::unix::signal(SignalKind::terminate()).unwrap();
        tokio::select! {
            _ = tokio::signal::ctrl_c() => {}
            _ = sigterm.recv() => {}
        }
        let _ = shutdown_tx.send(());
    });

    axum::serve(listener, app)
        .with_graceful_shutdown(async { shutdown_rx.await.ok(); })
        .await
        .unwrap();
}
```

### 5. Database with SQLx

```rust
use sqlx::{PgPool, FromRow, query_as};

#[derive(FromRow)]
struct User {
    id: Uuid,
    email: String,
    name: String,
    created_at: chrono::DateTime<chrono::Utc>,
}

// Compile-time checked queries
async fn get_user(pool: &PgPool, id: Uuid) -> AppResult<User> {
    sqlx::query_as!(
        User,
        r#"SELECT id, email, name, created_at FROM users WHERE id = $1"#,
        id
    )
    .fetch_optional(pool)
    .await?
    .ok_or_else(|| AppError::NotFound {
        resource: "user".into(),
        id: id.to_string(),
    })
}

// Transactions
async fn transfer_credits(pool: &PgPool, from: Uuid, to: Uuid, amount: i64) -> AppResult<()> {
    let mut tx = pool.begin().await?;

    sqlx::query!("UPDATE accounts SET balance = balance - $1 WHERE id = $2 AND balance >= $1", amount, from)
        .execute(&mut *tx)
        .await?;

    sqlx::query!("UPDATE accounts SET balance = balance + $1 WHERE id = $2", amount, to)
        .execute(&mut *tx)
        .await?;

    tx.commit().await?;
    Ok(())
}
```

## Best Practices

1. **Use `clippy`** with `#![deny(clippy::all)]` in CI
2. **Prefer `&str` over `String`** in function parameters
3. **Use `thiserror`** for library errors, `anyhow` for application errors
4. **Use `tracing`** instead of `log` for structured, async-aware logging
5. **Prefer `Arc<T>` over `Rc<T>`** unless single-threaded is guaranteed
6. **Use `tokio::spawn`** for CPU-bound work in `spawn_blocking`
7. **Prefer iterators** over manual loops -- they often optimize better
8. **Use `#[derive]` macros** extensively: `Debug, Clone, PartialEq, Serialize, Deserialize`
9. **Test with `#[tokio::test]`** for async tests
10. **Use `cargo deny`** to audit dependencies for vulnerabilities

## Common Pitfalls

| Pitfall | Impact | Fix |
|---------|--------|-----|
| Holding `MutexGuard` across `.await` | Deadlock | Scope the lock, clone data out |
| `unwrap()` in production code | Panics | Use `?` operator, `expect()` with context |
| Cloning everything to satisfy borrow checker | Performance degradation | Restructure code, use `Arc`, references |
| Blocking the Tokio runtime | Async task starvation | Use `tokio::task::spawn_blocking` |
| Not setting `#[tokio::main(flavor = "multi_thread")]` | Single-threaded runtime | Explicitly configure runtime |
| Unbounded channels | Memory exhaustion | Use `mpsc::channel(capacity)` |
