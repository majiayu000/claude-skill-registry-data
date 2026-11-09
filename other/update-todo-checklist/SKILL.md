---
name: update-todo-checklist
description: Ensure task checklist files exist, keep issue URLs for open work only, and sync out closed issue links.
engines: [AGNOSTIC]
---

## When to use
Use when task planning begins or the TODO file is missing.

## Rules
- Keep TODO as the ordered numbered checklist only
- Put full work instructions in per-task TASK.md files
- Keep only open issue URLs in `../.hephaera/.cache/tasks/OPEN_ISSUES.md`
- Remove closed issue URLs via issue sync before active planning

## Command
../commands/update-todo-checklist.sh
