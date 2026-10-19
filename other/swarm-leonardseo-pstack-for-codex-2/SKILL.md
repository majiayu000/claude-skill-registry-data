---
name: swarm
description: Fan out N parallel workers, drain them, and return one report. Use for
  /swarm, 'swarm this', or parallel coverage, races, gauntlets, and exploration.
---

Read [Codex runtime contract](../../CODEX-RUNTIME.md) before applying this workflow. It governs tools, delegation, models, authorization and fallbacks.


# Swarm

Fan out N parallel native workers when supported. They may cover separate slices, race the same brief, or mix both. The parent waits, aggregates, and returns one report.

## Start

Open a todolist with one entry per phase before launching anything.

1. Frame
2. Fan out
3. Aggregate
4. Report

## Phase A: Frame

1. State the done predicate and the artifact or report the swarm must return.
2. Choose the shape. Partition into slices, race N workers on identical briefs, or mix both. For a race or mixed shape, declare `first pass`, `rank all`, or `best-of` before spawning.
3. Set N from the user or derive it from the shape. N is total workers, not the host concurrency limit.
4. Default all workers to inherit-parent. Use only authorized, exposed model overrides; label actual models and any sequential fallback.
5. Give each worker its own writable output when it writes. When workers verify or measure commits, each brief names the exact SHAs. A measurement brief also names the method (sample count, what one sample is, order). The worker records both in its result.

## Phase B: Fan out

Launch workers through the host-native tools and actual schema under CODEX-RUNTIME.md. Give each its own scope and paths. Respect the host concurrency limit and perform overflow work sequentially.

For a non-default branch, explicitly prepare an isolated worktree at the requested ref and pass its absolute path in the brief.

Every brief stands alone. Include the goal, scope, exact slice or race arm, how to verify, and what to report. Reports use `PASS`, `ISSUES`, or `BLOCKED` with evidence. A worker that can prove a defect reports `ISSUES` and lists every issue it can prove, not only the first.

If a worker drops out, proceed with N-1 and note it.

## Phase C: Aggregate

Read the terminal results. Drop a result that does not record the SHAs and method its brief names, and respawn that worker once. After a second miss, record a gap. A gap does not count as a pass. For coverage, every required slice needs a result. For a race, apply the selection rule declared up front. Use first pass, rank all, or best-of. Do not paste raw worker dumps.

Keep a compact result table, one-line evidenced issues, and explicit gaps or dropouts.

## Phase D: Report

Return one consolidated in-chat report with the table, issue one-liners, gaps or dropouts, and the race rule when used.
