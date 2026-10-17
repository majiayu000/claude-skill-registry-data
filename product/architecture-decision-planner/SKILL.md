---
name: architecture-decision-planner
description: Identifies architecture decisions that must be made before implementation and prepares viable alternatives, trade-offs, decision criteria, evidence needs, owners, and deadlines. Use when a project, feature, migration, or integration has unresolved technical choices that affect scope, interfaces, data, dependencies, operations, security, or implementation order.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: project-planning
  task_type: planner
  audience: software-architects-and-technical-leads
  tags:
    - architecture
    - decision-making
    - tradeoffs
    - technical-planning
    - alternatives
    - decision-records
  status: draft
  side_effects: none
---

# Architecture Decision Planner

## Purpose

Expose the architecture choices that materially affect implementation, distinguish blocking decisions from choices that can be deferred, and prepare a decision-ready comparison without silently choosing on behalf of the responsible people.

## When to use this skill

Use this skill when:

- A project or feature is approaching implementation with unresolved technical choices.
- The team needs to compare architecture alternatives using explicit criteria and evidence.
- A migration, integration, platform change, or shared contract may constrain downstream work.
- The user wants a decision agenda, architecture decision backlog, or ADR-ready analysis.
- Estimates or implementation plans depend on choices about boundaries, data, interfaces, dependencies, deployment, security, reliability, or ownership.

Do not use this skill when:

- The architecture decision has already been made and only needs to be documented; use an ADR-writing workflow instead.
- The user wants an implementation task sequence after all material decisions are settled; use `implementation-plan-writer`.
- The main problem is incomplete product requirements rather than technical alternatives; use `requirements-gap-finder`.
- The request is to implement, benchmark, or migrate a system rather than plan the decisions first.

## Inputs to inspect

Start with the smallest relevant set of available inputs:

- Project brief, feature request, PRD, acceptance criteria, and explicit non-goals
- Existing architecture diagrams, ADRs, technical proposals, and system boundaries
- Repository structure, dependency manifests, configuration, schemas, API contracts, and deployment definitions
- Current operational constraints, service-level objectives, observability, security, privacy, accessibility, and compliance requirements
- Migration, compatibility, data retention, rollback, and interoperability requirements
- Team ownership, skills, maintenance capacity, delivery deadline, and cost constraints
- Known alternatives, prototypes, benchmarks, incidents, or stakeholder decisions

Do not infer that an absent requirement is unimportant. Record consequential missing information as an assumption, evidence gap, or prerequisite decision.

## Workflow

1. Define the decision boundary.
   - State the system, feature, migration, or integration in scope.
   - Identify the intended outcome, planning horizon, fixed constraints, and explicit non-goals.
   - Separate confirmed facts from assumptions and proposals.

2. Trace implementation-sensitive surfaces.
   - Inspect component and service boundaries, data ownership, APIs and events, state and persistence, third-party dependencies, deployment topology, security boundaries, reliability, observability, migration, rollback, and maintenance ownership.
   - Ask which choices would change interfaces, estimates, task order, testing strategy, operating cost, reversibility, or the work of multiple teams.

3. Build the decision inventory.
   - Phrase each item as one bounded choice, not a broad topic such as “choose the architecture.”
   - State the implementation work or contract the decision unlocks.
   - Merge duplicates and separate coupled decisions that require different owners or evidence.

4. Classify timing and impact.
   - Mark each decision as `blocking`, `time-bound`, or `deferrable`.
   - Rate impact as `high`, `medium`, or `low` based on blast radius, cost of reversal, uncertainty, and number of downstream consumers.
   - Explain the trigger or last responsible moment for every non-blocking decision.

5. Define decision criteria before comparing alternatives.
   - Derive criteria from goals and constraints rather than personal preference.
   - Consider functional fit, compatibility, accessibility, security, privacy, performance, reliability, scalability, delivery effort, operating cost, testability, observability, maintainability, team familiarity, vendor dependence, migration risk, and reversibility where relevant.
   - Mark hard constraints as pass/fail gates. Weight softer criteria only when the weighting can be justified.

6. Prepare viable alternatives.
   - Include the current-state or “defer change” option when it is genuinely viable.
   - Describe each option at comparable granularity.
   - Eliminate an option only with evidence that it violates a hard constraint; otherwise preserve uncertainty.
   - Avoid false balance: do not pad the comparison with obviously unsuitable choices.

7. Compare trade-offs and consequences.
   - Evaluate every viable alternative against the same criteria.
   - Record benefits, costs, risks, operational consequences, migration implications, lock-in, reversibility, and assumptions.
   - Distinguish facts from estimates and inferences. Do not invent benchmark numbers, costs, or organizational preferences.

