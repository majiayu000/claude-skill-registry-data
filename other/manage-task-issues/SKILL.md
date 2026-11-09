---
name: manage-task-issues
description: Create and maintain one GitHub issue per task, track only open issue URLs in `.hephaera/.cache/tasks`, and remove closed links during sync.
engines: [AGNOSTIC]
---

## When to use
Use when creating task plans, generating task files, or reviewing active task lists.

## Output
- task-to-issue association
- refreshed open issue URL tracker in `.hephaera/.cache/tasks/OPEN_ISSUES.md`
- closed issue URLs removed from active task tracking

## Notes
- Prefer one issue per substantial task.
- Track open issues as URLs only in `.hephaera/.cache/tasks/OPEN_ISSUES.md`.
- Run sync before planning to prune closed issue URLs.
- Import issue-backed tasks with `../commands/import-task-from-issue.sh "<issue-ref>"` when users ask to work from an existing issue number.

## Command
../commands/sync-task-issues.sh

## Additional command
../commands/import-task-from-issue.sh "<issue-ref>" [task_name]
