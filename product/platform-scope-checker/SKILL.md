---
name: platform-scope-checker
description: Assess MVP scope, phase boundaries, build risk, change impact, and hidden complexity for product requirements. Use when the user asks whether to include something now, whether a request is actually big, how to split MVP vs future iteration, whether to validate before building, or when a feature may affect data objects, permissions, workflow, UI, APIs, operations, rollout, migration, ownership, or platform consistency. Invoked internally by platform-product-orchestrator, or directly when the user names this skill; for a natural-language request that does not name a skill, platform-product-orchestrator is the entry point.
---

# Platform Scope Checker

Use this skill before drafting when the user is exploring whether a requirement belongs in the current phase.

## Operating Modes

Choose one mode before answering:

- MVP inclusion gate: decide whether the change belongs in the current phase.
- Hidden complexity scan: expand a "small request" into real system, ops, and rollout impact.
- Phase split: separate MVP, compatibility placeholder, future iteration, and out-of-scope behavior.
- Validation gate: decide whether demand evidence is strong enough to build now.
- Change impact review: evaluate impact across flow, data, UI, API, permissions, operations, and migration.

## Step 0: Stage Detection

Before giving a verdict, classify the request:

- Idea / demand signal: value is plausible but evidence may be weak.
- Scope expansion: a proposed addition may change MVP size or phase boundary.
- "Small" change: simple wording may hide lifecycle, API, permission, data, or operations impact.
- Platform capability decision: the change may create reusable capability or duplicate existing capability.
- Delivery tradeoff: timeline, dependency, or rollout risk needs a phase split.
- PRD-ready decision: scope is clear enough to route to `platform-prd-builder`.

## When NOT to Use

Do not use this skill to write the full PRD; after the scope verdict, route to `platform-prd-builder`. Do not use it as a final document review; use `platform-prd-reviewer`. If the business direction itself is unclear, route to `platform-product-guide` first.

## First Move

Do impact analysis before writing detailed PRD content.

Identify:

- current phase objective
- proposed change
- affected systems
- affected configuration/runtime objects
- affected UI/prototype areas
- affected API/data fields
- affected permissions and ownership
- operational and rollout impact

Classify the change before judging scope:

- Field-only / enum-only change
- API contract change
- Flow or state transition change
- Configuration surface change
- Migration / data correction change
- Operational SOP / manual handling change
- New platform capability

## Build Risk Gate

Before recommending inclusion, name the single biggest risk:

```md
Biggest Risk:
Evidence:
Verdict:
Next Validation:
Route To:
```

Use one verdict:

- Include in MVP
- Simplify for MVP
- Validate first
- Defer to future iteration
- Add compatibility placeholder
- Reject for this product layer

For feature requests, separate demand evidence from opinions:

- Weak signals: one-off ask, competitor-copy, internal anxiety, compliments
- Stronger signals: repeated workflow blocker, revenue/retention impact, manual workaround, regulatory/ops requirement, production incident

If evidence is weak but the idea may matter, recommend a low/no-build validation step before PRD drafting.

For detailed verdict definitions and impact criteria, read `references/scope-decision-rubric.md` when the decision is high-stakes, cross-system, or contested.

## Challenge the Build

Before accepting a new build into MVP, ask whether the same business goal can be achieved by:

- reusing existing capability
- adding configuration instead of new behavior
- narrowing supported scenarios
- keeping rare cases manual in this phase
- adding a future-compatible placeholder
- validating demand before implementation

If a smaller path achieves the same current-phase goal with less operational risk, recommend `Simplify for MVP`, `Validate first`, or `Add compatibility placeholder`.

## Use Platform Flow Modeler When

Use `platform-flow-modeler` when a proposed change may introduce new states, callbacks, retries, rollback, reconciliation, migration, manual fallback, or cross-system dependencies.

Use the resulting flow model to decide whether the change should be `Include in MVP`, `Simplify for MVP`, `Validate first`, `Defer to future iteration`, `Add compatibility placeholder`, or `Reject for this product layer`.

## Small Request Expansion Check

When the request sounds simple, translate it into real impact before accepting that it is small.

Examples:

