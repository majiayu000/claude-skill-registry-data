---
name: rust-testing
description: Use when writing or running Rust unit tests with cargo or nextest. Apply for crate-level tests that live beside modules, smoke tests for new crates, or when choosing cargo test vs cargo nextest. Do not use for GUI/TUI product-specific test frameworks.
capability: "Write and run generic Rust unit tests with cargo or nextest"
side_effect_level: local_write
approval_required: false
requires_tools: "cargo; optional cargo-nextest; project AGENTS.md test command"
output_schema: "Test command, file layout, and pass/fail evidence"
risk_class: medium
---

# Rust testing

## Purpose

Generic cargo/nextest unit-test conventions for rust-stack projects. Prefer the repo's `TEST_CMD`
from `AGENTS.md` when it is more specific.

## When to Use

- Adding or changing crate-level Rust tests.
- Choosing `cargo test` vs `cargo nextest run`.
- Placing tests beside a module or under `tests/`.

Do **not** use this skill for product-specific GUI, TUI, or integration harnesses. Those belong in
repo-local skills.

## Required Tools

- `cargo`
- `cargo nextest` when `nextest.toml` or `.config/nextest.toml` exists
- The project `TEST_CMD` from `AGENTS.md`

## Workflow

1. Read `AGENTS.md` for the canonical test command. If `nextest.toml` exists, prefer
   `cargo nextest run`; otherwise `cargo test`.
2. Put unit tests next to the module (`*_tests.rs` or an inline `#[cfg(test)]` module) unless the
   crate already uses `tests/` integration tests.
3. Run the narrowest command first (`cargo test <name>` or `cargo nextest run -E 'test(<name>)'`).
4. Keep one behavior per test; cover error paths, not only the happy path.

## Agent-Safe Patterns

- Do not disable or weaken tests to go green.
- Do not run workspace-wide test suites when a single crate or filter is enough.
- Format/clippy stay on the lint skill (`cargo fmt --check`, `cargo clippy`).

## Verification Checklist

- [ ] Used the repo `TEST_CMD` or a documented subset
- [ ] Targeted test failed for the intended reason before the fix (when adding coverage)
- [ ] Targeted test passed after the change

Resolve helper paths from this skill directory. Run project commands from the target workspace.
