---
name: requesting-code-review
description: Request a Godot code review after completing a plan step — use after finishing a task and verifying it before moving to the next task.
---

# Godot Requesting Code Review

After completing a plan task and verifying it (godot:verification-before-completion), invoke the code reviewer agent.

## Checklist

Create TodoWrite for each item below, then work through them in order.

- [ ] Verification passed (zero errors in get_log)
- [ ] Provide the reviewer with: task description, files changed, get_log output
- [ ] Address all Critical issues before continuing to next task
- [ ] Address all Important issues before final commit

## Context to Provide the Reviewer

```
Task N complete: <description>

Files changed:
- res://scripts/<script>.gd (created/modified)
- res://scenes/<scene>.tscn (modified)

get_log output (last 50 lines):
<paste output>

Please review for: GDScript idioms, scene structure, signal patterns, performance.
```

## After Review

- Critical: fix before continuing
- Important: fix before final commit on this branch
- Suggestions: use judgment
