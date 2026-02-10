---
name: github-pr-merge
description: Merges GitHub Pull Requests after validating pre-merge checklist. Use when user wants to merge PR, close PR, finalize PR, complete merge, approve and merge, or execute merge. Runs pre-merge validation (tests, lint, CI, comments), confirms with user, merges with proper format, handles post-merge cleanup.
---

# GitHub PR merge

Merges Pull Requests after validating pre-merge checklist and handling post-merge cleanup.

## Current PR

!`gh pr view --json number,title,state -q '"PR #\(.number): \(.title) (\(.state))"' 2>/dev/null`

## Core workflow

### 1. Check comments status

Verify all review comments have at least one reply:

```bash
REPO=$(gh repo view --json nameWithOwner -q '.nameWithOwner')
PR=$(gh pr view --json number -q '.number')

# Find unreplied comment IDs
gh api repos/$REPO/pulls/$PR/comments --jq '
  [.[] | select(.in_reply_to_id) | .in_reply_to_id] as $replied |
  [.[] | select(.in_reply_to_id == null) | select(.id | IN($replied[]) | not) | .id]
'
```

**If unreplied comments exist:**
- **STOP** the merge process
- Inform user: "Found unreplied comments: [IDs]. Run github-pr-review first."
- **NEVER** reply to comments from this skill

### 2. Run validation

Run tests, linting, and verify CI checks. All **MUST** pass before proceeding.

```bash
gh pr checks $PR
```

### 3. Confirm with user

**ALWAYS show checklist summary and ask before merging:**

```
Pre-merge checklist:
- Tests: passing
- Lint: passing
- CI: green
- Comments: all replied

Ready to merge PR #X. Proceed?
```

### 4. Execute merge

```bash
gh pr merge $PR --merge --delete-branch --body "$(cat <<'EOF'
- Key change 1
- Key change 2
- Key change 3

Reviews: N/N addressed
Tests: X passed (Y% cov)
Refs: Task N, Req M
EOF
)"
```

**Merge strategy**: always `--merge` (merge commit), never squash or rebase.

`--delete-branch` automatically deletes the remote branch after merge.

### 5. Post-merge cleanup

```bash
git checkout develop && git pull origin develop
```

## Merge message format

Concise format for a clean git log:

```
- Key change 1 (what was added/fixed)
- Key change 2
- Key change 3

Reviews: 7/7 addressed (Gemini 5, Codex 2)
Tests: 628 passed (88% cov)
Refs: Task 8, Req 14-15
```

- 3-5 bullet points max for changes
- One line each for reviews summary, test results, and task references
- No headers (##), no verbose sections
- Total: ~10 lines max

## Important rules

- **ALWAYS** run tests, lint, and CI checks before merging
- **ALWAYS** verify all review comments have replies
- **ALWAYS** confirm with user before executing merge
- **ALWAYS** use merge commit (`--merge`), never squash/rebase
- **ALWAYS** delete feature branch after successful merge
- **NEVER** merge with failing tests, lint, or CI checks
- **NEVER** skip user confirmation
- **NEVER** reply to PR comments from this skill - use github-pr-review instead
- **STOP** merge if unreplied comments exist and direct user to review skill
