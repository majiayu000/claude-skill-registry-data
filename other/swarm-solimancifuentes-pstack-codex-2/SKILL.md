---
name: swarm
description: "Fan out N parallel workers, drain them, and return one report. Use for /swarm, 'swarm this', or parallel coverage, races, gauntlets, and exploration."
disable-model-invocation: true
---

# Swarm

Fan out N workers through the executing host's selected runtime adapter.

## Start

Open a todolist with one entry per phase before launching anything.

1. Frame
2. Fan out
3. Aggregate
4. Report

## Phase A: Frame

1. State the done predicate and the artifact or report the swarm must return.
2. Choose the shape. Partition into slices, race N workers on identical briefs, or mix both. For a race or mixed shape, declare `first pass`, `rank all`, or `best-of` before spawning.
3. Set N from the user or derive it from the shape. N is total work items, not simultaneous workers. The live session limit includes the parent and nested agents.
4. Use the runtime `swarm workers` choice from [CODEX.md](../../CODEX.md), inheriting the parent's model and reasoning by default. For an explicitly authorized model comparison, name each actual available choice before launching. The native port does not supply Cursor cloud machines or Claude/Grok diversity.
5. Give each worker its own writable output when it writes. When workers verify or measure commits, each brief names the exact SHAs. A measurement brief also names the method (sample count, what one sample is, order). The worker records both in its result.

## Phase B: Fan out

Launch workers through the selected adapter's actual delegation tools within available capacity. Queue remaining work and refill as workers finish. Writers get disjoint output paths or actual isolated Git worktrees and branches. Pass each worktree's absolute path and required commit SHA in the brief. Verify each worker's actual environment. A branch name does not create checkout or credential isolation. Codex internal workers use the current collaboration environment; Dots may start a separately configured Codex task when its native tools support that operation.

If a worker must begin at a non-default ref, create or select a real checkout at that ref and verify its HEAD before dispatching. Do not invent `cloud_base_branch` support.

Every brief stands alone. Include the goal, scope, exact slice or race arm, how to verify, and what to report. Reports use `PASS`, `ISSUES`, or `BLOCKED` with evidence. A worker that can prove a defect reports `ISSUES` and lists every issue it can prove, not only the first.

If a worker drops out, proceed with N-1 and note it.

## Phase C: Aggregate

Read the terminal results. Drop a result that does not record the SHAs and method its brief names, and respawn that worker once. After a second miss, record a gap. A gap does not count as a pass. For coverage, every required slice needs a result. For a race, apply the selection rule declared up front. Use first pass, rank all, or best-of. Do not paste raw worker dumps.

## Phase D: Report

Return one consolidated in-chat report with the table, issue one-liners, gaps or dropouts, and the race rule when used.