8. Identify evidence needed to decide.
   - For material uncertainty, specify the smallest useful action: stakeholder answer, documentation check, prototype, benchmark, threat model, compatibility test, cost estimate, or operational review.
   - State what result would favor or eliminate an alternative.
   - Avoid open-ended research that has no decision threshold.

9. Assign decision mechanics.
   - Name the accountable decision owner when supported by the inputs; otherwise mark ownership unresolved.
   - Identify required contributors and affected consumers.
   - Set a decision deadline or triggering milestone based on downstream dependency and reversal cost, not an arbitrary date.

10. Order the decision agenda.
    - Put blocking, high-impact, and prerequisite decisions first.
    - Show dependencies between decisions and expose circular dependencies.
    - Recommend parallel evidence-gathering only when it does not assume an unresolved upstream choice.

11. Make a recommendation only when justified.
    - If evidence and authority are sufficient, name the leading alternative and explain why it best satisfies the criteria.
    - If they are insufficient, return a conditional recommendation or a decision-ready shortlist instead of pretending certainty.
    - Keep the decision itself open when the responsible owner has not authorized the agent to make it.

12. Check implementation readiness.
    - State which work can safely begin now, which work must wait, and which assumptions must be tracked if work proceeds conditionally.
    - Identify decisions suitable for an ADR after approval.

## Output format

Return the result using this structure:

```md
## Decision readiness summary

- Readiness: blocked | conditional | ready
- Scope: ...
- Decisions: X blocking, Y time-bound, Z deferrable
- Work safe to begin: ...
- Work that must wait: ...

## Known context and assumptions

- Confirmed: ...
- Assumed: ...
- Missing: ...

## Decision agenda

| ID | Decision | Timing | Impact | Unlocks | Owner | Deadline or trigger | Depends on |
|---|---|---|---|---|---|---|---|
| AD-01 | ... | blocking | high | ... | ... | ... | ... |

## Decision briefs

### AD-01 — Decision title

**Question:** One bounded decision question.

**Context and constraints:** ...

**Criteria:**

| Criterion | Gate or weight | Why it matters |
|---|---|---|
| ... | ... | ... |

**Alternatives:**

| Alternative | Benefits | Costs and risks | Reversibility | Evidence confidence |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

**Evidence needed:** ...

**Recommendation:** preferred | conditional | undecided — rationale.

**Consequences:** ...

## Decision dependencies and sequence

1. ...

## Implementation guardrails

- May begin now: ...
- Must wait: ...
- Track as explicit assumptions: ...
- Convert to ADR after approval: ...
```

Keep the comparison proportional. For a small, reversible choice, a compact decision brief is enough; reserve full matrices for consequential or contested decisions.

## Quality bar

The task is complete only when:

- Every listed decision is a bounded question that unlocks identifiable implementation work or a shared contract.
- Blocking decisions are separated from time-bound and safely deferrable choices.
- Alternatives are viable, compared at the same level, and assessed against criteria derived from actual goals and constraints.
- Facts, assumptions, estimates, recommendations, and unresolved questions are clearly distinguished.
- High-impact uncertainty has a focused evidence action and a result threshold tied to the decision.
- Decision dependencies, owners, affected consumers, and last responsible moments are explicit when knowable.
- Recommendations explain trade-offs and consequences rather than presenting a context-free winner.
- The output states what implementation may begin and what must wait.
- No architecture choice is treated as approved without evidence of the appropriate authority.

## Edge cases

- If context is sparse, produce a provisional decision inventory and targeted discovery questions; do not fabricate alternatives or constraints.
- If only one viable alternative remains, show which hard constraints eliminated the others and still assess the remaining option's risks.
- If a choice is cheap and reversible, defer it unless it blocks a contract or would create avoidable rework.
- If decisions are tightly coupled, identify a governing decision or propose a small experiment that resolves the coupling.
- If stakeholders optimize for conflicting outcomes, expose the conflict and required owner instead of hiding it in a weighted score.
- If a legacy system must remain operational, treat coexistence, migration, data integrity, rollback, and observability as first-class decision criteria.
- If external products or current platform capabilities determine feasibility, mark the required source verification; do not rely on stale recollection.
- If the user requests implementation during this workflow, finish the decision boundary first and obtain the missing decision authority before making consequential changes.

## Related skills

- `constraint-mapper`
- `requirements-gap-finder`
- `implementation-order-planner`
- `implementation-plan-writer`
- `task-dependency-mapper`
