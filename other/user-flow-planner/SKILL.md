---
name: user-flow-planner
description: Converts a feature brief, requirement, or product idea into primary, secondary, failure, empty, loading, and recovery user flows before implementation. Use when the user asks to map journeys, alternate paths, interface states, decision points, error handling, or recovery behavior before writing code.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: project-planning
  task_type: planner
  audience: product-designers-and-frontend-teams
  tags:
    - user-flows
    - product-planning
    - interaction-design
    - interface-states
    - error-recovery
    - requirements
  status: draft
  side_effects: none
---

# User Flow Planner

## Purpose

Turn a feature brief into an implementation-ready map of how users enter, progress through, leave, fail within, and recover from the experience. Cover meaningful alternate paths and transient states without inventing unsupported product requirements.

## When to use this skill

Use this skill when:

- A feature needs its user journeys defined before design or implementation begins.
- The user asks for a happy path plus alternate, failure, empty, loading, or recovery flows.
- Requirements describe an outcome but omit triggers, decision points, system responses, or exits.
- Designers, developers, and QA need one shared behavioral model.

Do not use this skill when:

- The user only needs an implementation task sequence; use an implementation-planning skill.
- The user wants a visual style, wireframe, or finished interface rather than behavioral flows.
- Existing flows need a coverage audit rather than a new plan; use `interface-state-coverage-review`.
- The request is only for technical architecture with no user interaction.

## Inputs to inspect

Start with the smallest useful set of available inputs:

- Feature brief, user story, acceptance criteria, or product requirements
- Target users, roles, permissions, and user goals
- Entry points, prerequisites, and authentication state
- Existing screens, routes, components, wireframes, or screenshots
- Relevant domain rules, data constraints, integrations, and platform conventions
- Related analytics, support issues, known failure modes, or current behavior

If essential context is absent, state assumptions and unresolved decisions. Do not silently turn assumptions into requirements.

## Flow model

For each flow, identify:

- **Actor:** the user or system role taking action
- **Goal:** the outcome the actor is trying to achieve
- **Trigger:** the event or entry point that begins the flow
- **Preconditions:** required permissions, data, connectivity, or prior state
- **Steps:** user actions and observable system responses
- **Decision points:** conditions that branch the path
- **States:** stable and transient interface states encountered
- **Exit:** success, cancellation, abandonment, handoff, or terminal failure
- **Recovery:** how the user retries, reverses, resumes, or gets help

Classify flows as:

1. **Primary:** the most common successful route to the feature's core outcome.
2. **Secondary:** valid alternatives such as editing, cancelling, skipping, returning, or using another entry point.
3. **Failure:** validation, permission, network, service, conflict, timeout, or unexpected-error paths.
4. **Empty:** first-use, no-results, deleted-content, unavailable-data, or filtered-to-zero paths.
5. **Loading:** initial, inline, deferred, background, long-running, and stale-data behavior.
6. **Recovery:** retry, undo, resume, reauthenticate, resolve conflict, restore input, contact support, or safely exit.

## Workflow

1. **Frame the feature.** Restate the user, goal, scope boundary, entry points, success outcome, and explicit exclusions. Separate evidence from assumptions.
2. **Inventory actors and starting conditions.** Identify roles, permissions, signed-in states, device or channel differences, existing versus first-time users, and relevant data conditions.
3. **Map the primary flow.** Write the shortest coherent path from trigger to confirmed outcome. Pair every user action with the system response the user can perceive.
4. **Add decision branches.** Mark choices and conditions that change the path. Name the rule governing each branch and show where paths rejoin or terminate.
5. **Map secondary flows.** Cover realistic alternatives such as back, cancel, edit, skip, save for later, switch method, revisit, and duplicate action. Exclude speculative edge cases with no product relevance.
6. **Map state-dependent flows.** Define empty and loading behavior at the points where they occur, including what the user sees, what remains actionable, and how progress or absence is communicated.
7. **Map failures by boundary.** Consider user input, permissions, local state, network, backend or integration, concurrency, and unexpected failures. Describe preserved data and prohibited actions after failure.
8. **Connect every recoverable failure to recovery.** Specify retry conditions, restored context, idempotency expectations, undo or escape routes, escalation, and what success looks like after recovery. Explicitly label terminal failures.
9. **Check continuity.** Verify each branch has an entry and exit, every action receives feedback, loading resolves, empty states offer an appropriate next step, and recovery does not loop indefinitely or duplicate work.
10. **Identify implementation implications.** Extract required states, permissions, validations, persistence needs, service dependencies, telemetry points, and acceptance scenarios without prescribing architecture prematurely.
11. **Record open decisions.** List only questions that materially change a flow, ordered by implementation impact. Provide a safe default when one is supportable.

## Output format

Return:

```md
## Feature frame

- User and goal:
- Scope:
- Entry points:
- Success outcome:
- Assumptions:
- Exclusions:

## Flow inventory

| ID | Type | Actor | Trigger | Outcome | Priority |
|---|---|---|---|---|---|

## Flow details

### F1 — Flow name

- Type:
- Preconditions:
- Steps:
  1. User ...
     - System ...
- Decisions and branches:
- Exit state:
- Recovery or next step:

## State coverage matrix

| Context | Default | Empty | Loading | Failure | Recovery |
|---|---|---|---|---|---|

## Implementation implications

- Required interface states:
- Validation and permissions:
- Data preservation and idempotency:
- Dependencies:
- Telemetry or support signals:

## Open decisions

| Priority | Decision | Why it changes the flow | Suggested default |
|---|---|---|---|

## Acceptance scenarios

- [ ] Given ..., when ..., then ...
```

Use text steps and tables by default. Add a Mermaid flowchart only when branching relationships are materially clearer as a diagram, and keep the written details as the source of truth.

## Quality bar

The task is complete only when:

- The primary flow reaches a clear, observable outcome.
- Relevant secondary, failure, empty, loading, and recovery flows are covered or explicitly marked not applicable.
- User actions and system responses are distinguishable at every step.
- Every branch has a condition and an exit, rejoin point, or terminal state.
- Recoverable failures preserve appropriate user input and describe a safe next action.
- Loading states define completion, timeout, cancellation, or failure behavior.
- Assumptions and unresolved product decisions are visible.
- Implementation implications and acceptance scenarios trace back to the mapped flows.

## Edge cases

- If the feature has multiple roles, map shared behavior once and split only where permissions or outcomes differ.
- If the flow spans devices or channels, identify handoff state, continuity requirements, and stale-state behavior.
- If an operation can be repeated, address duplicate submissions, idempotency, and confirmation ambiguity.
- If the user can abandon and return, define whether progress expires, autosaves, resumes, or restarts.
- If recovery is impossible, explain the terminal state, preserved data, support route, and safe exit.
- If requirements conflict, show the affected branches and request a decision instead of choosing silently.
- If a state category does not apply, record the reason rather than forcing an artificial flow.

## Related skills

- `project-brief-builder`
- `requirements-gap-finder`
- `implementation-plan-writer`
- `interface-state-coverage-review`
