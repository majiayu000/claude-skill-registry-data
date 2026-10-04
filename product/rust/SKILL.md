---
name: rust
description: "Applies Rust rules for ownership, modules, errors, unsafe code, concurrency, tests, and tooling."
---

# Skill: rust

## Purpose

Apply the shared engineering style to Rust projects while preserving idiomatic ownership, error handling, module structure, and safety.

## Inspect First

Before changing Rust code, inspect relevant files when present:

- `Cargo.toml`
- `Cargo.lock`
- `.cargo/config.toml`
- `rust-toolchain.toml`
- `rustfmt.toml`
- `clippy.toml`
- workspace layout
- existing modules and tests

Infer:

- edition;
- workspace structure;
- feature flags;
- dependency policy;
- error handling conventions;
- async runtime if present.

## Tooling Defaults

- Prefer `cargo nextest run` over `cargo test` when `cargo-nextest` is installed
  and compatible with the workspace.
- Use `bacon` for local interactive feedback loops when available.
- Use `cargo watch` for focused watch commands when available and useful.
- Do not introduce these tools as required project dependencies unless the user
  asks or the repository already standardizes on them.

## Style

- Follow existing module organization.
- Keep modules cohesive.
- Avoid giant `mod.rs` or `lib.rs` files.
- Prefer explicit domain names over generic `utils` modules.
- Keep public API surface intentionally small.
- Prefer simple ownership over lifetime acrobatics.

## Error Handling

- Use `Result` for recoverable failures.
- Do not `unwrap` or `expect` in production paths unless the invariant is proven and the message explains it.
- In tests, `unwrap`/`expect` may be acceptable when failure context is clear.
- Preserve error context.
- Use the repository's established error type approach.
- Do not introduce `anyhow`, `thiserror`, or custom error stacks unless already used or justified.

## Safety

- Avoid `unsafe`.
- If `unsafe` is necessary, isolate it, document invariants, and test the safe wrapper.
- Do not create undefined behavior for performance fantasies.

## Ownership and APIs

- Prefer borrowing over cloning when simple.
- Clone intentionally when it improves clarity or avoids complex lifetimes.
- Avoid exposing unnecessary concrete types in public APIs.
- Use traits when they express real abstraction or test seams.
- Do not create traits for one implementation unless boundary value is clear.

## Async

If async code is present:

- respect existing runtime;
- avoid blocking calls in async tasks;
- handle cancellation/drop behavior;
- avoid detached tasks without lifecycle management;
- use timeouts where external calls can hang.

## Tests and Validation

Common commands, only when configured or clearly available:

```bash
cargo nextest run
cargo test
cargo test --workspace
cargo fmt --check
cargo clippy --workspace --all-targets --all-features
cargo check
bacon
cargo watch -x test
```

Report exact commands and results.
## Shared Cross-Ecosystem Style


Apply the shared engineering style from:

- `../../engineering/05_design_principles.md`
- `../../engineering/06_responsibility_model.md`
- `../../engineering/07_complexity_budget.md`
- `../../engineering/12_naming_bible.md`

Language-specific idioms control syntax and ecosystem details, but they must not weaken the core rules: small cohesive units, explicit boundaries, honest validation, no dumping grounds, and no fake placeholders.
