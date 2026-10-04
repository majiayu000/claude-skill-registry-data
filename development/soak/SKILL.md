---
name: soak
description: Run the full software aging (soak) pipeline - useEffect cleanup audit, fixes, and soak tests.
disable-model-invocation: true
---

# Run Soak Tests

Run the full soak pipeline in order:

1. **useEffect cleanup audit** - scan all components for missing cleanup returns, leaked event listeners, unclosed PostgreSQL subscriptions, intervals/timeouts without `clearTimeout`/`clearInterval`
2. **Fix every issue** the audit finds
3. **Run `npm run test:soak:quick`** (dev server must be on port 3100 - ask user to start it if needed)
4. **If any test fails** - read the report, diagnose the root cause, fix it, and re-run until all 3 soak tests pass
5. **Commit everything** when done

What the soak tests measure: JS heap memory, DOM node count, console errors, and cycle time across 100+ repeated navigation loops. Uses Chrome DevTools Protocol (CDP). Fails if memory > 3x baseline, DOM nodes > 2x baseline, any console errors, or cycle time > 2x baseline.

Full docs: `docs/soak-testing.md`
