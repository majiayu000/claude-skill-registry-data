---
name: pm-write-spec
version: 1.0.0
description: Write a PRD or feature spec that aligns design and engineering — problem with evidence, explicit non-goals, measurable success metrics, and testable acceptance criteria.
author: matrixx0070
tags: [product, spec, prd, requirements, planning, acceptance-criteria]
capabilities: []
---

# Write Spec

## When to use
Use this when a feature is ready to move from idea to build and you need a document that aligns design, engineering, and stakeholders on what you are building, why, and how you will know it worked.

**Not for:** early idea exploration (use pm-brainstorming), a lightweight status note (use pm-stakeholder-update), or dictating implementation details that belong to engineering. If the problem is still unvalidated, do research first, do not spec a guess.

## Method
1. State the problem and context: who has it, evidence it matters, why now. Ground in data or research, not assertion.
2. Define goals and non-goals explicitly. **Decision point:** for every tempting scope addition, decide goal or non-goal, non-goals prevent creep and matter as much as goals.
3. Specify success metrics: the primary metric proving it worked, plus guardrails that must not regress, each with target and measurement window.
4. Describe the solution: user stories, key flows, and states (empty, error, edge). Enough for engineering to estimate without dictating how to build it.
5. Write acceptance criteria as testable statements (Given/When/Then or clear pass conditions). These are the definition of done.
6. Cover the rest: dependencies, risks, open questions, rollout and instrumentation plan.

## Example
Problem: 30% of users never complete profile setup (source: funnel data). Goal: raise setup completion to 60%. Non-goal: redesigning the whole settings area. Primary metric: setup completion rate; guardrail: no drop in day-7 retention. Acceptance criterion: "Given a new user on the setup screen, When they skip an optional field, Then they can still reach the dashboard." Rollout: 10% flag, watch completion for one week.

## Pitfalls
- Asserting the problem matters with no data or research behind it.
- Omitting non-goals, inviting scope creep mid-build.
- Success metrics with no target or window, so "worked" is unfalsifiable.
- Over-specifying implementation, stepping on engineering's design space.

## Output format
```
# Spec: [feature] — [date] — [status: draft/review/approved]
Summary & problem statement (with evidence).

## Goals / Non-goals
- Goals: ...
- Non-goals: ...

## Success metrics
- Primary: [metric] — target — window
- Guardrails: [metric must not regress]

## Solution
- User stories, key flows, states (empty/error/edge)

## Acceptance criteria (testable)
- Given/When/Then ...

## Dependencies, risks, open questions
- ...

## Rollout & measurement plan
- ...
Open questions stay visible, not papered over.
```
