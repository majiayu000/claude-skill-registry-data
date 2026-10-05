---
name: write-a-prd
description: Create a PRD through user interview, codebase exploration, and module design, then save it as a local artifact under a dedicated .prd folder.
---

You are helping the user define a product requirement clearly enough that it can be planned and implemented safely.

Your job is to interview the user, inspect the relevant codebase where useful, resolve major ambiguities, and then write a concrete PRD file.

## Process

1. Clarify the request

Ask focused questions until you understand:
- the user problem
- target users or actors
- desired outcomes
- major constraints
- known edge cases
- what is explicitly out of scope

Keep questions high-signal. Avoid long questionnaires when a few targeted questions will do.

2. Explore the codebase

Inspect the existing code to understand:
- related modules and boundaries
- existing terminology
- integration constraints
- implementation hotspots likely to shape scope

Do not over-index on current implementation details. The PRD should describe the desired product behavior and key system constraints, not prescribe fragile code-level mechanics.

3. Resolve ambiguity

Before writing, make sure the following are reasonably clear:
- problem statement
- user value
- success criteria
- important workflows
- boundaries and exclusions
- risks, dependencies, or unknowns worth calling out

If critical ambiguity remains, call it out explicitly in the PRD instead of pretending it is resolved.

4. Create the PRD folder

Create a dedicated folder for the PRD:
- `.prd/<prd-slug>/`

Inside it, write the PRD file at:
- `.prd/<prd-slug>/prd.md`

Also reserve these sibling folders for downstream artifacts when relevant:
- `.prd/<prd-slug>/issues/`
- `.prd/<prd-slug>/plans/`
- `.prd/<prd-slug>/rfcs/`

Use a short kebab-case slug derived from the feature or initiative name.

5. Write the PRD

Use this structure:

```md
# <Feature / Initiative Name>

## Summary
A short description of the feature and why it matters.

## Problem
What problem is being solved? Who has this problem?

## Goals
- Goal 1
- Goal 2

## Non-Goals
- Not in scope 1
- Not in scope 2

## Users / Actors
- Primary user or actor
- Supporting actor or system

## Requirements
### Functional
- Requirement 1
- Requirement 2

### Non-Functional
- Performance / reliability / operational constraints
- Security / compliance / UX constraints

## User Flows
- Flow 1
- Flow 2

## Success Criteria
- Metric or observable outcome 1
- Metric or observable outcome 2

## Risks / Constraints / Dependencies
- Risk or dependency 1
- Risk or dependency 2

## Open Questions
- Question 1
- Question 2
```

Keep the document specific and actionable. Prefer concrete outcomes, constraints, and flows over vague aspirations.

6. Final response

In your final response:
- give a short summary of what was clarified
- provide the final PRD path: `.prd/<prd-slug>/prd.md`
- mention any major open questions still unresolved

## Communication
Honor active caveman mode for user-facing replies per `../../references/communication-mode.md`. Keep durable artifacts normal unless the human asks otherwise. Drop caveman for safety/clarity when needed, then resume.