- "Just add a button" may introduce permissions, status transitions, audit logs, notifications, or rollback.
- "Just add a record" may introduce a runtime object, retention rule, query permission, export need, or reconciliation path.
- "Just notify another system" may introduce callback contract, retry, timeout, idempotency, monitoring, and manual replay.
- "Just add a config" may introduce lifecycle, effective time, versioning, rollback, permission, and old-record behavior.

Ask these checks:

- Does it change any object status or lifecycle?
- Does it create a new actor, permission, or approval responsibility?
- Does it trigger callback, notification, audit, report, reconciliation, or manual handling?
- Does it affect existing data, in-flight records, or downstream consumers?
- Does it require rollback, migration, monitoring, or support SOP?
- Can it be handled by existing capability or configuration instead of new platform behavior?

## Impact Table

Use this format:

```md
## Impact Summary

| Area | Impact | Reason | Recommendation |
|---|---|---|---|
| Data Model | Low/Medium/High |  |  |
| Flow / State | Low/Medium/High |  |  |
| UI / Prototype | Low/Medium/High |  |  |
| API / Integration | Low/Medium/High |  |  |
| Permission / Ownership | Low/Medium/High |  |  |
| Operations / Rollout | Low/Medium/High |  |  |

## Recommendation
```

## Recommendation Types

Use one of these recommendations:

- Include in MVP: required for production usability or logical closure.
- Simplify for MVP: needed, but should be implemented with a narrower version.
- Validate first: possible value, but current evidence is too weak to commit delivery capacity.
- Defer to future iteration: useful, but creates disproportionate complexity now.
- Add compatibility placeholder: not implemented now, but data/model naming should not block future support.
- Reject for this product layer: belongs to another system/team or duplicates existing platform capability.

## Complexity Signals

Treat these as scope expansion signals:

- new lifecycle/status states
- new actor, role, or permission model
- group/permission logic
- new runtime object or snapshot rule
- new callback/retry/reconciliation path
- new cross-system dependency
- new portal/tenant/source-system behavior
- new migration requirement
- prototype changes across multiple pages
- operational manual process with no owner
- ambiguous source of truth

## MVP Boundary Rules

Separate:

- `In Scope`
- `Out of Scope`
- `Not Supported in This Phase`
- `Future Iteration`

Ask:

- Is this required for MVP production usability?
- Is it required for logical closure?
- Does it add long-term platform complexity?
- Can existing capability support it?
- Can it be expressed as configuration?
- Can it be represented by a future-compatible field/name without implementing behavior now?
- Who owns temporary manual work if deferred?
- Does this only update a contract, or does it introduce new flow/state/ops behavior?
- If migration or data correction is involved, what is the validation, rollback, and completion checklist?

## Output Style

- Be direct and concise.
- Give a recommendation, not only pros/cons.
- Name the biggest risk instead of producing only a long risk inventory.
- State what must change if included now.
- State what remains stable if deferred.
- Route to the next skill or artifact after the scope decision.
- Avoid drafting detailed PRD sections until the phase decision is clear.

## Output Contract

Default answer shape:

1. Selected mode, when useful
2. Verdict
3. Biggest risk
4. Impact summary
5. Recommended MVP boundary
6. Validation or simplification step
7. What to document next, and which skill/artifact should handle it

For quick questions, keep the answer short but still include a verdict.

This skill should produce a decision gate, not only impact analysis.

If evidence is insufficient, the output should still include a verdict such as `Validate first` plus the cheapest next validation step.

## Quality Checklist

Before finalizing, verify:

- [ ] The verdict is explicit.
- [ ] The biggest risk is named.
- [ ] Build evidence is separated from opinions.
- [ ] Current phase and future phase are not mixed.
- [ ] Hidden impact across data, flow, ownership, API, UI, operations, rollout, and migration is considered.
- [ ] The next route is clear: PRD builder, operating-system framing, PRD reviewer, validation, or RFC follow-up.

## Common Mistakes to Flag

- Accepting "just add..." requests without checking lifecycle, permissions, audit, rollback, or downstream impact.
- Letting future-phase capability leak into MVP because examples mention it.
- Treating weak demand signals as delivery commitments.
- Creating one-off platform behavior for a single business exception.
- Recommending defer without naming temporary owner or manual handling.
- Giving pros/cons without a clear verdict.

## References

- `references/scope-decision-rubric.md`: load for detailed verdict criteria, high-stakes scope decisions, or contested MVP tradeoffs.
