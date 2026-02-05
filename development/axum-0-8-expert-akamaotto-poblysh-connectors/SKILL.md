---
name: axum-0-8-expert
description: Expert guidance for Axum 0.8.x web framework development in Rust. Use when working with Axum 0.8+, migrating from 0.7 to 0.8, or when users mention path parameter syntax issues, async_trait problems, or Option extractor changes.
version: 1.0.0
---

# Axum 0.8 Expert Skill

## Overview

This skill provides expert guidance for developing with Axum 0.8.x, the ergonomic and modular web framework built with Tokio, Tower, and Hyper. Axum 0.8 was released in January 2025 and includes several breaking changes from 0.7.

## Critical Breaking Changes from 0.7 to 0.8

### 1. Path Parameter Syntax Change (BREAKING - Affects Nearly All Users)

**Old Syntax (0.7):**
```rust
Router::new()
    .route("/users/:id", get(handler))
    .route("/files/*path", get(catch_all))
```

**New Syntax (0.8):**
```rust
Router::new()
    .route("/users/{id}", get(handler))
    .route("/files/{*path}", get(catch_all))
```

**Migration:**
- Replace `:param` with `{param}`
- Replace `*param` with `{*param}`
- This applies to ALL routes in your application
- The app will panic at startup if using old syntax, making it easy to catch

**Examples:**
```rust
// Single parameter
.route("/users/{user_id}", get(get_user))

// Multiple parameters
.route("/users/{user_id}/posts/{post_id}", get(get_post))

// Catch-all parameter
.route("/files/{*path}", get(serve_file))

// Extracting in handlers
async fn get_user(Path(user_id): Path<String>) { }
async fn get_post(Path((user_id, post_id)): Path<(String, String)>) { }
```

### 2. `async_trait` Macro Removal (BREAKING)

Rust now has native support for async trait methods (RPITIT - Return Position Impl Trait In Traits), so the `#[async_trait]` macro is no longer needed.

**Migration:**
```rust
// OLD (0.7)
use axum::async_trait;

#[async_trait]
impl<S> FromRequestParts<S> for MyExtractor
where
    S: Send + Sync,
{
    type Rejection = MyRejection;
    
    async fn from_request_parts(
        parts: &mut Parts,
        state: &S,
    ) -> Result<Self, Self::Rejection> {
        // ...
    }
}

// NEW (0.8)
use async_trait::async_trait; // Use this if you still need it elsewhere

impl<S> FromRequestParts<S> for MyExtractor
where
    S: Send + Sync,
{
    type Rejection = MyRejection;
    
    async fn from_request_parts(
        parts: &mut Parts,
        state: &S,
    ) -> Result<Self, Self::Rejection> {
        // ...
    }
}
```

**Important:**
- Remove `#[async_trait]` from custom `FromRequestParts` and `FromRequest` implementations
- If you need `async_trait` for other traits, import it from the `async-trait` crate directly
- Add `async-trait = "0.1"` to your `Cargo.toml` if needed

### 3. `Option<T>` Extractor Behavior Change (BREAKING)

Previously, `Option<T>` would silently swallow ANY rejection and return `None`. Now it requires `T` to implement `OptionalFromRequestParts` or `OptionalFromRequest`.

**Old Behavior (0.7):**
```rust
// This would ALWAYS succeed, even if token was invalid
async fn handler(user: Option<AuthenticatedUser>) {
    match user {
        Some(user) => // authenticated
        None => // could be missing OR invalid token
    }
}
```

**New Behavior (0.8):**
```rust
// This can now fail if the token is invalid
async fn handler(user: Option<AuthenticatedUser>) -> Result<Response, StatusCode> {
    match user {
        Some(user) => // authenticated with valid token
        None => // missing token (but would return error for invalid token)
    }
}
```

**Migration Strategy:**

