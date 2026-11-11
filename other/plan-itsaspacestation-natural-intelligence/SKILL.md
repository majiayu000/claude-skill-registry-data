---
name: plan
description: "Use when the user asks to plan a task or feature before implementing, create a workspace, write a design doc or ADR, break work into sessions and tasks for autopilot, resume an active workspace, or integrate workspace artifacts into docs."
---
# Plan

## When to use
- User enters plan mode or asks to plan before implementing
- User asks to create a workspace, design doc, ADR, or task breakdown
- User asks to resume, review, or amend an existing design or workspace
- User asks to integrate workspace artifacts into durable storage

## Overview

Planning must always take less time than implementation. The effort scales with
complexity, never the other way around. This file holds the triage: assess the
complexity, then load exactly one route file. Never load both.

## Complexity triage

Assess the work against three triggers, in order:

1. **Resuming?** Root `CLAUDE.md` has an `## Active workspaces` entry → load
   [complex-plan.md](complex-plan.md) and follow its Phase 0.
2. **Multi-session scope?** More than one session of work, more than ~5 tasks, or a
   domain model worth tracing → full workspace: load [complex-plan.md](complex-plan.md).
3. **Hard-to-reverse decision?** Persistence, protocol, public contract → that
   decision gets an ADR whatever the route; the route still follows trigger 2. On the
   small route an additive flag, a CLI option, or an output shape is a decision bullet,
   not an ADR. The small route writes an ADR only for persistence or a wire protocol,
   the small route's shortcut. Both pass the admission test in
   [complex-plan.md](complex-plan.md#phase-3--write-adrs).

None of the above → small plan: load [small-plan.md](small-plan.md) and produce one
document. Heavy scaffolding on a small task reads as noise to the human and costs
tokens without adding decisions.

The complex route reads [autopilot.md](autopilot.md) at Phase 5 and drafts from
[templates/](templates/DESIGN.md).

## Rules for both routes

**Delegated and one-shot contexts: decide, do not ask.** When the requester has
delegated ("your call", "decide and continue") or cannot answer (headless run, batch
job), make the decision, record it with its reason, and continue. Ask only when
blocked by a genuine externality the codebase and brief cannot resolve (a credential,
an unstated business rule). Ratification questions in a delegated context burn turns
without adding information.

**A task is a behaviour, not a layer.** Every task is one slice: one behaviour across
every layer it touches (Hunt and Thomas, *The Pragmatic Programmer*, "Tracer Bullets").
The first task is the walking skeleton: the thinnest path through the public surface,
end to end. Every later task widens it by one behaviour. Build layer by layer only when
nothing can run before the whole exists. Four cases: a protocol wrong until complete, a
cutover with no dual path, no partial delivery, a hardware bring-up. Then the task says
`Slice: whole — <reason>` and a reviewer may contest the reason. The Slice values and
their sequence live in [complex-plan.md](complex-plan.md#phase-4b--task-specification).

**The machine layer never disappears, it shrinks.** Every plan ends with resumable
state on disk: the full TASKS.md checklist on the complex route, the minimal task
section on the small route. A plan an agent cannot resume from is a chat message,
not a plan.

**Driving an implementation**: the [`tdd`](../tdd/SKILL.md) red run is a gate, not a
suggestion — implementation starts after the failing run is captured, and the final
report quotes it.

**One task at a time, closed by its commit.** Take the first unchecked task. Write its
test, capture the red run, make it green, tick its box, commit it. Only then open the
next task. Never write every test first, never tick boxes in a batch at the end. The
commit is part of the task, in every context: a headless or delegated run commits
without asking, and the final report lists one commit per task. Message and staging
rules live in [`git-conventions`](../git-conventions/SKILL.md#rules). Each task's
implementation covers its own test only ([`tdd`](../tdd/SKILL.md) rule 5), so the
next task goes red. When a test still passes on its first run, the previous slice
overshot: fold that test into the previous task's commit, tick the task, and name
the overshoot in the report. Never commit a tests-only slice.

## Boundaries

Whether the feature should exist at all belongs to
[`discovery`](../discovery/SKILL.md); this skill starts once the decision to build is
made. Claude Code's built-in plan mode covers interactive approval of an immediate
change; once a plan should persist to disk, this skill owns it at either scale. Implementation
methodology belongs to [`software-engineer`](../software-engineer/SKILL.md) and
[`tdd`](../tdd/SKILL.md); commits to [`git-conventions`](../git-conventions/SKILL.md).
Commands follow the shell rules in [`software-engineer`](../software-engineer/SKILL.md#onboarding).
