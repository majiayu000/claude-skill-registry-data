---
name: sdd-using-git-worktrees
description: Use when starting feature work that needs isolation from current workspace or before executing implementation plans - ensures an isolated workspace exists via native tools or git worktree fallback
disable-model-invocation: true
metadata:
    opencode/autoinvoke: false
---

# Using Git Worktrees

## Overview

Ensure work happens in an isolated workspace. Prefer your platform's native worktree tools. Fall back to manual git worktrees only when no native tool is available.

**Core principle:** Detect existing isolation first. Then use native tools. Then fall back to git. Never fight the harness.

**Announce at start:** "I'm using the sdd-using-git-worktrees skill to set up an isolated workspace."

## Step 0: Detect Existing Isolation

**Before creating anything, check if you are already in an isolated workspace.**

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
BRANCH=$(git branch --show-current)
```

**Submodule guard:** `GIT_DIR != GIT_COMMON` is also true inside git submodules. Before concluding "already in a worktree," verify you are not in a submodule:

```bash
# If this returns a path, you're in a submodule, not a worktree — treat as normal repo
git rev-parse --show-superproject-working-tree 2>/dev/null
```

**If `GIT_DIR != GIT_COMMON` (and not a submodule):** You are already in a linked worktree. Skip to Step 2 (Project Setup). Do NOT create another worktree.

Report with branch state:

- On a branch: "Already in isolated workspace at `<path>` on branch `<name>`."
- Detached HEAD: "Already in isolated workspace at `<path>` (detached HEAD, externally managed). Branch creation needed at finish time."

**If `GIT_DIR == GIT_COMMON` (or in a submodule):** You are in a normal repo checkout.

Has the user already indicated their worktree preference in your instructions? If not, ask for consent before creating a worktree:

> "Would you like me to set up an isolated worktree? It protects your current branch from changes."

Honor any existing declared preference without asking. If the user declines consent, work in place and skip to Step 2.

## Step 1: Create Isolated Workspace

**You have two mechanisms. Try them in this order.**

### 1a. Native Worktree Tools (preferred)

The user has asked for an isolated workspace (Step 0 consent). Do you already have a way to create a worktree? It might be a tool with a name like `EnterWorktree`, `WorktreeCreate`, a `/worktree` command, or a `--worktree` flag.

**Constraint even with native tools:** Worktrees MUST still be under `$ROOT/.worktrees`. Before using a native tool, verify its configured location:

```bash
ROOT=$(git rev-parse --show-toplevel)
# check tool's default path — if it would place outside $ROOT/.worktrees, do NOT use it without asking
```

If the native tool would place the worktree in `~/`, in the parent directory of `$ROOT`, or anywhere outside `$ROOT/.worktrees`, STOP and ask the user for permission to override or fall back to Step 1b. Never silently accept a home-dir or parent-dir location.

Native tools handle directory placement, branch creation, and cleanup automatically. Using `git worktree add` when you have a native tool creates phantom state your harness can't see or manage.

Only proceed to Step 1b if you have no native worktree tool available, or the native tool's location violates the strict `.worktrees` policy.

### 1b. Git Worktree Fallback

**Only use this if Step 1a does not apply** — you have no native worktree tool available. Create a worktree manually using git.

#### Directory Selection

**STRICT POLICY — project-local `.worktrees` only. No exceptions.**

The ONLY allowed location is `<project-root>/.worktrees` where `<project-root>` is the output of `git rev-parse --show-toplevel`.

**FORBIDDEN locations — MUST NEVER use:**

- Home directory: `~/`, `$HOME`, `~/.worktrees`, `~/worktrees`, or any path under `$HOME` outside the project
- Parent directory of the project root: `../worktrees`, `../.worktrees`, `$(dirname $ROOT)/worktrees`, or any sibling/parent path
- Any absolute path that is not `$ROOT/.worktrees/...`
- `worktrees/` without dot (deprecated — do not create, do not use; if it exists from legacy, ignore it and use `.worktrees` only)

Resolution:

1. **Resolve project root:**

    ```bash
    ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
    ```

2. **Check if the allowed directory exists:**

    ```bash
    ls -d "$ROOT/.worktrees" 2>/dev/null
    ```

    If it exists, use `LOCATION="$ROOT/.worktrees"`.

3. **If it does NOT exist — ASK BEFORE CREATING:**
   Do NOT create the directory and do NOT run `git worktree add` until the user explicitly approves. Ask via the `question` tool (or direct prompt if no tool):

    > "The `.worktrees` directory does not exist at `$ROOT/.worktrees`. May I create it? Worktrees will only be created there — nowhere else (not in home directory or parent directory)."
    - If user approves: `mkdir -p "$ROOT/.worktrees"` then proceed to Safety Verification.
    - If user declines: work in place and skip to Step 2. Honor the main/master branch consent rule (`sdd-subagent-driven-development` / `sdd-executing-plans` require explicit consent to work on main/master in place).

#### Safety Verification

**MUST verify `$ROOT/.worktrees` is ignored before creating worktree:**

```bash
git check-ignore -q "$ROOT/.worktrees" 2>/dev/null || git check-ignore -q .worktrees 2>/dev/null
```

**If NOT ignored:** Add `.worktrees/` to `$ROOT/.gitignore`, commit the change, then proceed.

**Why critical:** Prevents accidentally committing worktree contents to repository.

#### Create the Worktree

```bash
ROOT=$(git rev-parse --show-toplevel)
LOCATION="$ROOT/.worktrees"
path="$LOCATION/$BRANCH_NAME"

