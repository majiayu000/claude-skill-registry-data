---
name: setup-branch
description: Create branch, push to origin, optionally use worktree for dirty trees
user-invocable: false
model: haiku
allowed-tools: Bash, Read
---

# setup-branch

Model-invocable skill for creating and pushing branches.

## Purpose

Create a new branch from the current HEAD, push to origin with tracking, and handle dirty working trees via worktree or stash.

You DO the branch operations. You do NOT make decisions about branch naming — that comes from the caller.

## Input

Receive from agent:
- `branch_name` — Full branch name (e.g., `feature/42-add-oauth-login`)
- `issue_number` — Associated issue number (for reference only)
- `push_to_origin` — Whether to push (default: true)

## Process

### 1. Check Working Tree

```bash
git status --porcelain
```

Count changed files and lines to assess dirty state.

### 2. Check Branch Doesn't Exist

```bash
git branch --list "{branch_name}"
git ls-remote --heads origin "{branch_name}"
```

If branch exists locally or remotely, return error immediately.

### 3. Create Branch

**If clean tree:**

```bash
git checkout -b "{branch_name}"
```

**If dirty tree — assess scope:**

```bash
# Count changed files
git status --porcelain | wc -l
# Count changed lines
git diff --stat | tail -1
```

- **Minor changes** (≤5 files AND ≤100 lines): Stash, create branch, pop stash
  ```bash
  git stash push -m "garura: pre-branch stash for {branch_name}"
  git checkout -b "{branch_name}"
  git stash pop
  ```

- **Significant changes** (>5 files OR >100 lines): Use worktree
  ```bash
  git worktree add "../{repo-name}-{branch_slug}" -b "{branch_name}"
  ```

### 4. Push to Origin

If `push_to_origin` is true:

```bash
git push -u origin "{branch_name}"
```

### 5. Verify

```bash
git branch --show-current
git config --get branch.{branch_name}.remote
git config --get branch.{branch_name}.merge
```

## Output

Produce output using template: `templates/branch-output.md`

**IMPORTANT**: This skill produces operation results. The calling agent receives this output and decides what to do next. Do NOT instruct the agent to return or stop.

## Reference

Load branching conventions from: `reference/branching.md`

## Constraints

- NEVER force push
- NEVER delete existing branches
- NEVER modify existing branch content
- ALWAYS verify branch was created successfully before reporting
- ALWAYS check for existing branch before creating

## Version

| Field | Value |
|-------|-------|
| Version | 1.0.0 |
| Category | operations |
