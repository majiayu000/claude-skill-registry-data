---
name: rust
description: Rust ecosystem = cargo + rustc + clippy + rustfmt.
metadata:
  trit: 0
---

# rust

Rust ecosystem = cargo + rustc + clippy + rustfmt.

## Atomic Skills

| Skill | Commands | Domain |
|-------|----------|--------|
| cargo | 36 | Package manager |
| rustc | 1 | Compiler |
| clippy | 1 | Linter |
| rustfmt | 1 | Formatter |

## Workflow

```bash
cargo new project
cd project
cargo add serde tokio
cargo build --release
cargo test
cargo clippy
cargo fmt
```

## Cargo.toml

```toml
[package]
name = "myapp"
version = "0.1.0"
edition = "2021"

[dependencies]
serde = { version = "1.0", features = ["derive"] }
tokio = { version = "1", features = ["full"] }
```

## Cross-compile

```bash
rustup target add aarch64-apple-darwin
cargo build --target aarch64-apple-darwin
```
