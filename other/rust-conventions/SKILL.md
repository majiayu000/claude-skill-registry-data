---
name: rust-conventions
description: "Use when writing or reviewing Rust: type and API design, errors versus panics, unsafe and FFI, ownership and async, tests, the Cargo project layout and the supply chain, performance."
---

# rust-conventions

Step 6 of the pipeline (`WORKFLOW.md`). Frames the writing and review of Rust code. Every rule below holds in
a repo with **nothing installed beyond the toolchain** (`CONVENTIONS.md`, rule A): the compiler, `clippy` and
`rustfmt` are enough to check most of it.

**Special status**: like `go-conventions`, there is no in-house production experience behind this block yet.
The content comes from three published guideline sets (read on 2026-10-02, see `references/origin.md`),
not from real review feedback. Treat it as a solid base to be confronted with the first real Rust project, not
as proven doctrine. `samwise` reads it in a question register until that happens.

**Two kinds of Rust code, two registers.** A *library* (a crate other crates depend on) carries the whole
public-API discipline of §1, §2 and §5. An *application* (a binary nobody depends on) relaxes the error and
API rules (§2.9) but keeps everything about `unsafe`, panics, supply chain and tests. Say which one the diff
is before applying a row.

## When
As soon as Rust code is written or modified, during `code` (6) or `tdd` (5).

## Steps

**Read only the sections the task actually touches.** The rules live one file per section under
`references/`; a section read is a section that has to be applied.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Types and public API design | a type, a constructor, a signature, a trait, a name or a public re-export is written | [`01-types-and-api.md`](./references/01-types-and-api.md) |
| 2 | Errors and panics | a function can fail, a `Result` or `Option` is unwrapped, a panic or an error type is introduced | [`02-errors-and-panics.md`](./references/02-errors-and-panics.md) |
| 3 | Unsafe and FFI | an `unsafe` block, a raw pointer, `Send`/`Sync` by hand, `Drop`, a binding to C or a callback from C appears | [`03-unsafe-and-ffi.md`](./references/03-unsafe-and-ffi.md) |
| 4 | Ownership, concurrency, async | a smart pointer is exposed, a static is added, a task runs long, a future is public | [`04-ownership-concurrency-async.md`](./references/04-ownership-concurrency-async.md) |
| 5 | Tests, documentation, logging | a test is written, a public item is documented, a diagnostic is emitted | [`05-tests-docs-logging.md`](./references/05-tests-docs-logging.md) |
| 6 | Project, tooling, supply chain | `Cargo.toml`, a feature, a dependency, a lint level or a CI gate changes | [`06-project-tooling-supply-chain.md`](./references/06-project-tooling-supply-chain.md) |
| 7 | Performance and macros | a hot path, an allocation pattern, a benchmark or a macro is written | [`07-performance-and-macros.md`](./references/07-performance-and-macros.md) |

## Output / checkpoint
Code compliant with the sections above, and `cargo fmt --check`, `cargo clippy --all-targets` with the lint
set of §6.2 and `cargo test` with no new finding introduced by the diff. For code that contains `unsafe`, the
checkpoint also names the interpreter-level check that was or was not run (§3.7). Checked by `gate` (7) and
`review` (8).

## Guardrails
No comments in the code produced; the few places where a rule below asks for a written reason (the
preconditions of an `unsafe` item, a lint `reason`) use a declaration docblock or the attribute's own `reason`
field, not an inline comment.
Never loosen a lint level, never add `#[allow]` to get a diff through: that is a project decision. These rules
govern **new** code; existing code stays until migrated deliberately. This block has not met a real Rust
project: if a rule here diverges from an observed need, fix this block.

## Origin
Rules mined from three published guideline sets, rewritten in the house voice; the full provenance, licences
and source stamps are in [`references/origin.md`](./references/origin.md). Read it when checking whether a rule
is still current, not when applying one.
