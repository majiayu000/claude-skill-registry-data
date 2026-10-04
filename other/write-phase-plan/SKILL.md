---
name: write-phase-plan
description: >-
  Writes or restructures an implementation plan in the format the
  phase-orchestrator skill consumes: dependency-ordered phases with explicit
  scope, acceptance criteria, validation commands, and status/log conventions.
  Use when the user asks to write a plan for phase orchestration, prepare a
  plan or PRD for delegated multi-agent implementation, or convert a spec,
  checklist, or design doc into implementable phases.
license: MIT
---

# Write Phase Plan

## Goal

Produce a plan document that a phase-orchestrator run can execute without
re-deriving structure. Each phase must be implementable by a worker that has
no chat history: the phase section is the worker's entire brief, plus repo
rules and the code itself.

The plan is the source of truth during the run. The orchestrator updates phase
status and appends log entries as it goes, so the document must be written to
absorb that.

## Where The Plan Lives

Follow the repo's convention for design docs (for example `plans/<author>/` in
repos that define one). One markdown file per plan. Link out to the PRD/spec
rather than duplicating it.

## Document Structure

```markdown
# <Feature name>

## Overview
One or two paragraphs: what is being built and why. Link the PRD/spec.

## Constraints
Repo-wide facts every phase needs: commit/PR policy, validation commands,
branch or worktree requirements, anything the orchestrator must not infer.

## Phases
A short table or list: phase ID, name, depends-on, parallelizable-with.

## Phase 1: <name>
- **Status:** Not started
- **Depends on:** none | Phase N
- **Objective:** one sentence, the outcome not the activity.
- **Scope:** the files/modules this phase owns (its write scope).
- **Out of scope:** adjacent work this phase must not touch.
- **Approach:** implementation notes — key decisions already made, pointers
  to the code the worker should read first, known landmines.
- **Acceptance criteria:** checkable statements (see below).
- **Validation:** exact commands to run, plus any manual checks.

## Phase 2: <name>
...

## Implementation log
(Empty at authoring time. The orchestrator appends one entry per phase:
date, phase, summary, validation results, review outcome, commit SHAs,
deviations, remaining risks.)
```

## Sizing And Ordering Phases

- One phase = one implementer worker session. If a phase's Approach section
  needs subheadings to stay coherent, split it.
- Order by dependency, foundations first. A schema/migration phase is always
  its own phase (and in many repos its own PR — record that in Constraints).
- Phases that can run in parallel must have disjoint write scopes. Declare
  parallelizability explicitly in the phase list; the orchestrator will not
  guess.
- If a phase exists only to set up a later phase, say which one, so the
  orchestrator knows a deviation there propagates.

## Writing For A Context-Free Worker

The implementer sees the plan, the repo, and nothing else. So:

- Use standalone spec language. No "as discussed", "still", "instead of the
  old approach", or references to conversations that produced the plan.
- Name concrete things: file paths, function names, commands — not "the
  relevant helper" or "the usual checks".
- State decisions as decisions. If something is genuinely unresolved, mark it
  as an explicit open question and say who resolves it (the worker may decide
  in-scope questions; the orchestrator escalates cross-cutting ones).
- Put shared context in Constraints once rather than repeating it per phase.

## Acceptance Criteria

Each criterion must be checkable by the reviewer from the diff and the running
code, without asking the author:

- Good: "`POST /orgs/:id/invites` returns 403 for a non-admin member; covered
  by a route test."
- Bad: "Invites are properly secured."

Include the negative space: what must not change (existing behavior, public
contracts, performance characteristics) when regression there is a real risk.

## Status And Log Conventions

- Phase status vocabulary: Not started, In progress, Done, Partial, Blocked.
- The orchestrator owns status transitions and log entries during the run;
  the author sets everything to Not started.
- Keep the Implementation log section present even when empty, so run updates
  have a stable place to land.

## Anti-Patterns

- Phases split by activity (design/build/test) instead of by deliverable —
  every phase should end with validated, committable work.
- Two phases that edit the same files marked as parallel.
- Acceptance criteria that restate the objective instead of testing it.
- A plan that embeds the whole PRD — link it and keep the plan operational.
- Hidden sequencing: prose that implies an order the phase list doesn't state.
