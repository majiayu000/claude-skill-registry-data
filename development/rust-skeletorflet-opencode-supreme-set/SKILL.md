---
name: rust
description: Rust systems programming skill covering ownership, borrowing, traits, error handling, async, and cargo. Use when building Rust applications.
trigger: rust, rust-lang, rustc, cargo, ownership, borrowing, traits, async rust, serde, tokio, clap
---

## rust

### Core Concepts
- Ownership + Borrowing: each value has one owner, references (&/&mut) temporarily lend access without transferring ownership
- Structs + Enums + Traits: structs for data grouping, enums for sum types with pattern matching, traits for shared behavior
- Pattern Matching: exhaustive match arms, if let for single patterns, destructuring tuples/structs/enums

### Error Handling
- Result<T, E>: recoverable errors with ? operator for propagation
- Option<T>: nullable values, unwrap/expect for prototyping, map/and_then for chaining
- Custom error types: thiserror derive for library errors, anyhow for application-level error handling

### Async & Concurrency
- async/await: zero-cost futures, tokio runtime for I/O, tasks with tokio::spawn
- Channels: tokio::sync::mpsc for multi-producer, tokio::sync::oneshot for one-shot
- Shared state: Arc<Mutex<T>> for shared mutable state across tasks

### Common Cargo Patterns
- Cargo.toml: dependencies, features, profiles (dev/release)
- Tests: #[test] attribute, #[cfg(test)] module, cargo test with --test for integration
- Common crates: serde (serialization), tokio (async runtime), reqwest (HTTP client), clap (CLI parsing)
