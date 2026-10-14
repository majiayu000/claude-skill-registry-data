---
name: receiving-code-review
description: Process Godot code review feedback — use when the code-reviewer agent has provided feedback, before implementing suggestions.
---

# Godot Receiving Code Review

Do not implement suggestions blindly. Verify each claim before acting.

## Protocol

For each piece of feedback:

1. **Understand the claim** — what does the reviewer say is wrong?
2. **Verify it** — use `execute` to inspect live state, or read the file
3. **Assess** — is the claim correct for Godot 4.7? Is the fix appropriate?
4. **Act** — fix Critical and Important issues; use judgment on Suggestions
5. **Verify the fix** — run `godot:verification-before-completion` after changes

## Godot 4.x Correctness Checklist

Reject feedback that suggests pre-4.x patterns:

| Reviewer says | Correct Godot 4.x pattern |
|---|---|
| Use `setget` | Use `set(value):` property syntax |
| Use `yield` | Use `await` |
| Use `OS.get_ticks_msec()` for timing | Use `Timer` or `get_tree().create_timer()` |
| Use `connect("signal", self, "_handler")` | Use `signal.connect(_handler)` |
| Use `scene.instance()` | Use `scene.instantiate()` |

## If Feedback Seems Wrong

Run `godot:docs` to verify the correct Godot 4.7 API before pushing back on the reviewer.
