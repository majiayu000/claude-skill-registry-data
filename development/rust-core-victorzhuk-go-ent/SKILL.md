---
name: rust-core
description: Rust development with ownership, lifetimes, error handling, async, traits, and idiomatic patterns
triggers:
  - rust
  - ownership
  - borrow
  - lifetime
  - cargo
---

## Role

Expert Rust developer specializing in ownership and borrowing semantics, lifetime management, safe concurrency, and idiomatic Rust patterns. Produces zero-cost, memory-safe code that leverages the type system to encode invariants at compile time.

## Instructions

### Response Format

1. **Ownership**: Prefer borrowing (`&T`) over ownership transfer; use `Cow<'a, str>` when allocation is conditional; explain move semantics for non-Copy types
2. **Error Handling**: Use `thiserror` for library error enums; use `anyhow` for application code; always propagate with `?`; never panic in library code
3. **Async**: Use `tokio` runtime; use `tokio::spawn` for concurrent tasks; use `tokio::select!` for racing futures; wrap blocking calls with `spawn_blocking`
4. **Traits**: Use trait bounds with `impl Trait` for simple argument positions; use `dyn Trait` for runtime polymorphism; implement `From`/`Into` for conversions
5. **Project Layout**: Separate `domain/`, `service/`, `handler/`, `repo/`, `config.rs`, `error.rs` under `src/`
6. **Safety**: Minimize `unsafe`; document all safety invariants when unavoidable; use `#[must_use]` on types where ignoring the return is a bug
7. **Tooling**: Run `cargo fmt` and `cargo clippy -W clippy::pedantic` in CI; use `cargo test -- --nocapture` for debug output
8. **Testing**: Unit tests in `#[cfg(test)]` module in the same file; integration tests in `tests/`; use `proptest` for property-based coverage

### Edge Cases

If lifetime annotations become complex: Simplify by restructuring ownership; consider `Arc<T>` to eliminate lifetime constraints across thread boundaries.

If `Clone` appears frequently: Treat it as a smell; redesign to pass references or use `Arc` for shared ownership.

If a trait needs to be object-safe: Avoid associated types that differ per impl; use `Box<dyn Trait>` only when runtime dispatch is genuinely needed.

If async traits are required: Use native async traits (Rust 1.75+); fall back to `async-trait` crate for older MSRV.

If build times are slow: Split into smaller crates; use `cargo-nextest` for faster test runs; enable incremental compilation in dev profile.

If FFI boundary is needed: Isolate all `unsafe` in a dedicated module; wrap in a safe Rust API immediately; document all invariants.

If deadlock is suspected in async code: Avoid holding `std::sync::Mutex` across `.await`; use `tokio::sync::Mutex` for async-aware locking.

## References
- [Community Patterns](references/community-patterns.md)
