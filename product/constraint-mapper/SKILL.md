---
name: constraint-mapper
description: Identifies and maps technical, time, budget, platform, accessibility, privacy, and maintenance constraints that affect a project plan. Use when the user asks to surface planning constraints, test feasibility, expose tradeoffs, identify hard limits and assumptions, or revise scope, sequencing, architecture, and validation around real delivery conditions.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: project-planning
  task_type: planner
  audience: product-teams-and-project-planners
  tags:
    - constraints
    - feasibility
    - project-planning
    - tradeoffs
    - accessibility
    - privacy
    - maintenance
  status: draft
  side_effects: none
---

# Constraint Mapper

## Purpose

Turn stated and implied delivery limits into an evidence-based constraint map. Show which constraints are binding, uncertain, conflicting, or negotiable and explain how each one changes scope, architecture, sequencing, validation, or ongoing ownership.

## When to use this skill

Use this skill when:

- A project brief or proposed plan needs a feasibility and constraints pass.
- The user asks what limits the solution, what tradeoffs are unavoidable, or what could invalidate the plan.
- Deadlines, budgets, platforms, policies, accessibility needs, privacy obligations, or maintenance capacity may change the approach.
- A team needs constraints converted into planning decisions, acceptance conditions, spikes, or open questions.

Do not use this skill when:

- The user only needs a complete implementation plan; map constraints first, then use an implementation-planning skill.
- The task is a formal legal, privacy, security, or accessibility compliance audit requiring specialist judgment.
- The user wants effort or cost estimates without enough scope and delivery context to support them.
- A single known technical limitation is better handled by a focused compatibility or architecture investigation.

## Inputs to inspect

Start with the smallest relevant set of sources:

- Project brief, PRD, feature request, roadmap, acceptance criteria, and stated non-goals
- Existing implementation plan, architecture notes, decision records, diagrams, and API contracts
- Target platforms, browsers, devices, runtimes, hosting, integrations, and deployment model
- Delivery date, milestones, staffing, skills, procurement limits, and budget range
- Accessibility requirements, supported assistive technologies, and applicable quality standards
- Data categories, user consent expectations, retention rules, third parties, and privacy policies
- Ownership, support model, operational capacity, update cadence, and expected service lifetime
- Repository evidence such as `README.md`, `package.json`, configuration, workflows, source layout, tests, and dependency manifests when they clarify feasibility

Treat user statements and supplied artifacts as evidence. Do not search external sources or claim legal or regulatory requirements unless the user requests research and the environment supports it.

## Constraint model

Classify each item before recommending a response:

- **Hard constraint:** cannot be violated within the current decision boundary.
- **Soft constraint:** preferred limit that may be traded with explicit approval.
- **Assumed constraint:** inferred from incomplete evidence and awaiting confirmation.
- **Unknown:** missing information that could materially change the plan.

Also assign:

- **Category:** technical, time, budget, platform, accessibility, privacy, maintenance, or cross-cutting.
- **Source:** exact user statement, artifact, policy, platform fact, or inference.
- **Confidence:** confirmed, likely, or uncertain.
- **Plan effect:** scope, architecture, sequencing, staffing, procurement, validation, rollout, or operations.
- **Response:** comply, reduce scope, choose an alternative, validate early, seek an exception, or escalate a decision.

Do not label a preference as a hard constraint. Do not treat accessibility, privacy, security, testing, or maintainability as optional polish merely because they compete with schedule or budget.

## Workflow

1. Define the decision boundary.
   - State the project or feature being planned, the planning horizon, target outcome, and decisions the map should inform.
   - Separate fixed context from proposed solution details.
2. Extract explicit constraints.
   - Preserve the source wording and identify who or what imposes each limit.
   - Record measurable thresholds, dates, supported targets, exclusions, and approval conditions where available.
3. Surface implied constraints and unknowns by category.
   - **Technical:** existing architecture, dependencies, integration limits, data migration, performance, security, reliability, offline behavior, and testability.
   - **Time:** deadlines, milestone coupling, review lead times, procurement, migrations, release windows, and staffing availability.
   - **Budget:** engineering capacity, licenses, infrastructure, vendors, devices, testing, support, and recurring costs.
   - **Platform:** browsers, operating systems, devices, runtimes, app stores, hosting, APIs, permissions, and distribution rules.
   - **Accessibility:** semantic and keyboard behavior, assistive technology, zoom and reflow, contrast, motion, captions, cognitive load, testing, and user accommodations.
   - **Privacy:** data minimization, consent, purpose, retention, deletion, location, third parties, telemetry, access control, and incident handling.
   - **Maintenance:** ownership, documentation, dependency updates, observability, support load, content upkeep, compatibility testing, deprecation, and exit strategy.
