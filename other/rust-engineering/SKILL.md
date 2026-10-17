---
name: rust-engineering
description: Write production Rust — ownership done right, no unwrap in prod paths, clippy-clean, tested error paths.
version: 1
triggers: rust, write rust, ownership, clippy, rust code
category: Engineering & code
blurb: Write production Rust — ownership done right, no unwrap in production paths, clippy-clean, tested errors.
archetype: knowledge
example: Write this in idiomatic, production-grade Rust.
---

# Rust Engineering

Rust's compiler is a teammate: let it carry correctness. Use ownership as a design tool, and treat every `unwrap` as a promise you must keep.

## When to use
- Services, CLIs, hot paths, WASM, and security-sensitive components.
- Rewrites where C/C++ memory risk is the problem.

## Method
1. **Design with ownership**: borrow before cloning; keep lifetimes local; prefer owned data at boundaries, borrows within.
2. **Errors are types**: enums + `thiserror` for libraries, `anyhow` for binaries; `?` for propagation; **no `unwrap`/`expect` on fallible paths** (tests and startup-time invariants excepted, with messages).
3. **Clippy gate**: `cargo clippy -- -D warnings`; `cargo fmt --check`; fix lints, don't silence them without reason.
4. **Unsafe policy**: forbid by default; where needed, isolate in a module, document the invariant, and add tests — `unsafe` is a contract.
5. **Workspaces**: split crates when boundaries are real; feature flags kept minimal (no default bloat).
6. **Async**: structured tasks with `tokio`; no blocking calls inside async; bounded channels; timeouts everywhere.
7. **Testing**: unit tests beside code, integration tests in `tests/`, doc tests for examples; test the error paths; criterion for benches.
8. **Supply chain**: `cargo audit`; pinned MSRV; review new crates (`dependency-governance`).

## Quality gates
- [ ] clippy clean with `-D warnings`; fmt clean.
- [ ] Tests green including failure/error paths.
- [ ] Zero `unwrap`/`expect` in production paths.
- [ ] Every `unsafe` block documented + tested.

## Red lines
- No blocking work inside async runtimes.
- No unbounded channels or spawn-loops without backpressure.

## Related
`c-engineering`/`cpp-engineering` (FFI) · `secure-build-pattern` · `testing-strategy`.
