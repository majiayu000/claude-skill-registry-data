---
name: review-pr-comments
description: >-
  Fetches and triages PR review comments for the current branch using code-review-commons
  standards. Activated via /review-pr-comments.
---

# Review PR Comments Workflow

Fetches open pull request review comments and conversation threads for the current branch, evaluates each under `code-review-commons` standards, and presents an advisory triage report with actionable replacement diffs or draft replies.

## 0. Invocation Guard

- Activated explicitly via `/review-pr-comments` or direct requests to review/triage comments on the current branch's PR.

## 1. Branch & PR Resolution

1. Detect current repository root and branch:
   ```bash
   git rev-parse --show-toplevel
   git branch --show-current
   ```
2. Retrieve the active Pull Request via GitHub CLI:
   ```bash
   gh pr view --json number,title,url,headRefName,baseRefName,state
   ```
3. Fetch inline review comments and conversation threads:
   ```bash
   gh api repos/{owner}/{repo}/pulls/{number}/comments --paginate
   gh pr view --comments
   ```
   *Fallback:* If `gh` is unauthenticated or no PR exists for this branch, prompt user:
   > *"No active PR found via `gh`. Please supply the PR number, URL, or paste the comment thread."*

## 2. Evaluation via Code Review Commons

For each unresolved comment:
1. **Context Lookup**: Inspect the referenced file and line range using `view_file`.
2. **Apply Standards**: Evaluate strictly under [`skills/review-common/SKILL.md`](../review-common/SKILL.md) (`code-review-commons`):
   - **Substance First**: Does it identify a functional bug, security issue, race condition, or edge case?
   - **Filter Nits**: Ignore pure stylistic preferences or invalid reviewer assumptions.
   - **Severity**: Classify as **CRITICAL**, **HIGH**, **MEDIUM**, **LOW**, or **INVALID/NO FIX NEEDED**.
3. **Memory Check**: Query `node skills/review-memory/scripts/memory-store.mjs query` to respect known branch dismissals and conventions.

## 3. Advisory Triage Report

Present findings concisely without auto-modifying files:

### PR: [#<number>] <Title> (<current-branch> -> <base-branch>)

For each comment:
#### [COMMENT-<N>] `<file>:<line>` by @<reviewer>
> "<quoted comment>"

- **Assessment**: `[VALID - <SEVERITY>]` or `[DISPUTABLE / NO CHANGE NEEDED]`
- **Rationale**: 1-2 sentences on correctness and failure mode.
- **Actionable Replacement Diff** (if code change needed):
  ```diff
  - old code
  + suggested replacement code
  ```
- **Draft Reply** (if pushback, explanation, or clarification needed).
