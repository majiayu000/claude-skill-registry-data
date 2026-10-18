---
name: brief
description: Generate a structured delegation brief for any task
trigger: /brief
---

# Delegation Brief Generator

Quickly create a structured brief for delegating work to a sub-agent. Uses the template from `system/05_delegation_protocol.md`.

## Usage

`/brief [task description]`

## What It Produces

```
## Brief: [Task Name]

**From:** the AIgent
**To:** [Recommended agent based on task type]
**Priority:** [P0/P1/P2 based on context]
**Date:** [Today]

### Objective
[One sentence derived from the task description]

### Context
[Relevant context pulled from vault — active priorities, related project notes, recent decisions]

### Deliverable
[Specific, verifiable output]

### Constraints
[Time, scope, dependencies inferred from context]

### Verification
[How to check the work is actually done]
```

## Behavior

1. Parse the task description from the user's input
2. Check `vault/memory/ACTIVE_PRIORITIES.md` to understand current mode and context
3. Check `vault/memory/DELEGATION_TRACKER.md` for related pending work
4. Determine the right agent and priority level
5. Draft the brief using the delegation protocol template
6. Present to the principal for approval before sending

Always recommend a model tier for the receiving agent based on task complexity.
