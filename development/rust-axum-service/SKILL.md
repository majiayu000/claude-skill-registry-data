---
name: rust-axum-service
category: architecture
description: Use when building or extending a Rust service - axum on tokio (or the repository's actix-web / rocket), typed errors with IntoResponse, serde at the boundary, sqlx queries and migrations, never blocking the runtime, tracing, clippy
tech_stack: Rust
---
# Rust Service (axum on tokio)

## Overview

Rust moves a class of bugs to compile time, and leaves two to you: panics on a request path and blocking the async runtime. Most of the rules below are about those two.

**Core principle:** the repository's framework, error crates, database crate and workspace layout win. Handlers stay thin; the domain is plain Rust that compiles without the web framework.

## Layers

| Layer | Responsibility | axum surface |
|-------|----------------|--------------|
| Router / handler | Extract and validate input, call one service, map the result | `Router::new().route(...)`, extractors (`State`, `Path`, `Json`), `impl IntoResponse` |
| Service | Use-case orchestration and business rules | a struct holding its ports, `async fn` methods |
| Domain | Types and invariants: newtypes whose constructors validate | plain structs and enums, `thiserror` error enum |
| Adapter | Database, outbound HTTP, queues | a type implementing the port trait (sqlx, reqwest) |

In a workspace the domain is often its own crate; a crate that does not depend on axum cannot leak it.

## Patterns

- **Toolchain:** `rust-toolchain.toml` when present; edition from `Cargo.toml` (2024 for a new crate). Commit `Cargo.lock` for a binary. Add crates with `cargo add`, the version from crates.io, not memory.
- **No panics on a request path:** no `unwrap()`, `expect()`, indexing that can go out of bounds, or `as` casts that truncate on input-derived values. Use `?` with a typed error. `expect` is for startup invariants with a message that says why it cannot fail.
- **Errors:** a domain error enum with `thiserror`; an application error that implements `IntoResponse` and maps each variant to 400/404/409 in the repository's problem shape, logging the source of a 500 and never returning it. `anyhow` belongs in `main` and scripts, not in a library or a handler's signature.
- **Parse, don't validate:** request DTOs `#[derive(Deserialize)]` (with `#[serde(deny_unknown_fields)]` where the contract is strict), converted into domain newtypes (`TaskTitle::try_from(String)`) whose constructors enforce the invariant. A malformed JSON body is already a 4xx through `Json`'s rejection — keep that rejection in the same error shape.
- **State:** one `AppState` (`Clone`, cheap: `Arc`s and pools inside) passed with `.with_state(state)` and taken by `State<AppState>`; no global mutable statics.
- **Never block the runtime:** blocking I/O or CPU-heavy work goes to `tokio::task::spawn_blocking`; no `std::thread::sleep` in async code (`tokio::time::sleep`); never hold a `std::sync::Mutex` guard across `.await` — restructure, or use `tokio::sync::Mutex` when the lock must span an await.
- **Timeouts and limits:** `tower_http` layers — `TimeoutLayer`, `RequestBodyLimitLayer`, `TraceLayer`, `CorsLayer` configured, not `permissive()` in production. Outbound `reqwest` clients built once with a timeout and shared.
- **Database:** sqlx with bound parameters (`query!` / `query_as!` checked at compile time; keep the offline `.sqlx` data committed with `cargo sqlx prepare` when the repository uses offline mode) or the repository's diesel / sea-orm. Never `format!` a SQL string with input. Migrations with `sqlx migrate add <name>` (reversible when the repository's are) applied by `sqlx::migrate!()` or the deploy step; postgres-migrations covers safe DDL.
- **Logging:** `tracing` with structured fields and `#[tracing::instrument(skip(state, body))]` on handlers and service methods — skip anything secret or large; JSON output from `tracing-subscriber` where the repository logs JSON.
- **Graceful shutdown:** `axum::serve(listener, app).with_graceful_shutdown(signal)` on SIGTERM / Ctrl-C.
- **`unsafe`:** none in a feature task. If a dependency forces it, say so in a task comment; the security agent reviews every `unsafe` block.

## Worked Example

`POST /tasks`:

```rust
#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
pub struct CreateTask { title: String }

pub async fn create_task(
    State(state): State<AppState>,
    user: AuthUser,
    Json(body): Json<CreateTask>,
) -> Result<(StatusCode, Json<TaskResponse>), AppError> {
    let title = TaskTitle::try_from(body.title)?;            // 400 through AppError on a bad title
    let task = state.tasks.create(user.id, title).await?;    // the service owns the rule set
    Ok((StatusCode::CREATED, Json(TaskResponse::from(task))))
}
```

`TaskTitle::try_from` trims and rejects empty or over-200-character titles, so no `Task` with an invalid title can exist anywhere in the program.

## Verify

The repository's commands first (list_component_checks, the Makefile, CI). Otherwise: `cargo fmt --check`, `cargo clippy --all-targets --all-features -- -D warnings`, `cargo test`. For the runtime check build once — `cargo build --release` (or the workspace's `-p <api>`) — and start `target/release/<api>` in the background with its port and `DATABASE_URL` set, rather than `cargo run`, whose child a terminal timeout can orphan.

## Common Mistakes

- `.unwrap()` on a parse of user input — one bad request takes the connection down with a panic.
- `std::fs` or a synchronous client inside an `async fn` handler.
- Cloning a large value per request where an `Arc` would do — or the reverse, wrapping everything in `Arc<Mutex<_>>`.
- `#[allow(clippy::...)]` added to get the build green.

## Red Flags

- `format!("SELECT ... {}", input)` anywhere.
- A `MutexGuard` alive across an `.await`.
- `unsafe` in a diff with no comment explaining the invariant it relies on.
- `tokio::spawn` with the `JoinHandle` dropped and no error handling inside the task.
