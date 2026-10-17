---
name: implementation-order-planner
description: Determines what should be built first by ranking candidate work against dependencies, uncertainty, integration risk, and validation value. Use when the user asks which feature, component, layer, spike, or milestone should come first; how to sequence competing implementation options; or what smallest build step will reduce risk and produce useful evidence.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: project-planning
  task_type: planner
  audience: software-teams-and-coding-agents
  tags:
    - implementation-order
    - dependencies
    - uncertainty
    - integration-risk
    - validation
    - sequencing
  status: draft
  side_effects: none
---

# Implementation Order Planner

## Purpose

Decide what should be built first when several implementation paths are plausible. Produce an evidence-based sequence that respects prerequisites while pulling uncertainty, integration risk, and meaningful validation forward.

This is a planning-only skill. It chooses the order of candidate work; it does not expand every item into a complete implementation plan or write code.

## When to use this skill

Use this skill when:

- The user asks what to build first or how to order competing implementation tasks.
- A feature spans multiple components, services, layers, or repositories with unclear sequencing.
- The safest first step may be a spike, contract test, thin vertical slice, or integration proof rather than foundational production code.
- A team needs to choose between dependency-first, risk-first, or value-first sequencing.
- The current order appears driven by convenience, familiarity, or presentation rather than delivery evidence.

Example triggers:

- “What should we implement first?”
- “Put these features in the safest build order.”
- “Should we start with the API, data model, or UI?”
- “Find the smallest slice that validates this architecture.”
- “Which dependency or unknown should we resolve before committing to the build?”

Do not use this skill when:

- The order is already fixed by a hard external constraint and the user only needs task decomposition.
- The user wants a full implementation plan from settled requirements; use `implementation-plan-writer`.
- The user wants a multi-phase product or delivery roadmap; use `project-roadmap-builder`.
- The main task is to reconcile an existing plan with completed repository work; use `project-plan-reconciler`.
- The request is to implement, patch, or refactor code rather than decide the sequence.

## Inputs to inspect

Start with the smallest useful evidence set:

- Candidate features, tasks, components, or milestones.
- Requirements, acceptance criteria, and desired user outcome.
- Architecture notes, API contracts, schemas, diagrams, or decision records.
- Existing implementation and tests that reveal established boundaries or reusable foundations.
- External systems, libraries, teams, approvals, migrations, or data that impose dependencies.
- Known unknowns, assumptions, failure modes, rollout constraints, and irreversible decisions.
- Available validation methods such as prototypes, contract tests, integration tests, user trials, telemetry, or manual demonstrations.

If the candidates are not explicit, derive a provisional set from the provided brief and label that derivation as an assumption.

## Decision model

Evaluate each candidate across four primary factors:

| Factor | Question | Earlier when... |
|---|---|---|
| Dependency leverage | What later work does this unblock? | It is a real prerequisite or enables several downstream items. |
| Uncertainty reduction | What important assumption can this test? | Failure would materially change architecture, scope, cost, or feasibility. |
| Integration risk | Where are boundaries most likely to fail? | It proves a risky external, cross-layer, or cross-team interaction early. |
| Validation value | What useful evidence will completion produce? | It demonstrates meaningful behavior or enables a clear test or decision. |

Also account for effort, reversibility, and blast radius. Prefer small, reversible work that yields strong evidence, but never move a task ahead of a genuine prerequisite.

Do not calculate a false-precision score by default. Use qualitative ratings such as `high`, `medium`, and `low`, explain the decisive factors, and use numeric scoring only when the user supplies a scoring model or needs comparison across many candidates.

## Workflow

