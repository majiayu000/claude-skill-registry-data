---
name: action
description: Execute a small batch of conditional actions only after verifying they are safe and unused.
---

## Intent
Use for small cleanup actions like removing unused deps.

## Steps
1. Verify each target independently (rg search, import checks).
2. If used, skip with reason.
3. If unused, execute the action safely.
4. Report executed vs skipped.

## Limits
- Max 5 items per batch.
