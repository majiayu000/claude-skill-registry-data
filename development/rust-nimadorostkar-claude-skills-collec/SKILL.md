---
name: rust
description: Use when writing Rust or resolving borrow-checker, lifetime, and trait errors. Covers ownership models, error handling with thiserror and anyhow, async with Tokio, and safe abstractions over unsafe code.
metadata:
  category: languages
  version: 1.0.0
  tags: [rust, ownership, lifetimes, tokio, error-handling]
---

# Rust

## Purpose

Write Rust that satisfies the borrow checker by design rather than by fighting it. Ownership is a modeling decision made before the code is written, not a compiler obstacle discovered afterward.

## When to Use

- Building Rust libraries, services, or CLI tools.
- Resolving lifetime, borrow, or trait-bound errors.
- Designing error types for a library versus an application.
- Writing async Rust with Tokio.
- Auditing or minimizing `unsafe` blocks.

## Capabilities

- Ownership and borrowing design: when to clone, when to borrow, when to use `Rc`/`Arc`.
- Error modeling: `thiserror` for libraries, `anyhow` for binaries.
- Trait design, generic bounds, and trait objects.
- Async runtimes, `Send`/`Sync` bounds, and cancellation semantics.
- Safe encapsulation of `unsafe`, with documented invariants.

## Inputs

- Crate or module source.
- Edition and MSRV.
- Whether the artifact is a library (stable public API) or a binary.

## Outputs

- Code that compiles with zero warnings under `clippy::pedantic` (or a documented allow-list).
- Explicit error enums with `#[from]` conversions.
- Tests including compile-fail tests for API misuse where warranted.

## Workflow

1. **Model ownership first** — Decide who owns each value and how long it lives before writing the signature.
2. **Design the error type** — A library's error enum is public API. Enumerate failure modes explicitly.
3. **Implement** — Start with owned values and clones. Optimize to borrows only where profiling or ergonomics justify it.
4. **Constrain generics late** — Write it concrete, then generalize if a second caller appears.
5. **Gate** — `cargo clippy -- -D warnings`, `cargo fmt --check`, `cargo test`, `cargo deny check`.

## Best Practices

- A `clone()` in non-hot-path code is not a defect. Premature borrow optimization produces unreadable lifetimes.
- Libraries return concrete error enums; binaries use `anyhow::Result` and add context at each layer.
- Never `unwrap()` outside tests and `main`. Use `expect("invariant: ...")` where the invariant is genuinely proven.
- Prefer `impl Trait` in argument position for simple bounds; use named generics when the caller must choose the type.
- Every `unsafe` block gets a `// SAFETY:` comment stating the invariant that makes it sound.
- Use `#[non_exhaustive]` on public enums you may extend.

## Examples

**Library error type:**

```rust
use thiserror::Error;

#[derive(Debug, Error)]
#[non_exhaustive]
pub enum StoreError {
    #[error("key not found: {0}")]
    NotFound(String),

    #[error("storage backend unavailable")]
    Unavailable(#[source] std::io::Error),

    #[error("value for {key} exceeds {limit} bytes")]
    TooLarge { key: String, limit: usize },
}

pub fn get(key: &str) -> Result<Vec<u8>, StoreError> {
    std::fs::read(key).map_err(|e| match e.kind() {
        std::io::ErrorKind::NotFound => StoreError::NotFound(key.to_owned()),
        _ => StoreError::Unavailable(e),
    })
}
```

**Async with timeout and cancellation:**

```rust
use tokio::time::{timeout, Duration};

pub async fn fetch_with_deadline(url: &str) -> anyhow::Result<String> {
    let body = timeout(Duration::from_secs(5), reqwest::get(url))
        .await
        .context("request timed out after 5s")?
        .context("request failed")?
        .text()
        .await?;
    Ok(body)
}
```

## Notes

- Borrow-checker errors are usually design feedback. If a lifetime is hard to name, the ownership model is probably wrong.
- `Arc<Mutex<T>>` is a legitimate answer, not a failure. Contention, not the type, is what costs you.
- Async traits are stable as of Rust 1.75 for non-object-safe use; `async-trait` is still needed for trait objects.
