---
name: mvp-discovery
description: "Turn vague ideas into shippable MVPs: problem, users, scope cuts, stories, acceptance criteria. Use before any new product build."
---

# mvp-discovery

Discover the smallest thing that proves value, then specify it so an agent can build it.
## Inspection

Interview/behavioral evidence: who hurts, frequency, current workaround, willingness to pay or switch; competitor handling of the same job.

## Decision rules

One primary job-to-be-done for v1; explicit non-goals; impact × confidence ÷ effort ordering; success metric defined before build.


## Activate when

- Starting a feature, product, or significant change with unclear requirements.

## Do NOT activate for

- Pure technical refactors (see core/refactoring).

## Procedure

1. Problem: who hurts, how often, current workaround, willingness to pay/switch.
2. Cut: one primary job-to-be-done for v1; explicitly list non-goals.
3. Specify: user stories with acceptance criteria, UX flow, data needs, success metric (problem, users, scope cuts, prioritization, handoff criteria).
4. Prioritize: impact × confidence ÷ effort; flag risks and unknowns with owners.
5. Hand off: PRD feeds `../../core/requirements-analysis/` → `../../core/planning/`; no code before the spec is accepted.
6. Verify: walk the spec against the story (every claim testable), confirm analytics hook for the success metric.

## Failure modes

Solution-first specs; scope covering three jobs 'while we're at it'; success metric defined after launch; no named owner for unknowns.

## Escalation

Spec writing → core/requirements-analysis; analytics wiring → startup/launch-ops.
