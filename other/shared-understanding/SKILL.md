---
name: shared-understanding
description: Use only when explicitly requested with `$shared-understanding`, or through the full `github-issue-delivery` or `azure-devops-work-item-delivery` workflow before design preflight, to build a shared understanding of an existing written request, GitHub issue, or Azure DevOps Work Item with the user by reading back what it decides and settling what it leaves undecided. Frame an unsettled problem with `find-unknowns`; decide how to build in `design-preflight`.
---

# Shared Understanding

Build a shared understanding of an existing issue or Work Item with the user
before design starts. Issues are often drafted by AI and accepted without a close
read, and the user usually works through agent CLIs without rereading them: the
user knows the goal, not the text. Read the issue back so the user can judge it,
and have the user decide what it leaves open. Knowledge flows from the AI to the
user, and every judgment asked of the user is a real decision about intent.
Framing a problem that is still unsettled is `find-unknowns`; deciding how to
build is `design-preflight`.

Use read-only inspection. Propose issue edits; leave the issue itself unchanged.

## Workflow

### 1. Inspect

Read the issue body, comments, acceptance criteria, open questions, linked items,
and the code or docs that show the current behavior it describes. Then analyze
where the goal and the acceptance criteria diverge, what the issue excludes, and
its boundary cases. Sort the material findings into decisions the issue makes and
points it leaves undecided or ambiguous.

### 2. Present an overview

Write the overview for a user who has not reread the issue.

- State in one sentence what changes and why, and ask the user to confirm or
  correct it. When the user corrects it, revise the overview before step 3.
- Show one typical case as **before / after**: a concrete situation (input,
  operation, or state, using real names and values from the repository) and the
  observable result before and after the change.
- List the scope in 2-3 lines each: what is in scope and what is out of scope
  (non-goals).
- Cite the source of each claim (an issue quote or `file:line`). Label anything
  the sources leave unstated as your interpretation.

### 3. Read back the decisions

List the consequential decisions the issue makes, leading with those that do not
follow from the goal alone: an arbitrary choice in the acceptance criteria, an
exclusion, or a boundary. Give each decision with its observable consequence and
its source, and ask the user to accept or adjust each one. A decision stays open
until the user explicitly accepts or adjusts it.

### 4. Settle the undecided points

Take the consequential points from step 1 that the issue leaves undecided or
ambiguous, one at a time, and wait for each answer before the next. Show the
situation and say that you are asking for the user's intent, not for the issue's
text. Offer 2-3 options with equal detail, each an observable result of that
situation, plus `can't decide`. Keep scoping, process, and how-to-build choices
for step 5. When step 1 found no such point, go on to step 5.

Recommend one option with a one-line reason drawn from the sources; the
recommendation informs the user's choice, and the decision stays theirs. When
viewpoints favor different options, name each viewpoint and the option it
favors, then give the overall recommendation and why, for example
"short-term: A; long-term maintainability: B; recommended: B, because ...". The
default viewpoints are the short-term smallest change and long-term
maintainability; add another, such as risk or compatibility, only when the
sources show it favors a different option. The overall recommendation favors
long-term maintainability unless the user's request states another stance, such
as the smallest change or design-preflight's `conservative`. When the sources
support no recommendation, say so in place of one.

On `can't decide`, explain the readings the sources support and what each leads
to, then ask the user to choose or adjust one. A point the user still cannot
decide after that explanation stays open.

### 5. Record and route

- When an agreed decision differs from the issue text, record it as an agreed
  issue change and propose updating the issue.
- Carry durable design decisions (contracts, data formats, boundaries,
  compatibility) to design preflight; leave small implementation tactics to
  implementation.
- When the discussion shows that the problem itself is unsettled, recommend
  `find-unknowns` and close as `unresolved`.

The user may skip at any point; close as `skipped`. When interaction is
unavailable, close as `not run`; the judgments belong to the user alone.

## Draft for a coordinator

When a delivery coordinator asks for a draft, the drafter cannot ask the user;
the coordinator holds the dialogue. Do step 1, then write steps 2-4 as a draft
instead of asking: the overview, each decision to read back with its
consequence and source, and each undecided point with its options,
recommendation, and viewpoints as step 4 sets them. Ask the user nothing and
settle nothing; every decision and point stays open until the coordinator
returns the user's answers. Return:

```markdown
# Shared Understanding Draft: <issue or Work Item reference>

## Overview
## Decisions to Read Back
- <decision> -> <observable consequence> (<source>)

## Undecided Points
- <situation>: <options>; recommended: <option>, because <reason> (<source>)

## Carry to Design Preflight
```

The coordinator verifies the draft, runs steps 2-5 with the user from it, and
returns the user's answers. Answer its follow-up questions and revise the draft
when it asks; the coordinator closes the check with the Result below.

## Result

The check is complete when its status is one of:

- `confirmed`: the user accepted every consequential decision and settled every
  undecided point, with no change to the issue.
- `corrected`: the same, with at least one agreed issue change.
- `unresolved`: a consequential decision or point remains open, or the problem
  itself is unsettled. An open point closes here, never as `confirmed` or
  `skipped`.
- `skipped`: the user explicitly skipped the check.
- `not run`: interaction was unavailable.

Return:

```markdown
# Shared Understanding: <issue or Work Item reference>

Status: <status>

## Agreed Decisions
- <decision or situation> -> <agreed behavior> (<source>)

## Agreed Issue Changes
## Carry to Design Preflight
## Open Points
```

In `(<source>)`, cite the issue quote or `file:line`, and add `user decision` for
a point the user settled in step 4. List each open decision or point with what
keeps it open under `Open Points`. Write `None` for empty sections. Agreed
decisions serve as acceptance examples for preflight, implementation, and tests.
