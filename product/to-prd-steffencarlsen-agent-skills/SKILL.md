---
name: to-prd
description: Turn the current conversation, repository findings, issue discussion, or feature plan into a Product Requirements Document. Use when the user invokes to-prd, asks for a PRD, wants a feature spec, or needs implementation decisions captured before issue breakdown.
---

# To PRD

Create a PRD from existing context. Do not restart discovery unless the context is too thin to write a useful spec.

## Process

1. Inspect the relevant repo area if the PRD depends on current code behavior.
2. Use existing project vocabulary, conventions, ADRs, and issue labels when visible.
3. Ask only for blocking product decisions. Skip interviews when the conversation already contains enough detail.
4. Identify the highest practical test boundary for the feature. Prefer existing seams over new ones.
5. Draft the PRD. Publish it to the available issue tracker only when the user asked for publishing or the tracker/tooling is clearly configured.

## PRD Template

```markdown
## Problem Statement

Describe the user-facing problem.

## Solution

Describe the user-facing solution.

## User Stories

1. As an <actor>, I want <capability>, so that <benefit>.

## Implementation Decisions

- Capture modules, interfaces, schema/API contracts, behavior rules, and important constraints.
- Avoid file paths unless a specific path is itself part of the decision.

## Testing Decisions

- State the behavior to prove.
- Name the test boundary and similar existing coverage if found.

## Out of Scope

- List explicit non-goals.

## Further Notes

- Capture unresolved risks, dependencies, or follow-ups.
```
