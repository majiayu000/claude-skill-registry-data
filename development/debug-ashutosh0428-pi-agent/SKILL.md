---
name: debug
description: Find and fix the root cause of a bug, not the symptom.
trigger: when the user reports an error, failure, or wrong output
---
## When to use
Something errors, fails a test, or produces wrong output.

## How
1. Read the error/traceback and the relevant code before touching anything.
2. State a hypothesis about the **root cause** (not just where it surfaced).
3. Make the smallest `edit_file` that fixes the cause.
4. If a test reproduces the bug, mention running it to confirm the fix.

## Avoid
- Patching the symptom (swallowing the error) instead of the cause.
- Refactoring unrelated code while fixing.
- Guessing without reading the traceback.

## Done well
You can state: what was wrong, why, and the one change that fixes it — confirmed
by a test or a clear, specific reason.
