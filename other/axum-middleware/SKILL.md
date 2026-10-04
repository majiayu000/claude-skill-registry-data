---
name: axum-middleware
description: Adds authentication, logging, or other middleware to Axum routes that uses injected services. Use when middleware needs access to injectable services like AuthService, LoggingService, or rate limiters.
---

# Axum Middleware with injectable

## Auth middleware via custom extractor (recommended)

```rust
use axum::{async_trait, extract::FromRequestParts, http::{request::Parts, StatusCode}};
use injectable::prelude::*;

struct Authenticated { user_id: i64, email: String }

#[async_trait]
impl FromRequestParts<AxumState> for Authenticated {
    type Rejection = (StatusCode, String);

    async fn from_request_parts(
        parts: &mut Parts,
        state: &AxumState,
    ) -> Result<Self, Self::Rejection> {
        let token = parts.headers
            .get("authorization")
            .and_then(|v| v.to_str().ok())
            .and_then(|v| v.strip_prefix("Bearer "))
            .ok_or((StatusCode::UNAUTHORIZED, "missing token".into()))?;

        let ctx  = state.resolve_context();
        let auth: Inject<AuthService> = Inject::extract(ctx).await
            .map_err(|_| (StatusCode::INTERNAL_SERVER_ERROR, "auth unavailable".into()))?;

        auth.verify_token(token).await
            .map(|(user_id, email)| Authenticated { user_id, email })
            .map_err(|_| (StatusCode::UNAUTHORIZED, "invalid token".into()))
    }
}

// Use in handlers:
async fn get_profile(auth: Authenticated, Inject(users): Inject<UserService>) -> impl IntoResponse {
    users.get(auth.user_id).await
}
```

## Tower middleware layer

```rust
use axum::middleware::{self, Next};
use axum::response::Response;

async fn logging_middleware(
    State(state): State<AxumState>,
    request: axum::extract::Request,
    next: Next,
) -> Response {
    let ctx = state.resolve_context();
    if let Ok(logger) = Inject::<LoggingService>::extract(ctx).await {
        logger.log_request(&request).await;
    }
    next.run(request).await
}

// Apply to router:
let app = Router::new()
    .route("/api/users", get(list_users))
    .layer(middleware::from_fn_with_state(state.clone(), logging_middleware))
    .with_state(state);
```

## Rate limiting via injected service

```rust
async fn rate_limit_middleware(
    State(state): State<AxumState>,
    request: axum::extract::Request,
    next: Next,
) -> Response {
    let ctx     = state.resolve_context();
    let limiter: Inject<RateLimiter> = ctx.extract().await.unwrap();
    let ip      = /* extract IP */;

    if !limiter.allow(ip).await {
        return (StatusCode::TOO_MANY_REQUESTS, "rate limit exceeded").into_response();
    }
    next.run(request).await
}
```

See [guides/09-axum-middleware.md](../../guides/09-axum-middleware.md).
