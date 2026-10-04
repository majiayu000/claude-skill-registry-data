---
name: rust-sdlc
description: Complete Rust Software Development Lifecycle - Cargo, testing, memory safety patterns, async (Tokio), error handling, web frameworks (Axum, Actix), embedded development, CI/CD, cross-compilation, and deployment.
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Rust SDLC Skill

You are a Senior Rust Engineer specializing in the complete Software Development Lifecycle. You guide Rust projects from initial setup through production deployment with idiomatic, safe, and performant Rust code.

## Core Capabilities

### 1. Project Initialization

**Cargo New:**
```bash
# Binary
cargo new myproject --bin

# Library
cargo new mylib --lib

# Workspace
cargo new workspace --name myworkspace
```

**Project Structure:**
```
myproject/
├── Cargo.toml
├── Cargo.lock
├── src/
│   ├── main.rs        # Binary entry
│   ├── lib.rs         # Library root
│   ├── bin/           # Multiple binaries
│   └── internal/
├── tests/             # Integration tests
├── benches/           # Benchmarks
├── examples/          # Usage examples
├── .cargo/            # Cargo config
│   └── config.toml
└── rust-toolchain.toml
```

### 2. Cargo Configuration

**Cargo.toml:**
```toml
[package]
name = "myproject"
version = "0.1.0"
edition = "2021"
rust-version = "1.75"
authors = ["Your Name <you@example.com>"]
license = "MIT OR Apache-2.0"
repository = "https://github.com/you/myproject"
keywords = ["web", "api", "async"]
categories = ["web-programming::http-server"]

[dependencies]
# Async runtime
tokio = { version = "1", features = ["full"] }

# Web framework
axum = "0.7"
tower = "0.4"

# Serialization
serde = { version = "1", features = ["derive"] }
serde_json = "1"

# Error handling
thiserror = "1"
anyhow = "1"

# Database
sqlx = { version = "0.7", features = ["runtime-tokio", "postgres"] }

# Logging
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter"] }

[dev-dependencies]
tokio-test = "0.4"
criterion = "0.5"
mockall = "0.12"
```

**Feature Flags:**
```toml
[features]
default = ["std"]
std = []
async = ["tokio", "futures"]
database = ["sqlx"]
```

### 3. Memory Safety Patterns

**Ownership & Borrowing:**
```rust
// Move semantics
let data = vec![1, 2, 3];
process(data);           // data moved here
// data is no longer valid

// Borrowing
let data = vec![1, 2, 3];
process(&data);          // immutable borrow
process(&data);          // multiple immutable borrows OK
mutate(&mut data);       // single mutable borrow
```

**Smart Pointers:**
```rust
use std::sync::Arc;
use std::rc::Rc;

// Arc for thread-safe shared ownership
let data = Arc::new(vec![1, 2, 3]);
let data2 = Arc::clone(&data);

// Box for heap allocation
let large = Box::new([0u8; 1_000_000]);

// Rc for single-threaded shared ownership
let config = Rc::new(Config::new());
```

**Lifetimes:**
```rust
// Explicit lifetime annotation
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}

// Lifetime elision (compiler infers)
fn first_word(s: &str) -> &str {
    &s[..s.find(' ').unwrap_or(s.len())]
}
```

### 4. Error Handling

**thiserror (Library errors):**
```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("database error: {0}")]
    Database(#[from] sqlx::Error),

    #[error("validation error: {0}")]
    Validation(String),

    #[error("not found: {0}")]
    NotFound(String),

    #[error(transparent)]
    Other(#[from] anyhow::Error),
}

pub type Result<T> = std::result::Result<T, AppError>;
```

**anyhow (Application errors):**
```rust
use anyhow::{Context, Result};

fn read_config() -> Result<Config> {
    let path = std::env::var("CONFIG_PATH")
        .context("CONFIG_PATH not set")?;

    let content = std::fs::read_to_string(&path)
        .with_context(|| format!("failed to read {path}"))?;

    Ok(toml::from_str(&content)?)
}
```

### 5. Async Programming (Tokio)

**Basic Async:**
```rust
use tokio::time::{sleep, Duration};

#[tokio::main]
async fn main() {
    let handle = tokio::spawn(async {
        sleep(Duration::from_secs(1)).await;
        "completed"
    });

    let result = handle.await.unwrap();
    println!("{}", result);
}
```

**Concurrent Execution:**
```rust
use tokio::join;
use futures::future::try_join_all;

// Join multiple futures
let (user, orders) = join!(
    fetch_user(id),
    fetch_orders(id)
);

// Try join with error handling
let results: Vec<_> = try_join_all(
    urls.into_iter().map(fetch_url)
).await?;

// Select (race)
tokio::select! {
    result = timeout => println!("timeout"),
    result = response => println!("response"),
}
```

**Channels:**
```rust
use tokio::sync::mpsc;

let (tx, mut rx) = mpsc::channel(100);

tokio::spawn(async move {
    while let Some(msg) = rx.recv().await {
        process(msg).await;
    }
});

tx.send(message).await?;
```

### 6. Testing

**Unit Tests:**
```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add() {
        assert_eq!(add(2, 2), 4);
    }

    #[tokio::test]
    async fn test_async_operation() {
        let result = async_operation().await;
        assert!(result.is_ok());
    }

    #[test]
    #[should_panic(expected = "divide by zero")]
    fn test_divide_by_zero() {
        divide(1, 0);
    }
}
```

**Integration Tests:**
```rust
// tests/api_test.rs
use myapp::app;

#[tokio::test]
async fn test_health_check() {
    let app = app().await;
    let response = app
        .oneshot(Request::builder().uri("/health").body(Body::empty()).unwrap())
        .await
        .unwrap();

    assert_eq!(response.status(), StatusCode::OK);
}
```

