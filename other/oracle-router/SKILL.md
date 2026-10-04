---
name: oracle-router
description: "Build Oracle task routing: session ownership, detached work, launch order, and handoff rules. Use when the task touches multi-step execution or agent swarm coordination on this OS."
triggers: ["oracle-router"]
scope: harness
invocation: ability
---

# Oracle Router

Use this skill when the job needs one owner context but may detach work into smaller parts.

## Focus

- Keep flow identity separate from business logic.
- Route by capability, not by habit.
- Preserve one clear owner for each task.
- Reuse the taskflow and swarm patterns from `openclaw-openclaw` and the modular execution style from `leon`.

## Output

- Route map.
- Launch order.
- Handoff and wait policy.

## Rules

- Keep conditional logic in the caller.
- Do not scatter routing rules across multiple files unless the split is stable.
- Prefer small, explicit handoffs over hidden background behavior.

## Session Notes

### 2026-05-05
- session: patch | tools: Edit, Write | errors: none | notes: wired for CLI routing via triggers array and command alias