For extractors that should be truly optional (missing = None, invalid = error):
```rust
use axum::extract::rejection::OptionalFromRequestPartsError;

impl OptionalFromRequestParts<S> for AuthenticatedUser
where
    S: Send + Sync,
{
    type Rejection = OptionalFromRequestPartsError<MyRejection>;

    async fn from_request_parts(
        parts: &mut Parts,
        state: &S,
    ) -> Result<Option<Self>, Self::Rejection> {
        match Self::from_request_parts(parts, state).await {
            Ok(user) => Ok(Some(user)),
            Err(rejection) if rejection.is_missing() => Ok(None),
            Err(rejection) => Err(OptionalFromRequestPartsError::Inner(rejection)),
        }
    }
}
```

For truly optional behavior (ignore all rejections):
```rust
// Use Result instead
async fn handler(user: Result<AuthenticatedUser, AuthRejection>) {
    match user {
        Ok(user) => // authenticated
        Err(_) => // missing or invalid
    }
}
```

## Common Patterns and Best Practices

### Handler Signatures

**Multiple Extractors (Order Matters):**
```rust
async fn handler(
    Path(id): Path<String>,           // Path first
    State(state): State<AppState>,    // State second
    Query(params): Query<SearchParams>, // Query params
    Json(body): Json<CreateRequest>,  // Body last
) -> impl IntoResponse {
    // ...
}
```

**Optional Parameters:**
```rust
async fn handler(
    Path(id): Path<String>,
    pagination: Option<Query<Pagination>>,
) -> impl IntoResponse {
    let Query(pagination) = pagination.unwrap_or_default();
    // ...
}
```

### Path Parameters

**Struct-based (Recommended for multiple params):**
```rust
#[derive(Deserialize)]
struct UserParams {
    user_id: Uuid,
    team_id: Uuid,
}

async fn handler(Path(UserParams { user_id, team_id }): Path<UserParams>) {
    // ...
}

Router::new().route("/users/{user_id}/teams/{team_id}", get(handler))
```

**Tuple-based (Quick for 2-3 params):**
```rust
async fn handler(Path((user_id, team_id)): Path<(Uuid, Uuid)>) {
    // ...
}
```

**HashMap/Vec for dynamic parameters:**
```rust
use std::collections::HashMap;

async fn handler(Path(params): Path<HashMap<String, String>>) {
    // All path parameters as key-value pairs
}
```

### State Management

```rust
#[derive(Clone)]
struct AppState {
    db: PgPool,
    redis: RedisClient,
}

let state = AppState { db, redis };

let app = Router::new()
    .route("/", get(handler))
    .with_state(state);

async fn handler(State(state): State<AppState>) -> impl IntoResponse {
    // Access state.db, state.redis
}
```

### Error Handling

**Custom Rejection Types:**
```rust
use axum::{
    response::{IntoResponse, Response},
    http::StatusCode,
};

struct MyError(anyhow::Error);

impl IntoResponse for MyError {
    fn into_response(self) -> Response {
        (
            StatusCode::INTERNAL_SERVER_ERROR,
            format!("Error: {}", self.0),
        ).into_response()
    }
}

impl<E> From<E> for MyError
where
    E: Into<anyhow::Error>,
{
    fn from(err: E) -> Self {
        Self(err.into())
    }
}

async fn handler() -> Result<Json<Response>, MyError> {
    let data = fetch_data().await?;
    Ok(Json(data))
}
```

## Migration Checklist from 0.7 to 0.8

1. **Update `Cargo.toml`:**
```toml
[dependencies]
axum = "0.8"
tokio = { version = "1.0", features = ["full"] }
# Add if you use async_trait elsewhere:
async-trait = "0.1"
```

2. **Update all route paths:**
   - Search and replace: `/:` → `/{` and add closing `}`
   - Search and replace: `/*` → `/{*`

3. **Remove `#[async_trait]` from extractors:**
   - Find all `impl FromRequestParts` and `impl FromRequest`
   - Remove the `#[async_trait]` attribute
   - Change imports from `use axum::async_trait;` to `use async_trait::async_trait;` if needed elsewhere

