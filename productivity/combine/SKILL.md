---
name: combine
description: Cross-domain skill index for workflows that must combine or reason across multiple business domains such as Workbench, Timeoff, Employee, or Calendar. Use when a request cannot be answered correctly from a single domain alone.
---

# Combine Skill Tree

Use this guide to navigate cross-domain helpers that join multiple sources of truth.

## Available leaves
- `skills/combine/check_task_timeoff_overlap/SKILL.md`

## Internal conventions
- Use `combine/` only for genuine multi-domain workflows.
- Do not move a single-domain leaf into `combine/` unless its logic truly depends on more than one domain.
- Keep cross-domain workflows explicit about which domain leaf to call at each step.

## Suggested navigation
- Use `check_task_timeoff_overlap` when the user asks whether tasks, deadlines, projects, or assignees conflict with approved leave.
- Prefer single-domain leaves first when the question can be answered from one domain alone.
