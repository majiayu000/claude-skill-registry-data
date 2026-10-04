---
name: verify
description: Run format, lint, test, and build checks on the Rust project. Automatically invoked after completing a task or implementation step. Use this to ensure code quality before moving on.
allowed-tools: Bash, Read, Edit
---

Run the following checks sequentially, stopping on first failure:

1. **Format**: `mise run fmt`
2. **Lint**: `mise run lint 2>&1`
3. **Test**: `mise run test 2>&1`
4. **Build**: `mise run build 2>&1`

`mise run verify` chains all four in this order, which is equivalent when
nothing fails. The tasks wrap `cargo fmt --all`, `cargo clippy --all-targets --
-D warnings`, `cargo test`, and `cargo build`; call those directly only when
mise is unavailable, and note that `cargo` may not be on `PATH` without it.

## Behavior

- If format changes files, report which files were formatted
- If clippy produces warnings or errors, fix them before proceeding
- If tests fail, fix the failing tests before proceeding
- If build fails, fix compilation errors
- After all checks pass, report a brief summary: "verify: OK (fmt, clippy, test, build)"
- If any step required fixes, re-run all checks from the beginning to confirm

## When to invoke automatically

This skill MUST be run after:

- Completing any implementation task
- Before marking a task as completed (TaskUpdate status=completed)
- Before creating a commit

$ARGUMENTS
