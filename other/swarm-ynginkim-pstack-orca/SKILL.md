---
name: swarm
description: "Fan out N parallel workers, drain them, and return one report. Use for /swarm, 'swarm this', or parallel coverage, races, gauntlets, and exploration."
disable-model-invocation: true
---

# Swarm

> Names in backticks, such as `spawn-worker` and `find-sessions`, are capabilities, not commands. Read `../resolve-capability/SKILL.md` before the first step. It says how each one is done here and whether a worker on another agent can be started.

## Start

Open a plan with `track-todos`, one entry per phase, before launching anything.

1. Frame
2. Fan out
3. Aggregate
4. Report

## Phase A: Frame

1. State the done predicate and the artifact or report the swarm must return.
2. Choose the shape. Partition into slices, race N workers on identical briefs, or mix both. For a race or mixed shape, declare `first pass`, `rank all`, or `best-of` before spawning.
3. Pick the model. Read `~/.agents/skills/select-model/SKILL.md` and choose the worker's model and how to start it from it. Start every worker as the Subagents section of `../poteto-mode/SKILL.md` says, which also covers a missing `select-model`. The table says what a worker needs, not which model fills it. For a model race, name each arm's model up front. Pick each worker's reasoning level and speed for the job, per that section.

   | Seat | Kind | Needs | Count and diversity |
   |---|---|---|---|
   | Worker | code or read, by the slice | when it writes, `isolate-checkout`. When it verifies, the exact SHAs and its own checkout of them. | N, from the shape chosen in step 2. All start together. |
4. Give each worker its own writable output when it writes. Workers share this machine, so give each `isolate-checkout` (its own worktree, ports, and temp paths), per the **separate-before-serializing-shared-state** principle skill. When workers verify or measure commits, each brief names the exact SHAs, and the worker uses its own checkout of them. A measurement brief also names the method (sample count, what one sample is, order). The worker records both in its result.

## Phase B: Fan out

Start all N workers at once, each on the model chosen in step 3. When a worker must start from a non-default pushed branch, its brief names the branch and tells it to check that branch out first.

Every brief stands alone. Include the goal, scope, exact slice or race arm, how to verify, and what to report. Reports use `PASS`, `ISSUES`, or `BLOCKED` with evidence. A worker that can prove a defect reports `ISSUES` and lists every issue it can prove, not only the first.

If a worker drops out, proceed with N-1 and note it.

## Phase C: Aggregate

Read the terminal results. Drop a result that does not record the SHAs and method its brief names, and respawn that worker once. After a second miss, record a gap. A gap does not count as a pass. For coverage, every required slice needs a result. For a race, apply the selection rule declared up front. Use first pass, rank all, or best-of. Do not paste raw worker dumps.

## Phase D: Report

Return one consolidated in-chat report with the table, issue one-liners, gaps or dropouts, and the race rule when used.
