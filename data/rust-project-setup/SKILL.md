---
name: rust-project-setup
description: Initialize Rust projects with proper structure, essential crates, and Cargo.toml configuration. Use when starting new Rust binaries or libraries.
---

# Rust Project Setup

Initialize Rust projects with production-ready structure and dependencies.

## Project Initialization

```bash
cargo new project_name          # Binary
cargo new --lib project_name    # Library
```

## Recommended Structure

```
src/
├── lib.rs / main.rs
├── module/
│   ├── mod.rs
│   └── submodule.rs
├── error.rs                    # Error types
├── config.rs                   # Configuration
tests/                          # Integration tests
examples/                       # Runnable examples
benches/                        # Benchmarks
```

## Essential Crates by Category

### Async Runtime
```toml
tokio = { version = "1", features = ["full"] }
```

### Serialization
```toml
serde = { version = "1", features = ["derive"] }
serde_json = "1"
```

### Error Handling
```toml
thiserror = "1"      # Libraries
anyhow = "1"         # Applications
```

### Database
```toml
sqlx = { version = "0.7", features = ["runtime-tokio", "postgres", "native-tls"] }
```

### HTTP/Web
```toml
axum = "0.7"
reqwest = { version = "0.11", features = ["json"] }
```

### CLI
```toml
clap = { version = "4", features = ["derive"] }
```

### Observability
```toml
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter"] }
```

### Utilities
```toml
dotenvy = "0.15"     # Environment variables
num_cpus = "1"       # CPU detection
parking_lot = "0.12" # Fast locks
bytes = "1"          # Zero-copy buffers
```

## Production Cargo.toml Template

```toml
[package]
name = "my-service"
version = "0.1.0"
edition = "2021"
rust-version = "1.70"

[dependencies]
tokio = { version = "1", features = ["full"] }
serde = { version = "1", features = ["derive"] }
serde_json = "1"
thiserror = "1"
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter"] }
dotenvy = "0.15"

[dev-dependencies]
tokio-test = "0.4"

[profile.release]
opt-level = 3
lto = true
codegen-units = 1
strip = true
panic = 'abort'

[lints.rust]
unsafe_code = "forbid"

[lints.clippy]
all = "warn"
pedantic = "warn"
unwrap_used = "deny"
expect_used = "deny"
```

## Guidelines

- Use `edition = "2021"` for latest features
- Specify `rust-version` for MSRV
- Enable release optimizations for production
- Use workspace for monorepos
- Pin major versions, allow minor updates

## Examples

See `hercules-local-algo/Cargo.toml` for production configuration.