# SAFETY CHECK — refuse forbidden locations before running git
case "$path" in
  "$ROOT/.worktrees/"*) ;;
  *) echo "ERROR: worktree path must be under $ROOT/.worktrees — refused: $path (home/parent dirs forbidden)" >&2; exit 1 ;;
esac

# Extra guard: reject home or parent even if ROOT resolution failed
case "$path" in
  "$HOME"/*) echo "ERROR: worktree under HOME forbidden: $path" >&2; exit 1 ;;
  "$(dirname "$ROOT")"/*)
    # allow only if it's still under ROOT/.worktrees (already checked above)
    # this catches ../worktrees misuse
    if [[ "$path" != "$ROOT/.worktrees/"* ]]; then
      echo "ERROR: worktree in parent directory forbidden: $path" >&2; exit 1
    fi
    ;;
esac

git worktree add "$path" -b "$BRANCH_NAME"
cd "$path"
```

**Sandbox fallback:** If `git worktree add` fails with a permission error
(sandbox denial), tell the user the sandbox blocked worktree creation and
ask whether to proceed in the current directory. Never silently work in
place: if the current branch is main/master, the executor's
explicit-consent rule still applies (both
`sdd-subagent-driven-development` and `sdd-executing-plans`
require it), and if the user declines, stop rather than work in place.
Once the user consents, run setup and baseline tests in place.

## Step 2: Project Setup

Auto-detect and run appropriate setup:

```bash
# Node.js
if [ -f package.json ]; then npm install; fi

# Rust
if [ -f Cargo.toml ]; then cargo build; fi

# Python
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
if [ -f pyproject.toml ]; then poetry install; fi

# Go
if [ -f go.mod ]; then go mod download; fi
```

## Step 3: Verify Clean Baseline

Run tests to ensure workspace starts clean:

```bash
# Use project-appropriate command
npm test / cargo test / pytest / go test ./...
```

**If tests fail:** Report failures, ask whether to proceed or investigate.

**If tests pass:** Report ready.

### Report

```
Worktree ready at <full-path>
Tests passing (<N> tests, 0 failures)
Ready to implement <feature-name>
```

## Quick Reference

| Situation                                                            | Action                                                                          |
| -------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Already in linked worktree                                           | Skip creation (Step 0)                                                          |
| In a submodule                                                       | Treat as normal repo (Step 0 guard)                                             |
| Native worktree tool available but points outside `$ROOT/.worktrees` | STOP — ask user, or fall back to 1b                                             |
| Native worktree tool available and under `$ROOT/.worktrees`          | Use it (Step 1a)                                                                |
| No native tool                                                       | Git worktree fallback (Step 1b)                                                 |
| `$ROOT/.worktrees/` exists                                           | Use it (verify ignored)                                                         |
| `$ROOT/.worktrees/` missing                                          | ASK user for permission to `mkdir -p $ROOT/.worktrees` — do NOT create silently |
| `worktrees/` (no dot) exists                                         | Ignore it — only `.worktrees` is allowed                                        |
| Home dir `~/worktrees` or parent `../worktrees`                      | FORBIDDEN — refuse, force `$ROOT/.worktrees`                                    |
| Directory not ignored                                                | Add `.worktrees/` to `.gitignore` + commit                                      |
| Permission error on create                                           | Sandbox fallback, ask before working in place                                   |
| Tests fail during baseline                                           | Report failures + ask                                                           |
| No package.json/Cargo.toml                                           | Skip dependency install                                                         |

## Common Rationalizations

| Excuse                                                         | Reality                                                                                                                                                                  |
| -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| "I'm obviously not in a worktree — no need to check"           | Run Step 0. Harness-created isolation and submodules both fool eyeballing; the detection commands settle it.                                                             |
| "`git worktree add` is quicker than hunting for a native tool" | A native tool (e.g. `EnterWorktree`) owns placement, branching, and cleanup. Bypassing it is the #1 mistake — it creates phantom state your harness can't see or manage. |
| "The worktree directory is surely ignored already"             | Run `git check-ignore` on `$ROOT/.worktrees`. An unignored worktree directory commits the whole tree into the repo.                                                      |
| "Any directory name works"                                     | ONLY `$ROOT/.worktrees` is allowed. `~/`, `../`, and `worktrees/` are forbidden.                                                                                         |
| "I'll just put it in `~/worktrees` for convenience"            | FORBIDDEN — home directory worktrees are explicitly disallowed. Use `$ROOT/.worktrees`.                                                                                  |
| "Parent dir keeps the project clean"                           | FORBIDDEN — parent-directory worktrees are explicitly disallowed. Use `$ROOT/.worktrees`.                                                                                |
| "`.worktrees` doesn't exist, I'll create it silently"          | ASK FIRST — must get user permission via `question` tool before `mkdir -p $ROOT/.worktrees`.                                                                             |
| "The workspace is fresh — baseline tests can wait"             | A dirty baseline makes every later failure ambiguous. Run the tests now; proceeding past failures is your human partner's call.                                          |
