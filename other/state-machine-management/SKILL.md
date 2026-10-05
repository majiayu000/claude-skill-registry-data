---
name: state-machine-management
description: |
  Legacy/migration guidance for v1 StateMachine entities. In v2, lifecycle
  rules are implementation contracts owned by MCP servers, not first-class
  records to create during normal project work.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-state-machine-management
    version: "1.0.0"
    created: 2026-04-06T00:00:00Z
    category: processkit
    layer: 3
    uses:
      - skill: event-log
        purpose: Log events to keep the audit trail accurate after every write.
    provides:
      primitives: [StateMachine]
      templates: [statemachine]
---

# State Machine Management

## Intro

In v1, a StateMachine defined valid states and transitions for a
primitive. In v2, StateMachine is not a first-class primitive authoring
surface. Lifecycle rules live in the owning MCP server or implementation
contract, and transitions go through MCP tools that return structured
errors when a move is invalid.

## Overview

### Legacy v1 shape

```yaml
---
apiVersion: processkit.projectious.work/v1
kind: StateMachine
metadata:
  id: SM-workitem
  name: workitem
  created: 2026-04-06T00:00:00Z
spec:
  description: "WorkItem lifecycle with a formal review state."
  initial: backlog
  terminal: [done, cancelled]
  states:
    backlog:
      description: "Not started."
      transitions:
        - to: in-progress
        - to: cancelled
    in-progress:
      description: "Being actively worked on."
      transitions:
        - to: review
        - to: blocked
        - to: cancelled
    blocked:
      description: "Cannot proceed until a blocker is resolved."
      transitions:
        - to: in-progress
        - to: cancelled
    review:
      description: "Awaiting review."
      transitions:
        - to: done
        - to: in-progress
    done:
      description: "Complete."
      transitions: []
    cancelled:
      description: "Abandoned."
      transitions: []
---
```

### v2 lifecycle changes

Do not create new StateMachine records for v2 projects. To change a
lifecycle, update the owning MCP server or its reviewed implementation
contract, then migrate affected records explicitly.

Lifecycle changes must:
- Keep the same `initial` state (or migrate existing data).
- Not remove states that existing entities are currently in.
- Add new transitions only from states that already exist.

### Workflow

1. Identify the MCP server that owns the entity lifecycle.
2. Change the server contract and tests for allowed transitions.
3. Audit existing entities for states or edges the new contract removes.
4. Write or run a Migration for affected records.
5. Log the state-change policy update through the normal event path.

## Gotchas

Agent-specific failure modes — provider-neutral pause-and-self-check items:

- **Cycles in the state graph without explicit handling.** A cycle
  (e.g., `in-review → in-progress → in-review`) is fine if it's
  intentional, but every cycle should be marked and have an exit
  criterion. Unmarked cycles cause infinite loops in process
  execution.
- **Terminal states with outgoing transitions.** A "terminal"
  state by definition has no outgoing edges. If `cancelled` has a
  transition to `re-opened`, then `cancelled` isn't terminal —
  rename it. Mislabeled terminals confuse downstream queries
  filtering by lifecycle stage.
- **Missing initial state declaration.** Every state machine
  needs an explicit `initial` state. Without it, new entities
  have no lawful starting point and the validator can't reject
  malformed creations.
- **Creating new StateMachine records for v2 work.** That keeps the
  legacy primitive alive and bypasses the owning MCP server contract.
  Treat StateMachine files as migration inputs only.
- **State machine that doesn't match the entity's actual
  lifecycle.** If the schema says a workitem can be cancelled but
  the state machine has no `cancelled` state, the two are out of
  sync and queries break. Schema and state-machine must agree —
  treat them as one unit when changing either.
- **Forgetting to update consumers when transitions change.**
  When you remove a transition (e.g., dropping `in-progress →
  done` direct), every workitem currently in `in-progress` is
  stranded. Audit current entities before removing transitions
  and write a Migration if any are affected.
- **Adding states without removing dead ones.** State machines
  accumulate cruft over time. When you introduce a new state
  that supersedes an old one, remove or deprecate the old one.
  Otherwise the graph becomes a dictionary of every state anyone
  ever proposed.
- **Project-level lifecycle rules that diverge silently from
  defaults.** If a project changes lifecycle behavior, record the
  rationale as a DecisionRecord. Future maintainers need to know
  why the project's flow differs from processkit's default.

## Full reference

### Fields

| Field         | Type         | Notes                                                |
|---------------|--------------|------------------------------------------------------|
| `description` | string       | What this machine is for                             |
| `initial`     | string       | Starting state for new entities                     |
| `terminal`    | list[string] | States with no outgoing transitions                  |
| `states`      | map          | `state_name → {description, transitions}`           |

### Transition object

```yaml
transitions:
  - to: <state-name>
    guard: "optional human-readable precondition"
    on_enter: <event-type>        # LogEntry event to emit
    required_role: <role-name>    # who is allowed to make the transition
```

Guards are advisory unless enforced by an MCP server that knows about them.

### Validation

- No cycles from terminal states.
- Every non-terminal state has at least one outgoing transition.
- Every state referenced in `transitions` must exist in `states`.
- `initial` must exist in `states`.

### Machine history

Lifecycle contract changes should have LogEntries rather than git commits
alone. This lets queries reason about "what did the valid states look like
on date X?" without treating StateMachine as a new v2 entity.

### Multiple machines for one kind

Legacy v1 contexts may contain multiple machines for one primitive kind.
During v2 migration, collapse those variants into explicit WorkItem types,
Artifact-backed policy, or separate MCP lifecycle contracts rather than
creating new StateMachine records.
