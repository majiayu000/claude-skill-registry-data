---
name: subagent-driven-development
description: Execute an implementation plan through bounded implementer and independent reviewer agents with disjoint write ownership, explicit handoffs, evidence gates.
license: MIT
---

# Subagent-Driven Development

## Entry gate

Use subagents when work can be isolated by dependency or an independent review is valuable. Keep a tightly coupled, small, or highly interactive change with the coordinator.

## Task contract

Every delegated task receives:

```markdown
Outcome and acceptance criteria:
Required source paths/context:
Dependencies already complete:
Exclusive write scope, or READ ONLY:
Forbidden files/actions:
Existing user changes to preserve:
Required tests/evidence:
Output and handoff format:
Stop/escalation conditions:
```

Use the host's actual delegation interface and current model/session defaults. Do not invent tools, force a named model, switch providers, or spend externally. Capability, context isolation, and tool access determine role assignment.

## Execution

1. Parse the approved plan into a dependency graph.
2. Launch only dependency-ready tasks with non-overlapping mutable state.
3. The coordinator continues non-overlapping integration work; it does not duplicate each implementation.
4. Inspect returned files/diffs and run the claimed focused validation before accepting a task.
5. Assign a specification reviewer read-only access to verify acceptance criteria from source evidence.
6. Assign a quality/security reviewer when risk warrants it; do not leak the implementer's desired conclusion.
7. Send confirmed findings back as a narrow fix contract. Re-review the resulting diff.
8. Integrate in dependency order and run the complete relevant validation on the combined state.

## Failure handling

- `NEEDS_CONTEXT`: supply the missing source or narrow the contract.
- `BLOCKED`: verify the blocker, adjust scope/dependencies, or handle locally; do not automatically switch models.
- overlapping edits: stop parallel writes and reconcile sequentially.
- failed validation: isolate the responsible integration and repair or roll it back.
- unavailable agent: continue locally or reassign the same bounded contract.

The parent task's authority is the ceiling. Subagents may not push, publish, deploy, delete unrelated data, spend, or message anyone unless that action was explicitly authorized.

## Completion report

List the task graph, agent roles, accepted/rejected artifacts, independent checks, conflicts, commands/results, skipped validation, residual risk, and rollback. Completion requires integrated tests, not merely successful agent messages.
