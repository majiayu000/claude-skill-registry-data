---
name: rust-tokio-essentials
description: Core Tokio patterns including runtime setup, spawn_blocking for CPU work, and avoiding blocking operations. Use for any async Rust development.
---

# Tokio Essentials

Core patterns for async Rust with Tokio runtime.

## Runtime Setup

```toml
# Cargo.toml
[dependencies]
tokio = { version = "1", features = ["full"] }
```

```rust
#[tokio::main]
async fn main() -> Result<()> {
    // Initialize environment
    dotenvy::dotenv().ok();

    // Setup logging
    tracing_subscriber::fmt()
        .with_env_filter(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| tracing_subscriber::EnvFilter::new("info")),
        )
        .init();

    // Your async code here
    run_service().await
}
```

## Never Block the Runtime

```rust
// BAD: Blocks the async runtime
async fn bad() {
    std::thread::sleep(Duration::from_secs(1));  // BLOCKS!
    std::fs::read_to_string("file.txt");         // BLOCKS!
}

// GOOD: Use async alternatives
async fn good() {
    tokio::time::sleep(Duration::from_secs(1)).await;
    tokio::fs::read_to_string("file.txt").await?;
}
```

## spawn_blocking for CPU Work

```rust
// CPU-intensive work must be offloaded
async fn process_image(data: Vec<u8>) -> Result<Vec<u8>> {
    tokio::task::spawn_blocking(move || {
        // Heavy CPU computation runs on blocking thread pool
        expensive_image_processing(&data)
    })
    .await?
}

// FFI/blocking libraries
async fn call_python(code: &str) -> Result<String> {
    let code = code.to_string();
    tokio::task::spawn_blocking(move || {
        Python::with_gil(|py| {
            py.eval(&code, None, None)?.extract()
        })
    })
    .await?
}
```

## Spawning Tasks

```rust
// Fire and forget
tokio::spawn(async move {
    background_task().await;
});

// Track task completion
let handle = tokio::spawn(async move {
    compute_result().await
});
let result = handle.await?;

// Spawn with name (for debugging)
tokio::task::Builder::new()
    .name("worker")
    .spawn(async move { work().await })?;
```

## Timeouts

```rust
use tokio::time::{timeout, Duration};

// Timeout a future
let result = timeout(Duration::from_secs(30), slow_operation())
    .await
    .map_err(|_| Error::Timeout)?;

// Timeout with default
let result = timeout(Duration::from_secs(5), fetch_data())
    .await
    .unwrap_or_else(|_| default_value());
```

## Select for Racing

```rust
use tokio::select;

async fn with_cancellation(cancel: CancellationToken) -> Result<Data> {
    select! {
        result = fetch_data() => result,
        _ = cancel.cancelled() => Err(Error::Cancelled),
    }
}

// First to complete wins
let result = select! {
    a = source_a() => a,
    b = source_b() => b,
};
```

## Interval and Periodic Tasks

```rust
use tokio::time::{interval, Duration};

async fn periodic_cleanup() {
    let mut interval = interval(Duration::from_secs(60));

    loop {
        interval.tick().await;
        cleanup().await;
    }
}
```

## Runtime Configuration

```rust
// Custom runtime (when not using #[tokio::main])
let runtime = tokio::runtime::Builder::new_multi_thread()
    .worker_threads(4)
    .enable_all()
    .build()?;

runtime.block_on(async {
    main_async().await
});

// Current-thread runtime (single-threaded)
let runtime = tokio::runtime::Builder::new_current_thread()
    .enable_all()
    .build()?;
```

## Guidelines

- Never use `std::thread::sleep` in async code
- Never use blocking I/O (`std::fs`, `std::net`) in async code
- Use `spawn_blocking` for CPU-bound work and FFI
- Use `timeout` for operations that might hang
- Prefer `select!` over manual task management
- Use `#[tokio::main]` unless you need custom runtime config

## Examples

See `hercules-local-algo/src/main.rs` for production runtime setup.
