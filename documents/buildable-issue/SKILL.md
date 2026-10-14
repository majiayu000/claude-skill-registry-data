---
name: buildable-issue
description: >
  Creates agent-ready GitHub issues that are ready to build. Formerly framed as
  sdd-issue / SDD-ready issue creation. Use when creating a buildable issue,
  implementation-ready ticket, SDD-ready issue, preparing work for an
  orchestrator, or when the user says "create an issue", "write a ticket", or
  "I need to build X". Also use when the user references an existing issue and
  wants it enriched with scope, constraints, acceptance scenarios, and technical
  context.
license: MIT
metadata:
  author: andresnator
  status: backlog
  version: "2.1.3"
---

# Skill: buildable-issue

## Activation Contract

Use this skill when the user needs a GitHub issue that another agent or human can implement without guessing.

This is the renamed public capability for the older `sdd-issue` wording. Treat legacy phrases like “SDD-ready issue” as compatible triggers, but prefer `buildable-issue` in new documentation.

## Responsibility

Create or enrich GitHub issues with enough structure for implementation: intent, type, scope, acceptance scenarios, technical context, constraints, and priority.

Do not run the implementation, orchestrate SDD phases, or invent missing product decisions. Interview the user when critical fields are missing.

## Required Context

- Repository or project where the issue belongs.
- Intended change, bug, refactor, or chore.
- Known constraints, affected files/modules, and acceptance expectations.
- Existing issue number when enriching rather than creating.

## Hard Rules

- Search existing issues for likely duplicates before creating a new issue.
- Fill all issue sections; do not leave placeholder text behind.
- Every in-scope item needs observable acceptance scenarios.
- Acceptance scenarios use Given/When/Then language.
- Scope must include both in-scope and out-of-scope boundaries.
- Apply the `sdd-ready` label when the issue is structured for automated SDD consumption.
- Return the issue URL or updated issue reference when done.

## Issue Template

````markdown
## Intent

<Why this change is needed. Explain the problem or opportunity, not only the requested work.>

## Type

<feature | bugfix | refactor | chore>

## Scope

### In Scope
- <What will be built or changed>

### Out of Scope
- <What will not be changed>

## Acceptance Scenarios

### Scenario: <descriptive name>
- GIVEN <precondition>
- WHEN <action or trigger>
- THEN <observable expected result>

### Scenario: <descriptive name>
- GIVEN <precondition>
- WHEN <action or trigger>
- THEN <observable expected result>

## Technical Context

- **Affected files/modules**: <paths, packages, services, or unknown>
- **Related specs/docs**: <links or none>
- **Dependencies**: <new or existing dependencies, or none>
- **Breaking changes**: <yes/no and details>

## Constraints

- <Architectural, product, security, compatibility, or workflow constraints>

## Priority

<critical | high | medium | low>
````

## Workflow

1. Clarify missing critical context with at most one question at a time.
2. Search for duplicates with a focused GitHub issue query.
3. Fill every template section using the user's context and repository conventions.
4. Validate that each in-scope item has acceptance scenarios.
5. Create or update the issue with appropriate labels.
6. Return the issue URL and a short summary of what made it buildable.

## Creating the Issue

Use a conventional title:

```text
<type>(<scope>): <concise description>
```

Recommended labels:

| Type | Labels |
|---|---|
| feature | `enhancement`, `sdd-ready` |
| bugfix | `bug`, `sdd-ready` |
| refactor | `refactor`, `sdd-ready` |
| chore | `chore`, `sdd-ready` |

## Enriching an Existing Issue

When the user references an issue number:

1. Fetch the issue.
2. Preserve useful existing content.
3. Interview for missing template sections.
4. Replace or append the structured issue body.
5. Add the `sdd-ready` label when the structure is complete.

## Quality Checklist

- [ ] Intent explains why the change matters.
- [ ] Type is one of `feature`, `bugfix`, `refactor`, or `chore`.
- [ ] Scope has explicit in-scope and out-of-scope lists.
- [ ] Acceptance scenarios are observable and use Given/When/Then.
- [ ] Technical context names affected areas or says they are unknown.
- [ ] Constraints and priority are filled.
- [ ] No placeholder text remains.

## Output Contract

Return:

- issue URL or updated issue reference;
- labels applied;
- duplicate search result summary;
- any remaining assumptions or follow-up questions.