1. Define the decision boundary: state the outcome being sequenced, the candidate work, the planning horizon, and any fixed deadlines or constraints.
2. Identify hard dependencies. Distinguish genuine prerequisites from preferences, conventions, and work that can proceed in parallel.
3. Map uncertainty. Record assumptions whose failure would change the approach, and identify the smallest experiment or implementation slice that could resolve each one.
4. Locate integration risk. Highlight new or unstable boundaries involving external APIs, persistence, authentication, migrations, build systems, browser or platform behavior, or coordination with another team.
5. Identify validation opportunities. Favor increments that produce observable end-to-end behavior, contract evidence, user feedback, or a decisive feasibility result.
6. Compare candidates using the decision model. Include effort and reversibility as modifiers, not substitutes for dependency analysis.
7. Choose the first item. Explain why it dominates the alternatives and state the evidence its completion should produce.
8. Build the remaining order. Sequence prerequisites and risk-reducing slices before dependent expansion, then place polish and low-learning work later.
9. Mark parallel work only when the items do not compete for the same unresolved contract, resource, or decision.
10. Add decision gates. At each gate, state what result allows the plan to continue and what result requires reordering or changing approach.
11. Check for a thin vertical slice. When practical, ensure the sequence reaches a small working path across real boundaries before broad horizontal build-out.
12. State assumptions and confidence. Separate evidence-backed ordering from provisional choices that depend on missing information.

## Ordering heuristics

Use these heuristics as guidance, not absolute rules:

- Resolve architecture-changing unknowns before scaling an approach built on them.
- Test risky boundaries before filling in large amounts of internal implementation.
- Prefer a thin vertical slice when it validates more than isolated layers would.
- Build enabling contracts before their consumers, but use fakes or stubs when they create faster, honest learning.
- Delay irreversible migrations or broad rollouts until smaller proofs reduce uncertainty.
- Avoid building generic infrastructure without a concrete near-term consumer.
- Do not confuse visible UI progress with product validation if the critical risk lies elsewhere.
- Do not put all testing at the end; attach validation to the item whose assumption it checks.

## Output format

Return the result using this structure:

```md
## Recommendation

Build **[first item]** first because [decisive rationale].

## Decision context

- Outcome: ...
- Candidates: ...
- Fixed constraints: ...
- Assumptions: ...

## Candidate comparison

| Candidate | Dependencies | Uncertainty reduction | Integration risk exposed | Validation value | Effort / reversibility | Placement |
|---|---|---|---|---|---|---|
| ... | ... | high / medium / low | high / medium / low | high / medium / low | ... | first / later / parallel / blocked |

## Recommended order

1. **Item** — rationale; evidence expected; exit criteria.
2. **Item** — rationale; dependency satisfied; validation.

## Decision gates

- After step 1: continue if ...; reconsider if ...

## Parallel work

- ...

## Confidence and open questions

- Confidence: high / medium / low
- ...
```

If only two candidates are compared, keep the table compact. If the repository evidence is incomplete, provide a provisional order and name the exact evidence that could change it.

## Quality bar

The task is complete only when:

- The first recommendation is explicit and justified against credible alternatives.
- Hard dependencies are separated from convenient or assumed ordering.
- Important uncertainty and integration risk are moved early enough to affect decisions.
- Each early item produces defined evidence, not merely code volume.
- Validation is attached to the relevant implementation step.
- Parallel work is safe with respect to unresolved contracts and shared decisions.
- Decision gates explain when the sequence should change.
- Assumptions, missing evidence, and confidence are visible.
- The result stays at ordering granularity rather than becoming a full task-by-task implementation plan.

## Edge cases

- If a hard deadline dictates the first item, state that constraint and optimize the remaining order around it.
- If every candidate depends on one unresolved decision, recommend a decision task or spike first rather than arbitrarily ranking implementation work.
- If a prerequisite is large, look for the smallest contract, seam, or partial capability that safely unblocks validation.
- If an integration cannot be tested in the current environment, recommend the closest contract-level proof and record the residual risk.
- If candidates have similar value and risk, prefer the smaller, more reversible item and state that it is a tie-breaker.
- If work can genuinely proceed in parallel, still identify synchronization points and shared contracts.
- If the user supplies only goals, produce a provisional candidate set before ranking it.

## Related skills

- `implementation-plan-writer`
- `project-roadmap-builder`
- `project-plan-reconciler`
- `project-brief-builder`
