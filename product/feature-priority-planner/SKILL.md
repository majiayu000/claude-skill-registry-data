---
name: feature-priority-planner
description: Ranks proposed product or portfolio features by user value, implementation cost, dependency impact, risk, and portfolio value. Use when the user asks what to build next, how to prioritize a feature backlog, which ideas to defer, or why one proposed feature should precede another.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: project-planning
  task_type: planner
  audience: product-builders-and-project-maintainers
  tags:
    - feature-prioritization
    - product-planning
    - backlog
    - decision-making
    - portfolio
  status: draft
  side_effects: none
---

# Feature Priority Planner

## Purpose

Turn proposed features into an evidence-aware priority order. Compare user value, implementation cost, dependency impact, delivery risk, and portfolio value; expose assumptions and hard constraints; and recommend what to build now, validate first, defer, or reject.

## When to use this skill

Use this skill when:

- The user asks which proposed feature should be built first or next.
- A backlog needs a transparent, repeatable ranking.
- Product benefit must be balanced against engineering effort and risk.
- A personal, open-source, or commercial project should demonstrate useful portfolio capabilities.
- Stakeholders disagree about priorities and need the tradeoffs made explicit.

Do not use this skill when:

- Priorities are fixed and the user needs implementation sequencing; use `implementation-order-planner`.
- The user needs a phased delivery roadmap; use `project-roadmap-builder`.
- The task is to define the smallest viable release rather than rank a broader backlog; use `mvp-scope-planner`.
- There is only one feature and no meaningful alternative.
- The user asks to implement features. This skill produces a decision artifact, not code changes.

## Inputs to inspect

- Proposed feature names, descriptions, target users, and intended outcomes.
- Product goals, success measures, constraints, and planning horizon.
- User research, support requests, analytics, feedback, or issue frequency.
- Relevant architecture, source areas, technical debt, and test coverage.
- Dependencies, prerequisites, shared foundations, integrations, and blockers.
- Effort estimates, team capacity, deadlines, and operational obligations.
- Known security, privacy, accessibility, performance, compatibility, or maintenance risks.
- Portfolio goals, target roles or clients, and capabilities the project should credibly demonstrate.

If evidence is incomplete, continue with labeled assumptions. Ask only questions whose answers could materially change the ranking.

## Scoring model

Score each factor from 1 to 5. Higher is always better: cost and risk scores represent affordability and safety, not raw cost and danger.

| Factor | 1 | 3 | 5 |
|---|---|---|---|
| User value | Little verified benefit | Useful to a meaningful segment | Solves a frequent, severe, or strategic user problem |
| Implementation cost | Very large or uncertain effort | Moderate effort | Small, bounded effort |
| Dependency impact | Blocked or creates substantial coupling | Mostly independent | Unblocks or simplifies important follow-on work |
| Risk | High delivery or outcome risk | Manageable risk | Low risk with familiar recovery paths |
| Portfolio value | Adds little credible signal | Demonstrates a relevant capability | Creates distinctive, demonstrable evidence for a target audience |

Use these default weights unless the user provides priorities:

- User value: 35%
- Implementation cost: 20%
- Dependency impact: 15%
- Risk: 15%
- Portfolio value: 15%

```txt
score = (user value × 0.35) + (implementation cost × 0.20) +
        (dependency impact × 0.15) + (risk × 0.15) +
        (portfolio value × 0.15)
```

Treat the score as decision support, not an automatic verdict. Hard blockers, regulatory duties, critical defects, contractual commitments, and prerequisite relationships can override the numeric order. Do not inflate portfolio value at the expense of user safety or product reliability.

## Workflow

1. Define the decision: identify the product goal, target users, planning horizon, constraints, and what priority should optimize.
2. Normalize candidates as comparable outcomes with a beneficiary and scope. Split bundled ideas when value or cost differs materially; merge duplicates.
3. Record supporting facts, estimates, assumptions, and unknowns. Distinguish observed user need from stakeholder preference.
4. Before scoring, mark mandatory work, hard blockers, prerequisites, mutually exclusive choices, and features needing a validation spike.
5. Confirm the weights. Use the defaults or adapt them to the stated strategy, explaining changes. If portfolio value is irrelevant, set it to zero and redistribute its weight explicitly.
6. Score every factor with consistent anchors. Add a short rationale and confidence level (`high`, `medium`, or `low`) for each feature.
7. Calculate totals, then perform a constraint pass. Change the recommended order only for explicit gates or obligations, and explain each override.
8. Test sensitivity for close results by changing the most uncertain score by one point or applying a plausible alternative weighting. Treat candidates as tied when modest assumptions reverse their order.
9. Place features into `build now`, `validate first`, `later`, or `do not pursue`.
10. Recommend the next decision or evidence-gathering step for low-confidence and closely ranked candidates.

## Output format

Return:

```md
## Recommendation

One concise statement of what to build next and why.

## Decision context

- Goal:
- Target users:
- Constraints:
- Weights:

## Ranked features

| Rank | Feature | User value | Cost | Dependencies | Risk | Portfolio | Weighted score | Confidence | Action |
|---:|---|---:|---:|---:|---:|---:|---:|---|---|
| 1 | ... | ... | ... | ... | ... | ... | ... | ... | build now |

## Rationale and evidence

- **Feature:** evidence, assumptions, decisive tradeoffs, and any override.

## Dependencies and overrides

- Prerequisites, blockers, obligations, or ties that affect the numeric order.

## Validation needs

- Unknowns that could change the ranking and the cheapest way to resolve them.

## Deferred or rejected

- Feature — reason and condition for reconsideration.
```

If the input is too sparse for defensible numbers, return a provisional tiered ranking and an evidence plan instead of manufacturing precision.

## Quality bar

The task is complete only when:

- Every candidate is comparable in scope or explicitly marked otherwise.
- Scores use consistent direction and anchors, with higher always more favorable.
- Each score is traceable to evidence or a labeled assumption.
- Dependencies and mandatory work are handled outside the formula when they act as gates.
- Numeric rank is distinguished from the final recommended order.
- Close or low-confidence rankings receive a sensitivity check.
- The result says what to build, validate, defer, and reconsider later.
- Portfolio value reflects credible, demonstrable relevance rather than novelty alone.

## Edge cases

- If features serve different user groups, state whose value is optimized or provide separate views.
- If estimates use inconsistent units, normalize them before scoring and flag remaining uncertainty.
- If one feature is a prerequisite for another, rank the outcome separately but sequence the prerequisite first when the outcome is selected.
- If work is mandatory for safety, accessibility, compliance, or a contract, label it mandatory instead of forcing it to compete with elective features.
- If candidates tie, prefer stronger evidence, lower downside, faster learning, or greater reversibility; otherwise report the tie.
- If portfolio goals conflict with user goals, prioritize user safety and product integrity.
- If the backlog is large, triage it into rough tiers before scoring realistic near-term candidates.

## Related skills

- `implementation-order-planner`
- `mvp-scope-planner`
- `project-roadmap-builder`
- `milestone-planner`
- `requirements-gap-finder`
