---
name: fp-review
description: >-
  Phase 3 of the feature-pipeline suite. Run this after /fp-implement has pushed
  all commits and printed the M2 stop hook. Spawns a sandboxed sub-agent (HEAVIER)
  in an isolated worktree to run RED/GREEN tests against the PR diff and post a
  structured review comment. Use when you need an independent agent to verify
  correctness of implementation changes before CI runs — especially for schema
  mutations, CLI surface changes, or doc-touching commits. Triggers on: "review
  the PR", "run sandbox review", "fp-review", "Phase 3", "check the implementation",
  "validate the changes", "run tests on the PR", or any instruction to verify
  what /fp-implement just pushed.
version: 3.0.0
---

# fp-review  (Phase 3 — Sandbox Review)

Spawn HEAVIER in an isolated worktree to run RED/GREEN tests, then post a
structured review comment to the PR. This phase is read-and-comment only —
no commits leave this phase.

The sandbox isolation matters: it prevents a flawed review from dirtying the
working branch, and it forces HEAVIER to reproduce failures from a clean state
rather than relying on local cache.

## Setup

```bash
STATE=".agents/skills/feature-pipeline/scripts/state.sh"
branch=$($STATE get branch)
pr=$($STATE get prNumber)
phase=$($STATE get phase)
```

Confirm `phase == 4` (set by /fp-implement on completion). If it is not 4,
print a clear message explaining the pipeline order and end your turn — running
out of order will produce a review against incomplete or wrong commits.

## HEAVIER brief

Spawn HEAVIER with `isolation: worktree` on `$branch`. Give it exactly this
brief (substitute variables):

> You are reviewing PR #$pr on branch $branch. Your job is to verify each
> changed public surface with RED/GREEN tests, then post a review comment.
> Do not push any commits.
>
> 1. Read the full diff:
>    ```bash
>    git diff origin/main...HEAD
>    ```
>
> 2. For each changed public surface (function, CLI flag, schema field):
>    a. Write a RED test that FAILS before the fix. Verify this by temporarily
>       reverting that change, running the test, then re-applying it.
>    b. Write a GREEN test that PASSES with the fix in place.
>
> 3. For schema-touching commits, run:
>    ```bash
>    gaia dev validate
>    ```
>
> 4. For doc-touching commits, run:
>    ```bash
>    gaia dev docs --check
>    ```
>
> 5. Post this exact comment structure to the PR via `gh pr comment`:
>
> ```markdown
> ## Sandbox Review
>
> ### RED tests
> | Description | Result | Notes |
> |-------------|--------|-------|
>
> ### GREEN tests
> | Description | Result | Notes |
> |-------------|--------|-------|
>
> ### Issues found
> - [ ] <description> — `<file>:<line>`
>
> ### Verdict: APPROVE / REQUEST CHANGES
> ```

After HEAVIER finishes, capture the comment URL from its output.

## Phase completion

```bash
$STATE set reviewCommentUrl "<url>"
$STATE set phase 5
```

Print the M3 stop hook and end your turn:

```
╔══ STOP HOOK M3 ══════════════════════════════════════════════════════════════╗
║  Sandbox review posted — PR #<N>                                             ║
║  Review the comment, then run /fp-iterate to address findings + watch CI.   ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## Constraints

- If HEAVIER fails to spawn, write `.fp-handover.md` with the diff URL and
  branch name so a human can complete the review manually. End your turn — do
  not attempt the review yourself; the sandbox isolation is the point.
- Do not push any commits. This phase is read + comment only.
