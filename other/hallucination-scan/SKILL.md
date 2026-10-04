---
name: hallucination-scan
description: Run the full Zero Hallucination audit - optimistic updates, silent failures, no-op handlers, hardcoded values, stale cache, ts-nocheck exports.
disable-model-invocation: true
---

# Zero Hallucination Scan

Run the full audit. Report findings in the same format as `docs/zero-hallucination-audit.md`.

## Checks

1. **Optimistic updates** - search all `startTransition` and `useTransition` calls for missing `try/catch` + rollback
2. **Silent failures** - search for catch blocks that return zero/default/empty without UI feedback
3. **No-op handlers** - search for `onClick` with empty bodies, `// placeholder`, `// TODO`, `return { success: true }` on functions that don't persist
4. **Hardcoded display values** - search for dollar amounts, counts, or metrics that aren't from a query or constant
5. **Stale cache** - check that every `unstable_cache` tag has matching `revalidateTag` calls in all relevant mutations
6. **`@ts-nocheck` exports** - find files with both `@ts-nocheck` and `export` that could crash on call
7. **Demo/sample data visibility** - check that `is_demo` or equivalent flags are consumed by the UI

Update `docs/zero-hallucination-audit.md` with any new findings.
