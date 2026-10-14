---
name: e4008-task
description: "Evaluate the tasks of an SMP schedule artefact against ECSS-E-ST-40-08C clause 5.4.4 and the three normative items that clause places on them. Use when a schedule has to be accepted before it is armed: giving each task a unique name and at least one step, expanding nested task invocations into the single ordered activity sequence a trigger actually produces, refusing a step that advances simulated time or blocks the scheduler so the task stays atomic at one point on the time line, resolving every invocation and schedule entry, and naming any chain of invocations that reaches back on itself. Trigger: ecss, e-st-40-08-simulation-modelling-scope, e4008-task, schedule-task-definition, task-activity-order, task-atomic-execution, task-invocation-cycle, unreachable-schedule-task."
license: Apache-2.0
compliance: STANDARDS-REF
standards:
  - id: ecss
    reference-only: true
gated: false
domain: space-systems
pack: space-systems
compatibility: "agentskills.io SKILL.md; any SKILL.md host (Claude Code, Hermes, OpenClaw)"
metadata:
  domain: space-systems
  subdomain: ecss
  tags: [ecss, e-st-40-08-simulation-modelling-scope, e4008-task, schedule-task-definition, task-activity-order, task-atomic-execution, task-invocation-cycle, unreachable-schedule-task]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS Simulation Modelling — Schedule Task (space-systems/ecss/e4008-task)

Use when the task is the schedule task of ECSS-E-ST-40-08C clause
5.4.4 -- the named unit a schedule entry triggers, holding an ordered
list of steps that all run at one point on the time line, and the
three normative items that fix what a task may contain.

## Domain quick reference

- A schedule entry does not name an activity. It names a task, and
  the task is what carries the ordered steps, so the task is the
  smallest thing the schedule can trigger.
- Order is declared, not derived. The steps run in the order they
  appear, and a checker that sorts them by name or by target changes
  the behaviour of a schedule nobody edited.
- A task runs as one unit at a single scheduling point. Nothing
  inside it advances simulated time and nothing inside it blocks, so
  no other task can interleave between two of its steps. A step that
  declares a duration is not slow -- it is a different kind of thing
  that does not belong in a task.
- A task may invoke another task, which is what makes the real
  execution order a flattening rather than a list. The order a
  trigger produces is only visible after the invocations have been
  expanded in place.
- Invocation is transitive, so a cycle is a property of the schedule
  and not of any one task. Every task in a cycle can look correct on
  its own; only the walk over the whole set finds it.
- A cycle does not make the order wrong, it makes the order
  undefined. The expansion does not terminate, so the honest answer
  is to produce no order at all rather than a truncated one.
- A task that nothing reaches is worth reporting and is not a defect.
  It is usually an activity set kept for a contingency, and failing
  the schedule for it would push people to delete it.

## Workflow

1. Index the tasks from the declared list rather than from a
   name-keyed mapping, so an unnamed task and a repeated name are
   both visible instead of silently collapsing.
2. Walk each task's steps in order. Reject an unknown step kind, an
   unnamed activity and an unnamed invocation target, and record a
   repeated activity name inside one task.
3. Check atomicity on every step: a non-zero declared duration and a
   blocking flag are each findings, because either one breaks the
   single-point execution the schedule depends on.
4. Resolve every invocation target against the index, so a missing
   task is named against the step that wanted it.
5. Walk the whole invocation graph for cycles, reporting each cycle
   once rather than once per task on it.
6. Expand each task into its flattened activity order, but only when
   no finding makes the expansion undefined, then report which tasks
   the schedule entries reach and which are reachable from nothing.

## Pitfalls

- Reading a task's activity list as its execution order. Any nested
  invocation contributes activities from another task, and the real
  order is the flattening, not the literal step list.
- Expanding invocations without cycle detection. The recursion
  terminates only by exhausting the stack, and a depth-limited
  expansion returns a plausible order for a schedule that cannot run.
- Reporting a cycle once per task involved. A three-task cycle then
  reads as three defects and each one looks individually fixable.
- Treating a step with a duration as merely slow. It advances
  simulated time inside a unit that is defined not to, so the next
  task on the same scheduling point runs at a time the schedule never
  declared.
- Failing a schedule for a task nothing reaches. Contingency tasks
  are meant to sit unreferenced until an operator arms them; the
  right response is to name them, not to reject the artefact.
- Assuming an invocation target exists while walking reachability.
  An unresolved target is already a finding, and a walk that indexes
  it directly turns that finding into a crash.

## Behavior contract (gate 3)

The task indexing with unnamed and duplicate detection, the declared
step order, the flattened execution order over nested invocations, the
atomicity checks on duration and blocking, invocation resolution,
whole-graph cycle detection reported once per cycle, and the reached
and unreachable task sets are exercised by the gate 3 contract test:
scripts/test_e4008_task.py against scripts/e4008_task_logic.py
(stdlib unittest, offline). Run:
python3 scripts/test_e4008_task.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
