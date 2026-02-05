---
name: auto-linter
description: Run linters/formatters on changed files and apply safe, mechanical fixes. Use in Flow 3 and Flow 4.
allowed-tools: Bash, Read, Write
---

# Auto Linter Skill

You are a helper for running formatters and linters in this repository (Rust-focused).

## Behavior

1. Run formatting and linting for Rust code:
   - Format: `cargo fmt` (allowed to modify files).
   - Lint: `cargo clippy --all-targets --all-features` (report findings; do not auto-apply fixes).

2. Prefer running on changed files when possible:
   - Use `git diff --name-only origin/main...HEAD` and filter for `*.rs`.
   - If no changed-files info is available, run `cargo fmt` and `cargo clippy` at repo root.

3. Capture output:
   - Save lint output to `lint_output.log` and a short summary to `lint_summary.md`.

4. Allowed fixes:
   - `cargo fmt` may reformat files.
   - Do not perform semantic code changes or remove tests.

5. Report back to caller with counts of warnings/errors and any files modified by formatting.

