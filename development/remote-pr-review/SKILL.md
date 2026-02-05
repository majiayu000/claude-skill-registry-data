---
name: remote-pr-review
description: Create a dedicated worktree for a GitHub PR (use `wf` for openai/openai workforests, `wt` for all other repos), check out the PR locally, run `codex review` plus a PAL `mcp__pal__precommit` review against the PR base, then merge both into one actionable review summary.
---

# Remote PR Review

## Overview

Create a clean, throwaway worktree for a PR, then run two independent review passes (`codex review` and PAL precommit) and merge the feedback into one prioritized set of fixes.

## Inputs

- `pr`: PR number or URL (preferred)
- `repo`: optional `OWNER/REPO` (used when `pr` is a number and you’re not already in the target repo)
- `repo-dir`: optional local repo path (required for non-openai/openai PRs if you aren’t already in that repo)
- `extra`: optional focus areas (perf, security, API, tests, etc.)

## Quick start

- Prepare a `pr-review-<pr-number>` worktree and print JSON:
  - `python "<path-to-skill>/scripts/prepare_pr_worktree.py" --pr "<number-or-url>" --json`
  - If `--pr` is just a number and you’re not in the target repo, add `--repo "<owner/repo>"`.
  - For non-openai/openai repos, add `--repo-dir "<path-to-local-clone>"` when needed.

The JSON includes at least: `worktree_dir`, `repo`, `pr_number`, `base_ref`, `head_ref`, `pr_url`.

## Workflow

### 1) Create / reuse the PR worktree

- Run `prepare_pr_worktree.py`.
- If it fails due to a dirty worktree/repo, stop and either clean it up or delete the worktree and retry.

### 2) Run Codex review (CLI)

- `cd <worktree_dir>`
- Ensure base ref exists locally (pick the right remote for the repo; prefer `upstream` if present, else `origin`):
  - `git fetch <remote> <base_ref>`
- Run review and capture the full output as `codex_review`:
  - Default prompt (if the user didn’t provide one):
    - `codex review --base "<remote>/<base_ref>" "Review for correctness, security, performance, tests, and maintainability. Prioritize issues (blockers vs suggestions vs nits) and reference files/paths when possible."`
  - If the user provided extra focus areas, append them to the prompt.

### 3) Run PAL precommit review (tool)

- Call `functions.mcp__pal__precommit` against the PR base (not staged/unstaged):
  - `path`: `<worktree_dir>`
  - `compare_to`: `"<remote>/<base_ref>"`
  - `precommit_type`: `"external"`
  - `severity_filter`: `"all"`

Capture the output as `pal_review`.

### 4) Merge feedback and present a single review

- Deduplicate overlapping findings; reconcile disagreements (call them out explicitly).
- Prioritize into:
  - **Blockers (must fix)**: correctness, security, data loss, breaking API/ABI, missing tests, CI failures.
  - **High-signal improvements**: maintainability, performance, edge cases, observability.
  - **Nits**: style/consistency (only if low-noise).
- Provide a short **verification checklist** (tests to run, manual steps, roll-out risk).

## Cleanup (optional)

- openai/openai (workforest): `wf rm pr-review-<pr-number> -y`
- other repos (git worktree): `wt rm "<worktree_dir>" -f` (or `git -C "<repo-dir>" worktree remove "<worktree_dir>"`)
