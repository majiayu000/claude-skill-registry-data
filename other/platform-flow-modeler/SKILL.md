---
name: platform-flow-modeler
description: Model cross-system product flows, state transitions, exception paths, callbacks, retries, rollback, reconciliation, migration, and manual fallback for platform, workflow, back-office, and fintech requirements. Use when creating, clarifying, or reviewing flows before PRD writing, scope decisions, product direction, or PRD review. Invoked internally by platform-product-orchestrator, or directly when the user names this skill; for a natural-language request that does not name a skill, platform-product-orchestrator is the entry point.
---

# Platform Flow Modeler

Use this skill to model product and system flows before prose. It can be used directly, or as a specialist layer inside `platform-product-guide`, `platform-prd-builder`, `platform-scope-checker`, and `platform-prd-reviewer`.

This skill does not write the full PRD, make the final scope verdict, or produce the final review score. It produces flow evidence that other skills can use.

## When to Use

Use this skill when a requirement involves:

- 3+ systems, roles, or operational actors
- lifecycle/status changes
- callback, retry, timeout, notification, or downstream sync
- rollback, cancellation, return, resubmission, or reversal
- reconciliation, settlement, migration, or cutover
- manual fallback, exception queue, or operational intervention
- PRD sections such as Overall Flow, Flow Details, Scenarios, State Transition, or Operations
- scope decisions where a "small" change may introduce hidden flow or state complexity
- PRD review where flow closure, state consistency, or exception handling is uncertain

## When NOT to Use

Do not use this skill as the main tool when:

- the request has no meaningful flow, state, or cross-system complexity
- the user needs a full PRD artifact; route to `platform-prd-builder`
- the user needs a final include/defer decision; route to `platform-scope-checker`
- the user needs a full PRD readiness review; route to `platform-prd-reviewer`
- the business problem or platform direction is still unclear; route to `platform-product-guide`
- the request is pure engineering implementation such as database schema, queue design, or scheduler design

## Flow Types

Choose the relevant flow types before modeling:

- Main happy path
- Exception / failure path
- Callback / retry / timeout path
- Rollback / cancellation / resubmission path
- Reconciliation / settlement / migration path
- Manual fallback / operations intervention path
- State transition / lifecycle path

If multiple flow types apply, model the main path first, then the highest-risk exception paths.

## Step 0: Flow Classification

Before building tables or diagrams, identify:

- Trigger: what starts the flow
- Starting state and ending state
- Actors/systems involved
- Source of truth for status and key data
- Persistence points
- Status changes
- External dependencies
- User-visible and ops-visible outcomes
- Current-phase vs future-phase behavior

If key flow facts are missing, label them as open questions instead of inventing decisions.

## Modeling Workflow

1. Define the trigger and starting state.
2. List actors/systems and their roles.
3. Model the main flow from trigger to final state.
4. Mark persistence points, status changes, and source-of-truth updates.
5. Add exception flows for validation failure, downstream failure, timeout, duplicate submission, cancellation, rollback, or manual handling.
6. Add callback, retry, timeout, and replay semantics at product level.
7. Add reconciliation, migration, or manual fallback if operational closure depends on it.
8. List unresolved flow decisions and route them to the right follow-up skill or owner.

## Output Contract

Default output:

### Flow Classification

State the flow type, trigger, starting state, ending state, and strictness needed.

### Actors / Systems

| Actor / System | Role in Flow | Owner | Source of Truth? |
|---|---|---|---|
|  |  |  |  |

### Main Flow

| Step | Actor / System | Action | Data / Persistence | Status Change | Owner |
|---|---|---|---|---|---|
| 1 |  |  |  |  |  |

### Exception Flows

| Scenario | Trigger | Handling | Final Status | Owner | User/Ops Impact |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

### State Transition

| Current State | Trigger | Next State | Allowed Actor | Side Effect |
|---|---|---|---|---|
|  |  |  |  |  |

### Callback / Retry / Timeout

Define product-level behavior: when callback happens, what failure means, who can retry/replay, what users or ops see, and what final unresolved state means.

### Rollback / Cancellation / Resubmission

Define whether each action is supported, who can trigger it, what status changes, what data remains, and what downstream systems must know.

### Reconciliation / Manual Fallback

Define how inconsistent or unresolved cases are detected, who owns manual handling, what record/audit is needed, and what completion criteria close the case.

### Open Flow Questions

List only decision-driving questions. Each question should name the owner or decision role when known.

## Quality Checklist

Before finalizing, verify:

- [ ] The trigger, starting state, and ending state are clear.
- [ ] Every status change has an owner and source of truth.
- [ ] Persistence points are visible.
- [ ] Exception paths end in a defined final or unresolved status.
- [ ] Callback, retry, timeout, and replay behavior are explicit when relevant.
- [ ] Rollback, cancellation, and resubmission semantics are clear when relevant.
- [ ] Reconciliation and manual fallback have owners.
- [ ] Current-phase behavior is separated from future-phase behavior.
- [ ] Open questions are real decisions, not generic reminders.

## Common Mistakes to Flag

- Describing flow only in prose when systems, states, or ownership are complex.
- Updating status without naming the source of truth.
- Adding callbacks without failure, retry, timeout, or manual replay behavior.
- Treating rollback, cancellation, or resubmission as obvious.
- Hiding operational work behind "manual handling" without owner, record, or closure criteria.
- Letting future-phase flow leak into current-phase requirements.
- Turning product-level flow requirements into engineering implementation choices too early.

## Routing

- Route to `platform-product-guide` when the flow exposes unresolved business direction, platform capability, or ownership model.
- Route to `platform-prd-builder` when the flow model should be converted into PRD sections.
- Route to `platform-scope-checker` when the flow reveals hidden MVP complexity or phase-boundary risk.
- Route to `platform-prd-reviewer` when the flow model is being used as evidence for PRD readiness.
- Route RFC-level implementation details to engineering follow-up while preserving product semantics in the flow.
