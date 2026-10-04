---
name: recovery
description: Resume interrupted change work from durable repository, task, worktree, and verification evidence without relying on conversation history.
---

# Recovery

## Stages

1. Identify the change, branch/worktree, base revision, and current repository state.
2. Read proposal, requirements, design, `tasks.md`, execution records, and gate evidence.
3. Reconcile task checkboxes with the actual diff and test results. Worker claims alone do not establish completion.
4. Detect drift: changed proposal/tasks, moved paths, changed base, conflicting work, stale evidence, or missing resources.
5. If state is trustworthy, resume at the first incomplete task or failed gate. If not, stop and report the exact inconsistency.
6. Re-run stale or missing verification before continuing dependent work.
7. Persist the new state after every meaningful task or gate transition.

Never silently rebuild a changed plan, mark uncertain work complete, or delete evidence to make recovery pass.
