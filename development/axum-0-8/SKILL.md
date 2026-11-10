---
name: axum-0-8
description: Builds, upgrades and reviews Rust HTTP services on axum 0.8 (checked against axum 0.8.9, tokio 1.54, hyper 1.12, tower-http 0.7). Covers the 0.7 to 0.8 changes ({id} and {*rest} paths, extractors without #[async_trait], OptionalFromRequestParts), the silent defaults that ship bugs (the 2 MB DefaultBodyLimit that RequestBodyLimitLayer does not raise, plain-text extractor rejections with 400/413/415/422, layers that skip later routes, Query with repeated keys), one JSON error type for every failure path without leaking internals, handler futures that are dropped on client disconnect or timeout (cleanup after .await never runs), graceful shutdown with SIGTERM and a drain deadline, and testing with tower::ServiceExt::oneshot. Use when writing or reviewing axum handlers, extractors, middleware, error types, upload or body-limit code, per-key limits, timeouts, background tasks or shutdown in a tokio service, when bumping axum from 0.6/0.7, or when you see "Path segments must not start with `:`", "length limit exceeded" or text/plain errors from a JSON API.
license: MIT
---

# axum 0.8 services

axum **0.8.9** is the current release (November 2026), on tokio 1.54, hyper 1.12, tower 0.5 and
tower-http 0.7. Most axum code on the web and in training data is 0.6 or 0.7. Everything below was
checked against those versions on Rust 1.99, and the behaviour claims were reproduced by running
them (see [references/sources.md](references/sources.md)).

## 1. Check what the project runs

```sh
cargo tree -i axum --depth 0          # the axum version this crate builds with
cargo tree -e features -i axum        # which axum features are enabled
```

| Found | Write |
| --- | --- |
| `axum 0.8.x` | this skill |
| `axum 0.7.x` | `/:id` paths and `#[async_trait]` extractors are still right there; plan the upgrade with [references/migration-0-7-to-0-8.md](references/migration-0-7-to-0-8.md) |
| axum from git `main` | unreleased 0.9 work: `serve` output type, default `header_read_timeout`, `tower-log` no longer default. Read the CHANGELOG |

`#[derive(FromRequest)]`, `#[derive(FromRef)]` and `#[debug_handler]` need the `macros` feature,
which is **not** a default. In an offline or vendored build you can only use features already
enabled in `Cargo.toml`; check before reaching for one.

## 2. 0.7 → 0.8: loud changes

These fail at compile time, when the router is built, or on the first request to the route, so
tests catch them. Fix them all at once.

| 0.7 code | On 0.8.9 | Write |
| --- | --- | --- |
| `.route("/users/:id", ..)` | panics: ``Path segments must not start with `:`. For capture groups, use `{capture}`...`` | `"/users/{id}"` |
| `.route("/files/*path", ..)` | panics: ``Path segments must not start with `*`. For wildcard capture, use `{*wildcard}`...`` | `"/files/{*path}"` |
| `#[async_trait] impl FromRequestParts<S> for X` | lifetime mismatch errors; `axum::async_trait` no longer exists | plain `impl` with `async fn from_request_parts` (section 6) |
| `Option<MyExtractor>` | trait bound error | also implement `OptionalFromRequestParts` / `OptionalFromRequest` |
| `Option<Query<T>>` | not implemented | `Query<T>` with `Option` fields, or `axum_extra::extract::OptionalQuery` |
| `axum::extract::Host` | not found | `axum_extra::extract::Host` |
| handler or service that is `Send` but not `Sync` | trait bound error | make it `Sync` (wrap state in `Arc<Mutex<..>>`, not `RefCell`) |
| `Path<(A, B)>` with a different number of captures | 500 at runtime | tuple length must equal the number of captures |
| `ws::Message::Text(String)` / `Binary(Vec<u8>)` | type errors | `Utf8Bytes` / `Bytes`: `Message::Text("hi".into())` |
| `serve(..).tcp_nodelay(true)` | method gone | `listener.tap_io(\|tcp\| { let _ = tcp.set_nodelay(true); })` via `axum::serve::ListenerExt` |

Literal colons or asterisks in a path need `Router::without_v07_checks()`.

## 3. Silent behaviours that ship bugs

Nothing fails until the request that hits them. Tests that only cover the happy path pass.

| You write | What axum 0.8.9 actually does |
| --- | --- |
| `RequestBodyLimitLayer::new(15 << 20)` and a `Bytes`/`Json`/`String`/`Form` extractor | bodies over **2 MB** still get 413. Extractors enforce `DefaultBodyLimit` (2,097,152 bytes) on their own; the tower-http layer can only lower the limit. Use `DefaultBodyLimit::max(n)` (section 5) |
| `DefaultBodyLimit::max(64 << 10)` on the router and another on one route | the innermost one wins: the route-level layer overrides the router-level one, in both directions |
| `body: Body` or `req: Request` as the extractor | **no limit at all**: `DefaultBodyLimit` does not apply. Cap it yourself (`axum::body::to_bytes(body, max)`) or add `RequestBodyLimitLayer` |
| `Json<T>` in a JSON API | rejections are **text/plain**: 415 (no or non-JSON content type), 400 (syntax, empty body, trailing characters), 422 (wrong fields or types), 413 (too large). Your error type never sees them unless you route them through it (section 4) |
| `Path<u64>` | `/items/abc` is a 400 text/plain `Invalid URL: Cannot parse ...` before your handler runs |
| `Query<Filter>` with `tags: Vec<String>` | `?tags=a&tags=b` (and even `?tags=a`) is a 400: `serde_urlencoded` can't build sequences. Use `Query<Vec<(String, String)>>` or `axum_extra::extract::Query` (feature `query`) |
| unmatched path / wrong method | 404 / 405 with an **empty body**; the 405 carries `Allow` |
| `.layer(auth)` then `.route("/admin/x", ..)` | the later route is **not** behind `auth`: `layer` wraps only routes added before it |
| `.layer(auth)` on the whole router | unknown paths answer 401 instead of 404 (the middleware runs for unmatched requests). `route_layer` runs only on matched routes |
| `Option<Json<T>>` | no content type gives `None`, but malformed JSON with a JSON content type is still a 400 rejection |
| a handler that panics | the connection is dropped with no response, unless `tower_http::catch_panic::CatchPanicLayer` is installed (then 500 `Service panicked`) |
| `cleanup()` after an `.await` in a handler | skipped whenever the client disconnects or a timeout fires: the handler future is dropped (section 7) |
| `with_graceful_shutdown(signal)` | waits for every in-flight response **forever**, including streams; stops accepting, closes idle keep-alive connections. Add a drain deadline (section 8) |
| `tokio::signal::ctrl_c()` as the shutdown signal | containers and Kubernetes send SIGTERM. Without a handler the process is killed mid-request (as PID 1 it ignores SIGTERM and gets SIGKILL after the grace period) |

## 4. One error type for every failure path

A JSON API has five sources of errors: your handlers, extractor rejections, unmatched paths,
unmatched methods and panics. Route all five through one type.

```rust
use axum::{
    Json, Router,
    extract::{FromRequest, rejection::JsonRejection},
    http::StatusCode,
    response::{IntoResponse, Response},
};
use serde_json::json;

#[derive(Debug, thiserror::Error)]
pub enum HttpError {
    #[error("booking {0} not found")]
    NotFound(u64),
    #[error("{0}")]
    Invalid(String),
    #[error(transparent)]
    Rejected(#[from] JsonRejection),
    #[error("internal error")]
    Internal(#[from] anyhow::Error),
}

impl IntoResponse for HttpError {
    fn into_response(self) -> Response {
        let (status, code, message) = match &self {
            HttpError::NotFound(_) => (StatusCode::NOT_FOUND, "not_found", self.to_string()),
            HttpError::Invalid(m) => (StatusCode::UNPROCESSABLE_ENTITY, "invalid", m.clone()),
            // Keep axum's status (400/413/415/422); its text is about the client's input.
            HttpError::Rejected(r) => (r.status(), "bad_request", r.body_text()),
            HttpError::Internal(err) => {
                tracing::error!(error = format!("{err:#}"), "request failed"); // log the chain
                (StatusCode::INTERNAL_SERVER_ERROR, "internal", "internal server error".into())
            }
        };
        (status, Json(json!({ "error": { "code": code, "message": message } }))).into_response()
    }
}

/// `Json<T>` whose rejection is `HttpError` (needs the `macros` feature).
#[derive(FromRequest)]
#[from_request(via(axum::Json), rejection(HttpError))]
pub struct Payload<T>(pub T);

pub fn routes(router: Router) -> Router {
    router
        .fallback(|| async {
            (StatusCode::NOT_FOUND, Json(json!({ "error": { "code": "not_found" } })))
        })
        .method_not_allowed_fallback(|| async {
            (StatusCode::METHOD_NOT_ALLOWED, Json(json!({ "error": { "code": "method_not_allowed" } })))
        }) // axum keeps the Allow header on this response
}
```

- Never put `err.to_string()` of a driver, I/O or `anyhow` error in a response. The official
  axum `anyhow` example returns `format!("Something went wrong: {}", self.0)`; copying it leaks
  connection strings, user names and SQL. Log the chain (`{:#}`), return a generic message.
- Need to tell rejection kinds apart? Match the variants: `JsonDataError` (422),
  `JsonSyntaxError` (400), `MissingJsonContentType` (415), `BytesRejection` (413 when over the
  limit, check `.status()`). The enum is `#[non_exhaustive]`: keep a `_` arm.
- Without the `macros` feature, take `body: Result<Json<T>, JsonRejection>` and map it, or use
  `axum_extra::extract::WithRejection<Json<T>, HttpError>` (feature `with-rejection`). Same for
  `QueryRejection`, `PathRejection`, `FormRejection`.
- A `map_response` middleware that rewrites empty 404/405 bodies is fine for the fallbacks, but
  it can't tell a JSON syntax error from a bad query string (both 400): map rejections by type.
- `CatchPanicLayer::custom(|_| ...)` returns your JSON 500 for panics. Don't echo the panic message.

Full rejection table and patterns: [references/errors-and-rejections.md](references/errors-and-rejections.md).

## 5. Body limits

```rust
use axum::{Router, extract::DefaultBodyLimit, routing::{post, put}};
use tower_http::limit::RequestBodyLimitLayer;

let json_api = Router::new()
    .route("/v1/bookings", post(create_booking))
    .layer(RequestBodyLimitLayer::new(64 * 1024)); // or DefaultBodyLimit::max(64 * 1024)

let uploads = Router::new()
    .route("/v1/rooms/{room_id}/floorplan", put(upload_floorplan)) // takes `Bytes`
    .layer(DefaultBodyLimit::max(25 * 1024 * 1024)); // raises the 2 MB extractor default

let app = json_api.merge(uploads);
```

- `DefaultBodyLimit::max(n)` raises or lowers the limit for `Bytes`, `String`, `Json`, `Form` and
  `Multipart`, and it holds for chunked bodies with no `Content-Length` (measured).
- `RequestBodyLimitLayer::new(n)` rejects a too-large `Content-Length` up front and caps streamed
  bodies, for every extractor including raw `Body`. It never raises the extractor default.
- To stream a large body without buffering: `DefaultBodyLimit::disable()` plus
  `RequestBodyLimitLayer::new(max)` on that route, and read `Body` frame by frame.
- A limit applied with `.layer` after the merge covers the merged upload route too. Put the JSON
  limit on the JSON router before merging (as above), or on each `MethodRouter` (`post(h).layer(..)`).

## 6. State and extractors

- `Router::new()...with_state(state)`; handlers take `State<AppState>`. `axum::serve` only accepts
  a `Router<()>`, so a forgotten `.with_state` is a compile error at the `serve` call.
- Substates: `#[derive(Clone, FromRef)]` on the app state, then `State<PgPool>` in a handler.
  `Extension<T>` still works but fails at runtime (500) when the layer is missing; prefer `State`.
- Shared mutable data: `Arc<std::sync::Mutex<T>>` when the lock is never held across `.await`
  (the compiler rejects a std guard held across `.await` in a handler, because the future must be
  `Send`). `tokio::sync::Mutex` only when you must hold it across `.await`, and never across
  slow work: that serializes every request.
- The body extractor (`Json`, `Bytes`, `String`, `Form`, `Request`) must be the **last** argument.
- Custom extractors are native async traits now:

```rust
use axum::{extract::{FromRequestParts, OptionalFromRequestParts}, http::{StatusCode, request::Parts}};

pub struct Caller { pub tenant: String }

impl<S: Send + Sync> FromRequestParts<S> for Caller {
    type Rejection = StatusCode;
    async fn from_request_parts(parts: &mut Parts, _: &S) -> Result<Self, Self::Rejection> {
        let tenant = parts.headers.get("x-tenant").and_then(|v| v.to_str().ok());
        tenant.map(|t| Caller { tenant: t.to_owned() }).ok_or(StatusCode::UNAUTHORIZED)
    }
}

// Needed for `Option<Caller>`: decide what "absent" means instead of swallowing every error.
impl<S: Send + Sync> OptionalFromRequestParts<S> for Caller {
    type Rejection = StatusCode;
    async fn from_request_parts(parts: &mut Parts, s: &S) -> Result<Option<Self>, Self::Rejection> {
        if !parts.headers.contains_key("x-tenant") { return Ok(None); }
        <Self as FromRequestParts<S>>::from_request_parts(parts, s).await.map(Some)
    }
}
```

## 7. Cancellation: a handler can stop at any `.await`

When the client disconnects, hyper **drops** the handler future; `TimeoutLayer` drops it when the
timeout fires; `tokio::select!` drops the losing branches. Code after the pending `.await` never
runs. Reproduced on 0.8.9: closing the TCP connection (even a half-close) and `TimeoutLayer` both
dropped the handler, and a counter decremented after the `.await` stayed incremented.

- **Release in `Drop`, not after `.await`.** Counters, slots, locks in external systems, "in
  progress" flags: hold a guard whose `Drop` releases them. It runs on success, on `?` early
  returns, on panic unwinding and on cancellation.
- Per-key concurrency limits: `tokio::sync::Semaphore` per key and
  `semaphore.try_acquire_owned()`; the `OwnedSemaphorePermit` is the guard. Or a counter map with
  a guard type (below). Drop map entries when they reach zero, or the map grows with every key.
- `let _ = limiter.try_acquire(..)` drops the guard **immediately**. Bind it: `let _permit = ...`.
- Work that must finish even if the client leaves (charging a card, writing an audit record):
  `tokio::spawn` it (or `TaskTracker::spawn`) and await the `JoinHandle`. Work that should stop
  when the client leaves (a search, a preview render): keep it in the handler future.
- In `select!` loops, only use cancel-safe operations as branches (`mpsc::Receiver::recv`,
  `TcpListener::accept`, `CancellationToken::cancelled`); `read_exact`, `read_to_end` or a
  half-finished write lose data when the other branch wins.

```rust
use std::{collections::HashMap, sync::{Arc, Mutex}};

#[derive(Clone, Default)]
pub struct KeyedLimiter { inner: Arc<Mutex<HashMap<String, usize>>> }

pub struct LimitGuard { key: String, inner: Arc<Mutex<HashMap<String, usize>>> }

impl KeyedLimiter {
    pub fn try_acquire(&self, key: &str, max: usize) -> Option<LimitGuard> {
        let mut map = self.inner.lock().unwrap();
        let n = map.entry(key.to_owned()).or_insert(0);
        if *n >= max { return None; } // check and increment under one lock: no race
        *n += 1;
        Some(LimitGuard { key: key.to_owned(), inner: self.inner.clone() })
    }
}

impl Drop for LimitGuard {
    fn drop(&mut self) {
        let mut map = self.inner.lock().unwrap();
        if let Some(n) = map.get_mut(&self.key) {
            *n -= 1;
            if *n == 0 { map.remove(&self.key); }
        }
    }
}
// In the handler:  let Some(_guard) = limiter.try_acquire(&tenant, 3) else { return busy() };
//                  render(&tenant).await   // _guard is released however this ends
```

## 8. Timeouts and graceful shutdown

```rust
use std::time::Duration;
use axum::http::StatusCode;
use tower_http::timeout::TimeoutLayer;

// TimeoutLayer::new is deprecated (tower-http 0.6.7+): say which status the client gets.
let app = app.layer(TimeoutLayer::with_status_code(StatusCode::SERVICE_UNAVAILABLE, Duration::from_secs(30)));
```

```rust
async fn shutdown_signal() {
    let ctrl_c = async { tokio::signal::ctrl_c().await.expect("install Ctrl+C handler") };
    #[cfg(unix)]
    let terminate = async {
        tokio::signal::unix::signal(tokio::signal::unix::SignalKind::terminate())
            .expect("install SIGTERM handler")
            .recv()
            .await;
    };
    #[cfg(not(unix))]
    let terminate = std::future::pending::<()>();
    tokio::select! { _ = ctrl_c => {}, _ = terminate => {} }
}

let token = tokio_util::sync::CancellationToken::new();   // tokio-util, for your own tasks
let server = axum::serve(listener, app)
    .with_graceful_shutdown({ let t = token.clone(); async move { shutdown_signal().await; t.cancel() } });
// Drain deadline: graceful shutdown alone waits for in-flight requests forever.
let drained = tokio::time::timeout(Duration::from_secs(25), async {
    server.await?;          // io::Result<()> on 0.8.9
    tracker.close();        // tokio_util::task::TaskTracker (feature "rt") running background jobs
    tracker.wait().await;   // they watch `token.cancelled()` and finish their current item
    Ok::<_, std::io::Error>(())
}).await;
```

- Keep the drain deadline under the orchestrator's grace period (Kubernetes default 30 s).
- Long-lived responses (SSE, WebSocket, streaming downloads) keep graceful shutdown waiting; end
  them from the token (`token.cancelled()` in their stream) or rely on the deadline.
- `JoinSet` aborts its tasks when dropped; `tokio::spawn` tasks are killed mid-await when the
  runtime shuts down. Track anything that must finish.

Details, including slow-client body timeouts: [references/limits-timeouts-cancellation.md](references/limits-timeouts-cancellation.md).

## 9. Testing

`tower::ServiceExt::oneshot` (tower feature `util`) runs a request through the router in-process.
Simulate a disconnect by spawning the request and calling `abort()` on the handle; test timeouts
with `#[tokio::test(start_paused = true)]` (tokio feature `test-util`), which jumps the clock while
everything is waiting. [references/testing.md](references/testing.md) has helpers for JSON
requests, chunked bodies and blocked fakes.

## Review checklist

- [ ] Paths use `{name}` / `{*rest}`; no `#[async_trait]` on axum extractor impls.
- [ ] Every error path returns the API's error shape: handler errors, `Json`/`Query`/`Path`
      rejections, `fallback`, `method_not_allowed_fallback` (keeps `Allow`), panics.
- [ ] No internal error text in responses; errors are logged with their source chain.
- [ ] Each route's body limit is what the product needs: `DefaultBodyLimit` for extractor limits
      above 2 MB, `RequestBodyLimitLayer` or `to_bytes(body, max)` for raw `Body`.
- [ ] Layers added after all routes they must cover; auth via `route_layer` where 404s matter.
- [ ] Resources released in `Drop` guards, not after `.await`; guards bound to a named variable.
- [ ] Limits check and increment under one lock; per-key maps shrink.
- [ ] Timeouts with an explicit status; graceful shutdown on SIGTERM and Ctrl+C with a deadline;
      background tasks tracked and cancelled.
- [ ] Tests cover rejections, oversize and chunked bodies, unknown paths and methods, and dropped
      requests, not only the happy path.

## Anti-patterns

- `(StatusCode::INTERNAL_SERVER_ERROR, err.to_string())` → leaks internals. Log, return generic.
- `.layer(RequestBodyLimitLayer::new(50 << 20))` to "allow big uploads" → still 413 above 2 MB.
- `counter += 1; work().await; counter -= 1;` → leaks a slot on every disconnect or timeout.
- `let _ = semaphore.try_acquire_owned()?` → the permit is gone before the work starts.
- Holding a `tokio::sync::Mutex` guard across the slow call → every request waits in line.
- `.route("/v1/x/:id", ..)` copied from 0.7 docs → panics when the router is built.
- `Query<Vec<String>>` for repeated keys → 400 for every request.
- `with_graceful_shutdown(ctrl_c())` alone → SIGTERM kills in-flight requests; streams block exit.

## More

- [references/migration-0-7-to-0-8.md](references/migration-0-7-to-0-8.md): every breaking change, with greps.
- [references/errors-and-rejections.md](references/errors-and-rejections.md): rejection statuses and bodies, mapping patterns.
- [references/limits-timeouts-cancellation.md](references/limits-timeouts-cancellation.md): limit matrix, timeouts, shutdown, background tasks.
- [references/testing.md](references/testing.md): oneshot helpers, chunked bodies, paused time, disconnects.
- [references/sources.md](references/sources.md): documentation and the experiments behind each claim.
