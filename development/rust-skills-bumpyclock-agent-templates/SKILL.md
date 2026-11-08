---
name: rust-skills
description: Rust guidance for ownership, APIs, concurrency, and safety. Use when writing, reviewing, or refactoring Rust code.
license: MIT
metadata:
  author: leonardomso
  version: "1.5.1"
  sources:
    - Rust API Guidelines
    - Rust Performance Book
    - Rust 2024 Edition Guide
    - The Rustonomicon
    - ripgrep, tokio, serde, polars, axum, cargo codebases
---

# Rust guidance

Use the repository's Rust edition, MSRV, libraries, and conventions.
Read only rule files relevant to the current decision.
Treat rule summaries as guidance with constraints, not automatic refactor requirements.
Preserve unsafe-code invariants, safety comments, and public API contracts.
Measure performance before changes to optimization settings or data structures.

## Select a category

Locate matching files under `rules/` by prefix.
Use [the full catalog](RULES.md) only when you need summaries to select a rule.

| Decision | Prefixes |
| --- | --- |
| Ownership or allocation | `own-`, `mem-` |
| Error propagation | `err-` |
| Unsafe code or FFI | `unsafe-` |
| Public APIs, types, or traits | `api-`, `type-`, `trait-` |
| Async or concurrent work | `async-`, `conc-` |
| Numeric operations or conversions | `num-`, `conv-` |
| Compile-time expressions | `const-` |
| Serialization | `serde-` |
| Patterns, macros, or callbacks | `pat-`, `macro-`, `closure-` |
| Collections | `coll-` |
| Names, documentation, or diagnostics | `name-`, `doc-`, `obs-` |
| Performance or compiler optimization | `perf-`, `opt-` |
| Project layout or lints | `proj-`, `lint-` |
| Tests | `test-` |
| Suspected anti-pattern | `anti-` |
