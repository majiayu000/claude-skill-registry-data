---
name: rust-best-practices
description: Implement, refactor, or debug Rust with attention to ownership, error contracts, API compatibility, and safety. Use for substantive Rust code changes; use rust-review for review-only requests. Simple conceptual questions do not require this workflow.
---

# Rust best practices

Produce idiomatic Rust that satisfies the requested behaviour and the project's contracts. Follow repository instructions, established conventions, and supported toolchains. Keep changes scoped; do not replace working architecture or introduce dependencies solely to satisfy a preference here.

## Establish the contract

Read the affected code, tests, Cargo manifests, toolchain configuration, and relevant CI commands. Identify the edition, minimum supported Rust version (MSRV), deployment targets, feature combinations, and whether the changed interface has downstream consumers. A `lib.rs` alone does not imply a published compatibility promise.

Before refactoring, establish observable behaviour and relevant failure semantics. Preserve public signatures, errors, output, and feature behaviour unless the request authorises changes. A panic-to-error conversion can change a public signature; explain the migration rather than assuming it is compatible. Add focused regression coverage for demonstrated bugs or fragile behaviour.

## Implement with explicit contracts

- Prefer clear concrete types and direct code. Use enums or newtypes when they prevent meaningful invalid states or unit confusion; introduce traits and builders for actual variation or construction needs.
- Borrow when reading, use mutable borrows for in-place updates, and consume by value when storing or transferring ownership. Prefer `&str` and slices when callers need no container-specific operations. Choose generic conversion/iterator parameters only when their flexibility earns the complexity.
- Start with unique ownership. Use `Arc`, `Rc`, locks, and interior mutability when sharing or mutation is intentional. Their presence in an API is a design question, not automatically a defect. Before cloning to resolve a borrow conflict, consider shortening the borrow, separating disjoint state, or moving with `take`/`replace`; deliberate cheap copies are valid.
- Use `Option` for normal absence, `Result` for expected failures, and panics for violated internal invariants. Check whether external input can violate a claimed invariant. A justified `expect` should explain the invariant; do not mechanically replace every `unwrap` or promise panic-free behaviour without evidence.
- Preserve actionable error context and causal chains. Public error types should support the contracts callers need, normally `Display` and `Error`; require `Send`, `Sync`, or `'static` when the execution/API model needs them. Prefer typed errors when callers inspect failures; error erasure can be intentional. Do not add an error framework by default.
- Keep visibility narrow and public APIs intentional. Implement applicable standard traits and conversion conventions; use fallible conversions when validation can fail. Keep `Eq`, `Ord`, `PartialOrd`, and `Hash` consistent over the same semantic value. Derived implementations are fine when consistent with custom ones.
- Treat public fields, trait bounds, enum variants, feature behaviour, and exposed dependency types as compatibility decisions. Follow existing API conventions; do not add sealing, `non_exhaustive`, or new wrappers without considering their costs.
- Bound work and resource consumption for untrusted input. Check parser sizes, allocation growth, retries, and partial-failure cleanup where relevant; safe Rust does not prevent resource exhaustion.
- Handle integer range and conversion semantics explicitly at trust boundaries. Choose checked, saturating, wrapping, or fallible operations according to the contract. A numeric `as` cast can truncate; do not confuse truncation with a panic.
- Prefer readable iteration and pattern matching over mechanical rewrites between loops, combinators, and `match`. Avoid speculative abstraction and unmeasured optimisation. Keep externally visible ordering deterministic when the contract requires it.
- Document public contracts that types cannot express: failure modes, panics, safety obligations, side effects, and meaningful ownership or complexity constraints. Examples should demonstrate realistic error handling. Follow existing documentation conventions instead of imposing a template on every private helper.

## Load specialised guidance only when relevant

Read the corresponding reference before making decisions in these areas; do not load every reference for ordinary edits:

- Changing an externally consumed API or feature surface: [API and Cargo](references/api-and-cargo.md).
- Async execution, shared state, cancellation, or blocking work: [Concurrency](references/concurrency.md).
- Unsafe code, raw pointers, foreign layouts, or unwinding boundaries: [Unsafe and FFI](references/unsafe-and-ffi.md).

These files contain additional task-specific checks, not optional substitutes for the core contracts above.

## Validate the change

Use the project's documented validation commands and supported feature/target matrix. For ordinary changes, run formatting, relevant Clippy checks, and focused tests; broaden to integration, documentation, or workspace checks when affected. Use `cargo fmt --check` when inspecting and `cargo fmt` when editing, keeping unrelated formatting out of the diff.

If the repository defines no commands, start with `cargo fmt --check`, `cargo clippy --all-targets`, and `cargo test` from the appropriate workspace/package. Enable warnings-as-errors only according to project policy or for a clean changed scope. Do not assume `--all-features` is a supported configuration. For public documentation, build docs and run relevant doctests; a documentation build alone does not execute examples or automatically deny missing documentation.

For a bug fix, verify the regression test fails on the original behaviour and passes with the fix when practical. Use properties, boundary inputs, and independent expected results rather than mirroring implementation branches. Use Miri, fuzzing, or benchmarks when the affected risk justifies them, without claiming those tools prove complete correctness.

Inspect the final diff for accidental API changes, unrelated edits, suppressed diagnostics, and unsupported language features. Separate existing failures from regressions. Report changed behaviour, checks actually run, and material validation gaps. Do not report success for commands that were skipped or failed.

## Attribution

Adapted from Morgan Linton's BeautifulRust; see [NOTICE.md](NOTICE.md) for provenance and [LICENSE](LICENSE) for the retained MIT notice.
