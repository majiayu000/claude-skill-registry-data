---
name: check
description: Run the full local quality gate (lint, typecheck, unit tests) and summarize failures with file:line. Use before committing or when CI is red.
---

Run from the repo root:

```bash
pnpm check
```

If anything fails:

1. Show only the first failing task's errors, grouped by file.
2. For lint/type errors, open the file and fix the cause. Re-run only that workspace
   (`pnpm --filter <name> lint` / `typecheck` / `test`) until green, then re-run `pnpm check`.
3. For test failures in `packages/queue-engine`, read the spec in `docs/QUEUE_RULES.md` before
   changing the expectation; the test is usually right.
4. For i18n key mismatch failures, add the missing key to the other locale with a real
   translation, not a copy of the English.

Report: green/red per workspace, and what you changed.
