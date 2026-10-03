---
name: swarm
description: "Coordinate independent routine execution or exploration batches and return one reviewed report. Use for $swarm or large separable work that justifies parallel overhead."
---

# Swarm

Before delegating or using optional capabilities, read [the runtime contract](../david-mode/references/agent-runtime.md). It owns eligibility, model selection, limits, and fallback.

Coordinate isolated workers for routine batches whose interfaces and acceptance criteria the parent has decided. Prefer distinct slices; duplicate attempts require an explicit comparison request. The parent plans the work, handles difficult implementation, reviews results, and returns one report. Select narrow for search/tagging/mechanical lanes and complex for bounded implementation/debugging lanes, using the active client's route and fallback from the runtime contract for every worker.

## Start

Open a todolist with one entry per phase before launching anything.

1. Frame
2. Fan out
3. Aggregate
4. Report

## Phase A: Frame

1. State the done predicate and expected artifacts. Apply the runtime's context and overhead gates before choosing workers.
2. Partition into independent execution or exploration slices. Keep prerequisite work sequential; new filenames do not remove dependencies. For an explicitly requested race, declare `first pass`, `rank all`, or `best-of` before spawning.
3. Set N from the number of useful independent batches. Apply the runtime concurrency limit and queue excess work; never drop it silently.
4. Resolve the worker tier, model, and effort from the runtime contract. A race compares attempts using that same selected route; it does not select additional models.
5. Give each worker exclusive files, a separate worktree, or a separate output directory. Keep architectural decisions and difficult boundary code assigned to the parent.

## Phase B: Fan out

After proving independent reads or isolated writes, dispatch ready workers within the runtime limit. Every worker is a leaf using the exact configured pair. Work requiring unavailable tools stays with the parent. For a non-default base, create or select the exact worktree before dispatch and name it in the brief.

Every brief stands alone. Include the goal, scope, exact slice or race arm, how to verify, and what to report. Reports use `PASS`, `ISSUES`, or `BLOCKED` with evidence.

If a worker drops out, reconcile its partial state and make one bounded retry when safe. Otherwise proceed with a labeled partial result or fail closed when that lane is required.

## Phase C: Aggregate

Inspect each result's diff or source evidence and run the relevant check before accepting it. Apply the runtime correction limit and take over difficult or repeatedly failing work. For coverage, every required slice needs a result. For a race, apply the declared selection rule only to verified attempts. Do not paste raw worker dumps.

Keep a compact result table, one-line evidenced issues, and explicit gaps or dropouts.

## Phase D: Report

Return one consolidated in-chat report with the table, issue one-liners, gaps or dropouts, and the race rule when used.
