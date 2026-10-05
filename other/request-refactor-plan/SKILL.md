---
name: request-refactor-plan
description: Create a detailed refactor plan with tiny commits via user interview, then save it as a local refactor RFC. Use when user wants to plan a refactor, create a refactoring RFC, or break a refactor into safe incremental steps.
---

This skill is for shaping a refactor request into a concrete, low-risk RFC. Skip steps only when the context is already strong.

1. Ask the user for a detailed description of the problem, why the current design is unsatisfactory, and any candidate solutions they already have in mind.

2. Explore the repo to verify assumptions, understand the current structure, and identify the real seams, dependencies, and likely blast radius.

3. Ask whether they have considered alternative approaches. Present alternatives and tradeoffs where useful.

4. Interview the user thoroughly about implementation constraints, desired end state, rollout concerns, compatibility needs, and migration expectations.

5. Hammer out the exact scope. Clarify what will change, what must not change, and what should be postponed.

6. Check the codebase for test coverage in the affected area. If coverage is weak, ask the user what their testing plan should be and what safety nets are required before refactoring.

7. Break the implementation into a plan of tiny commits. Follow the principle that each step should be small, reviewable, and leave the system in a working state.

8. Write the refactor RFC as markdown in a local `.rfcs/` folder. Create the folder if needed. Use a kebab-case filename derived from the refactor name, and return the final file path.

<refactor-plan-template>

# RFC: <refactor name>

## Problem Statement

The problem from the developer or maintainer perspective.

## Goals

What this refactor should improve.

## Non-Goals

What this refactor will intentionally not address.

## Proposed Approach

The proposed solution from the developer's perspective.

## Commit Plan

A long, detailed implementation plan in plain English, broken into the smallest practical commits. Each commit should leave the codebase in a working state.

## Decision Record

Implementation decisions made so far, such as:

- Modules or subsystems likely to be built or modified
- Interface or boundary decisions
- Technical clarifications
- Architectural choices
- Schema changes
- API contracts
- Important interactions or migration rules

Do NOT include brittle file paths or large code snippets.

## Testing Decisions

Testing decisions made so far, including:

- What makes a good test for this refactor
- Which modules or behaviors deserve tests
- Relevant prior art in the codebase
- Risks that should be covered explicitly

## Out of Scope

What is intentionally excluded from this refactor.

## Open Questions

Anything still unresolved.

## Further Notes

Any other context that may help future implementation.

</refactor-plan-template>

## Communication
Honor active caveman mode for user-facing replies per `../../references/communication-mode.md`. Keep durable artifacts normal unless the human asks otherwise. Drop caveman for safety/clarity when needed, then resume.
