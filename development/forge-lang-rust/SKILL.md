---
name: forge-lang-rust
description: Rust development standards including cargo test, clippy, and rustfmt. Use when working with Rust files, Cargo.toml, or Rust tests.
---

# Rust Development

## Testing

```bash
# Run all tests
cargo test

# Run with output
cargo test -- --nocapture

# Run specific test
cargo test test_name

# Run ignored tests
cargo test -- --ignored
```

## Linting

```bash
# Run clippy
cargo clippy -- -D warnings

# Check without building
cargo check
```

## Formatting

```bash
# Format code
cargo fmt

# Check format without changing
cargo fmt --check
```

## Project Structure

```
project/
├── src/
│   ├── lib.rs
│   └── main.rs
├── tests/
│   └── integration_test.rs
├── Cargo.toml
└── README.md
```

## Cargo.toml Template

```toml
[package]
name = "project-name"
version = "0.1.0"
edition = "2021"

[dependencies]

[dev-dependencies]

[lints.rust]
unsafe_code = "forbid"

[lints.clippy]
all = "warn"
pedantic = "warn"
```

## TDD Cycle Commands

```bash
# RED: Write test, run to see it fail
cargo test test_new_feature

# GREEN: Implement, run to see it pass
cargo test test_new_feature

# REFACTOR: Clean up, ensure tests still pass
cargo test && cargo clippy && cargo fmt --check
```
