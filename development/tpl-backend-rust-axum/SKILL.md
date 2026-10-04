---
name: tpl-backend-rust-axum
description: Template do pack (backend/09-rust-axum.md). Orienta o agente em APIs, servicos e arquitetura backend alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: backend/09-rust-axum.md
  generated_by: install_pack_templates_as_claude_skills
---

# PROJECT: Rust Axum REST API

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `backend/09-rust-axum.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## STACK
- **Language:** Rust (edition 2021, stable)
- **Framework:** Axum 0.7
- **Database:** PostgreSQL via SQLx 0.7
- **Middleware:** Tower + tower-http
- **Serialization:** serde + serde_json
- **Error handling:** thiserror + anyhow
- **Tracing:** tracing + tracing-subscriber
- **Testing:** cargo test + sqlx test macros

---

## PROJECT STRUCTURE
```
src/
├── main.rs                   # Server bootstrap, router assembly
├── config.rs                 # Config struct from env vars
├── state.rs                  # AppState definition
├── error.rs                  # AppError enum (thiserror)
├── db/
│   └── mod.rs                # PgPool creation + migrations
├── routes/
│   ├── mod.rs                # Router assembly
│   ├── users.rs
│   └── posts.rs
├── handlers/
│   ├── users.rs
│   └── posts.rs
├── models/
│   ├── user.rs               # DB model + request/response types
│   └── post.rs
└── middleware/
    ├── auth.rs               # JWT extractor
    └── request_id.rs
migrations/
└── 001_init.sql
tests/
└── integration/
    └── users_test.rs
```

---

## ARCHITECTURE RULES
1. **`AppState` is cloned via `Arc`** — never use `Mutex` for read-heavy shared state; use `RwLock` if writes are needed.
2. **Extractors validate input** — use custom `JsonExtractor<T>` that returns `AppError` on invalid JSON.
3. **`AppError` implements `IntoResponse`** — handlers return `Result<impl IntoResponse, AppError>` only.
4. **SQLx compile-time checked macros** — prefer `sqlx::query_as!` over raw query strings.
5. **Tracing spans on every handler** — `#[tracing::instrument]` on all public handler functions.
6. **No `unwrap()`/`expect()` in handlers** — propagate errors through `?` operator.
7. **Database migrations run at startup** — `sqlx::migrate!().run(&pool).await?` in `main`.

---

## ERROR TYPES (thiserror)

```rust
// src/error.rs
use axum::{
    http::StatusCode,
    response::{IntoResponse, Response},
    Json,
};
use serde_json::json;
use thiserror::Error;

#[derive(Debug, Error)]
pub enum AppError {
    #[error("Not found: {0}")]
    NotFound(String),

    #[error("Unauthorized: {0}")]
    Unauthorized(String),

    #[error("Unprocessable entity: {0}")]
    UnprocessableEntity(String),

    #[error("Internal error")]
    Internal(#[from] anyhow::Error),

    #[error("Database error")]
    Database(#[from] sqlx::Error),
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, message) = match &self {
            Self::NotFound(msg)              => (StatusCode::NOT_FOUND, msg.clone()),
            Self::Unauthorized(msg)          => (StatusCode::UNAUTHORIZED, msg.clone()),
            Self::UnprocessableEntity(msg)   => (StatusCode::UNPROCESSABLE_ENTITY, msg.clone()),
            Self::Internal(_) | Self::Database(_) => {
                tracing::error!(error = %self);
                (StatusCode::INTERNAL_SERVER_ERROR, "Internal server error".into())
            }
        };
        (status, Json(json!({ "error": message }))).into_response()
    }
}
```

---

## STATE MANAGEMENT WITH ARC

```rust
// src/state.rs
use sqlx::PgPool;
use std::sync::Arc;

#[derive(Clone)]
pub struct AppState {
    pub db:     PgPool,
    pub config: Arc<crate::config::Config>,
}

// src/config.rs
#[derive(Debug, Clone)]
pub struct Config {
    pub database_url: String,
    pub jwt_secret:   String,
    pub port:         u16,
}

impl Config {
    pub fn from_env() -> anyhow::Result<Self> {
        Ok(Self {
            database_url: std::env::var("DATABASE_URL")?,
            jwt_secret:   std::env::var("JWT_SECRET")?,
            port:         std::env::var("PORT").unwrap_or("3000".into()).parse()?,
        })
    }
}

// src/main.rs
#[tokio::main]
async fn main() -> anyhow::Result<()> {
    tracing_subscriber::fmt()
        .with_env_filter(tracing_subscriber::EnvFilter::from_default_env())
        .init();

    let config    = Arc::new(Config::from_env()?);
    let pool      = PgPool::connect(&config.database_url).await?;
    sqlx::migrate!("./migrations").run(&pool).await?;

    let state  = AppState { db: pool, config };
    let router = routes::create_router(state);
    let addr   = format!("0.0.0.0:{}", config.port);

    let listener = tokio::net::TcpListener::bind(&addr).await?;
    tracing::info!("Listening on {addr}");
    axum::serve(listener, router).await?;
    Ok(())
}
```

