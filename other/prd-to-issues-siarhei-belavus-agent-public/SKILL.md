---
name: prd-to-issues
description: Break a PRD into independently grabbable implementation issues using tracer-bullet vertical slices, saved as local issue files alongside the PRD.
---

Your job is to convert a PRD into a set of well-scoped implementation issues that can be picked up independently.

The output should favor tracer-bullet vertical slices over broad horizontal phases. Each issue should produce visible progress, reduce risk, and leave the system in a coherent state.

## Process

1. Read the PRD carefully

Understand:
- the problem being solved
- the key user flows
- constraints and non-goals
- the highest-risk or least-certain parts

If the PRD path is not given explicitly, infer the PRD slug from the provided PRD artifact and use that slug consistently.

2. Identify vertical slices

Break the work into slices that:
- are end-to-end where practical
- exercise meaningful user value early
- reduce uncertainty quickly
- can be validated independently
- avoid producing a pile of disconnected infrastructure work

Do not split work purely by layer such as backend/frontend/database unless that is genuinely the safest shape.

3. Create issue files

Write issue files under:
- `.prd/<prd-slug>/issues/`

Use ordered filenames:
- `.prd/<prd-slug>/issues/01-<slice-slug>.md`
- `.prd/<prd-slug>/issues/02-<slice-slug>.md`

Create the `issues/` directory if it does not exist.

4. Write each issue

Each issue should use this structure:

```md
# <Issue title>

## Parent PRD
.prd/<prd-slug>/prd.md

## Goal
What this slice delivers and why it exists.

## Scope
- In scope item 1
- In scope item 2

## Out of Scope
- Out of scope item 1
- Out of scope item 2

## Implementation Notes
- Important constraints
- Relevant modules or boundaries
- Risks or edge cases to watch

## Validation
- How to verify the slice works
- Tests, manual checks, or observability needed

## Dependencies
- Optional dependency on another issue or artifact
```
```

Keep each issue independently understandable. Avoid hidden assumptions that require rereading the full PRD to make progress.

5. Sequence the work

Order issues so that:
- the earliest slices reduce the most important uncertainty
- later slices build on proven capability
- the sequence is practical, not just conceptually neat

Call out explicit dependencies only when necessary.

6. Final response

In your final response:
- summarize how many issues were created
- list the created file paths
- briefly explain the sequencing logic

## Communication
Honor active caveman mode for user-facing replies per `../../references/communication-mode.md`. Keep durable artifacts normal unless the human asks otherwise. Drop caveman for safety/clarity when needed, then resume.
