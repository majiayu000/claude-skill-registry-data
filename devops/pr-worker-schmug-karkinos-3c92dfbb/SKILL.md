---
name: pr-worker
description: Spawn a Claude worker to address PR feedback, fix CI failures, or continue work on a pull request. Use when a PR needs updates based on review comments or failing checks.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# PR Worker Skill

Spawn a Claude worker to address PR feedback or continue PR work.

## Usage

```
/pr-worker <pr-number>
/pr-worker <pr-number> --review    # Address review comments
/pr-worker <pr-number> --ci        # Fix CI failures
```

## Examples

```
/pr-worker 123
/pr-worker 123 --review
/pr-worker 123 --ci
```

## Instructions

When the user invokes `/pr-worker`, follow these steps:

### 1. Fetch PR Details

```bash
gh pr view <pr-number> --json number,title,body,headRefName,baseRefName,state,reviewDecision,statusCheckRollup,reviews,comments
```

### 2. Determine Work Type

Based on flags or auto-detect:
- `--review`: Focus on addressing review comments
- `--ci`: Focus on fixing CI failures
- Default: Analyze PR state and decide

### 3. Get Existing Worktree or Create One

Check if worktree for this branch already exists:
```bash
git worktree list | grep <headRefName>
```

If not, create one:
```bash
BRANCH="<headRefName>"
WORKTREE_PATH="../artemis-pr-<number>"
git worktree add "$WORKTREE_PATH" "$BRANCH"
```

### 4. Build Task Prompt

#### For Review Comments (`--review`):

```bash
gh pr view <number> --comments
gh api repos/{owner}/{repo}/pulls/<number>/comments
```

Build prompt:
```
You are addressing review feedback on PR #<number>: <title>

## Review Comments to Address
<list of unresolved comments with file paths and line numbers>

## Your Task
1. Address each review comment
2. Make the requested changes
3. Commit with message: "fix: address PR review feedback"
4. Do NOT push - the orchestrator will handle that
```

#### For CI Failures (`--ci`):

```bash
gh pr checks <number>
gh run view <failed-run-id> --log-failed
```

Build prompt:
```
You are fixing CI failures on PR #<number>: <title>

## Failed Checks
<list of failed checks with error logs>

## Your Task
1. Analyze the CI failure logs
2. Fix the issues causing failures
3. Commit with message: "fix: resolve CI failures"
4. Do NOT push - the orchestrator will handle that
```

### 5. Spawn Worker

```bash
cd "$WORKTREE_PATH" && claude --print --dangerously-skip-permissions "$PROMPT"
```

### 6. Report and Push

After worker completes:
1. Show commits made
2. Offer to push: `git push origin <branch>`
3. Show updated PR status

```bash
git push origin <branch>
gh pr checks <number>  # Verify CI is running
```

## Notes

- PR workers reuse existing worktrees if the branch exists
- Worker should NOT force push or amend existing commits
- Always show diff before pushing
- CI worker may need multiple iterations if fixes introduce new failures
