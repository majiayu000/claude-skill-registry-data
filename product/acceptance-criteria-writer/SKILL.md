---
name: acceptance-criteria-writer
description: Converts a feature idea, user story, change request, or bug report into clear, observable, and verifiable acceptance criteria. Use when the user asks to define done, make requirements testable, prepare criteria for an issue or backlog item, describe expected behavior, or turn a defect into regression criteria without prescribing implementation details.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: project-planning
  task_type: generator
  audience: product-managers-developers-designers-qa-and-project-maintainers
  tags:
    - acceptance-criteria
    - requirements
    - feature-planning
    - bug-reports
    - testing
    - definition-of-done
  status: draft
  side_effects: none
---

# Acceptance Criteria Writer

## Purpose

Convert a feature idea or bug report into a concise contract describing behavior that a reviewer or tester can verify. Preserve unknowns, cover meaningful boundaries, and avoid turning acceptance criteria into implementation instructions.

## When to use this skill

Use this skill when:

- A feature idea, user story, change request, or backlog item needs testable acceptance criteria.
- A bug report needs expected behavior and regression criteria.
- Words such as “works,” “supports,” “easy,” “fast,” or “properly” need observable definitions.
- Product, engineering, design, and QA need a shared definition of done for one bounded change.
- Existing criteria need to be clarified, deduplicated, or made independently verifiable.

Do not use this skill when:

- The request is to write a full project brief, implementation plan, test suite, or QA script.
- The scope is too broad to represent one coherent outcome; split or clarify the work first.
- The user only wants success metrics or business outcomes rather than behavior-level acceptance.
- The task is to judge whether existing requirements are complete; use `requirements-gap-finder`.

## Inputs to inspect

- The supplied feature idea, user story, change request, or bug report.
- Current behavior, expected behavior, reproduction steps, and environment details when reporting a defect.
- Relevant users, permissions, states, inputs, outputs, constraints, dependencies, and explicit non-goals.
- Linked designs, specifications, issues, examples, or repository behavior when available.
- Existing terminology and acceptance-criteria conventions used by the project.

Inspect only the evidence needed to understand the requested behavior. Do not infer implementation architecture from repository structure unless it changes what users can observe.

## Criteria principles

- Describe externally observable behavior, state, or output.
- Make each criterion independently passable or fail-able.
- State preconditions when behavior depends on role, state, data, configuration, or environment.
- Use concrete inputs, triggers, results, and boundaries where the source supports them.
- Separate requirements from assumptions and unresolved decisions.
- Cover the primary path plus relevant validation, permission, empty, error, retry, and recovery behavior.
- Preserve explicit accessibility, privacy, security, compatibility, and performance constraints.
- Avoid UI layout, database, framework, class, function, or algorithm prescriptions unless they are binding requirements.
- Avoid duplicating the issue description or listing implementation tasks as criteria.

## Workflow

1. **Classify the source.** Determine whether the input is a feature, behavior change, or bug. For a bug, separate observed behavior from expected behavior and retain the reproduction conditions.
2. **Extract the behavioral contract.** Identify the actor, starting state, trigger, intended result, affected data or system state, constraints, and explicit exclusions.
3. **Mark uncertainty.** Distinguish facts from reasonable assumptions. Record missing decisions that would materially change behavior instead of silently choosing an answer.
4. **Define the core outcome.** Write the smallest set of criteria that proves the requested value or regression fix. Keep one observable expectation per criterion where practical.
5. **Add relevant boundaries.** Check roles and permissions, invalid or empty input, repeated actions, failure and recovery, persistence, state transitions, and supported environments. Include only cases that are plausible and in scope.
6. **Preserve quality constraints.** Translate supplied accessibility, privacy, security, compatibility, or performance requirements into verifiable conditions. Do not invent numeric thresholds; flag missing thresholds as open questions.
7. **Choose a readable format.** Default to a numbered checklist in plain language. Use Given/When/Then when preconditions and state transitions materially improve precision. Do not force every simple criterion into that syntax.
8. **Run a verifiability pass.** For each criterion, confirm that a tester can identify the setup, action, and expected result without knowing the implementation. Replace subjective language with observable evidence or expose the missing decision.
9. **Check scope and duplication.** Remove criteria that merely restate another criterion, prescribe tasks, introduce unrelated enhancements, or broaden the original request.
10. **Return criteria with caveats.** Present the criteria first, followed by assumptions, open questions, and out-of-scope notes only when they are needed.

## Feature and bug guidance

For a feature or behavior change:

- Center criteria on the user outcome and system response.
- Cover the initial, successful, invalid, unavailable, and persisted states when relevant.
- Treat content, interaction, and feedback requirements as behavior when users must observe them.

For a bug:

- Include at least one criterion that reproduces the reported conditions and confirms the corrected behavior.
- Add adjacent regression coverage only when it protects the same behavior or likely failure boundary.
- Preserve unaffected behavior when the fix could reasonably cause a regression.
- Do not encode the suspected root cause as a requirement unless it is confirmed and externally binding.

## Output format

Return:

```md
## Acceptance criteria

1. [Observable, verifiable condition.]
2. [Observable, verifiable condition.]

## Assumptions

- [Assumption used to draft the criteria.]

## Open questions

- [Decision needed because different answers change acceptance.]

## Out of scope

- [Explicit boundary when needed.]
```

Omit empty sections. When Given/When/Then is useful, format each criterion as:

```md
### AC1 — Short behavior label

- Given [relevant starting state]
- When [actor or system trigger]
- Then [observable result]
```

## Quality bar

The task is complete only when:

- Every criterion can produce a clear pass or fail result.
- The core requested behavior is covered without requiring knowledge of the implementation.
- Feature criteria describe value and behavior; bug criteria prove the regression is corrected under the reported conditions.
- Relevant roles, states, boundaries, failures, and recovery paths are covered without speculative scope expansion.
- Subjective terms are replaced with observable evidence or called out as unresolved.
- Assumptions and open questions are not disguised as confirmed requirements.
- Criteria do not duplicate one another or become implementation tasks.

## Edge cases

- If the input is very thin, draft a minimal useful set and label assumptions rather than blocking on every unknown.
- If multiple actors or workflows are bundled together, group criteria by actor or recommend splitting the item.
- If a design specifies exact visible behavior, criteria may reference that design, but should still state what must be verifiable.
- If a non-functional requirement lacks a measurable threshold, preserve the intent and ask for the threshold instead of inventing one.
- If current behavior is unclear in a bug report, distinguish the reported observation from any inferred reproduction step.
- If criteria conflict, surface the conflict and avoid producing a falsely coherent set.

## Related skills

- `requirements-gap-finder`
- `project-brief-builder`
- `plan-to-issues-converter`
- `edge-case-test-planner`
