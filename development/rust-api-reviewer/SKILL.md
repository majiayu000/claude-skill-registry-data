---
name: rust-api-reviewer
description: |
  WHEN: Rust API review with Actix-web/Axum/Rocket, async patterns, extractors, middleware
  WHAT: Async handlers + Extractors + State management + Error responses + Tower middleware
  WHEN NOT: General Rust → rust-reviewer, Go API → go-api-reviewer
---

# Rust API Reviewer Skill

## Purpose
Reviews Rust web API projects using Actix-web, Axum, or Rocket for async patterns and API design.

## When to Use
- Rust REST API code review
- Actix-web/Axum/Rocket project review
- Async handler patterns
- Middleware and extractors
- State management review

## Project Detection
- `actix-web` in Cargo.toml
- `axum` in Cargo.toml
- `rocket` in Cargo.toml
- `handlers/`, `routes/` directories
- `tower` middleware usage

## Workflow

### Step 1: Analyze Project
```
**Framework**: Axum 0.7+
**Runtime**: Tokio
**Database**: SQLx / SeaORM / Diesel
**Validation**: validator crate
**Auth**: JWT / OAuth2
```

### Step 2: Select Review Areas
**AskUserQuestion:**
```
"Which areas to review?"
Options:
- Full API review (recommended)
- Async handlers and patterns
- Extractors and validation
- State and dependency injection
- Error handling and responses
multiSelect: true
```

## Detection Rules

### Axum Patterns

#### Handler Organization
| Check | Recommendation | Severity |
|-------|----------------|----------|
| All routes in main | Use Router::nest | MEDIUM |
| No route grouping | Group by resource | MEDIUM |
| Missing method routing | Use method_router | LOW |

```rust
// BAD: All routes in main
#[tokio::main]
async fn main() {
    let app = Router::new()
        .route("/users", get(list_users).post(create_user))
        .route("/users/:id", get(get_user).put(update_user))
        .route("/products", get(list_products))
        // ... 50 more routes
        .with_state(state);
}

// GOOD: Organized with nest
fn user_routes() -> Router<AppState> {
    Router::new()
        .route("/", get(list_users).post(create_user))
        .route("/:id", get(get_user).put(update_user).delete(delete_user))
}

fn product_routes() -> Router<AppState> {
    Router::new()
        .route("/", get(list_products).post(create_product))
        .route("/:id", get(get_product))
}

fn api_routes() -> Router<AppState> {
    Router::new()
        .nest("/users", user_routes())
        .nest("/products", product_routes())
}

#[tokio::main]
async fn main() {
    let state = AppState::new().await;

    let app = Router::new()
        .nest("/api/v1", api_routes())
        .layer(TraceLayer::new_for_http())
        .with_state(state);

    // ...
}
```

#### Extractors
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Manual JSON parsing | Use Json extractor | HIGH |
| No validation | Use ValidatedJson | HIGH |
| Order of extractors | Body extractors last | HIGH |

```rust
// BAD: Manual parsing
async fn create_user(body: String) -> Result<Json<User>, AppError> {
    let req: CreateUserRequest = serde_json::from_str(&body)?;
    // ...
}

// GOOD: Json extractor
async fn create_user(
    Json(req): Json<CreateUserRequest>,
) -> Result<Json<User>, AppError> {
    // req is already deserialized
}

// GOOD: With validation (using validator crate)
#[derive(Debug, Deserialize, Validate)]
struct CreateUserRequest {
    #[validate(length(min = 1, max = 100))]
    name: String,
    #[validate(email)]
    email: String,
}

async fn create_user(
    State(state): State<AppState>,
    ValidatedJson(req): ValidatedJson<CreateUserRequest>,
) -> Result<Json<User>, AppError> {
    // req is validated
}

// IMPORTANT: Extractor order matters!
// Body-consuming extractors must be last
async fn handler(
    State(state): State<AppState>,    // First: doesn't consume
    Path(id): Path<i32>,              // Second: from URL
    Query(params): Query<Params>,     // Third: from query
    Json(body): Json<Request>,        // LAST: consumes body
) -> Response {
    // ...
}
```

#### State Management
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Global static state | Use State extractor | HIGH |
| No connection pool | Use shared pool | HIGH |
| Mutex in async | Use tokio::sync::Mutex | CRITICAL |

```rust
// BAD: Global static
static DB: OnceCell<Database> = OnceCell::new();

async fn get_user(Path(id): Path<i32>) -> Json<User> {
    let db = DB.get().unwrap();  // Bad pattern
    // ...
}

// GOOD: State extractor
#[derive(Clone)]
struct AppState {
    db: PgPool,
    cache: Arc<Cache>,
    config: Arc<Config>,
}

async fn get_user(
    State(state): State<AppState>,
    Path(id): Path<i32>,
) -> Result<Json<User>, AppError> {
    let user = sqlx::query_as!(User, "SELECT * FROM users WHERE id = $1", id)
        .fetch_one(&state.db)
        .await?;
    Ok(Json(user))
}

// BAD: std::sync::Mutex in async
struct AppState {
    cache: std::sync::Mutex<HashMap<String, Value>>,  // Blocks!
}

// GOOD: tokio Mutex or RwLock
struct AppState {
    cache: tokio::sync::RwLock<HashMap<String, Value>>,
}

async fn get_cached(
    State(state): State<AppState>,
    Path(key): Path<String>,
) -> Result<Json<Value>, AppError> {
    let cache = state.cache.read().await;
    cache.get(&key).cloned().ok_or(AppError::NotFound)
}
```

