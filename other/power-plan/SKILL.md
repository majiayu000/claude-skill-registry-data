---
name: power-plan
description: Use when a design or set of requirements exists and work needs decomposing into tasks, before touching any code
---

# Write an Executable Plan

If no approved design exists, stop and use `pwdev-power:power-brainstorm` first. A plan
without a spec is a guess with numbered steps.

Read `.planning/power/context/project.md` and `.planning/power/context/stack.md` when they
exist ([context](../../references/context.md) says what each holds). `File Structure` must name
paths that exist in this repository, and every verification step must use the project's real
commands — a plan step that runs `npm test` against a `pytest` project fails on the first task,
for the most avoidable reason there is. Read [artifacts](../../references/artifacts.md) before
writing `plan.md` or `state.md`, and [collaboration](../../references/collaboration.md) at the
gate: approval is the human's, never inferred.

## Who you are writing for

An engineer who joins at this task, has none of your context, cannot see the conversation, and
will not see the other tasks. Everything they need must be in their own task. Assume good
faith and questionable taste: if a value can be misread, it will be.

## Structure

```markdown
# <Feature> — Plan
Status: DRAFT
Spec: .planning/power/features/<slug>/spec.md
Updated: <ISO date>

For agentic workers: execute this with pwdev-power:power-execute.

## Goal
## Architecture
## Tech Stack

## Global Constraints
<exact values copied verbatim from the spec — timeouts, limits, formats, names, versions>

## File Structure
<every file this plan creates or changes, decided here, before any task>

## Task 01 — <name>
Complexity: low | medium | high
Files: <exact paths>
Interfaces:
  Consumes: <exact signatures from earlier tasks>
  Produces: <exact signatures later tasks will consume>
Steps:
- [ ] Write a failing test for <behavior>
- [ ] Run it, watch it fail for the right reason
- [ ] Implement <the minimum that passes>
- [ ] Run it, watch it pass
- [ ] Commit
```

**`Global Constraints` is copied verbatim, not summarized.** The reviewer checks the
implementation against this block, so a paraphrase here becomes a wrong verdict there.

**The `Interfaces:` block is load-bearing.** It is the only way an implementer who sees one
task discovers what its neighbours expect. Exact signatures and types, not descriptions.

## Task sizing

The smallest unit that carries its own test cycle and deserves a fresh reviewer's gate. Fold
setup, config, and docs into the task whose deliverable needs them. Split only where a
reviewer could plausibly accept one half and reject the other.

Hard limits: at most 5 files per task, at most 7 steps per task, at most 8 tasks per plan. A
plan that wants more is describing more than one feature — say so.

## No placeholders

Every step carries the real code, the real command, the real value. Never "similar to Task 02",
never "and so on", never `...`. The implementer cannot see Task 02.

## Self-review, three passes

1. **Coverage** — does every acceptance criterion in the spec map to at least one task?
2. **Placeholders** — search the plan for `TBD`, `...`, `etc`, "similar to", "as above".
3. **Type consistency** — does every `Consumes:` match a `Produces:` from an earlier task,
   exactly? A mismatch here becomes a failed task and a fix round later.

## Gate

Present the task map — id, name, complexity, files — and wait for approval. On approval, set
`Status: APPROVED` and record the gate in `state.md`.

Then hand off to `pwdev-power:power-execute`. Do not start implementing because the plan is
fresh in your context; that context is exactly what the execution discipline is designed to
keep out.
