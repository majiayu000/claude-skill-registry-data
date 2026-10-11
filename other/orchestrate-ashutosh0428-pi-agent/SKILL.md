---
name: orchestrate
description: Split a large job into focused sub-agent tasks via delegate.
trigger: large or multi-part tasks (whole-repo review, explain + fix, multi-file change)
---
## When to use
A task is large or has clearly separable parts, and the `delegate` tool is available.

## How
1. `update_plan` with the high-level steps.
2. For each self-contained part, `delegate` a specific, complete task to a
   sub-agent (e.g. "explore the repo and list entry points + key modules"). It
   shares the workspace but starts fresh — give it everything it needs.
3. Delegate **one at a time**; wait for each result before the next.
4. Synthesise the sub-agents' results into one coherent answer — don't paste them.

## Avoid
- Delegating small tasks you could just do (it costs extra tokens + time).
- Vague sub-tasks ("look at the code") — be specific.
- Expecting sub-agents to share memory; each is independent.

## Done well
A big job decomposed into a few sharp sub-tasks, each done well, merged into a
single clear result.
