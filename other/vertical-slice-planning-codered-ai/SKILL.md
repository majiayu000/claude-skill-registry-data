---
name: vertical-slice-planning
description: >
  Use this skill when the user asks for an implementation plan for work that spans
  multiple components or services — "plan this out", "break this into tasks",
  "write a plan for wiring X to Y". Produces an executable plan directory: tasks
  ordered as vertical slices so every unit of work verifies the whole path it
  touches instead of deferring integration to the end, each task a single
  idempotent Python script that applies its change through hashline and proves it
  with runnable gates. Plan-only — it emits the directory and stops.
---

# Vertical Slice Planning

Ordinary plans are horizontal: build the backend, then the client, then wire them
together. Every integration defect surfaces at the end, at maximum cost, and
progress is unmeasurable until the last step. Two habits cause it — gates written
as prose that nothing forces to run, and edits described rather than executed.

This skill emits a plan where neither is possible. Each task is a Python script
that applies its own change and proves it, and the ordering guarantees a task
never defers the integration it depends on.

**Announce at start:** "I'm using the vertical-slice-planning skill to create the plan."

**This skill is plan-only.** Emit the directory and stop. Execution is a separate
act by a human or another agent.

## Output

    docs/plans/YYYY-MM-DD-<feature>/
      plan.md                machine-facing index
      plan_superpowers.md    human-facing plan
      taskkit.py             copied verbatim from references/
      run.py                 copied verbatim from references/
      tasks/task_NN_*.py     one apply+verify script per task

See `references/plan_formats.md` for both document schemas.

## The Six Steps

**1. Seam map first.** Before any task exists, enumerate the components and the
*seams* between them — HTTP route, queue topic, DB table, module import. Seams,
not components, drive the ordering.

**2. Order as vertical slices.** Each task is a thin path through every component
it touches. Task 1 of a multi-component feature wires the seam end-to-end with
the most trivial payload that can be verified: a hardcoded response, one field,
one row. Later tasks thicken it. A task that adds capability to exactly one
component without exercising a seam is allowed only when no seam is yet in scope.

**3. Assign gate tiers.** Each task's `verify()` composes these; declare the tier
in `plan.md`.

| Tier | Runs | Required when |
|---|---|---|
| T0 structural | asserts the edit landed | always |
| T1 component | the touched component's own tests | always |
| T2 crossing | a real end-to-end call through the seam this task wired | task touches 2+ components |

T2 is neither optional nor deferrable — it is the property this skill exists to
buy. If a T2 gate cannot be run in the target environment, **the plan is wrong**:
say so now rather than emitting a task that cannot prove itself.

**4. Decide scripted vs manual**, per task, in this order:

- New file → **scripted**, full content embedded in `apply()` via `create_file`.
- Edit whose target set and result are determinable now → **scripted** via `Editor`.
- Otherwise (design judgement, ambiguous refactor) → **manual**: prose steps in
  `plan_superpowers.md`, `apply()` raises `ManualTask` carrying them.

`verify()` is always fully written and runnable. **The gate never goes manual.**

**5. Emit the directory.** Scripts first; both markdown files are generated from
them. Copy `references/taskkit.py` and `references/run.py` in verbatim — do not
regenerate or edit them. Start each task from `references/task_template.py`.

**6. Self-check before handing over.** From the target repo root, run
`python3 docs/plans/<dir>/run.py --status`. Tasks always run with `cwd = the target repo root`,
never the plan directory. If you're running from elsewhere, use
`python3 docs/plans/<dir>/run.py --status --repo-root /path/to/repo` to override the target directory.
Every gate must **fail cleanly** (exit 1) rather than error. A gate that errors
is a defect in the plan — fix it before handing over. See `references/hashline_rules.md`
(the exit contract section) for how to distinguish a clean gate failure from a crash.

## Editing Rules

All edits go through `taskkit.Editor`, which uses hashline. `grep`, `sed`,
string-replace tools and `open(...).write()` are banned in emitted code. Anchors
are resolved at run time, never baked in at plan time. Drift halts with exit 3;
hashline being unavailable degrades to a loud recorded fallback. Full details and
the exit contract: `references/hashline_rules.md`.

## Red Flags

| Thought | Reality |
|---------|---------|
| "I'll add the integration test as the last task" | That is the horizontal plan this skill exists to prevent. T2 belongs to the first task that crosses the seam. |
| "This task only touches the backend, so T1 is enough" | Check the seam map. If it changes something the other side reads, it crosses. |
| "The gate is obvious, prose is fine" | A gate that isn't runnable code isn't a gate. Write `verify()`. |
| "I'll bake in the line number I read just now" | The file will have moved by then. Use `locate()` at run time. |
| "hashline rejected the patch, I'll use the fallback" | Rejection is drift — a true signal. Exit 3 and replan. |
| "This edit is too subtle to script, so the task is manual" | Manual means the *edit* is manual. The gate is still fully written. |
| "The plan is done, I'll start on task 1" | This skill is plan-only. Emitting the directory is the deliverable. |
