---
name: worktree-start
description: Start work on a GitHub issue using a git worktree. Use when starting a new feature or fix from an issue number.
---

# Start Worktree — Issue → Worktree → Branch

Follow these steps to start working on a GitHub issue.

## Step 0 — Should you use a worktree?

| Situation | Use worktree? | Why |
|-----------|---------------|-----|
| New feature (> 1 hour of work) | YES | Isolate from presentation |
| Bug fix that needs separate PR | YES | Clean diff, easy review |
| Hotfix while mid-feature | YES | Don't stash, don't lose context |
| Next lot of an epic (e.g. #158) | YES | Each lot = separate branch/PR |
| Quick fix (< 30 min, same scope) | NO | Commit directly on presentation |
| Minor bug in same PR scope | NO | Fix in current PR, `Refs #N` |

If NO → inform the user and suggest committing directly with `Refs #N`.

## Step 1 — Fetch issue info

```bash
gh issue view $ARGUMENTS
```

Extract:
- The **title** to name the branch (slug en kebab-case)
- The **type**: feat / fix / refactor / test / chore
- The **labels** for context
- Check if this issue mentions a **parent epic** (e.g. "Parent: #158")

## Step 2 — Update presentation locally

```bash
git fetch origin
git checkout presentation
git pull origin presentation
```

**Never use `develop` or `main` as base for this project. Always use `presentation`.**

## Step 3 — Create the worktree

Folder format: `../KLASSCIv2-issue-<N>`
Branch format: `issue-<N>-<slug>`

Example for issue #42 "Add filière liaison modal":
- Folder: `../KLASSCIv2-issue-42`
- Branch: `issue-42-filiere-liaison-modal`

```bash
git worktree add ../KLASSCIv2-issue-<N> -b issue-<N>-<slug> origin/presentation
```

Verify with:
```bash
git worktree list
```

## Step 4 — Configure commit author in the worktree

```bash
cd ../KLASSCIv2-issue-<N>
git config user.name "James10192"
git config user.email "djedjelipatrick@gmail.com"
```

## Step 5 — Copy .env if it exists

```bash
cp ../KLASSCIv2/.env ../KLASSCIv2-issue-<N>/.env 2>/dev/null || true
```

## Step 6 — Confirm to user

Output:
```
Worktree created:
  Folder : ../KLASSCIv2-issue-<N>
  Branch : issue-<N>-<slug>
  Base   : origin/presentation
  Author : James10192 <djedjelipatrick@gmail.com>
  Issue  : #<N> — <title>
  Epic   : #<P> — <parent title> (if linked)

Workflow:
  1. Code in ../KLASSCIv2-issue-<N>/
  2. /commit (auto-adds Refs #<N>)
  3. /create-pr (links to issue + epic)
  4. /worktree-finish <N>
```

## Rules

- **Never work directly on `presentation`, `main`, or `develop`**
- Always base from `origin/presentation` (not local, not develop)
- Worktree is a sibling directory: `../KLASSCIv2-issue-<N>` (one level above the repo)
- Branch naming: `issue-N-slug` (no type prefix)
- Commit author must be set in the worktree: `James10192 <djedjelipatrick@gmail.com>`
- NEVER `git add .` or `git add -A` — always stage files explicitly
- NEVER "Generated with Claude Code" or "Co-Authored-By" in commits

$ARGUMENTS
