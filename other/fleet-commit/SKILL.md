---
name: fleet-commit
description: >
  Create a conventional commit with task reference in a fleet worktree.
  Use when you've made changes and need to commit them following fleet standards.
  Triggers on: "commit", "save changes", "commit my work", "fleet commit".
user-invocable: true
---

# Fleet Commit

Create a properly formatted conventional commit following fleet standards.

## When to Use

After making changes in a project worktree, use this skill to commit with
the correct format, task reference, and branch.

## Commit Format

```
type(scope): description [task:TASK_SHORT]
```

**Types:** feat, fix, docs, refactor, test, chore, ci, style, perf

## Steps

1. Read TOOLS.md for `BOARD_ID` and `AUTH_TOKEN`
2. Identify the task ID from the current session context or task assignment
3. Check `git status` to see what changed
4. Stage the relevant files: `git add <files>` (never `git add .`)
5. Determine the commit type from the nature of the change:
   - New feature → `feat`
   - Bug fix → `fix`
   - Documentation → `docs`
   - Restructuring → `refactor`
   - Tests → `test`
   - Config/deps → `chore`
6. Write the commit message:
   ```bash
   git commit -m "type(scope): concise description [task:XXXXXXXX]"
   ```
7. One commit per logical change — don't batch everything

## Rules

- **Never** `git add .` or `git add -A` — stage specific files
- **Never** commit secrets, credentials, or `.env` files
- **Never** force-push or amend published commits
- **Always** include the task reference `[task:XXXXXXXX]`
- **Always** check that tests pass before committing
- Scope should be the module/area affected (e.g., `core`, `api`, `auth`)

## Examples

```bash
git add nnrt/core/engine.py
git commit -m "feat(core): add type hints to engine module [task:ea36a032]"

git add tests/test_pipeline.py
git commit -m "test(pipeline): add integration tests for NLP passes [task:ea36a032]"

git add docs/api.md
git commit -m "docs(api): document new REST endpoints [task:8b57cab5]"
```