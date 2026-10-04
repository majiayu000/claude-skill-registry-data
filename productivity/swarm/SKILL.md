---
name: swarm
description: "Use for \"swarm this\", parallel coverage, a race on the same brief, or a batch of independent tasks. Fans out N workers, drains them, returns one report. Manual mode writes the briefs for a human to dispatch instead of spawning."
disable-model-invocation: true
---

# Swarm

Fan out N workers. They cover separate slices, race the same brief, or both. You wait, merge what comes back, and return one report.

## Start

A todo list with one entry per phase before anything launches: frame, fan out, aggregate, report.

## Frame

1. **State the done predicate** and the artifact or report the swarm has to return.
2. **Pick the shape.** Slices, each worker owns one part. Race, N workers on identical briefs. Or both. For a race, declare the selection rule before spawning: first pass, rank all, or best of.
3. **Set N.** From the human, or derived from the shape. N is total workers, not the harness's concurrency limit.
4. **Give each worker its own place to write.** A worktree, a branch, or its own directory. Two workers writing to the same path is the bug `no-shared-writes` exists to prevent.
5. **Write the briefs.** Every brief stands alone; the worker has no memory of anything else. Goal, scope, its exact slice or race arm, how to verify, what to report. Reports come back as PASS, ISSUES, or BLOCKED, with evidence.

## Fan out

Spawn all N at once, in the background. If a worker needs something only on the human's machine, run it locally. Otherwise wherever the harness runs subagents.

If a worker drops out, continue with N minus one and note it.

### Manual mode

Sometimes the human dispatches, not you. They paste each brief into a fresh session, the worker turns in, and the human merges. Use this when the human asks to run the lanes themselves, when workers need permissions you don't have, or when the batch is tracker issues and a person wants to stay in the loop between plan and execution.

In manual mode you don't spawn. You do everything else. Read all the source material end to end before planning: the bug reports, screenshots, tracker items, not just titles. Map every issue to its tracker item. Group into lanes by the files a change touches, not by feature name. Inside a lane, tasks run one at a time. Across lanes, in parallel. Settle any product decision with the human before a brief goes out. Write the briefs. Then review every turn-in for drift from the brief and for proof before the human merges. You don't write the feature code, and the human merges every time unless they hand it to you.

## Aggregate

Read the results. For slices, every required slice needs a result. For a race, apply the rule you declared. Never paste raw worker output into the report.

Keep a compact table, one line per worker. Issues as one-liners with evidence. Gaps and dropouts named.

## Report

One report. The table, the issue one-liners, the gaps, and the race rule if there was one.
