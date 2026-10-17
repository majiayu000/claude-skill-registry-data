---
name: delivery-planning
description: Plan and run delivery in phases — plan gates, milestones, risk register, decision log, and honest status.
version: 1
triggers: delivery plan, phased plan, milestones, risk register, project planning, roadmap
category: Engineering & code
blurb: Plan and run delivery in phases — plan gates, milestones, a risk register and honest status.
archetype: knowledge
example: Turn this project into a phased delivery plan with exit criteria.
---

# Delivery Planning — phased delivery & the PMO seat

Charter: **chat → plan → build → deploy → test → recommend**. No building before an approved plan; never a direct-to-production change.

## When to use
- Any task beyond a trivial fix: plan it before building.
- Multi-step projects: milestones, dependencies, sequencing.
- Status is unclear: re-establish the plan and log it.

## Method
1. **Frame**: goal, deliverable, constraints (time, cost, licenses, environment), and the definition of done.
2. **Phase the work**: phases with **exit criteria** — what must be true to move on.
3. **Estimate honestly**: sizes (S/M/L) with assumptions listed; flag the least-known item as the top risk.
4. **Risk register**: top risks with mitigation and trigger; reviewed each phase.
5. **Decision log**: append-only (date, decision, rationale, alternatives). Log at decision time, not later.
6. **WIP limit**: finish phases; don't parallelize beyond capacity. One worked item per lane; batch bulk imports.
7. **Status**: phase, done, next, blockers, confidence — one screen, no status theater.

## Artifacts
- `PLAN.md` (phases + exit criteria), `RISKS.md`, decision-log entries.

## Quality gates
- [ ] Plan approved before build starts.
- [ ] Every phase has exit criteria and an owner.
- [ ] Risks have triggers and mitigations.
- [ ] Decisions logged when made (not reconstructed later).

## Red lines
- No silent re-scoping — plan updates go through approval.
- Deploys are HITL (human approves); automation prepares, humans decide.

## Related
`product-requirements` (what to build) · `release-management` (ship gates) · `code-review-practice` (per-change gates).
