---
name: worktrees
version: 1.0.0
description: |
  worktree, git worktree, isolated branch, separate copy, work in isolation,
  parallel branch, feature isolation, worktree setup.
  Create isolated git worktrees for feature work with auto-detected project setup.
argument-hint: [branch-name]
allowed-tools:
  - Bash
  - Read
  - Glob
  - AskUserQuestion
---

# Git Worktrees

Create isolated git worktrees for feature work. The worktree gets its own directory, branch, and dependencies — your main workspace stays clean.

## Step 1: Determine branch name

If `$ARGUMENTS` has a branch name, use it. Otherwise, use AskUserQuestion:
> What should the feature branch be called? (e.g., `feat/new-auth`, `fix/login-bug`)

## Step 2: Choose worktree directory

Check these locations in order:

1. **CLAUDE.md** — look for a `worktree-dir` or similar convention.
2. **Existing worktrees** — run `git worktree list` to see where previous worktrees live. Use the same parent directory.
3. **Default** — `../worktrees/<branch-name>` (sibling to the repo root).

If none of the above resolve clearly, ask via AskUserQuestion:
> Where should the worktree be created? Default: `../worktrees/<branch-name>`

## Step 3: Safety checks

Before creating:

1. Verify the target directory doesn't already exist.
2. Verify the branch doesn't already exist (`git branch --list <name>`).
3. If the worktree parent is inside the repo, verify it's in `.gitignore`. **Do not create worktrees inside the repo without gitignore coverage.**

## Step 4: Create the worktree

```bash
git worktree add <path> -b <branch-name>
```

If branching from a specific base:
```bash
git worktree add <path> -b <branch-name> origin/main
```

## Step 5: Project setup

Auto-detect and run the appropriate setup in the new worktree:

```bash
cd <worktree-path>
```

| Signal | Setup Command |
|---|---|
| `package-lock.json` | `npm install` |
| `pnpm-lock.yaml` | `pnpm install` |
| `yarn.lock` | `yarn install` |
| `Cargo.toml` | `cargo build` |
| `requirements.txt` | `pip install -r requirements.txt` |
| `pyproject.toml` | `poetry install` or `pip install -e .` |
| `go.mod` | `go mod download` |

If no lock file or manifest is found, skip setup.

## Step 6: Verify baseline

Run the project's test suite to confirm the worktree starts clean:

```bash
# Auto-detect from package.json scripts, Makefile, etc.
npm test  # or equivalent
```

If tests fail on a fresh worktree, warn the user — the base branch may have issues.

## Step 7: Report

```text
Worktree created:
  Branch:   <branch-name>
  Location: <absolute-path>
  Base:     origin/main
  Setup:    <package manager> install completed
  Tests:    passing (or N failures on base)

To work in the worktree: cd <path>
To clean up later: /ship clean (removes gone branches + worktrees)
```

## Gotchas

- **Worktrees share the same `.git` database.** Commits in one are visible in others via `git log --all`. But uncommitted changes are isolated.
- **Never create a worktree inside the repo** without gitignore coverage — it will show up as untracked files.
- **`/ship clean` handles worktree cleanup.** It removes worktrees for branches marked as `[gone]` on remote.
- **Node modules are NOT shared.** Each worktree needs its own `npm install`. This is by design — different branches may have different dependencies.
- **If the worktree directory already exists**, the command will fail. Check first and report clearly rather than trying to recover.
