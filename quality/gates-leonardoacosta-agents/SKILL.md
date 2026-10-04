---
name: gates
description: Select and run the smallest relevant set of quality checks for a change, recording fresh evidence and handling failures truthfully.
---

# Gates

Quality gates enforce evidence, not a fixed architecture pipeline.

## Stages

1. Inspect the proposal, changed files, dependency edges, and risk.
2. Select checks by changed surface:
   - source/types → format, lint, typecheck
   - Rust source → use the repository-pinned toolchain and its configured formatter and linter (commonly rustfmt via `cargo fmt` and Clippy via `cargo clippy`). Check `rust-toolchain.toml`, contributor/agent instructions, and CI workflows for the repository's exact commands and flags. Run focused tests for behavior changes.
   - behavior → focused unit/integration tests
   - API or schema contract → contract/integration tests and migration checks
   - UI behavior → focused browser or component tests
   - build/config/package → build and packaging checks
   - security-sensitive code → appropriate security analysis and review
3. Run cheap, deterministic checks first; defer expensive checks until prerequisites pass.
4. Record exact command, revision, scope, result, and relevant output.
5. Classify failures as implementation, environment, flaky, or unrelated; never hide a failure.
6. After repair, rerun the failed gate and any dependent gates.

A repository may require broader gates for release, high-risk, or cross-cutting changes. Do not claim full-suite confidence from targeted checks.

## Working Tree Gate

Run this gate for both modes:

- **My-change-only:** account for every status line caused by the current change. Explicitly name
  pre-existing dirt that is intentionally out of scope.
- **Whole-tree:** account for every status line in the tree before declaring the gate clean.

In either mode, run `git status --short` and require no unexplained dirt. Run `git diff --check`
and require clean whitespace and conflict-marker checks. Run `git diff --stat` and summarize its
result in the gate record, including the scope used. A dirty tree is not a failure when every line
is accounted for, but an unaccounted line blocks the gate.
