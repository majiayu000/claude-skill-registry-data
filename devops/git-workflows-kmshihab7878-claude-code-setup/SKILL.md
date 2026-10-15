---
name: git-workflows
description: >
  Git and GitHub workflow patterns, commit conventions, branching strategies, and PR best practices.
  Use when making commits, creating branches, opening PRs, or resolving conflicts.
---

# git-workflows

Git and GitHub workflow patterns.

## how to use

- `/git-workflows`
  Apply these conventions to all git operations in this conversation.

- `/git-workflows <context>`
  Review the context against rules below and suggest improvements.

## when to apply

Reference these guidelines when:
- writing commit messages
- creating or naming branches
- opening or reviewing pull requests
- resolving merge conflicts
- deciding between rebase and merge
- running destructive git commands

## rule categories by priority

| priority | category | impact |
|----------|----------|--------|
| 1 | commit conventions | critical |
| 2 | branching strategy | critical |
| 3 | PR best practices | high |
| 4 | conflict resolution | high |
| 5 | destructive commands | critical |
| 6 | repository hygiene | medium |

## quick reference

### 1. commit conventions (critical)

- follow Conventional Commits: `type(scope): description`
- valid types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`
- scope is optional but encouraged for multi-module repos
- description must be imperative mood, lowercase, no period
- body explains WHY, not WHAT (the diff shows what)
- breaking changes: add `!` after type/scope and `BREAKING CHANGE:` in footer
- keep subject line under 72 characters
- one logical change per commit; split unrelated changes

### 2. branching strategy (critical)

- main/master: always deployable, protected
- feature branches: `feature/<ticket>-<short-description>`
- bug fixes: `fix/<ticket>-<short-description>`
- hotfixes: `hotfix/<description>` (branch from main, merge to main + develop)
- release branches: `release/<version>` when applicable
- delete branches after merge
- never commit directly to main/master

**Decision tree**:
- Single developer, simple project: trunk-based with short-lived branches
- Team with CI/CD: GitHub Flow (main + feature branches)
- Multiple release versions: Git Flow (main + develop + feature/release/hotfix)

### 3. PR best practices (high)

- title: concise, under 70 chars, describes the change
- description: include Summary (what + why), Test Plan, and Breaking Changes
- keep PRs focused: one concern per PR
- prefer small PRs (< 400 lines changed)
- link related issues with `Closes #123` or `Fixes #123`
- request reviewers explicitly
- address all review comments before merging
- use draft PRs for work-in-progress

### 4. conflict resolution (high)

- pull/rebase frequently to minimize conflicts
- understand both sides before resolving; never blindly accept one side
- test after resolving conflicts
- for complex conflicts, discuss with the other author
- prefer `git rebase` for local-only branches to maintain linear history
- prefer `git merge` for shared branches to preserve context

### 5. destructive commands (critical)

- **never** force-push to main/master or shared branches
- **always** confirm before: `git reset --hard`, `git clean -f`, `git checkout .`, `git push --force`
- prefer `--force-with-lease` over `--force` when force-pushing
- back up work before destructive operations: `git stash` or create a backup branch
- `git reflog` is your safety net for recovering lost commits
- never use `--no-verify` to skip hooks without explicit user request

### 6. repository hygiene (medium)

- keep `.gitignore` up to date; never commit generated files, build artifacts, or secrets
- use `.gitattributes` for line ending consistency
- tag releases with semantic versioning: `v1.2.3`
- write meaningful branch descriptions for long-lived branches
- prune stale remote branches periodically: `git remote prune origin`
- keep commit history clean; squash fixup commits before merge

## common fixes

| problem | fix |
|---------|-----|
| wrong commit message | `git commit --amend` (if not pushed) |
| committed to wrong branch | `git stash`, switch branch, `git stash pop` |
| need to undo last commit | `git reset --soft HEAD~1` (keeps changes staged) |
| accidentally committed secrets | remove file, add to .gitignore, use `git filter-repo` to purge history, rotate credentials immediately |
| merge conflict in lockfile | delete lockfile, regenerate, commit |
| diverged from remote | `git pull --rebase` for linear history |
