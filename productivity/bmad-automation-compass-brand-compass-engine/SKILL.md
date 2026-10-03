---
name: bmad-automation
description: Use when the user wants Compass BMAD automation wrappers, Beads-aware orchestration, approval gates, or resume/retry behavior instead of a single manual workflow step.
---

# BMAD Automation

## When to Use

Use this skill when the user asks for:

- `auto-plan`, `auto-epic-start`, `auto-story`, or `auto-epic-end`
- approval-gated orchestration across BMAD phases
- Beads-integrated automation behavior
- retry, resume, stale output, or approval marker rules

## Instructions

1. Treat `_bmad/tools/automation/` as the source of truth for automation behavior.
2. Keep `bd` as the task system of record.
3. Do not present automation as a replacement for the BMAD workflow; it orchestrates the same underlying workflow surfaces.
4. If the user only needs one workflow entry point, prefer the manual BMAD skill instead of automation.

## References

- Read `references/automation-surfaces.md` for the shipped automation entry points.
- Read `_bmad/tools/automation/policies/state-model.md` when approval gates, stale outputs, or resume behavior matter.
