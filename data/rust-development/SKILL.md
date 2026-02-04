---
name: rust-development
description: |
  Modern Rust development with cargo, clippy, rustfmt, async programming, and memory-safe
  systems programming. Covers ownership patterns, concurrency, Tokio, and the Rust ecosystem.
  Triggers: "rust", "cargo", "clippy", "async rust", "tokio", "ownership", "lifetimes".
allowed-tools: Bash, Read, Edit, Write, Grep, Glob, WebFetch, WebSearch
---

# Rust Development

Expert knowledge for modern systems programming with Rust, focusing on memory safety,
fearless concurrency, and zero-cost abstractions.

## Core Commands

```bash
# Project setup
cargo new my-project          # Binary crate
cargo new my-lib --lib        # Library crate
cargo init                    # Initialize in existing directory

# Development
cargo build                   # Debug build
cargo build --release         # Optimized build
cargo run                     # Build and run
cargo test                    # Run all tests
cargo bench                   # Run benchmarks

# Code quality
cargo clippy                  # Lint code
cargo clippy -- -D warnings   # Treat warnings as errors
cargo fmt                     # Format code
cargo fmt --check             # Check formatting

# Dependencies
cargo add serde --features derive  # Add dependency
cargo update                       # Update deps
cargo audit                        # Security audit
```

## Ownership & Memory Safety

```rust
// Borrowing and lifetimes
fn process(data: &str) -> &str {
    &data[..10]
}

// Interior mutability
use std::cell::RefCell;
use std::sync::{Arc, Mutex, RwLock};

let shared = Arc::new(Mutex::new(Vec::new()));
let cache = RwLock::new(HashMap::new());

// Smart pointers
use std::rc::Rc;
let shared_data = Rc::new(Data::new());
let cloned = Rc::clone(&shared_data);
```

## Error Handling

```rust
use thiserror::Error;
use anyhow::{Context, Result, bail};

#[derive(Error, Debug)]
pub enum AppError {
    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),

    #[error("not found: {0}")]
    NotFound(String),
}

// Application code with anyhow
async fn process(id: &str) -> Result<Response> {
    let data = fetch(id).await.context("Failed to fetch")?;
    Ok(parse(&data)?)
}

// Let-else for early returns
let Some(config) = load_config() else {
    return Err(ConfigError::NotFound.into());
};
```

## Async Programming with Tokio

### Setup

```toml
# Cargo.toml
[dependencies]
tokio = { version = "1", features = ["full"] }
futures = "0.3"
async-trait = "0.1"
```

### Basic Patterns

```rust
use tokio::time::{sleep, Duration};

#[tokio::main]
async fn main() -> Result<()> {
    let result = fetch_data("https://api.example.com").await?;
    println!("Got: {}", result);
    Ok(())
}

async fn fetch_data(url: &str) -> Result<String> {
    sleep(Duration::from_millis(100)).await;
    Ok(format!("Data from {}", url))
}
```

### Concurrent Execution

```rust
use tokio::task::JoinSet;
use futures::stream::{self, StreamExt};

// Spawn multiple concurrent tasks
async fn fetch_all(urls: Vec<String>) -> Vec<String> {
    let mut set = JoinSet::new();
    for url in urls {
        set.spawn(async move { fetch_data(&url).await });
    }

    let mut results = Vec::new();
    while let Some(res) = set.join_next().await {
        if let Ok(Ok(data)) = res {
            results.push(data);
        }
    }
    results
}

// With concurrency limit
async fn fetch_limited(urls: Vec<String>, limit: usize) -> Vec<Result<String>> {
    stream::iter(urls)
        .map(|url| async move { fetch_data(&url).await })
        .buffer_unordered(limit)
        .collect()
        .await
}

// Select first to complete
use tokio::select;

async fn race(url1: &str, url2: &str) -> Result<String> {
    select! {
        result = fetch_data(url1) => result,
        result = fetch_data(url2) => result,
    }
}
```

### Channels

