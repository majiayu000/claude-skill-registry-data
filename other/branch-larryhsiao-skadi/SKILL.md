---
name: branch
description: Use when the user runs /branch [target] [strategy] to switch to a target branch, safely handling uncommitted work first.
purpose: Switches to a target branch, safely stashing or committing uncommitted work first.
stage: forge
---

# Switch Branch

Switches to a target branch, handling uncommitted changes before checkout.

## Arguments

`/branch [target] [strategy]`

- `target`: branch name to switch to. If omitted, ask the user.
- `strategy`: `temp` or `stash`. Defaults to `temp` if not provided.
  - `temp` — stage all changes and create a commit with message `"temp"` before switching
  - `stash` — stash all changes before switching

## Workflow

### 1. Parse arguments

- Extract `target` and `strategy` from arguments.
- If `strategy` is not provided or not one of `temp`/`stash`, default to `temp`.

### 2. Resolve target branch

If `target` was provided, use it directly.

If not provided, ask via AskUserQuestion:
- `dev`
- `demo`
- `release`
- Other (user types a custom branch name)

### 3. Check working tree

```bash
git status --porcelain
```

If output is empty, the tree is clean — skip to step 5.

### 4. Handle uncommitted changes

**If strategy is `temp`:**

```bash
git add -A
git commit -m "temp"
```

**If strategy is `stash`:**

```bash
git stash push -m "auto-stash before switching to TARGET_BRANCH"
```

### 5. Switch branch

```bash
git checkout TARGET_BRANCH
git pull
```

If checkout fails (branch doesn't exist locally or remotely), tell the user and stop.

## Rules

- Never discard changes — always commit or stash before switching
- Default strategy is `temp` when not specified
- Always `git pull` after checkout
