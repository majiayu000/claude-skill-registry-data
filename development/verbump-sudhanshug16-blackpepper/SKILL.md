---
name: verbump
description: Bump the Blackpepper version, review full git diffs (including unrelated changes), craft a Conventional Commit message, and push the current branch. Use when the user asks to "verbump", "bump version", "increment version", "release", or explicitly requests version bump + commit + push for this repo.
---

# Verbump

## Overview

One-shot bump: update `crates/blackpepper/Cargo.toml`, review the full diff (including unrelated changes), commit with a clean message, and push the current branch.
For this project, commits are the changelog.

## Workflow

1. Pick target version (no confirmation prompt)
   - If the user specifies a version, use it.
   - If the user says "verbump" or "bump", default to a patch bump and proceed.
   - Only ask for clarification if the user explicitly asks for a major/minor bump without giving a version.

2. Review repository state and diffs
   - Run `git status -sb`.
   - Review complete diffs with `git diff --stat` and `git diff`.
   - If unrelated changes exist, call them out and confirm whether they should be included. Do not revert changes unless explicitly requested.

3. Bump the version
   - Update only `crates/blackpepper/Cargo.toml`.
   - Keep edits ASCII-only and preserve file formatting.
   - Re-check with `rg -n "version" crates/blackpepper/Cargo.toml` if needed.

4. Validate and re-check diffs
   - Re-run `git status -sb` and `git diff --stat`.
   - Ensure only expected files changed before committing.
   - If tests are run, report results; if skipped, state why.

5. Commit and push
   - Stage the relevant files (usually `crates/blackpepper/Cargo.toml`, plus anything already expected).
   - Craft a Changelog style Commit message.
   - `git commit -m "<message>"`.
   - `git push` the current branch.

## Output expectations

- Always report the chosen version and the final commit message.
- Summarize any unrelated diffs you saw and whether they were included.
