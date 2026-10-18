---
name: wrap-up
description: End a work session - verify, update PROGRESS.md and the session log, commit, push to main and confirm CI is green.
disable-model-invocation: true
---

Wrap up this session.

1. Run `scripts/check.sh` (add `--e2e` if user-facing code changed). Fix failures first.
2. Append a short entry to docs/progress/SESSION_LOG.md:

   ```
   ## YYYY-MM-DD — <short title>
   **Built:** ...
   **Decisions:** ... (link ADRs if any)
   **Next time:** ...
   ```
3. Update docs/progress/PROGRESS.md: tick finished items and set "Next step".
4. Commit (conventional message) and push to `main`; watch CI with `gh run watch` and fix
   anything red immediately.
5. Report: what shipped, the commit link, and the next step.
