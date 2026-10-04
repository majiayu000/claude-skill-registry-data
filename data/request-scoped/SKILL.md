---
name: request-scoped
description: Implements per-request dependency injection with RequestScoped scope. Use when a service needs one instance per HTTP request, like database transactions or request-specific state.
---

# Request-Scoped Dependencies

`RequestScoped` creates a fresh instance for each HTTP request when used with Axum's `Inject<T>` extractor.

## Basic pattern

```rust
use injectable::prelude::*;

#[injectable(scope = RequestScoped)]
pub struct RequestContext {
    request_id: String,
}

#[injectable]
impl RequestContext {
    #[injectable(ctor)]
    fn new() -> Self {
        Self {
            request_id: std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .unwrap()
                .as_nanos()
                .to_string(),
        }
    }

    pub fn begin(&self) {
        println!("Starting request {}", self.request_id);
    }
}
```

## With Axum handler

```rust
async fn create_user(
    Inject(ctx): Inject<RequestContext>,  // fresh RequestContext per request
    Json(body): Json<CreateUser>,
) -> impl IntoResponse {
    ctx.begin();
    // ctx.request_id is unique to this request
}
```

## Request context propagation

The Axum `FromRequestParts` impl creates a per-request `ResolveContext`:

```rust
// Each Inject<RequestContext> in a handler gets a fresh RequestContext
async fn handler_a(ctx: Inject<RequestContext>) {
    println!("Request A: {}", ctx.request_id);
}

async fn handler_b(ctx: Inject<RequestContext>) {
    println!("Request B: {}", ctx.request_id);
}
```

## Shared request-scoped data

```rust
#[injectable(scope = RequestScoped)]
pub struct RequestContext {
    pub user_id: Option<i64>,
    pub trace_id: String,
    pub start_time: std::time::Instant,
}

#[injectable]
impl RequestContext {
    #[injectable(ctor)]
    fn new() -> Self {
        Self {
            user_id: None,
            trace_id: std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .unwrap()
                .as_nanos()
                .to_string(),
            start_time: std::time::Instant::now(),
        }
    }
}

async fn handler(ctx: Inject<RequestContext>) {
    println!("[{trace_id}] Request started", trace_id = ctx.trace_id);
}
```

## Scoping vs Transient

| Scope | Instance per | Use when |
|---|---|---|
| `Singleton` | Container (one per app) | DB pools, caches, config |
| `Transient` | Manual resolution | Loggers with IDs, per-call factories |
| `RequestScoped` | HTTP request (via Axum) | Transactions, per-request state |

## Pre-populating request context

```rust
use axum::{async_trait, extract::FromRequestParts, http::request::Parts};

struct AuthenticatedUser { user_id: i64 }

#[async_trait]
impl FromRequestParts<AxumState> for AuthenticatedUser {
    type Rejection = StatusCode;

    async fn from_request_parts(parts: &mut Parts, state: &AxumState) -> Result<Self, StatusCode> {
        let user_id = /* extract from auth header */;
        Ok(AuthenticatedUser { user_id })
    }
}

async fn handler(user: AuthenticatedUser, ctx: Inject<RequestContext>) {
    // user.user_id populated by extractor, ctx.user_id can be set manually
}
```

Request-scoped dependencies are ideal for anything that should exist once per
HTTP request — transactions, logging context, tenant isolation, and auth data.