---

## EXTRACTOR PATTERN + HANDLER

```rust
// src/models/user.rs
use serde::{Deserialize, Serialize};
use uuid::Uuid;
use chrono::{DateTime, Utc};

#[derive(Debug, Serialize, sqlx::FromRow)]
pub struct User {
    pub id:         Uuid,
    pub email:      String,
    pub name:       String,
    pub created_at: DateTime<Utc>,
}

#[derive(Debug, Deserialize, validator::Validate)]
pub struct CreateUserRequest {
    #[validate(email)]
    pub email: String,
    #[validate(length(min = 2, max = 100))]
    pub name:  String,
}

// src/handlers/users.rs
use axum::{
    extract::{Path, State},
    http::StatusCode,
    Json,
};
use uuid::Uuid;

#[tracing::instrument(skip(state))]
pub async fn create_user(
    State(state): State<AppState>,
    Json(body):   Json<CreateUserRequest>,
) -> Result<(StatusCode, Json<User>), AppError> {
    let user = sqlx::query_as!(
        User,
        "INSERT INTO users (email, name) VALUES ($1, $2) RETURNING *",
        body.email,
        body.name
    )
    .fetch_one(&state.db)
    .await?;

    Ok((StatusCode::CREATED, Json(user)))
}

#[tracing::instrument(skip(state))]
pub async fn get_user(
    State(state): State<AppState>,
    Path(id):     Path<Uuid>,
) -> Result<Json<User>, AppError> {
    let user = sqlx::query_as!(User, "SELECT * FROM users WHERE id = $1", id)
        .fetch_optional(&state.db)
        .await?
        .ok_or_else(|| AppError::NotFound(format!("User {id} not found")))?;

    Ok(Json(user))
}

// src/routes/mod.rs
use axum::{routing::get, Router};
pub fn create_router(state: AppState) -> Router {
    Router::new()
        .route("/api/users",     axum::routing::post(handlers::users::create_user))
        .route("/api/users/:id", get(handlers::users::get_user))
        .layer(tower_http::trace::TraceLayer::new_for_http())
        .with_state(state)
}
```

---

## ROUTING TABLE

| Method | Path | Auth | Action |
|--------|------|------|--------|
| POST | /api/users | No | Create user |
| GET | /api/users | Yes | List users (paginated) |
| GET | /api/users/:id | Yes | Get user by UUID |
| PUT | /api/users/:id | Yes (owner) | Update user |
| DELETE | /api/users/:id | Yes (admin) | Delete user |
| POST | /api/auth/login | No | Authenticate, return JWT |
| GET | /api/posts | No | List public posts |
| POST | /api/posts | Yes | Create post |
| GET | /api/posts/:id | No | Get post |
| GET | /health | No | Liveness probe (200 OK) |

---

## QUALITY GATES
- [ ] `cargo check` — zero warnings
- [ ] `cargo clippy -- -D warnings` — clean
- [ ] `cargo test` — all tests pass
- [ ] No `unwrap()` or `expect()` outside of `main` or test code
- [ ] All handlers instrument with `#[tracing::instrument]`
- [ ] `AppError::Internal` logs full error; client never sees stack trace
- [ ] SQLx macro queries verified against DB schema (`cargo sqlx prepare`)
- [ ] Migration files committed and idempotent
- [ ] `cargo audit` — no known vulnerabilities

---

## FORBIDDEN
- ❌ `panic!()` / `unwrap()` in handler code paths
- ❌ `.clone()` on large data structures inside hot paths
- ❌ Blocking I/O (`std::fs`, `std::thread::sleep`) inside async handlers — use `tokio::fs`, `tokio::time`
- ❌ `Mutex<PgPool>` — SQLx pool is already `Clone + Send + Sync`
- ❌ Returning raw `sqlx::Error` to the client
- ❌ Hardcoded SQL table names as string literals outside of `query!` macros
- ❌ Skipping `sqlx::migrate!()` at startup
