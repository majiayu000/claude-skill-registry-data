---
name: mission-control-delivery
description: Preserve Mission-to-release lineage, evidence, and authority boundaries. Use when Mission Control or a similar software factory governs the work.
compatibility: Works in Claude Code, Codex, and Agent Skills-compatible harnesses. Mission Control mutations require separately installed integration skills or tools and explicit task authority.
metadata:
  author: software-factory
  version: "1.0.0"
  owner: software-factory
  risk: low
  capabilities: governed-delivery,evidence-lineage,operator-handoff
---

# Mission Control Delivery

Keep software-factory work traceable from operator intent through verified
delivery. This skill governs how to reason about the work. It does not grant
permission to claim tasks, change Mission Control state, publish packages,
merge pull requests, deploy releases, or spend money.

## Start from the execution contract

Before editing, identify the available contract fields:

- Mission, WorkOrder, and Task identifiers
- requested outcome and acceptance criteria
- repository, base revision, and allowed code scope
- assigned owner, worker, and approval policy
- change budget, cost budget, and deadline
- required checks, evidence, and review gates

Use repository instructions and the current task context as evidence. Mark a
missing material field as `Needs confirmation`; do not invent identifiers,
approvals, owners, or completion state. Routine implementation details inside
an authorized scope can be inferred when they do not change the outcome or
expand authority.

## Execute one bounded Attempt

1. Confirm the repository and base revision before making changes.
2. Use the worktree or checkout assigned to this Attempt. Create isolation only
   when the harness has not already provided it.
3. Keep edits within the WorkOrder's code scope and change budget. Surface a
   needed scope expansion before making it.
4. Follow repository architecture and testing rules. Load specialized skills
   only when their trigger matches the work.
5. Record material decisions, blockers, commands, and evidence against the
   current Attempt when Mission Control tooling is available.
6. On failure, preserve the failed Attempt and its evidence. Retry through a
   new Attempt or the product's recovery path instead of rewriting history.

## Build the evidence chain

Evidence must identify what it proves and the exact candidate it covers.
Capture the failing state before a bug fix when practical, then capture the
passing state after the change.

For each required check, retain:

- requirement or acceptance criterion
- command, interaction, or observation
- result: passed, failed, or untested with a reason
- commit SHA, deployment URL, or artifact digest
- artifact path or durable link
- known limitation or stale condition

Tests and visual evidence complement each other. Neither substitutes for the
other when the WorkOrder requires both. Never attach old passing evidence to a
new candidate without rerunning or proving that it remains current.

## Respect decision boundaries

Pause before an action that exceeds the execution contract or requires a human
decision. Common examples include expanding scope, changing production data,
publishing a context package, merging, deploying, changing an approval policy,
or accepting a known failed gate.

Prepare the reviewable result and supporting evidence before requesting the
decision when safe work remains. If an approval is denied or expires, stop the
dependent action and preserve the current state.

## Handoff contract

End with a factual operator handoff:

```markdown
## Handoff — <WorkOrder or Task ID>

State: <current authoritative state>
Outcome: <what changed or Needs confirmation>
Candidate: <commit, branch, PR, or artifact>
Evidence: <checks and durable references>
Unresolved risk: <known risk or none known>
Decision required: <approval or none>
Next owner: <person, role, or Needs confirmation>
Next action: <one explicit action>
```

Task completion is not automatically WorkOrder acceptance, Mission completion,
pull-request approval, or release authorization. Report each boundary at its
actual state.

## Mission Control integration

When the repository provides focused Mission Control integration skills, use
them for API-specific operations such as registration, heartbeat, task
lifecycle, approvals, deliverables, memory, budget, and run logging. Their
contracts control those mutations. This skill supplies the delivery model and
does not replace them.