4. **Review `Option<T>` extractors:**
   - Identify where you use `Option<CustomExtractor>`
   - Determine if you want errors to propagate or be ignored
   - Implement `OptionalFromRequestParts` if needed

5. **Test all routes:**
   - The app will panic on startup with old path syntax
   - Test edge cases with optional extractors

## Common Gotchas

### 1. Nested Routers and Fallbacks
```rust
// In 0.8, fallback behavior with nested routers may differ
// Test your fallback routes carefully after migration
let api = Router::new()
    .route("/users", get(users))
    .fallback(api_fallback);

let app = Router::new()
    .nest("/api", api)
    .fallback(app_fallback);
```

### 2. Service vs Handler
```rust
// get_service is removed in favor of more specific methods
// OLD: .route("/assets/*path", get_service(ServeDir::new("assets")))
// NEW: Use fallback_service or route_service
.route_service("/assets/*path", ServeDir::new("assets"))
```

### 3. Body Types
Axum 0.8 works with `http-body 1.0`. Ensure your body types are compatible.

### 4. Query/Form Validation
```rust
use validator::Validate;

#[derive(Deserialize, Validate)]
struct SearchQuery {
    #[validate(length(min = 1, max = 100))]
    q: String,
    #[validate(range(min = 1, max = 100))]
    limit: Option<u32>,
}

async fn search(Query(query): Query<SearchQuery>) -> Result<Json<Results>, StatusCode> {
    query.validate().map_err(|_| StatusCode::BAD_REQUEST)?;
    // ...
}
```

## Recommended Dependencies (Axum 0.8 Compatible)

```toml
[dependencies]
axum = "0.8"
tokio = { version = "1.0", features = ["full"] }
tower = "0.5"
tower-http = { version = "0.6", features = ["trace", "cors"] }
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"

# Database
sqlx = { version = "0.8", features = ["runtime-tokio-rustls", "postgres"] }

# Validation
validator = { version = "0.18", features = ["derive"] }

# UUID & Time
uuid = { version = "1.0", features = ["v4", "serde"] }
chrono = { version = "0.4", features = ["serde"] }

# Tracing
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter"] }
```

## Performance Tips

1. **Use `State` efficiently:**
   - Clone is cheap for `Arc<T>` wrapped state
   - Consider using `Arc<AppState>` directly in your state

2. **Avoid unnecessary cloning:**
   ```rust
   // Good: Use references where possible
   async fn handler(State(state): State<Arc<AppState>>) {
       // state is Arc, cloning is cheap
   }
   ```

3. **Use middleware wisely:**
   ```rust
   use tower_http::trace::TraceLayer;
   
   let app = Router::new()
       .route("/", get(handler))
       .layer(TraceLayer::new_for_http());
   ```

## Testing

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use axum::http::{Request, StatusCode};
    use tower::ServiceExt;

    #[tokio::test]
    async fn test_route() {
        let app = app();
        
        let response = app
            .oneshot(
                Request::builder()
                    .uri("/users/123")
                    .body(Body::empty())
                    .unwrap(),
            )
            .await
            .unwrap();

        assert_eq!(response.status(), StatusCode::OK);
    }
}
```

## When to Use This Skill

- Writing new Axum 0.8 applications
- Migrating from Axum 0.7 to 0.8
- Debugging path parameter issues
- Implementing custom extractors
- Handling optional authentication
- Setting up proper error handling
- Understanding breaking changes

## Additional Resources

- Official Announcement: https://tokio.rs/blog/2025-01-01-announcing-axum-0-8-0
- Axum Documentation: https://docs.rs/axum/latest/axum/
- Changelog: https://github.com/tokio-rs/axum/blob/main/axum/CHANGELOG.md
- Examples: https://github.com/tokio-rs/axum/tree/main/examples
