---
name: implement-spec
description: "Implement a specification in code."
disable-model-invocation: true
---

You have been provided a spec. This spec should have tickets associated with it, describing how to implement the spec.

The goal is a PR which implements the entire spec on a single branch. Treat an invocation whose scope requests this workflow as authorization for those mutations. If the invocation explicitly requests branch-only work, use that branch and report the resulting handoff; do not add a second approval gate when the request already specifies the workflow.

The tickets are not a list of steps. They are a **task graph** with blocking relationships between them. This means there is always a **frontier** of tickets which are ready to be grabbed.

Communication to and from subagents should be sparse. Communicate primarily through **context pointers**: to the spec, tickets, research notes, and previous commits. Don't duplicate information already available via pointers.

**Implementer subagents** should be run in the background where possible for **maximum concurrency**. If the native harness lacks the required isolation or delegation capability, work the frontier sequentially on the authorized branch while preserving the same roles and blocking edges.

## Steps

1. Read the spec and tickets. Read enough to understand the task graph.

2. (optional) Use an **exploration subagent** to conduct any exploration required by the tickets - relevant codebase files or external documentation. Ensure the exploration subagent can save files - it should save its markdown notes in a directory outside the repo, accessible by all future subagents. This lets **implementer subagents** focus on implementation rather than exploration.

3. Create a branch and draft PR. Treat an invocation whose scope requests this workflow as authorization for those mutations. If the invocation explicitly requests branch-only work, use the current authorized branch and record that no PR was created; do not add a second approval gate when the request already specifies the workflow.

4. Use **implementer subagents** to implement each ticket in the background where possible for maximum concurrency. Give each isolated worktree and branch when the native harness supports the required isolation; otherwise implement the ticket on the authorized branch without inventing a worktree topology.

5. Once an **implementer subagent** completes, merge its work to the target branch with a **merger subagent**. If the native harness cannot support that role, the coordinator may integrate directly through the authorized merge path.

6. If this changes the **frontier** of available tickets, kick off more **implementer subagents** to work on the new tickets. If the native harness cannot support that delegation, continue sequentially while preserving the blocking edges.

7. Once all tickets are complete, run /code-review on the target branch or PR. Fix all issues raised by the code review in a single **implementer subagent**. If the native harness cannot support that role, the coordinator fixes them through the authorized implementation path.

8. Mark the PR as ready for review when a PR was created; otherwise report the completed branch state.

9. Clean up all **implementer subagent** worktrees.
