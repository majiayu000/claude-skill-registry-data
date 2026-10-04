---
name: cleanup-build-artifacts
description: Removes transient build artifacts this task produced in the ironlint repo before declaring work done. Use at the end of any task that ran `cargo build --release`, `cargo mutants`, `cargo llvm-cov`, generated a one-off binary, wrote a scratch file like `pr.diff` or an ad-hoc tarball, or any other throwaway output. Do NOT use to wipe the actively-iterating `target/` directory.
metadata:
  author: chris
  version: 1.0.0
  category: workflow
  tags: [ironlint, rust, cleanup, disk-hygiene]
---

# Cleanup Build Artifacts

Sweep up the transient artifacts *this task* produced so the working tree and disk stay clean. Implements the AGENTS.md / AGENTS.md rule: "Clean up build artifacts you produced once the task is done."

## Scope

**In scope** — artifacts created during this task:
- Release binaries built for one-off verification (`target/release/<bin>`)
- `cargo mutants` output (`mutants.out/`, `mutants.out.old/`)
- `cargo llvm-cov` reports (`target/llvm-cov-target/`, generated `lcov.info` / HTML report dirs)
- Scratch files at the repo root: `pr.diff`, `*.diff`, ad-hoc `*.tar`/`*.tar.gz`, throwaway `*.log`, `scratch_*`, `tmp_*`
- One-off binaries built outside `target/` (e.g. via `--out-dir`)
- Temporary fixture dirs created for an investigation that aren't checked in

**Out of scope — DO NOT TOUCH:**
- The persistent `target/` debug tree being actively iterated on (`cargo build`, `cargo test` incremental output). Leave it.
- Anything tracked by git that's modified (M) or staged — those are real work.
- `.ironlint/` runtime state unless the task explicitly created it for a one-off check.
- Pre-existing files in the working tree the task didn't author.

If unsure whether something is yours, leave it.

## Instructions

### Step 1: Enumerate what this task produced

Before cleaning, list candidates. Run these in parallel:

```bash
# Untracked files that appeared during the task
git status --short --untracked-files=normal

# Release binaries (likely candidates if you ran `cargo build --release`)
ls -la target/release/ 2>/dev/null | grep -v -E '^(d|total|\.|deps|build|examples|incremental)'

# Mutants output
ls -d mutants.out* 2>/dev/null

# Coverage output
ls -d target/llvm-cov-target lcov.info coverage/ 2>/dev/null

# Repo-root scratch files
ls *.diff *.tar *.tar.gz *.log scratch_* tmp_* 2>/dev/null
```

Cross-reference with what the conversation actually did. If you didn't run `cargo mutants` this task, leave `mutants.out/` alone — it belongs to a prior run.

### Step 2: Confirm before destructive operations

If the list contains anything non-obvious (e.g. a `.diff` you don't recognize, a binary you didn't build, an `.ironlint/` directory with data), surface it to the user before deleting. The user's AGENTS.md says investigate-before-deleting when finding unfamiliar state.

For artifacts clearly produced this turn, proceed without asking.

### Step 3: Remove with the right command

| Artifact | Command |
|---|---|
| One-off release binary | `rm target/release/<binary-name>` (NOT `rm -rf target/release/`) |
| All artifacts for one crate (when you `cargo build --release -p X`) | `cargo clean -p <crate-name>` |
| `cargo mutants` output | `rm -rf mutants.out mutants.out.old` |
| `cargo llvm-cov` output | `cargo llvm-cov clean --workspace` |
| Scratch diff/tar/log at repo root | `rm <file>` (one at a time, named explicitly) |
| Throwaway fixture directory | `rm -rf <explicit-path>` |

Rules:
- Always pass explicit paths. Never `rm -rf target/`, never `rm *.rs`, never globs that could match tracked files.
- Use `cargo clean -p <crate>` rather than `rm -rf target/release/` so the rest of `target/` survives.
- One `rm` per logical artifact unless they're clearly the same family (e.g. `mutants.out` + `mutants.out.old`).

### Step 4: Verify

```bash
git status --short
du -sh target/ 2>/dev/null
```

The diff to `git status` should be limited to whatever real work the task did — no leftover untracked scratch files. `target/` may still be large; that's expected (it's the working tree).

If a release binary was rebuilt at ~30MB+ purely to verify behavior and is now gone, mention the freed space in the end-of-turn summary.

## Examples

### Example 1: Built a release binary to spot-check CLI output

User asked to verify that `ironlint check` exits 2 on a Block verdict. The task ran `cargo build --release` and `./target/release/ironlint check tests/fixtures/...`.

Actions:
1. `ls target/release/ironlint` — confirm it exists
2. `cargo clean -p ironlint-cli` — drops the binary and its build cache for the cli crate
3. `git status --short` — confirm no other scratch files

Result: `target/release/ironlint` gone, `target/debug/` (the iterating tree) untouched.

### Example 2: Ran `cargo mutants` on a diff

The task ran `git diff main.. > pr.diff && cargo mutants --in-diff pr.diff`.

Actions:
1. `rm pr.diff`
2. `rm -rf mutants.out mutants.out.old`
3. `git status --short` — clean

Result: 2MB+ of mutants output and the diff file gone.

### Example 3: Task only edited source files

The task added a new `pub fn` and a test, ran `cargo test -p ironlint-core`, all green.

Actions:
1. `git status --short` — only the intentional file edits show
2. No artifacts to remove. `target/debug/` stays (it's the iterating tree).

Result: Skill no-ops cleanly. Don't invent work.

## Troubleshooting

### `cargo clean -p <crate>` says "package not found"

Cause: Wrong crate name. The workspace has `ironlint-core` and `ironlint-cli`; the binary is `ironlint` but the package is `ironlint-cli`.

Solution: Check `Cargo.toml` `[package] name =` fields, or `cargo metadata --no-deps --format-version 1 | jq '.packages[].name'`.

### `git status` still shows scratch files after cleanup

Cause: The files match a pattern in `.gitignore` (e.g. `mutants.out*/` is ignored) so `git status` won't show them even when present. Re-run `ls` from Step 1 to confirm physical removal.

Solution: Trust the filesystem check, not just `git status`.

### Found an unfamiliar `.ironlint/` or scratch directory you didn't create

Cause: Prior session or another tool produced it.

Solution: Don't delete. Surface it to the user: "Found `<path>` — not from this task, leaving it. Want me to remove?"
