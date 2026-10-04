---
name: review-local-changes
description: Comprehensive review and audit of uncommitted local code changes in git working copy (staged, unstaged, untracked). Use when asked to review local changes, audit git diff, check uncommitted work before commit/PR/push, or inspect working copy edits for potential bugs, security issues, formatting, or regression risks.
---

# Review Local Code Changes

Use this skill to perform a thorough, evidence-based review of uncommitted local code modifications in the working repository.

---

## 🚫 HARD RULE — Rust commands (OOM / system freeze)

LibrAgent `src-tauri/tests/*.rs` files are **separate Cargo test binaries** (~600MB+ each with Tauri). Linking many at once OOMs even a **32GB** machine.

### NEVER (any time)

| Forbidden                                                                                                       | Why                                               |
| --------------------------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| `cargo test`                                                                                                    | Multi-target link graph → OOM                     |
| `cargo test --tests`                                                                                            | Same, worse                                       |
| `cargo test --all` / bare `cargo test` in `src-tauri/`                                                          | Same                                              |
| `cargo clippy` / `cargo build` / `cargo check` raw                                                              | Use pnpm wrappers (jobs/nice caps)                |
| Assuming “full suite needs `--test` only” and skipping `pnpm rust:test` when the user asked for full validation | Full suite is safe **only** via sequential runner |

### When to run what

Default **code review / local-change audit** is **diff-based static analysis**. Do **not** start heavy tests or builds unless the user explicitly asks (e.g. “테스트 돌려봐”, “run tests”, commit/PR readiness with tests). That matches `.agents/AGENTS.md` / `GEMINI.md`.

| Command                                   | When allowed                                                                                                                      |
| ----------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `pnpm rust:fmt:check` / `pnpm rust:check` | Optional light gates during review if useful                                                                                      |
| `pnpm rust:clippy`                        | Only when user asked for lint/validation of Rust                                                                                  |
| `pnpm rust:test --test <target>`          | When user asked to test; use while iterating                                                                                      |
| `pnpm rust:test`                          | When user asked for full / functional verification — sequential, OOM-safe. **Not** the default for a plain “review local changes” |

If the user **did** ask for tests: prefer touched `--test <target>` first; use full `pnpm rust:test` when they want the whole suite. Fmt/check alone is **not** a functional audit in that case.

`pnpm rust:test` without `--test` is **safe** (sequential). Raw `cargo test --tests` is **not**.

If you (or another agent) already started a raw `cargo test --tests` and the machine is thrashing: **stop it**; switch to `pnpm rust:test --test <name>`.

**Target name** = basename of a root `src-tauri/tests/<name>.rs` (e.g. `text_encoding_tests`). Modules under `tests/integration/` are **not** their own Cargo targets — filter the monolith: `pnpm rust:test --test integration_tests -- workspace_skill_access_regression_tests` (Linux/macOS only; `integration_tests` skipped on Windows).

---

## Workflow

### 1. Identify Working Copy State

Run git commands to inspect modified, staged, and untracked files:

```bash
git status -s
git diff --stat
```

- Distinguish between **staged** changes (`git diff --cached`), **unstaged** changes (`git diff`), and **untracked files**.
- If a target branch or base branch is specified (e.g., `main`), check branch context using `git branch --show-current`.

### 2. Extract and Inspect Detailed Diffs

Retrieve full diffs for analysis:

- For unstaged edits: `git diff`
- For staged edits: `git diff --cached`
- For all uncommitted working tree changes: `git diff HEAD`
- For untracked files: read file contents if relevant to the change context.

If the diff is large (>300 lines), analyze file by file or by functional area to avoid missing subtle bugs.

### 3. Analyze Code Changes

Evaluate changes against [references/review-checklist.md](references/review-checklist.md) covering:

1. **Correctness & Logic**: Functional intent, edge cases, error handling, async/concurrency.
2. **Type Safety & Contracts**: Explicit types, Zod/schema validations, interface alignment.
3. **Leftovers & Cleanliness**: Unintended `console.log`, `dbg!`, commented code, hardcoded credentials.
4. **Security & Safety**: Command injection, path traversal, secrets leakage.
5. **Performance & Architecture**: Unnecessary re-renders, resource leaks, breaking changes.
6. **Rust test / harness regressions**: new root-level `tests/*.rs` binaries without need; skill-alias write/read split; resource-unsafe scripts.

### 4. Code Health Verification

Default review stays static (diff + checklist). Run commands only when the user asked for validation/tests, or when noting what **should** be run before commit/PR:

- **TypeScript/React** (if asked): `pnpm lint`; `pnpm test:run` if frontend behavior changed.
- **Rust** (if asked) — follow the HARD RULE above for **which** commands are safe:
  1. `pnpm rust:fmt:check`
  2. `pnpm rust:check`
  3. `pnpm rust:clippy` (when touching Rust)
  4. Touched root targets: `pnpm rust:test --test <target>` (e.g. `text_encoding_tests`)
  5. Integration modules: `pnpm rust:test --test integration_tests -- <module_filter>`
  6. Full suite only when user asked: `pnpm rust:test` (sequential — OOM-safe)
- **🚫 NEVER** raw `cargo test` / `cargo test --tests` / raw `cargo clippy|build|check`.
- Do **not** run `pnpm refactor:validate` unless the user explicitly requested the full pipeline.

Report exact compiler errors, linter output, or failing test names if validation was run and failed. If tests were not requested, say so under Validation Status.

### 5. Structure the Review Report

Present review findings clearly in the following structure:

1. **Executive Summary**: High-level overview of modified files and purpose of changes.
2. **Critical Issues / Blockers** (if any): Logic bugs, security vulnerabilities, breaking changes, or build failures.
3. **Warnings & Code Quality** (if any): Type safety gaps, missing error handling, debug artifacts, performance concerns.
4. **Suggestions & Best Practices**: Cleanups, readability improvements, or minor refactorings.
5. **Validation Status**: Exact commands run + results (especially which `--test` targets).
6. **Verdict**: `Approved`, `Approved with minor suggestions`, or `Needs changes before commit`.
