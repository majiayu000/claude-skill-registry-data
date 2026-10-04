---
name: plan
description: Use when asked to plan, create a plan, or write a plan for any feature, task, or spec. Triggered by phrases like "plan X", "write a plan for X", "let's plan X", "create a plan for X", or when starting work on a task that requires an implementation plan.
---

# Plan

Announce at start: `Planning...`

Plan like a senior engineer who will personally execute and own the result. Choose the simplest
design that fully meets the requirements without compromising correctness, maintainability,
reliability, security, or established best practice. Introduce abstractions when they improve those
qualities; development cost, time, effort, and perceived difficulty are never selection criteria.

Three properties separate a real plan from a guess:

- **Grounded** - every claim about the repo was verified by reading the repo, not recalled.
- **Contracted** - where work crosses a boundary (client/server, app/DB, generated/manual,
  config/runtime), the plan names the contract and how the implementation proves it holds.
- **Gated** - larger work is one file split into ordered phases, each ending in a verification gate
  that passes before the next phase starts.

## 1. Check for an existing plan

Determine the repo name from the working directory or git remote, then:

```bash
ls ~/.agents/plans/<repo-name>/ 2>/dev/null | grep -i "<task-slug>"
```

Skip any candidate starting with `EXECUTED-` - those are historical records of completed work, not
reusable plans, and they never block writing a new one.

Judge relevance before asking the user anything: read each candidate's title, Goal, and Approach and
compare them against the current request, not the filename. A plan is relevant only when its user
outcome and implementation surface materially overlap. If none are, say so in one line and continue.

If one is genuinely relevant, show the path and a one-sentence reason it matches, then ask "Use it or
write a new one?" On "use it", send the link and stop.

When another skill hands you an explicit source - a findings file, a review file, a spec path - read
that file first and judge relevance against it, and record its path as the plan's `**Source:**`. A
slug match against an old plan never overrides the spec you were handed.

**Code-review remediation:** when the code-review skill invokes planning with a review file, always
write a new plan. Earlier plans for that branch are the artifacts that produced the defects being
corrected. Save as `~/.agents/plans/<repo>/YYYY-MM-DD-<review-slug>-from-code-review.md`, where
`<review-slug>` is the review filename without `-code-review.md`.

## 2. Ground the plan in the codebase

Read the repo's own instructions first:

```bash
sed -n '1,220p' AGENTS.md 2>/dev/null
sed -n '1,220p' ~/AGENTS.md 2>/dev/null
```

If `AGENTS.md` carries a **Context Map**, use it: read only the rows matching this task and load the
narrowest file each row points at. A planning session that loads the whole `context/` tree pays for
that context on every later turn and produces a worse plan. Where the map points at a directory
index, read the index and follow only the leaves this task needs. Read any `AGENTS.md` inside a
subtree you will be working in.

Then inspect the actual implementation - what exists, what does not, and which APIs are already in
use. Every file path and framework API that reaches the plan must come from this step.

Before writing questions, resolve these against what you just read:

- **Working backwards** - what does the user actually get, and do the steps trace back to it?
- **YAGNI** - does each piece of work appear in the spec, or is it anticipating future needs?
- **Existing implementations** - which modules, helpers, composables, routes, or patterns should
  this extend rather than duplicate?
- **Dependency reality** - is the package already installed, and is a new one justified?
- **Framework constraints** - SSR vs client-only, lazy-loading, boot order, shutdown, build impact.
- **Type-safety** - does the approach lean on unchecked casts, inferred shapes, or presence checks
  that don't prove the inner value's type?
- **Pre-mortem** - it is 3 months from now and this failed silently in production. Name the top 3
  causes.

For work touching 2+ layers, generated artifacts, or runtime config, audit the contracts that apply
- data shape and nullability, ordering (sort, cursor, dedup, idempotency, tie-breaks), types
(generated vs handwritten vs runtime-validated), config (env, flags, defaults), auth and access,
runtime (retries, timeouts, shutdown, cache invalidation). Each applicable contract earns a concrete
implementation step in the plan, or an explicit note that it is unaffected.

## 3. Grill the user

Non-negotiable when real unknowns remain. Read `references/question-format.md` and follow it exactly
for every question - including `Why A wins:` and `If wrong:`.

When codebase inspection already settled everything, say so and skip this step. The goal is removing
ambiguity, not performing thoroughness.

Wait for answers before writing. Record every answer in the plan's `## Decisions` section.

## 4. Write the plan

Save to `~/.agents/plans/<repo-name>/YYYY-MM-DD-<task-slug>.md`.

