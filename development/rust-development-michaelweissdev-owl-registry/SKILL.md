---
name: rust-development
description: >
  Develop, review, and optimize idiomatic, memory-safe Rust code following the
  Rust API Guidelines. Use when writing Rust crates, managing ownership, borrowing,
  and lifetimes, designing robust traits and error hierarchies with Result/Option,
  configuring Clippy/rustfmt, choosing an edition or MSRV, or evaluating safe
  alternatives to unsafe code. Do not use for C/C++ FFI binding generation details,
  embedded no_std board bring-up, or general performance profiling unrelated to Rust
  language choices.
compatibility: >
  Agent Skills-compatible coding agents operating on Rust 2021 or 2024 edition
  codebases with Cargo available. Edition 2024 requires Rust 1.85+. Version facts
  checked against the Rust release notes (stable 1.99.0, 2026-10-01) in October 2026.
metadata:
  author: michaelweissdev
  version: "1.1.0"
  tags: "rust, cargo, clippy, ownership, lifetimes, memory-safety, traits"
  topics: "programming-languages, software-development"
---

# Idiomatic Rust Development

Rust delivers memory safety, concurrency guarantees, and zero-cost abstractions through its strict ownership, borrowing, and type system. Idiomatic Rust code favors clear ownership semantics, rich enum modeling, structured error propagation via `Result<T, E>`, and adherence to the [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/).

Detailed reference documentation is provided in:
- [Ownership, Borrowing & Lifetimes](references/ownership-lifetimes.md)
- [Error Handling with Result & Option](references/error-handling.md)
- [Trait Design & API Patterns](references/traits-api-design.md)
- [Unsafe Rust Guidelines & Invariants](references/unsafe-guidelines.md)
- [Editions, toolchain, and dependency hygiene](references/editions-and-toolchain.md)

---

## Core Rules

1. **Safety first**: Write 100% safe Rust code by default. Never introduce `unsafe` blocks when safe, idiomatic alternatives exist in the standard library.
2. **Never use `.unwrap()` in library code**: Propagate errors using the `?` operator or return meaningful fallbacks. Reserve `.unwrap()` and `.expect()` strictly for tests or provable invariants.
3. **Do not abuse `.clone()` to appease the borrow checker**: Excessive cloning wastes performance and obscures poor ownership design. Restructure data flow or borrow references (`&T`, `&mut T`).
4. **Leverage the type system for correctness**: Make illegal states unrepresentable using enums and the typestate pattern.
5. **Comply with Clippy and Rustfmt**: Always ensure code compiles cleanly with `cargo clippy -- -D warnings` and `cargo fmt --check`.
6. **Document public interfaces with Rustdoc**: Write doc-tests for all public API functions (`///`).

---

## 1. Idiomatic Data Modeling: Enums and Pattern Matching

Replace boolean flags and optional tuples with explicit algebraic data types:

```rust
/// Represents the connection state of a network client.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ConnectionState {
    Disconnected,
    Connecting { attempt: u32 },
    Connected { session_id: String },
    Terminated { reason: String },
}

impl ConnectionState {
    pub fn is_active(&self) -> bool {
        matches!(self, Self::Connected { .. })
    }
}
```

---

## 2. Structured Error Handling

In applications, use `anyhow` for ergonomic error bundling. In libraries, define strongly typed error enums using `thiserror`:

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum DataStoreError {
    #[error("I/O error occurred while accessing {path}: {source}")]
    Io {
        path: String,
        #[source]
        source: std::io::Error,
    },

    #[error("Item with key '{0}' was not found in cache")]
    NotFound(String),

    #[error("Serialization failed: {0}")]
    Serialization(#[from] serde_json::Error),
}

pub type Result<T> = std::result::Result<T, DataStoreError>;
```

---

## 3. Idiomatic API Design: Borrowed Types in Arguments

Follow the rule of least privilege for function inputs:
- Accept `&str` instead of `&String`.
- Accept `&[T]` instead of `&Vec<T>`.
- Accept `&Path` instead of `&PathBuf`.
- Accept `impl AsRef<Path>` or `impl Into<String>` where ergonomics justify minor monomorphization.

```rust
use std::path::Path;

// Highly ergonomic: accepts &str, String, &Path, PathBuf
pub fn load_configuration<P: AsRef<Path>>(path: P) -> Result<Config> {
    let path_ref = path.as_ref();
    let content = std::fs::read_to_string(path_ref).map_err(|e| {
        DataStoreError::Io {
            path: path_ref.display().to_string(),
            source: e,
        }
    })?;
    Ok(serde_json::from_str(&content)?)
}
```

---

## 4. Common Mistakes and Anti-Patterns

| Anti-Pattern | Bug / Risk | Correct Practice |
| :--- | :--- | :--- |
| `.unwrap()` in library code | Panics production application on unexpected input | Return `Result<T, E>` and propagate with `?` |
| Calling `.clone()` on everything | Unnecessary heap allocations | Borrow with `&T`, or use `Cow<'_, T>` |
| Implementing `Deref` for inheritance | Violates API guidelines and misleads type system | Implement specific traits or explicit delegation |
| Public struct with all public fields | Breaking change on adding private invariants | Provide private fields with constructor (`pub fn new(...)`) and getters |
| Using `unsafe` for performance without profiling | Undefined behavior risk for unmeasured micro-optimizations | Profile first; write safe idiomatic iterators |

---

## 5. Edition and Toolchain Decisions

- New crates: `edition = "2024"` (stable since Rust 1.85) and an explicit `rust-version` (MSRV). Existing crates: migrate with `cargo fix --edition` on a clean branch, review the diff, and run tests; do not bump the edition inside an unrelated change.
- Pin the toolchain for reproducibility with `rust-toolchain.toml`; test on MSRV and stable in CI.
- Configure lints centrally in `Cargo.toml` under `[lints]` / `[workspace.lints]` rather than scattering `#![deny]` attributes.
- Check dependencies: `cargo audit` (RustSec advisories) and `cargo deny` (licenses, sources, bans) are separate tools you must install; they are not part of `cargo`.

## 6. Tooling and Quality Checks

Run these standard verification commands:

```bash
# Format check
cargo fmt --check

# Strict linting (treat Clippy warnings as errors)
cargo clippy --all-targets --all-features -- -D warnings

# Run all unit and integration tests including doc-tests
cargo test --all-features

# Build and verify documentation
cargo doc --no-deps
```

---

## 7. Verification Checklist

- [ ] All public types and functions have `///` documentation comments with examples.
- [ ] No unconditional `.unwrap()` or `.expect()` calls in production paths.
- [ ] Error types implement `std::error::Error` (or derive with `thiserror`).
- [ ] Code passes `cargo clippy -- -D warnings` with zero warnings.
- [ ] Tests pass across all workspace crates (`cargo test`).
- [ ] Every `unsafe` block has a `// SAFETY:` comment and a test (Miri where applicable).
- [ ] Edition and `rust-version` are stated in `Cargo.toml` and exercised in CI.
