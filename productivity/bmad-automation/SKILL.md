---
name: bmad-automation
description: Use when the user wants Compass BMAD automation wrappers, Beads-aware orchestration, approval gates, or resume/retry behavior instead of a single manual workflow.
---

# BMAD Automation

## When to Use

Use this skill when the user asks for:

- `auto-plan`, `auto-epic-start`, `auto-story`, or `auto-epic-end`
- approval-gated BMAD orchestration
- Beads-aware automation behavior
- resume, retry, or stale-output handling

## Instructions

1. Treat `_bmad/tools/automation/` as the source of truth for automation behavior.
2. Keep `bd` as the task system of record.
3. Prefer the direct BMAD workflow when the user only needs one workflow step.
4. Use automation only when orchestration value clearly outweighs a single direct workflow entry point.

## References

- Read `references/automation-surfaces.md` for the shipped automation entry points.
- Read `_bmad/tools/automation/policies/state-model.md` when approval gates and resume behavior matter.
