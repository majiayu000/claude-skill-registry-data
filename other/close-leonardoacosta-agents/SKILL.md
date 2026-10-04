---
name: close
description: Verify and truthfully finalize a completed change, update its artifacts, archive it when appropriate, and report remaining work.
---

# Close

## Stages

1. Confirm all required tasks are complete or explicitly deferred/blocked.
2. Run fresh final gates appropriate to the change and integration state.
3. Perform or confirm independent review with no unresolved blocking findings.
4. Inspect final diff and repository status for scope, generated files, and accidental changes.
5. Update `tasks.md` and execution evidence with final results.
6. Archive the change only when completion criteria are satisfied and repository policy permits archival.
7. Report completed work, verification commands/results, deferred work, accepted risks, and cleanup state.

A change is not complete because an agent says it is complete. Do not archive partial work, conceal failed gates, push automatically, or claim cleanup without evidence.