4. Normalize the findings.
   - Merge duplicates while preserving distinct sources.
   - Separate facts from interpretations and assumptions.
   - Rewrite vague limits into testable statements when evidence permits; otherwise retain them as questions.
5. Evaluate impact and binding strength.
   - For each constraint, explain the concrete planning consequence and what fails if it is ignored.
   - Mark constraints that determine feasibility, critical-path timing, minimum quality, or total cost of ownership.
6. Find interactions and conflicts.
   - Identify combinations that amplify risk, such as a fixed deadline plus broad platform support, or a low operating budget plus a high-maintenance architecture.
   - Flag conflicts that cannot be solved by sequencing alone and require a scope, budget, deadline, platform, or quality decision.
7. Convert constraints into plan changes.
   - Recommend scope boundaries, architectural guardrails, sequencing changes, early experiments, acceptance criteria, review gates, rollout controls, and ownership commitments.
   - Prefer reversible responses when evidence is uncertain.
8. Prioritize validation.
   - Put high-impact uncertain constraints first.
   - Name the smallest useful check, prototype, stakeholder answer, policy review, or platform test and the decision it unlocks.
9. State residual risk and readiness.
   - Distinguish resolved constraints from accepted risk and unresolved blockers.
   - Rate the work `ready to plan`, `conditionally ready`, or `not ready`, with a concise reason.

## Output format

Return:

```md
## Constraint summary

- Planning boundary: ...
- Binding constraints: ...
- Highest-impact unknown: ...
- Readiness: ready to plan | conditionally ready | not ready

## Constraint map

| Priority | Category | Constraint | Class | Source / confidence | Plan effect | Recommended response |
|---|---|---|---|---|---|---|
| P0-P3 | ... | ... | hard / soft / assumed / unknown | ... | ... | ... |

## Interactions and tradeoffs

- Constraint A + Constraint B: combined effect and decision required.

## Required plan changes

- Scope: ...
- Architecture: ...
- Sequencing and validation: ...
- Delivery and operations: ...

## Questions and validation actions

| Order | Unknown or assumption | Why it matters | Smallest validation | Decision unlocked | Owner |
|---|---|---|---|---|---|

## Residual risks

- ...
```

Use `P0` for a feasibility, safety, legal, or delivery blocker; `P1` for a major plan-changing constraint; `P2` for a meaningful but manageable constraint; and `P3` for a low-impact consideration. Omit empty sections rather than inventing content.

## Quality bar

The task is complete only when:

- All seven requested domains are considered, even when the result is “no evidence provided.”
- Every constraint is tied to a source or explicitly labeled as an inference or unknown.
- Hard constraints, preferences, assumptions, and unknowns are not conflated.
- Findings explain concrete effects on the plan rather than merely naming concerns.
- Interactions between constraints and total lifecycle costs are considered.
- Accessibility and privacy are incorporated into scope and acceptance conditions, not deferred as polish.
- High-impact uncertainty has a proportionate validation action and decision owner when known.
- The final readiness judgment follows from the evidence and identifies any blockers.

## Edge cases

- If inputs are sparse, produce a provisional map, avoid false precision, and prioritize the few questions most likely to change feasibility or scope.
- If a deadline and fixed scope conflict, state that capacity, quality, risk, or the deadline must change; do not manufacture a schedule that satisfies all four.
- If budget is unknown, identify cost drivers and decision thresholds instead of inventing a monetary estimate.
- If a constraint comes from law, policy, contract, or platform rules, quote or cite the supplied source and recommend specialist verification when interpretation matters.
- If accessibility or privacy requirements are unspecified, preserve a reasonable quality floor and record target standards, data practices, and test coverage as unresolved decisions.
- If a legacy platform is mandatory, include its effect on architecture, tooling, testing capacity, performance, and maintenance rather than treating support as a single checkbox.
- If maintenance ownership is absent, treat long-lived infrastructure, dependencies, content, and data processes as plan risks with an explicit ownership decision.
- If constraints conflict across stakeholders, name the decision owner if known and present viable tradeoffs without silently choosing one stakeholder's preference.

## Related skills

- `requirements-gap-finder`
- `project-brief-builder`
- `mvp-scope-planner`
- `implementation-order-planner`
- `implementation-plan-writer`
- `project-roadmap-builder`
