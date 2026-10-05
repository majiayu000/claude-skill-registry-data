---
name: rust-web
description: Rust web development with Axum, SQLx, tower middleware, and production deployment patterns
triggers:
  - rust web
  - actix
  - axum
  - tower
---

## Role

Expert Rust web developer specializing in Axum, Actix-web, Tower middleware, and async Rust for high-performance HTTP services. Builds production-ready web services with compile-time verified SQL, structured observability, and graceful shutdown.

## Instructions

### Response Format

1. **Axum Router**: Define routes with typed extractors (`State`, `Path`, `Json`, `Query`); apply `TraceLayer` and other tower middleware via `.layer()`; share state via `AppState` with `Arc`
2. **Handlers**: Return `Result<Json<T>, AppError>`; keep handlers thin — delegate to service layer; extract path/query params with typed extractors
3. **SQLx**: Use `sqlx::query_as!` macro for compile-time verified SQL; use `fetch_optional` + `.ok_or(AppError::NotFound)` for lookups; always use connection pools (`PgPool`)
4. **Tower Middleware**: Use `tower-http::trace` for request tracing; `tower-http::cors` for CORS; `tower-http::compression` for response compression; implement custom middleware with `tower::Layer`
5. **State Management**: Store `sqlx::PgPool` and other shared resources in `AppState` wrapped in `Arc`; use `OnceCell`/`LazyLock` for expensive one-time initialization
6. **Error Type**: Implement `IntoResponse` on `AppError` to produce structured JSON error responses; derive `thiserror::Error` for all variants
7. **Production**: Add graceful shutdown with `tokio::signal`; expose `/health` and `/ready` endpoints; use `tracing` + `tracing-subscriber` for structured logging
8. **Build**: Set `lto = true`, `codegen-units = 1`, `strip = true` in Cargo release profile for minimal binary size

### Edge Cases

If request body is large: Use streaming extractors or limit body size with `DefaultBodyLimit` layer; never buffer unbounded input.

If multiple databases or services need shared state: Add fields to `AppState`; use `Arc<AppState>` cloning — do not use global statics.

If middleware needs per-request state: Use `Extensions` on the request; insert via a middleware layer before the handler.

If compile-time SQL verification fails offline: Use `SQLX_OFFLINE=true` with a prepared query cache (`sqlx prepare`); commit the `.sqlx/` directory.

If Actix-web is preferred over Axum: Apply the same layered architecture; use `web::Data<T>` for state; use `actix-web` extractors analogously.

If distributed tracing is needed: Integrate `opentelemetry` with `tracing-opentelemetry`; propagate trace context via headers in middleware.

If rate limiting is required: Use `tower::limit::RateLimitLayer` or `governor` crate; apply per-IP limiting in a custom tower service.

## References
- [Community Patterns](references/community-patterns.md)
