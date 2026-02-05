---
name: up-to-date
description: Sync git repository with upstream. Use at the start of a session, when asked to sync, get up to date, check git status, or when working on a stale branch. Checks branch status, uncommitted changes, PR state, and upstream drift, then takes appropriate actions.
allowed-tools: Bash, Read
---

# Up To Date

Diagnose and sync the current git repository state with upstream.

## When To Use

- At the start of a new session (proactively)
- When the user says "up to date", "sync", "git status", or similar
- When you suspect you're on a stale or merged branch
- Before starting new work

## Understanding Remote Setup

First, detect the remote configuration:

```bash
git remote -v
```

**Two common setups:**

| Setup         | Remotes           | Source of Truth | Push To |
| ------------- | ----------------- | --------------- | ------- |
| Fork workflow | origin + upstream | upstream/main   | origin  |
| Direct access | origin only       | origin/main     | origin  |

**Key principle**: Always sync against the canonical source:

- If `upstream` exists → compare against `upstream/main`
- If only `origin` → compare against `origin/main`

```bash
# Detect which remote is the source of truth
if git remote | grep -q '^upstream$'; then
    SOURCE_REMOTE="upstream"
else
    SOURCE_REMOTE="origin"
fi
echo "Source of truth: $SOURCE_REMOTE/main"
```

## Diagnostic Steps

Run these checks:

```bash
# Current state
git branch --show-current
git status --porcelain
git stash list

# Fetch all remotes
git fetch --all --prune 2>&1

# Determine source remote
SOURCE_REMOTE=$(git remote | grep -q '^upstream$' && echo "upstream" || echo "origin")

# Compare against source of truth
echo "Behind $SOURCE_REMOTE/main:"
git rev-list --count HEAD..$SOURCE_REMOTE/main 2>/dev/null || echo "0"

echo "Ahead of $SOURCE_REMOTE/main:"
git rev-list --count $SOURCE_REMOTE/main..HEAD 2>/dev/null || echo "0"

# Show what landed upstream
git log --oneline HEAD..$SOURCE_REMOTE/main 2>/dev/null | head -10
```

If on a feature branch (not main), also check PR status:

```bash
gh pr view --json state,number,title,mergeable,reviewDecision 2>/dev/null || echo "NO_PR"
```

## Decision Tree and Actions

### Determine source remote first

```bash
SOURCE_REMOTE=$(git remote | grep -q '^upstream$' && echo "upstream" || echo "origin")
```

### On main branch

**With upstream remote (fork workflow):**

```bash
# Pull from upstream, push to origin to keep fork in sync
git pull upstream main
git push origin main  # Keep fork's main up to date
```

**Without upstream (direct access):**

```bash
git pull origin main
```

### On feature branch with PR

- **PR merged** → Switch to main, sync properly, delete branch (no need to ask; it's already merged):

  ```bash
  BRANCH=$(git branch --show-current)
  git checkout main

  # Sync main with source of truth
  if git remote | grep -q '^upstream$'; then
      git pull upstream main
      git push origin main  # Keep fork in sync
  else
      git pull origin main
  fi

  git branch -d "$BRANCH"
  ```

- **PR closed (not merged)** → Ask user: delete branch or keep working?

- **PR open** → Report status, show any review comments:
  ```bash
  gh pr view --json reviews,comments --jq '.reviews[-3:], .comments[-3:]'
  ```

### On feature branch without PR

- **Has commits ahead of main** → Ask if user wants to create PR
- **No commits ahead** → Ask if user wants to delete branch

### Fork is stale

If origin/main is behind upstream/main:

```bash
# Check if fork's main is behind upstream
FORK_BEHIND=$(git rev-list --count origin/main..upstream/main 2>/dev/null || echo "0")
if [ "$FORK_BEHIND" -gt 0 ]; then
    echo "Fork's main is $FORK_BEHIND commits behind upstream"
    # After pulling upstream, push to keep fork in sync
    git checkout main
    git pull upstream main
    git push origin main
fi
```

### Uncommitted changes present

- **List them clearly** with `git status`
- **Ask user** what to do: commit, stash, or discard
- Do NOT automatically commit or discard

### Stashed changes present

- **List stashes** with `git stash list`
- **Inform user** they have stashed work

## Cleanup: Delete Merged Branches

After switching to main, clean up merged branches:

```bash
git branch --merged main | grep -v '^\*' | grep -v 'main' | while read branch; do
    echo "Deleting merged branch: $branch"
    git branch -d "$branch"
done
```

## Output Format

First, report the remote setup:

```
Remote setup: Fork workflow (origin=fork, upstream=source)
```

or

```
Remote setup: Direct access (origin=source)
```

Then summarize findings in a table:

| Check                | Status           | Action            |
| -------------------- | ---------------- | ----------------- |
| Branch               | `feature-xyz`    | -                 |
| PR                   | #123 MERGED      | Switching to main |
| Uncommitted          | 2 files modified | Listed below      |
| Behind upstream/main | 5 commits        | Will pull         |
| Fork main stale      | 3 commits behind | Will sync         |

Then take the actions and report results.

## Safety Rules

- NEVER force push
- NEVER delete unmerged branches without asking (deleting merged branches is OK without asking)
- NEVER commit uncommitted changes without user approval
- NEVER discard changes without explicit user confirmation
- Always preserve user's work
- When pushing to origin after upstream pull, use regular push (not force)
