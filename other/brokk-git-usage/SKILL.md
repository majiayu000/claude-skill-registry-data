---
name: brokk-git-usage
description: Perform local git operations — branching, staging, committing — without modifying existing history.
---

# Git Usage

## Purpose

Local git operations for version control during implementation: branch creation, staging, committing, and history inspection. Scoped to local, forward-only operations that never modify existing git history.

## When to Use

- When starting implementation work on a new task — create a branch first.
- When staging and committing completed work.
- When inspecting repository state (status, diff, log) to understand current changes.
- Alongside any other implementation skill when changes need to be committed.
- When the requesting agent asks for commit history or branch information.

## Workflow

1. **Create a branch.**
   - Create a feature, fix, or refactor branch: `git checkout -b <type>/<name>` or `git switch -c <type>/<name>`.
   - Use `feature/`, `fix/`, `refactor/` prefix with kebab-case description (e.g., `feature/add-user-auth`, `fix/login-redirect`).

2. **Implement and stage changes.**
   - Make focused code changes for a single logical concern.
   - Run `git status` and `git diff` to review all changes.
   - Stage individual files by name: `git add src/auth.ts src/auth.test.ts`.
   - Use `git rm` for deletions and `git mv` for renames.
   - Review `git diff --cached` before committing.

3. **Verify and commit.**
   - Run tests (and linter if present); fix failures before committing.
   - Commit: `git commit -m "<type>: <description>"` — types: `feat:`, `fix:`, `refactor:`, `test:`, `docs:`, `release:`.
    - Subject line: imperative, lowercase, no period, ~50 characters; never WIP-style ("wip:", "todo:") — use real, descriptive messages. Add a body for non-trivial commits explaining *why* (blank line separator, wrapped at 72).

4. **Repeat and report.**
   - Stage and commit each concern separately; re-verify tests before each commit.
   - Summarize the branch, commit count, and messages to the requesting agent.

## Quality Criteria

- Each commit is atomic — one logical change with a conventional, descriptive message (types: `feat:`, `fix:`, `refactor:`, `test:`, `docs:`, `release:`).
- Tests pass at every commit (full test suite, not just final state).
- All changes committed to a feature, fix, or refactor branch — never directly to `main` or `develop`.
- Staged diff reviewed before every commit.
- Clean tree: no secrets (API keys, `.env` files), no junk (`.DS_Store`, `node_modules/`, `dist/`, build artifacts), no commented code, no large binaries.

## Anti-Patterns

- **History modification** (`--amend`, `rebase`, `reset`, `filter-branch`): Rewrites or destroys commits — use a new commit instead.
- **Blind staging** (`git add .` or `git add -A`): Risk committing unintended files or secrets; stage by name after reviewing `git status` and `git diff`.
- **Committing secrets or junk**: API keys, `.env` files, `.DS_Store`, build artifacts — review the staged diff and verify `.gitignore` before every commit.
- **Shell operators in git commands** (`git add . && git push`, `git commit -m "…" || echo error`): Chaining with `&&`, `||`, `;`, pipes, `$()`, or redirection can bypass safeguards; run each git command individually.
- **Remote or shared-state operations** (`push`, `pull`, `fetch`, `merge`, `cherry-pick`, `revert`): These affect shared repositories or rewrite history — defer to the requesting agent for orchestration decisions. Create commits on the current branch only.
