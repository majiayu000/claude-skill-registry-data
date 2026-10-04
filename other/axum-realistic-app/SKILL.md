---
name: axum-realistic-app
description: Builds a complete realistic Axum application with injectable, including database, authentication, and CRUD routes. Use when starting a new Axum project or adding injectable to an existing one.
---

# Realistic Axum App with injectable

## Project structure

```
src/
├── main.rs
├── config.rs      — AppConfig (#[injectable(ctor)] reads env)
├── db.rs          — make_db_pool (#[injectable(factory)])
├── auth.rs        — AuthService (#[injectable])
├── users.rs       — UserService (#[injectable])
└── api.rs         — Axum handlers + router
```

## Skeleton

```rust
// config.rs
#[injectable]
impl AppConfig {
    #[injectable(ctor)]
    fn new() -> Self {
        Self {
            database_url: std::env::var("DATABASE_URL")
                .unwrap_or_else(|_| "sqlite::memory:".into()),
            jwt_secret: std::env::var("JWT_SECRET")
                .unwrap_or_else(|_| "dev-secret".into()),
        }
    }
}

// db.rs
#[injectable(factory)]
async fn make_db_pool(cfg: Inject<AppConfig>) -> Result<Pool<Sqlite>, sqlx::Error> {
    Pool::<Sqlite>::connect(&cfg.database_url).await
}

// auth.rs
#[injectable]
struct AuthService {
    #[injectable(inject(use_factory_async = crate::db::make_db_pool))]
    pool:   Pool<Sqlite>,
    #[injectable(inject)]
    config: Arc<AppConfig>,
}

// users.rs
#[injectable]
struct UserService {
    #[injectable(inject(use_factory_async = crate::db::make_db_pool))]
    pool: Pool<Sqlite>,
    #[injectable(inject)]
    auth: Arc<AuthService>,
}
```

## Router

```rust
use injectable::axum::AxumState;

pub fn router(state: AxumState) -> Router {
    Router::new()
        .route("/api/login",  post(login))
        .route("/api/users",  get(list_users).post(create_user))
        .route("/api/users/:id", get(get_user).put(update_user))
        .with_state(state)
}

async fn list_users(
    _auth: AuthenticatedUser,           // custom extractor validates JWT
    Inject(users): Inject<UserService>,
) -> impl IntoResponse {
    axum::Json(users.list().await.unwrap())
}
```

## main.rs

```rust
#[tokio::main]
async fn main() {
    let container = Container::builder().build().await.unwrap();

    // Warm up — triggers post_construct migrations
    container.context().extract::<Inject<UserService>>().await.unwrap();

    let state = AxumState::new(container);
    let app   = api::router(state);

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await.unwrap();
    axum::serve(listener, app).await.unwrap();
}
```

See [guides/13-axum-realistic-app.md](../../guides/13-axum-realistic-app.md).
