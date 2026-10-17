---
name: task-scope-clarifier
description: Clarifies a rough implementation request into a bounded task with a goal, inclusions, exclusions, likely affected files, acceptance criteria, risks, unknowns, and a recommended first step. Use when the user asks to check a request before implementation, turn a request into a clear task, identify what files or behavior a change should affect, or prevent a small change from expanding into unrelated work.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: project-planning
  task_type: planner
  audience: developers-maintainers-technical-leads-and-coding-agents
  tags:
    - task-scoping
    - requirements
    - acceptance-criteria
    - impact-analysis
    - scope-control
    - implementation-planning
  status: draft
  side_effects: none
---

# Task Scope Clarifier

## Purpose

Turn a rough change request into a small, implementation-ready scope. Define the intended outcome, explicit boundaries, likely repository impact, observable completion criteria, and unresolved risks without designing or implementing unrelated improvements.

## When to use this skill

Use this skill when:

- The user asks to check or clarify a request before implementation.
- A request names a desired change but leaves its boundaries or completion criteria unclear.
- The user asks what files and behavior a change should affect.
- A coding task needs explicit inclusions and exclusions before editing begins.
- A seemingly small request could invite speculative refactoring, polish, or feature expansion.

Common trigger phrases include:

- “Check this request before implementing it.”
- “Turn this into a clear task.”
- “What files and behavior should this change affect?”
- “Clarify the scope before coding.”
- “Keep this change focused.”

Do not use this skill when:

- The user has already supplied a precise, bounded task with testable acceptance criteria.
- The request needs a full project brief, roadmap, architecture decision, or implementation plan.
- The main goal is to classify newly proposed additions against an already agreed scope; use `scope-creep-guard`.
- The user needs a detailed repository-wide blast-radius analysis; use `repository-area-impact-planner`.
- The user has asked to implement the change and no meaningful scope ambiguity remains.

## Inputs to inspect

Start with the smallest evidence set that can establish the task boundary:

- The user's request, issue, bug report, acceptance notes, screenshots, or linked specification.
- Repository instructions such as `AGENTS.md`, `CONTRIBUTING.md`, architecture notes, and local conventions.
- Files, symbols, components, routes, commands, or behaviors explicitly named in the request.
- Nearby source files and direct callers, consumers, tests, fixtures, examples, or docs found through targeted search.
- Existing tests or documentation that reveal the current behavior and intended contract.
- Relevant constraints such as backward compatibility, accessibility, security, privacy, performance, or supported platforms.

Do not scan the entire repository by default. Do not treat a guessed file path or behavior as confirmed evidence.

## Workflow

1. **Restate the requested outcome.** Express the task as one observable result for a named user, system, or maintainer. Preserve the user's intent without adding a broader product goal.
2. **Inspect the minimum relevant context.** Read repository instructions and use targeted searches around named behavior, files, symbols, tests, and docs. Expand only when direct dependencies show that another area is relevant.
3. **Separate evidence from assumptions.** Record what the request or repository confirms, what is inferred, and what remains unknown. Resolve ambiguity from local evidence when possible; ask a question only when different answers would materially change the task.
4. **Define the behavior boundary.** List the behavior, states, inputs, outputs, and compatibility expectations that must change or remain intact. Include necessary tests or documentation in scope when they are part of completing the requested behavior.
5. **Define explicit exclusions.** Name plausible adjacent work that is not required, such as unrelated refactors, redesigns, new abstractions, dependency upgrades, broad cleanup, extra platforms, or speculative edge features. Do not exclude baseline correctness, accessibility, security, privacy, or data-integrity obligations that the requested change necessarily touches.
6. **Identify likely affected files.** List evidence-backed paths or symbols first. Label uncertain entries as `likely` or `possible`, explain why each matters, and distinguish files to inspect from files likely to edit. Include tests, fixtures, docs, examples, configuration, or generated artifacts only when the task affects them.
7. **Write acceptance criteria.** Use observable, testable statements covering the requested success path, necessary failure or edge behavior, preserved behavior, and relevant validation. Avoid implementation prescriptions unless the repository contract requires them.
8. **Surface risks and unknowns.** Name ambiguity, compatibility concerns, hidden coupling, missing test coverage, data migration, accessibility, privacy, security, performance, or environmental risks. State whether each item blocks implementation or can be checked during it.
9. **Recommend the first step.** Choose the smallest action that most reduces uncertainty or establishes a safe implementation foothold, such as confirming a contract, reproducing a bug, opening the primary module, or adding a failing test.
10. **Stop at clarification.** Return the scoped task. Do not edit code, create a full implementation plan, or expand the task unless the user separately asks for that work.

## Output format

Return exactly these top-level sections:

```md
## Goal

One concise statement of the observable outcome.

## In scope

- Required behavior, states, tests, documentation, or compatibility work.

## Out of scope

- Plausible adjacent work explicitly excluded from this task.

## Files likely affected

| Confidence | Path or symbol | Inspect or edit | Reason |
|---|---|---|---|
| Confirmed/Likely/Possible | `path` or symbol | Inspect/Edit/Add | Evidence-backed relationship to the task |

## Acceptance criteria

- [ ] Observable and testable result.

## Risks and unknowns

- Risk or unknown — blocking/non-blocking — next check or decision needed.

## Recommended first step

The smallest concrete action that reduces the most uncertainty or begins the task safely.
```

If no repository is available, keep `Files likely affected` provisional and describe file roles or areas instead of inventing paths. If a section has no items, state `None identified from the available evidence` rather than omitting it.

## Quality bar

The task is complete only when:

- The goal describes one observable outcome rather than a bundle of loosely related improvements.
- In-scope behavior is specific enough to guide implementation.
- Out-of-scope items guard against the most likely forms of accidental expansion.
- Likely files are tied to repository evidence or clearly labeled as provisional.
- Acceptance criteria are observable, testable, and implementation-agnostic where possible.
- Necessary tests, docs, compatibility, accessibility, security, privacy, and data-integrity work are considered without becoming a general audit.
- Risks and unknowns distinguish blockers from checks that can occur during implementation.
- The recommended first step is concrete, proportionate, and within scope.
- No implementation, remote mutation, or unrelated cleanup is performed.

## Edge cases

- If the request contains several independent outcomes, split them into separate candidate tasks and scope only the prerequisite or user-selected task first.
- If repository evidence contradicts the request, show the mismatch under risks and unknowns rather than silently rewriting the goal.
- If a named file is generated, identify the source of truth and avoid recommending direct edits to generated output.
- If the exact path is unknown, name the likely area and the search needed to confirm it; do not fabricate precision.
- If the smallest correct change crosses several files, keep those files in scope. Small scope means no unrelated work, not an arbitrary file-count limit.
- If an adjacent issue is worth addressing but unnecessary for acceptance, place it out of scope and recommend a separate follow-up task.
- If ambiguity does not materially affect the outcome, state a reasonable assumption and continue instead of blocking clarification.

## Related skills

- `project-brief-builder`
- `acceptance-criteria-writer`
- `repository-area-impact-planner`
- `requirements-gap-finder`
- `scope-creep-guard`
- `task-context-packager`
