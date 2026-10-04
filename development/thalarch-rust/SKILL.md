---
name: thalarch-rust
description: >
  Project-aware Rust engineering for libraries, services, CLIs, async applications, and
  systems code. Use for Rust source, Cargo workspaces/features, ownership/lifetimes, unsafe
  code, concurrency, tests, performance, or Rust-specific refactoring.
---

# Thalarch Rust

Use the repository's toolchain/MSRV, Cargo features, async runtime, lint policy, and architecture.
Do not require the newest edition or rewrite working code merely to use newer syntax.

## Preflight

Inspect:

- `Cargo.toml` workspace/package structure;
- `rust-toolchain*` and MSRV policy;
- feature flags/default features;
- async runtime and ecosystem dependencies;
- `clippy`/format/test/CI configuration;
- generated/FFI/unsafe boundaries.

## Ownership and API design

Prefer ownership/borrowing that makes lifetime and mutation intent obvious.

- Avoid cloning solely to appease the borrow checker without understanding ownership.
- Avoid complex lifetime machinery when a simpler owned boundary is clearer and acceptable.
- Preserve public error and feature contracts.
- Use enums/newtypes where they eliminate invalid states or ambiguous primitives.
- Keep trait abstractions tied to real polymorphism/generic requirements rather than speculative flexibility.

## Errors

- Use `Result`/`?` for recoverable failure propagation.
- Add context at boundaries where it helps operators/callers.
- Do not `unwrap`/`expect` on production paths unless the invariant is truly impossible to violate and the reason is evident.
- Preserve error source chains where the project ecosystem supports them.

## Unsafe and FFI

Treat `unsafe` as a separate proof obligation.

For every new/changed unsafe block:

- state the invariant that makes it sound;
- identify pointer/aliasing/lifetime/thread-safety assumptions;
- keep the unsafe surface minimal;
- prefer a small safe wrapper around it;
- run targeted tests/sanitizer/Miri-style tools if the repository already supports them or the risk warrants setup.

Do not expand unsafe code as a performance guess.

## Async/concurrency

Preserve the existing runtime (Tokio/async-std/smol/etc.) unless the task explicitly changes it.
Review task ownership, cancellation, blocking calls on async executors, channel backpressure,
shared-state locking, `Send`/`Sync` assumptions, and task leaks.

## Testing

Use unit/integration/doc tests according to the contract. Add property/fuzz tests for parsers,
protocols, codecs, state machines, or invariant-heavy code when tooling is available/justified.

Run repository-native `cargo test`; use `cargo fmt --check`, `cargo clippy`, feature-matrix tests,
or target checks when configured and relevant.

## Performance

Profile/benchmark before optimizing. Examine allocations/copies, algorithmic complexity, lock
contention, async scheduling, I/O, serialization, and cache behavior. Use the project's benchmark
stack when present.

## Verification

Report the toolchain/feature/target combination actually tested. A default-feature host build
does not prove optional features or cross-target behavior.
