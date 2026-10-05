---
name: pr
description: Push a branch and open a PR with pre-flight checks
user-invocable: true
---

# Push PR

Push the current branch and open a pull request, with pre-flight hygiene checks.

## Arguments

- No arguments: run all checks, push, and open PR
- `--dry-run`: run checks only, don't push or create PR
- A PR title in quotes: use as the PR title instead of generating one

## Pre-flight checks (all must pass before pushing)

Run these steps in order. Stop on first failure.

### 1. Rebase on latest main

```
git fetch origin main
git rebase origin/main
```

If rebase fails, stop and report the conflict.

### 2. Build

```
cargo build --features nalgebra
```

### 3. Clippy (deny warnings)

```
cargo clippy --all-targets --features nalgebra -- -D warnings
```

### 4. Test

```
cargo test --features nalgebra
```

### 5. Check for uncommitted changes

```
git status
```

If there are unstaged changes, stop and ask the user what to do.

### 6. Review the diff

Run `git diff origin/main...HEAD --stat` and `git log --oneline origin/main..HEAD` to summarize what's being pushed. Show this to the user.

## Push and create PR

Only after all checks pass:

1. Push the branch: `git push -u origin <branch-name>`
2. Create the PR using the GitHub MCP tool `mcp__github__create_pull_request`
3. Base branch: `main`
4. Title: use the provided title, or generate one from the commit messages
5. Body: include a `## Summary` section with bullet points describing changes, and a `## Test plan` section

## Rules

- Do NOT push to `main` directly — always use a feature branch
- Do NOT include Claude session links in the PR body or commits
- If `--dry-run` was passed, stop after the checks and report results
- If any check fails, do NOT push. Fix the issue or report it to the user.
- Keep `API_COVERAGE.md` in sync if any safe wrappers were added or changed
