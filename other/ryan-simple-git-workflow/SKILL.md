---
name: ryan-simple-git-workflow
description: Use when Ryan asks for Git help, branch management, workspace management, committing, merging, checking repository status, safe task branches, or when he says he does not understand Git, repositories, branches, workspace, commits, merges, or rollback.
---

# Ryan Simple Git Workflow

## Purpose

Ryan is a Git beginner and prefers stable, low-token, low-risk repository work. Treat Git operations as a guarded workflow: inspect first, explain risk briefly, then act conservatively.

## Default Rules

- Speak Chinese unless the project explicitly requires otherwise.
- Prefer one task, one branch.
- Do not develop directly on `main` unless Ryan explicitly asks.
- Never run destructive commands such as `git reset --hard`, `git checkout -- .`, branch deletion, force push, or history rewriting without explicit confirmation.
- Preserve unrelated user or agent changes. If the worktree is dirty, identify whether changes are related before editing.
- Keep command output capped and focused. Use `git status --short`, `git branch --show-current`, and targeted `git diff` before broad commands.
- If repository governance is missing or unclear, invoke `ryan-multi-ai-repo-governance`.

## Start Of Task

1. Identify the current directory and whether it is inside a Git repo:
   ```bash
   pwd
   git rev-parse --show-toplevel
   ```
2. Check project rules before business work:
   ```bash
   test -f AGENTS.md && sed -n '1,220p' AGENTS.md
   ```
3. Check current branch and worktree:
   ```bash
   git branch --show-current
   git status --short
   ```
4. If on `main` and the task requires edits, create a task branch with a clear prefix:
   ```bash
   git switch -c codex/<short-task-name>
   ```
5. If there are existing changes, explain them briefly and avoid mixing unrelated work into the task.

## During Work

- Keep edits scoped to the requested task.
- Use targeted diffs while working:
  ```bash
  git diff -- <path>
  ```
- For multiple independent tasks, recommend separate branches or worktrees instead of mixing them.
- Explain Git concepts in plain language, not jargon, when Ryan asks.

## Before Commit

1. Summarize changed files:
   ```bash
   git status --short
   git diff --stat
   ```
2. Review the actual diff for risky files, secrets, generated artifacts, dependency churn, and unrelated edits.
3. Run the project validation command if known. If unknown, state that clearly and run only obvious lightweight checks.
4. Ask Ryan before committing if the diff includes broad, risky, or unrelated changes.

## Commit And Merge

- Use short English commit messages.
- Do not merge back to `main` unless Ryan asks.
- Before merging, verify the task branch is clean or only contains intended changes.
- After merge or commit, report branch, changed files, validation, skipped checks, and remaining risks.

## When To Escalate To Governance Skill

Use `ryan-multi-ai-repo-governance` when:

- `AGENTS.md` is missing or stale.
- The directory may need to become its own repo.
- There are nested Git repos, submodules, or parent-child repo confusion.
- There may be tracked secrets, local databases, logs, archives, or generated outputs.
- Multiple AI agents or tools will touch the same repository.