```markdown
# [Feature Name] - Implementation Plan

**Task:** [ticket link, issue URL, or task reference]
**Source:** [path to the spec, findings, or review this plan was built from - omit if none]
**Date:** YYYY-MM-DD

## Goal
One sentence: what the user gets and why it matters, from the user's perspective.

## Approach
2–3 sentences on the technical strategy, the key decisions and why, and any repo or framework
constraint that shapes the implementation. Challenge complexity the spec did not ask for.

## Key Contracts
Only the contracts that matter here. For each: what must stay true (precondition / postcondition /
invariant), where it crosses a boundary, and how the implementation proves it holds.

## File Map
| File | Action | What it does |
|------|--------|--------------|
| `path/to/file.ts` | Create | ... |
| `path/to/existing.ts` | Modify | ... |

## Phases

### Phase 1: [Outcome-sized name]
**Goal:** the independently useful result this phase delivers.
**Files:** exact files touched
**Depends on:** none, or earlier phase(s)

#### Tasks
- [ ] **T1.1** Concrete, actionable task

#### Task Ownership
| Task | Files owned | Depends on | Risk |
|------|-------------|------------|------|
| T1.1 | `path/to/file.ts` | - | standard |

#### Phase Verification Gate
- [ ] Exact command, test, inspection, or behavior check proving this phase is complete
- [ ] Confirm this phase's contracts and negative paths still hold

**Proceed only when:** every task and check above passes. On failure, fix or re-plan this phase
before starting the next.

### Phase 2: [Outcome-sized name]
...

## Validation
- [ ] The repo's documented lint, typecheck, and build commands
- [ ] Task-specific verification proving the behavior works, not just that the build passed

## Pre-mortem
The top ways this silently fails even with all checks green.
- **Scenario:** what breaks
  **Prevention:** what the plan does about it
  **Verification:** how to confirm it held

## Decisions
- **[question]** → [chosen option]. [User's reason, if given.]

## Out of Scope
Anything explicitly excluded.

## Open Questions
Remaining unknowns that don't block the plan.
```

Small self-contained work uses one phase. Larger work splits into ordered phases in this same file -
never separate files per phase. Phases are always sequential; independence lives at the task level,
which is what the Task Ownership table records.

### The Task Ownership table

The executing agent uses this table to decide what runs concurrently and how much model capability
each task is worth. Both decisions are only as good as this table, so fill it from what you verified
in step 2, never from guesswork.

**Files owned** - every file the task will create or modify, by path, matching the File Map. A file
appears under exactly one task per phase. If two tasks genuinely must both edit one file, that is a
sequencing fact: give the file to one task and make the other `Depends on` it.

**Depends on** - the task IDs whose output this one consumes: a type, function, export, migration,
generated artifact, or route it imports or calls. `-` means it consumes nothing from a sibling.
Getting this wrong is the expensive error - a task launched before its dependency lands fails against
code that does not exist yet, so when unsure, declare the dependency.

**Risk** - one of:

- `mechanical` - fully specified, no judgment left: renames, moved constants, copy changes, config
  the plan spells out, repeating a pattern that already exists in the repo.
- `standard` - bounded work inside one layer: a route, a component, a service method, a migration,
  tests for existing behavior. The design is settled; judgment applies only locally.
- `contract` - the task touches something in Key Contracts or Pre-mortem, crosses layers, or involves
  ordering, state, concurrency, idempotency, auth, or a design question the plan left open.

Classify by what the task can silently break, not by how much typing it involves. A one-line change
to a sort comparator or an auth guard is `contract`. Never name a model in the plan - the executing
agent maps risk to capability, and that mapping changes as models do.

State the integration task explicitly whenever tasks fan out: which task reunites the work, and one
owner for it throughout.

**Execution protocol:** after approval, execute one phase at a time in this file. Complete the tasks,
run and record the gate, then start the next phase. A failed gate keeps work inside that phase until
it is fixed or the plan is explicitly revised. The Validation section covers the whole feature and
never substitutes for a phase gate.

## 5. Quality bar

Before saving, confirm each of these holds. Fix the plan where one does not.

- Every step traces to the spec, and the Goal describes what the user gets.
- Every file path and framework API was verified against the repo in step 2.
- Every step is a concrete action - an executor could start it without interpretation.
- Contracts are named with the check that proves each one.
- Validation distinguishes "the build passes" from "the behavior is correct".
- Every new endpoint, job, or write path has a negative-path step.
- The Pre-mortem names specific scenarios with specific prevention.
- Each abstraction generalizes 3+ cases, or the plan says why it earns its place anyway. Each new
  dependency is justified against what the stack already does.
- Tasks and Out of Scope agree, and nothing is left TBD.
- Each phase has a gate that proves its stated outcome, and each task belongs to exactly one phase.
- Every task appears in its phase's Task Ownership table, no file is owned by two tasks in a phase,
  and the owned files reconcile with the File Map.
- Every dependency a task's text implies is declared in `Depends on` - re-read each task asking what
  it imports, calls, or reads that a sibling produces.
- Every task touching a Key Contract or a Pre-mortem scenario is classified `contract`.
- Commit, push, and PR steps stay out of the plan.

## 6. Show the plan and wait

```
Plan saved → ~/.agents/plans/<repo-name>/<filename>.md - reply "go" to execute, or tell me what to change.
```

Add a 1–3 sentence summary of the main decisions. Keep the plan body out of chat.

Then stop and wait for explicit approval before any implementation.
