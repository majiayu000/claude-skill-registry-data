---
name: requirements-to-solution
description: "Translate business requirements into domain models, acceptance criteria, design options, and a deployable implementation plan."
---

# Requirements → solution
1. Inspect repository, `CLAUDE.md`, relevant features and ADRs before design. If no repo, work from explicit assumptions.
2. Extract business goals, actors, use cases, business terminology, validations, invariant rules, data and authorization ownership.
3. Enumerate user journeys and domain events; illustrate happy, invalid, concurrent and integration-failure paths.
4. Capture measurable NFRs: P95, availability, peak traffic, tenancy, offline, audit, privacy, regulatory, budget, deployment team capacity.
5. Surface **only blocking unknowns** as questions; label others assumptions with confidence and validation plan.
6. Evaluate 2–3 architecture options using `knowledge/ARCHITECTURE_PLAYBOOK.md`; score complexity, team fit, cost, failure modes, evolvability.
7. Choose one simplest viable option; decide module and transaction boundaries, API contracts, events, data ownership, auth, observability and release strategy.
8. Produce a solution proposal per `templates/SOLUTION_PROPOSAL.md`, separate phased tasks with verifiable acceptance tests and estimates as ranges (if requested).
9. Do **not implement** until explicitly asked to implement; requirements-only task returns design and clear next action.
