---
name: workspace-orchestration
description: Use when Codex needs to run AgentBoard workspace cards through planning, review, implementation, and audit with parallel spawned agents.
---

# Workspace Orchestration

This skill defines how to run a board pipeline safely in Codex.

## Preconditions

- AgentBoard is authenticated and healthy.
- A target app and board exist.
- Cards are present in the relevant input column.
- `codegraph` and `codebase-rag` are available when the work needs code understanding.

## Waves

1. Planning
2. Review
3. Implementation
4. Audit

## Board Rules

- Read `auto_transitions` before starting.
- Respect `review_blocking` and `audit_blocking`.
- Default to pausing at checkpoints unless the board configuration clearly allows auto-progression.

## Codex Execution Model

Use `spawn_agent` for independent cards.

Each worker should own:

- one card
- one bounded responsibility
- one isolated write scope when code changes are involved

Do not delegate blocking orchestration decisions. The main agent should:

- select the board
- choose the cards for each wave
- decide whether to continue after checkpoints
- integrate and summarize outcomes

## Worker Templates

Do not invent the worker roles ad hoc. Use the stored templates under:

- `skills/orchestrate/references/planning-worker.md`
- `skills/orchestrate/references/review-worker.md`
- `skills/orchestrate/references/implementation-worker.md`
- `skills/orchestrate/references/audit-worker.md`

The orchestrator should read the relevant template before each wave and embed its instructions into the worker prompt with live card-specific variables.

## Wave Behavior

### Planning

Input: cards needing a concrete implementation plan.

Output:

- a plan artifact or equivalent planning note
- the card moved forward only if the plan is specific and actionable

### Review

Input: planned cards.

Output:

- pass to implementation if the plan is coherent, scoped, and consistent with constraints
- send back for replanning if the plan is vague, risky, or incomplete

### Implementation

Input: approved cards.

Output:

- code changes
- implementation artifact or notes
- verification evidence

Implementation rules:

- run repo-appropriate verification, not hardcoded project-foreign commands
- if verification fails, stop and surface the real failure
- implementation workers must be spawned as `worker` agents with explicit ownership of the card and write scope

### Audit

Input: implemented cards.

Output:

- independent verification
- pass to finished only when the implementation actually satisfies the card

Audit rules:

- default to read-only validation
- findings should be concrete and tied to files or behaviors
- do not silently convert audit into another implementation pass

## Retry Policy

- Replanning after review rejection: at most 2 retries per card before escalation.
- Implementation verification failure: stop and escalate immediately.
- Audit failure: keep the card out of `finished` until the issue is addressed.

## Artifact Quality Gate

Before submitting an artifact, verify:

- no TODO or placeholder text
- no unanswered research gaps
- concrete file references where applicable
- enough detail that another agent could continue without redoing the discovery work

## Reporting

After each wave, report:

- cards processed
- passes
- failures
- blocked items
- whether a checkpoint requires user confirmation