```rust
use tokio::sync::{mpsc, broadcast, oneshot, watch};

// Multi-producer, single-consumer
let (tx, mut rx) = mpsc::channel::<String>(100);
tokio::spawn(async move {
    tx.send("Hello".to_string()).await.unwrap();
});
while let Some(msg) = rx.recv().await {
    println!("Got: {}", msg);
}

// Broadcast: multi-producer, multi-consumer
let (tx, _) = broadcast::channel::<String>(100);
let mut rx1 = tx.subscribe();
let mut rx2 = tx.subscribe();

// Oneshot: single value, single use
let (tx, rx) = oneshot::channel::<String>();

// Watch: latest value, multi-consumer
let (tx, mut rx) = watch::channel("initial".to_string());
```

### Graceful Shutdown

```rust
use tokio::signal;
use tokio_util::sync::CancellationToken;

async fn run_server() -> Result<()> {
    let token = CancellationToken::new();
    let token_clone = token.clone();

    tokio::spawn(async move {
        loop {
            tokio::select! {
                _ = token_clone.cancelled() => break,
                _ = do_work() => {}
            }
        }
    });

    signal::ctrl_c().await?;
    token.cancel();
    tokio::time::sleep(Duration::from_secs(5)).await;
    Ok(())
}
```

## Clippy Linting

### Configuration (Cargo.toml)

```toml
[workspace.lints.clippy]
correctness = { level = "deny", priority = -1 }
complexity = "warn"
perf = "warn"
style = "warn"
pedantic = "warn"

# Selective allows
must_use_candidate = "allow"
missing_errors_doc = "allow"

# Restriction lints (opt-in)
dbg_macro = "warn"
print_stdout = "warn"
todo = "warn"
unwrap_used = "warn"
```

### clippy.toml

```toml
cognitive-complexity-threshold = 15
too-many-arguments-threshold = 5
too-many-lines-threshold = 100

disallowed-methods = [
  { path = "std::option::Option::unwrap", reason = "Use proper error handling" },
  { path = "std::process::exit", reason = "Return from main instead" },
]
```

### Usage

```bash
cargo clippy --all-targets --all-features
cargo clippy -- -W clippy::pedantic -W clippy::nursery
cargo clippy -- -D warnings  # CI: treat warnings as errors
```

### Inline Suppression

```rust
#[allow(clippy::too_many_arguments)]
fn complex_function(a: i32, b: i32, c: i32, d: i32, e: i32, f: i32) {}

// Module level
#![warn(clippy::all)]
#![deny(clippy::unwrap_used)]
```

## Project Structure

```
my-project/
├── Cargo.toml
├── clippy.toml
├── src/
│   ├── lib.rs        # Library root
│   ├── main.rs       # Binary entry
│   ├── error.rs      # Error types
│   └── modules/
├── tests/            # Integration tests
├── benches/          # Benchmarks
└── examples/
```

## Common Crates

| Crate | Purpose |
|-------|---------|
| `serde` | Serialization |
| `tokio` | Async runtime |
| `reqwest` | HTTP client |
| `sqlx` | Async SQL |
| `clap` | CLI parsing |
| `tracing` | Logging |
| `anyhow` | App errors |
| `thiserror` | Library errors |

## Best Practices

**Async:**
- Use `tokio::select!` for racing futures
- Prefer channels over shared state
- Use `JoinSet` for managing tasks
- Handle cancellation with `CancellationToken`
- Never use `std::thread::sleep` in async code

**Error Handling:**
- Use `thiserror` for library errors
- Use `anyhow` for application errors
- Propagate errors with `?`
- Add context with `.context()`

**Code Quality:**
- Run `cargo clippy` before commits
- Use `cargo fmt` for consistent formatting
- Enable pedantic lints selectively
- Document suppressions

## Documentation

- [Rust Book](https://doc.rust-lang.org/book/)
- [Tokio Tutorial](https://tokio.rs/tokio/tutorial)
- [Async Book](https://rust-lang.github.io/async-book/)
- [Clippy Lints](https://rust-lang.github.io/rust-clippy/master/)