**Mocking:**
```rust
use mockall::mock;

#[automock]
trait Database {
    async fn get_user(&self, id: i64) -> Option<User>;
}

#[tokio::test]
async fn test_with_mock() {
    let mut mock = MockDatabase::new();
    mock.expect_get_user()
        .with(eq(1))
        .returning(|_| Some(User::new(1, "Alice")));

    let service = UserService::new(mock);
    let user = service.get_user(1).await.unwrap();
    assert_eq!(user.name, "Alice");
}
```

### 7. Web Frameworks

**Axum (Recommended):**
```rust
use axum::{
    routing::{get, post},
    Router,
    Json,
    extract::State,
    http::StatusCode,
};
use std::sync::Arc;

#[derive(Clone)]
struct AppState {
    db: Database,
}

#[tokio::main]
async fn main() {
    let state = Arc::new(AppState { db: Database::new() });

    let app = Router::new()
        .route("/", get(root))
        .route("/users", post(create_user))
        .route("/users/:id", get(get_user))
        .with_state(state);

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await.unwrap();
    axum::serve(listener, app).await.unwrap();
}

async fn get_user(
    State(state): State<Arc<AppState>>,
    axum::extract::Path(id): axum::extract::Path<i64>,
) -> Result<Json<User>, StatusCode> {
    state.db.get_user(id).await
        .map(Json)
        .map_err(|_| StatusCode::NOT_FOUND)
}
```

**Actix Web:**
```rust
use actix_web::{get, web, App, HttpServer, Responder, HttpResponse};

#[get("/")]
async fn index() -> impl Responder {
    HttpResponse::Ok().body("Hello world!")
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| App::new().service(index))
        .bind(("127.0.0.1", 8080))?
        .run()
        .await
}
```

### 8. Database (SQLx)

**Compile-time Checked SQL:**
```rust
use sqlx::postgres::PgPool;

pub struct UserRepository {
    pool: PgPool,
}

impl UserRepository {
    pub async fn find_by_id(&self, id: i64) -> Result<Option<User>, sqlx::Error> {
        sqlx::query_as::<_, User>(
            "SELECT id, name, email FROM users WHERE id = $1"
        )
        .bind(id)
        .fetch_optional(&self.pool)
        .await
    }

    pub async fn create(&self, user: &NewUser) -> Result<User, sqlx::Error> {
        sqlx::query_as::<_, User>(
            "INSERT INTO users (name, email) VALUES ($1, $2) RETURNING *"
        )
        .bind(&user.name)
        .bind(&user.email)
        .fetch_one(&self.pool)
        .await
    }
}
```

### 9. CI/CD

**GitHub Actions:**
```yaml
name: Rust CI
on: [push, pull_request]
env:
  CARGO_TERM_COLOR: always
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
      - uses: Swatinem/rust-cache@v2
      - run: cargo test --all-features
      - run: cargo clippy -- -D warnings
      - run: cargo fmt --check
      - run: cargo doc --no-deps
```

**Pre-commit:**
```yaml
repos:
  - repo: local
    hooks:
      - id: fmt
        name: cargo fmt
        entry: cargo fmt -- --check
        language: system
        pass_filenames: false
      - id: clippy
        name: cargo clippy
        entry: cargo clippy -- -D warnings
        language: system
        pass_filenames: false
```

### 10. Cross-Compilation

**Target Platforms:**
```toml
# .cargo/config.toml
[target.aarch64-unknown-linux-gnu]
linker = "aarch64-linux-gnu-gcc"

[target.x86_64-unknown-linux-musl]
linker = "x86_64-linux-musl-gcc"
```

**Cross:**
```bash
# Install cross
cargo install cross

# Build for different targets
cross build --target x86_64-unknown-linux-musl
cross build --target aarch64-unknown-linux-gnu
```

### 11. Deployment

**Docker Multi-stage:**
```dockerfile
# Builder
FROM rust:1.75-slim AS builder
WORKDIR /app
COPY . .
RUN cargo build --release --bin myapp

# Runtime
FROM debian:bookworm-slim AS runtime
RUN apt-get update && apt-get install -y ca-certificates
COPY --from=builder /app/target/release/myapp /usr/local/bin/
ENTRYPOINT ["/usr/local/bin/myapp"]
```

**Distroless:**
```dockerfile
FROM gcr.io/distroless/cc-debian12
COPY target/release/myapp /app
ENTRYPOINT ["/app"]
```

## Quick Commands

```bash
# Build
cargo build --release

# Test
cargo test
cargo test --all-features
cargo test -- --nocapture

# Code quality
cargo fmt
cargo clippy -- -D warnings
cargo check

# Documentation
cargo doc --open

# Benchmark
cargo bench

# Run
cargo run --release

# Dependencies
cargo tree
cargo outdated  # requires cargo-outdated
cargo audit     # requires cargo-audit
```

## Best Practices Checklist

- [ ] Use Rust 1.70+ (preferably latest stable)
- [ ] Edition 2021
- [ ] Strict Clippy lints
- [ ] thiserror for libraries
- [ ] anyhow for applications
- [ ] Tokio for async
- [ ] sqlx with compile-time checks
- [ ] Axum for web APIs
- [ ] Serde for serialization
- [ ] Tracing for logging
- [ ] Criterion for benchmarks
- [ ] Mockall for mocking
- [ ] cargo-audit for security
- [ ] cargo-outdated for updates
- [ ] Cross-compilation testing
- [ ] Minimal Docker images
- [ ] Health check endpoints
- [ ] Graceful shutdown handling
