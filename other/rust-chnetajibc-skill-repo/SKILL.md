---
name: rust
description: "Idiomatic Rust engineering: ownership/borrowing/lifetimes, traits, Result/Option, Tokio/Axum/Serde, Cargo workspaces, testing/benches. Use for Rust work; never transliterate Java/Python architectures."
---

# rust

Ownership is the design tool: encode invariants in types so illegal states do not compile.

## Activate when

- Writing, reviewing, or testing Rust; choosing async runtime, web framework, serialization; Cargo workspace decisions.

## Do NOT activate for

- Syntax-only questions (rustc + `cargo doc` answer those faster).

## Procedure

1. Version: detect edition/toolchain from Cargo.toml/Cargo.lock/rust-toolchain.toml; research in https://doc.rust-lang.org/ (Book, std, Cargo) for that toolchain. Never assume latest-stable features on pinned toolchains.
2. Ownership design: borrow by default; lifetimes describe real relationships, not appeasement (`'static` sprawl is a smell); `Clone` only where duplication is semantically right (`Arc` for shared ownership, channels for handoff).
3. Errors: `Result`/`Option` with `?`; `thiserror` for libraries, `anyhow` for applications (confirm versions first); no `unwrap`/`expect` outside tests and proven invariants.
4. Traits/generics: small trait bounds, behavior-first; generics with static dispatch preferred; dynamic dispatch (`dyn`) only at real heterogeneity points.
5. Async: Tokio runtime chosen deliberately; `Send`/`Sync` understood, not fought; no blocking calls inside async (use `spawn_blocking`); backpressure on channels.
6. Web/serde: Axum handlers as thin extractors + typed errors (see https://docs.rs/axum/ for the pinned version); Serde derives with explicit renames/deny-unknown-fields at trust boundaries (see https://serde.rs/).
7. Cargo: workspaces with shared lockfile; features additive; `cargo test`, `clippy -D warnings`, `cargo fmt --check`; benches with criterion or std harness for perf claims.
8. Unsafe/FFI: `unsafe` minimal, documented invariants, Miri-tested where feasible; FFI boundaries validated on both sides.
9. Verify: `cargo test` + clippy + fmt green; perf claims backed by bench numbers; unsafe blocks listed in the PR.

## Failure modes

- Fighting the borrow checker instead of remodeling ownership; hidden blocking in async; `unwrap` in library code; feature unification surprises across workspace members.

## References
- Registry: `../../research/documentation-search/references/framework-registry.yaml` (rust, tokio, axum, serde).
