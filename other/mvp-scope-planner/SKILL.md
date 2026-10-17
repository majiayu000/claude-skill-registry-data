---
name: mvp-scope-planner
description: Defines the smallest coherent MVP scope that can test a product assumption or deliver a usable first outcome, with explicit inclusions, exclusions, validation criteria, tradeoffs, and follow-on work. Use when the user asks to scope an MVP, cut a first release, prioritize must-haves, reduce feature scope, or decide what to build now versus later.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: project-planning
  task_type: planner
  audience: product-teams-and-builders
  tags:
    - mvp
    - scope
    - prioritization
    - product-planning
    - validation
    - tradeoffs
  status: draft
  side_effects: none
---

# MVP Scope Planner

## Purpose

Define the smallest coherent first release that serves a specific user, completes a core journey, and produces evidence about a key assumption. Minimize scope without reducing the MVP to disconnected features, unusable shortcuts, or a release that cannot validate its premise.

## When to use this skill

Use this skill when:

- The user asks what belongs in an MVP or first release.
- A feature list must be divided into build now, later, and not planned.
- Time, budget, or capacity requires explicit scope tradeoffs.
- A product assumption needs the smallest credible validation vehicle.
- A broad concept needs a narrow end-to-end release boundary.

Do not use this skill when:

- The problem, target user, or desired outcome has not been defined well enough to scope.
- The user only needs milestones for an already-decided scope.
- “MVP” actually means a production launch with fixed compliance, reliability, or contractual requirements; preserve those gates and label the release accurately.
- The task is to implement features rather than decide scope.

## Inputs to inspect

- Problem statement, target user, core job, and desired outcome.
- Product brief, requirements, feature ideas, user journeys, or backlog.
- Primary assumption to validate and the evidence needed to evaluate it.
- Constraints such as deadline, capacity, platforms, integrations, compliance, accessibility, privacy, reliability, and support.
- Existing product capabilities, reusable assets, technical dependencies, and known risks.
- Success measures and conditions that would trigger iteration, expansion, or stopping.

## Workflow

1. Frame the MVP decision: name the target user, painful problem, core job, intended outcome, primary assumption, and binding constraints.
2. Define the thinnest complete user journey from entry to achieved outcome. Include essential feedback, failure recovery, accessibility, privacy, security, and operational needs; these are quality constraints, not optional polish.
3. Inventory candidate capabilities. Rewrite vague features as user or operational outcomes before prioritizing them.
4. Test every candidate against four questions:
   - Is it necessary to complete the core journey?
   - Is it necessary to test the primary assumption?
   - Is it required by safety, law, trust, accessibility, privacy, security, or platform constraints?
   - Does excluding it make the result misleading, unusable, or prohibitively manual?
5. Classify each item as `MVP`, `later`, `experiment-only`, or `not planned`. Record the reason and consequence of deferral.
6. Prefer reversible, manual, or narrow solutions when they preserve the user outcome and validation integrity. Do not create hidden operational work that the team cannot sustain.
7. Define MVP acceptance and validation criteria: what must work, for whom, under what conditions, and what evidence will count as success, failure, or inconclusive.
8. Identify scope risks, dependency traps, quality floors, and assumptions that could invalidate the plan. Recommend a spike or prototype when uncertainty should be retired before building the MVP.
9. Specify the post-MVP decision path. Tie later work to evidence or triggers rather than treating it as an automatic phase two.
10. Check coherence: the MVP must deliver one complete outcome, be operable by the team, and generate evidence that can change a decision.

## Output format

Return:

```md
## MVP thesis

- Target user:
- Problem and core job:
- MVP outcome:
- Primary assumption:
- Constraints and quality floors:

## Core journey

1. ...

## Scope decisions

| Capability | Classification | Rationale | Deferral consequence or trigger |
|---|---|---|---|

## MVP acceptance criteria

- [ ] ...

## Validation plan

- Evidence to collect:
- Success signal:
- Failure signal:
- Inconclusive result:
- Next decision:

## Risks and tradeoffs

| Risk or tradeoff | Impact | Response |
|---|---|---|

## Open decisions and assumptions

- ...
```

## Quality bar

The task is complete only when:

- The MVP is tied to one explicit user outcome and one primary learning goal.
- The core journey is complete rather than a loose collection of features.
- Every candidate capability has a clear disposition and rationale.
- Required quality, trust, accessibility, privacy, security, and compliance constraints remain in scope.
- Success, failure, and inconclusive evidence lead to explicit next decisions.
- Deferred work has evidence-based triggers and is not silently promised.

## Edge cases

- If the user has multiple unrelated target users or problems, choose one MVP wedge or present separate alternatives rather than combining them.
- If no meaningful assumption remains, frame the work as a minimum viable release and optimize for outcome, risk, and operability instead of artificial experimentation.
- If a manual workaround transfers unacceptable burden or risk to users or operators, keep the enabling capability in scope.
- If an integration dominates cost or uncertainty, consider a concierge test, prototype, or dependency spike before committing to the MVP build.
- If stakeholders label every feature essential, expose the consequence of removing each item and offer coherent scope options with explicit cost and learning tradeoffs.

## Related skills

- `project-brief-builder`
- `milestone-planner`
- `project-roadmap-builder`
- `implementation-plan-writer`