### Error Handling
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Panic in handler | Return Result | CRITICAL |
| No IntoResponse impl | Implement for errors | HIGH |
| Leaking internal errors | Map to HTTP errors | HIGH |

```rust
// GOOD: Custom error type with IntoResponse
#[derive(Debug)]
enum AppError {
    NotFound,
    Unauthorized,
    Validation(String),
    Internal(anyhow::Error),
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, message) = match self {
            AppError::NotFound => (StatusCode::NOT_FOUND, "Not found"),
            AppError::Unauthorized => (StatusCode::UNAUTHORIZED, "Unauthorized"),
            AppError::Validation(msg) => {
                return (StatusCode::BAD_REQUEST, Json(json!({
                    "error": "validation_error",
                    "message": msg,
                }))).into_response();
            }
            AppError::Internal(err) => {
                tracing::error!("Internal error: {:?}", err);
                (StatusCode::INTERNAL_SERVER_ERROR, "Internal server error")
            }
        };

        (status, Json(json!({ "error": message }))).into_response()
    }
}

// Implement From for automatic conversion
impl From<sqlx::Error> for AppError {
    fn from(err: sqlx::Error) -> Self {
        match err {
            sqlx::Error::RowNotFound => AppError::NotFound,
            _ => AppError::Internal(err.into()),
        }
    }
}
```

### Middleware (Tower)
| Check | Recommendation | Severity |
|-------|----------------|----------|
| No tracing | Add TraceLayer | MEDIUM |
| No timeout | Add TimeoutLayer | MEDIUM |
| Auth in handler | Use middleware | MEDIUM |

```rust
use tower::ServiceBuilder;
use tower_http::{
    trace::TraceLayer,
    timeout::TimeoutLayer,
    cors::CorsLayer,
};

fn app(state: AppState) -> Router {
    Router::new()
        .nest("/api", api_routes())
        .layer(
            ServiceBuilder::new()
                .layer(TraceLayer::new_for_http())
                .layer(TimeoutLayer::new(Duration::from_secs(30)))
                .layer(CorsLayer::permissive())
        )
        .with_state(state)
}

// GOOD: Auth middleware
async fn auth_middleware(
    State(state): State<AppState>,
    mut req: Request,
    next: Next,
) -> Result<Response, AppError> {
    let token = req
        .headers()
        .get(AUTHORIZATION)
        .and_then(|v| v.to_str().ok())
        .and_then(|v| v.strip_prefix("Bearer "))
        .ok_or(AppError::Unauthorized)?;

    let claims = validate_token(token, &state.jwt_secret)?;

    req.extensions_mut().insert(claims);
    Ok(next.run(req).await)
}

// Apply to routes
let protected = Router::new()
    .route("/me", get(get_me))
    .route_layer(middleware::from_fn_with_state(state.clone(), auth_middleware));
```

### Actix-web Patterns
```rust
// Actix-web equivalent
use actix_web::{web, App, HttpServer, HttpResponse};

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let pool = create_pool().await;

    HttpServer::new(move || {
        App::new()
            .app_data(web::Data::new(pool.clone()))
            .service(
                web::scope("/api/v1")
                    .service(
                        web::scope("/users")
                            .route("", web::get().to(list_users))
                            .route("", web::post().to(create_user))
                            .route("/{id}", web::get().to(get_user))
                    )
            )
            .wrap(actix_web::middleware::Logger::default())
    })
    .bind("127.0.0.1:8080")?
    .run()
    .await
}

// Actix handler
async fn create_user(
    pool: web::Data<PgPool>,
    req: web::Json<CreateUserRequest>,
) -> Result<HttpResponse, actix_web::Error> {
    let user = User::create(&pool, req.into_inner()).await?;
    Ok(HttpResponse::Created().json(user))
}
```

## Response Template
```
## Rust API Code Review Results

**Project**: [name]
**Framework**: Axum 0.7 | **Runtime**: Tokio

### Handler Organization
| Status | File | Issue |
|--------|------|-------|
| MEDIUM | main.rs | 30+ routes without nesting |

### Extractors
| Status | File | Issue |
|--------|------|-------|
| HIGH | handlers/user.rs:23 | Manual JSON parsing |

### State Management
| Status | File | Issue |
|--------|------|-------|
| CRITICAL | state.rs | std::sync::Mutex in async context |

### Error Handling
| Status | File | Issue |
|--------|------|-------|
| HIGH | handlers/product.rs | No IntoResponse for errors |

### Recommended Actions
1. [ ] Organize routes with Router::nest
2. [ ] Use Json extractor with validation
3. [ ] Replace std Mutex with tokio Mutex
4. [ ] Implement IntoResponse for AppError
```

## Best Practices
1. **Extractors**: Use typed extractors, body last
2. **State**: Clone-friendly, async-safe
3. **Errors**: Custom type with IntoResponse
4. **Middleware**: Tower layers for cross-cutting
5. **Tracing**: Use tracing crate for observability

## Integration
- `rust-reviewer`: General Rust patterns
- `security-scanner`: API security audit
- `perf-analyzer`: Async performance
