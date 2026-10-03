---
name: callesnikov-parallel-execution-optimizer
description: Accelerate substantial Codex tasks with dependency-aware parallelism while preserving correctness. Use when the user explicitly asks for faster execution, parallel agents, concurrent research or verification lanes, batched tool calls, isolated worktrees, or many independent subtasks whose read and write surfaces can be separated safely.
---

# Callesnikov Parallel Execution Optimizer

Use GPT-5.6 Sol as the orchestrator. Turn urgency into a dependency graph, run only independent work concurrently, and merge results through explicit verification.

## Build the execution graph

Before substantial parallel work:

1. Define the objective and observable done signal.
2. Identify the immediate blocker and keep it on the main agent's critical path.
3. Split the remaining work into independent lanes.
4. Mark every lane as `parallel`, `sequential`, or `gated`.
5. Assign a read surface, write surface, risk, and verification command to each lane.

```text
Lane | Mode | Read surface | Write surface | Gate | Verification
Repo map | parallel | repository | none | none | rg evidence
Backend patch | parallel | API modules | src/api | schema known | focused tests
UI patch | parallel | UI modules | app/components | contract known | screenshot + tests
Integration | gated | both patches | shared branch | both complete | build + smoke
```

## Execution rules

- Batch independent file reads, searches, metadata queries, and status checks.
- Spawn agents only for bounded work that materially advances the task.
- Give every agent a concrete output, minimal context, and a disjoint write surface.
- Let agents inherit the current GPT-5.6 Sol model unless the user explicitly requests another model or a lane has a justified workload-specific reason.
- Keep blocking, tightly coupled, or high-judgment work on the main agent.
- Use worktrees only when independent implementation lanes would otherwise collide.
- Poll long-running builds and tests deliberately; do not leave required sessions running at handoff.
- Pause dependent lanes when new evidence invalidates their assumptions.
- Review every delegated patch before integration.

Do not parallelize destructive operations, migrations, shared-state writes, edits to the same file, or live deployments without an explicit gate and authority.

## Merge discipline

1. Collect each lane's artifacts and verification evidence.
2. Check for conflicting assumptions, contracts, files, generated assets, and dependency versions.
3. Integrate the smallest compatible result.
4. Run cross-lane verification after focused lane checks pass.
5. Report incomplete and blocked lanes separately from completed work.

## Failure modes

- Creating agents before defining the dependency graph.
- Delegating the immediate blocker and then waiting idly.
- Giving two agents overlapping files or mutable state.
- Repeating the same investigation in several lanes.
- Treating agent completion as proof of correctness.
- Hiding skipped verification behind a speed claim.
- Leaving background processes alive after the task is handed off.

## Report

```text
Parallel execution result
Lanes: <total>
Completed: <count>
Blocked: <lane and reason>
Integrated: <artifacts or files>
Verification: <exact checks and results>
Residual risk: <unverified boundary>
```

Measure success by elapsed work plus correctness evidence, not by agent count.
