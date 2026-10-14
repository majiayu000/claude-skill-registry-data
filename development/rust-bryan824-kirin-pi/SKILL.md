---
name: rust
description: "When writing, refactoring, testing, or configuring Rust — follow Bryan's toolchain, error-handling, crate, API-design, and structure preferences and the standard verification gate."
allowed-tools: Bash(cargo:*) Bash(rustup:*) Bash(rustc:*) Read Edit Write Grep Glob
---

# Rust

Write small, idiomatic, readable Rust for Bryan's projects — clear over clever.
Respect the repo's toolchain, and prove changes with the standard gate before
calling them done. Each principle below has a reference; load it when a change
goes deep in that area, not for routine edits.

Resist: hiding errors with `unwrap`/`expect`/`panic`/`assert` on user-controlled input,
adding crates that don't cut real complexity, clever code.

- Respect repo `rust-toolchain.toml`/`rust-toolchain` first; `rustup` for toolchains,
  `cargo` for tasks. Scan before edits: `rustup show active-toolchain`,
  `cargo metadata --no-deps --format-version 1`, `cargo check`; read `AGENTS.md`, architecture, README.
- Errors are typed and surfaced — libraries return `Result<T, Error>` with typed errors;
  apps print a concise top-level error and exit non-zero. A detected programming bug or
  broken invariant panics; genuinely fallible input returns `Result`. Prefer `snafu`; avoid
  `anyhow`/`thiserror` unless the project already uses them; hand-implement
  `std::error::Error` in zero-dep projects. Depth: `references/ERRORS.md`.
- Add a crate only when it reduces meaningful complexity, and say why; avoid broad
  frameworks in small CLIs. Preferred picks by task: `references/CRATES.md`.
- Keep `src/main.rs` thin (parse → call lib → print); logic in `src/lib.rs`, modules by
  domain (parser, renderer, cli, error). Use the strongest type as early as possible
  (`&str`/`Path` over `String`/`PathBuf`, newtypes over loose primitives); validate bounds
  before slicing; `*::from_le_bytes` for binary; test malformed input and edge offsets.
  Idiomatic API, library, and doc design: `references/API_DESIGN.md`. For `unsafe`/FFI:
  `references/SAFETY.md`. For hot paths: `references/PERFORMANCE.md`.
- Verify before done: `cargo fmt -- --check`, `cargo clippy --all-targets -- -D warnings`,
  `cargo test`, `cargo check` (add `rustfmt`/`clippy` components if missing). Recommended
  lint config and deeper checks (`cargo-audit`/`-hack`/`-udeps`, Miri): `references/VERIFICATION.md`.

Deliver: the change, why any new crate earned its place, and the verification results.
