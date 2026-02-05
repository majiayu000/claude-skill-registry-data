---
name: code-review
description: Run `codex review` plus PAL `codereview` (via the `pal-mcporter` skill) against a git base ref, then merge both outputs into one prioritized, actionable review.
---

# Code Review

## When to use

Use when you have a local git repo and a base ref to diff against (e.g. `upstream/main`, `origin/master`, or a commit SHA) and you want a single merged review from:

- `codex review`
- PAL `codereview` (run via `pal-mcporter`)

## Inputs

- `path`: repo root directory (prefer absolute)
- `compare_to`: git ref to compare against (e.g. `upstream/main`)
- `extra` (optional): focus areas (perf, security, tests, API, etc.)

## Workflow

### 1) Ensure the base ref exists locally

- `cd <path>`
- If `compare_to` is a remote ref like `upstream/main`, ensure it’s present:
  - `git fetch <remote> <branch>`

### 2) Run Codex review + PAL codereview (parallel)

These two passes are independent once `compare_to` exists locally, so run them in parallel to reduce wall-clock time.

- Codex review (capture as `codex_review`):
  - `cd <path> && codex review --base "<compare_to>"`
  - Note: the current `codex review` CLI does not accept a custom prompt when `--base` is used; run it without a prompt.
- PAL review via MCPorter (capture as `pal_review`):
  - `bash "<path-to-pal-mcporter-skill>/scripts/pal" -o markdown codereview --step "Review changes vs <compare_to>. <extra>" --step-number 1 --total-steps 1 --next-step-required false --findings "" --model auto --review-validation-type internal --review-type quick --severity-filter all --focus-on "<extra>"`

Implementation note (when tool-parallelism is available): use `multi_tool_use.parallel` to run two `functions.exec_command` calls concurrently (one for `codex review`, one for `pal ... codereview`).

### 3) Merge feedback into one review

- Deduplicate overlapping findings; reconcile disagreements (call them out explicitly).
- Prioritize into:
  - **Blockers (must fix)**: correctness, security, data loss, breaking API/ABI, missing tests, CI failures.
  - **High-signal improvements**: maintainability, performance, edge cases, observability.
  - **Nits**: style/consistency (only if low-noise).
- End with a short verification checklist (tests to run, manual steps, rollout risk).
