---
name: refactor
description: Restructure code without changing its behaviour.
trigger: when the user asks to refactor, clean up, or simplify code
---
## When to use
The user wants code cleaner / simpler / restructured, with the same observable
behaviour.

## How
1. Read the file and its tests first.
2. Make one focused change at a time with `edit_file` (exact, unique old_string).
3. Preserve behaviour — outputs must not change. Keep names and style consistent.
4. Suggest running the tests after each change.

## Avoid
- Behaviour changes smuggled into a "refactor".
- Rewriting unrelated code.
- Big-bang rewrites instead of small, safe steps.

## Done well
The code reads better, the tests still pass, and you can state in one line why
each change is behaviour-preserving.
