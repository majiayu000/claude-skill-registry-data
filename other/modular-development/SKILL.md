---
name: modular-development
description: Split metisa work into independently validated checkpoints that can be reverted or selectively integrated.
---

# Modular Development

## Use when

Planning any multi-file change, risky firmware edit, refactor, port, or set of independent improvements.

## Procedure

1. Read `project-rules/modular-development.md` and inspect current repository status/history.
2. Break the task into logical units with dependencies, acceptance checks, files, and rollback boundaries.
3. Implement one unit at a time; separate formatting, behavior, licensing, and hardware changes where practical.
4. Validate the unit before moving on and record exact evidence in the workbook.
5. When Git metadata exists, checkpoint each independently validated unit. Include prerequisite checkpoint IDs for dependent work.
6. On cherry-pick/integration, rerun affected tests against the destination state; stop on semantic conflicts.

## Constraints

- Never claim arbitrary rollback or selective integration when there is no Git repository/history.
- Review the exact staging set before a baseline commit; exclude secrets, local paths, generated data, and licensing-uncleared public artifacts.
- Do not push or publish as part of local checkpointing.
- Keep safety behavior and EEPROM schema migrations in isolated, reviewable units.

## Done when

The change is independently testable, its dependencies and rollback boundary are explicit, and its checkpoint is local and validated or a precise Git-metadata blocker is recorded.