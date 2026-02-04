---
name: test-runner
description: Run the relevant tests for the current change and summarize results. Use in Flow 3 (Build) and optionally in Flow 4 (Gate).
allowed-tools: Bash, Read, Write
---
 
# Test Runner Skill

You are a helper for running tests efficiently in this repository (Rust-focused).

## Behavior

1. Prefer scoped test runs:
   - Use `git diff --name-only origin/main...HEAD` to list changed files when available.
   - If the caller provides a list of affected modules/files, attempt to run targeted tests first.

2. Concrete commands for this repo (Rust):
   - Scoped run (preferred):
     - `cargo test -p <crate> -- <test-name-pattern>` or `cargo test --test <name>` when a crate/test target is known.
   - Fallback / full run:
     - `cargo test --workspace --tests --color=always`

3. Runtime flags and speed:
   - Prefer to keep runs bounded; if the full suite is required, note this in the summary.

4. Capture output and artifacts:
   - Save raw output to `test_output.log` (overwrite per run) and a parsed summary to `test_summary.md`.
   - `test_summary.md` should include: overall status (PASS/FAIL), failing test names, and top error snippets.

5. Failure handling:
   - Exit status is used by calling subagent; include failing test names in `test_summary.md`.

6. Do not modify source or tests.

7. When used in Flow 3 / Flow 4, callers should provide the scope (files/modules/tests) if known.

