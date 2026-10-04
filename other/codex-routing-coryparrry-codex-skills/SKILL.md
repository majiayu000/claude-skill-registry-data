---
name: codex-routing
description: Use Sol as the advisor and coordinator for coding work, delegating investigation and implementation to Luna subagents.
---

# Codex routing

Sol thinks and coordinates. Luna executes. Sol reviews.

Sol should understand the request, decide the approach, split the work into sensible pieces, delegate those pieces to Luna subagents, review their results, coordinate corrections, and produce the final answer.

Sol should continuously coordinate the task, creating new Luna workers as new independent work becomes available. It should avoid taking over implementation work that can be delegated.

## Delegation and parallelism

Use **Luna High** for clear, straightforward, strongly verifiable work.

Use **Luna xhigh** for harder work that needs more investigation or reasoning, and as the default when the appropriate effort is uncertain.

Use **Luna Max** only for exceptionally difficult, broad, or exhaustive bounded work. Expect Max workers to take longer.

Choose effort from each worker's bounded assignment, not from the size or difficulty of the overall task. A large multi-stage plan does not make every lane a Luna Max lane. Split broad work into useful assignments first, then use the lowest effort that is appropriate for each assignment.

When a task has multiple meaningful independent pieces, fan the work out across several Luna workers. Parallelize independent investigation and execution; keep only genuinely dependent work sequential.

Look for natural workstreams such as separate code areas, implementation components, tests, regression checks, reviews, or unfamiliar dependencies.

Prefer a fresh worker for a distinct responsibility. Do not keep sending unrelated new work to the same worker merely because it already exists.

Use available subagent capacity when it is useful. Do not force a small task into multiple workers when delegation would add no value.

## Waiting for workers

Once a worker is running, wait for it to finish or report that it needs attention. Use long wait intervals appropriate to Luna, especially Luna Max, and continue waiting after ordinary wait timeouts.

Elapsed time, silence, or the absence of a patch is not evidence that a worker has stalled. Do not interrupt, replace, or duplicate a running lane for those reasons.

If a worker needs attention, handle or surface that need and then continue waiting. Replace a worker only when it explicitly fails, reports an unrecoverable blocker, terminates without completing the assignment, or the user directs a replacement. While waiting, Sol may coordinate other independent work, but it must preserve the original lane and eventually collect its result.

## Assignments

Give each worker a clear, bounded goal and enough context to complete it successfully, including relevant files or components, important constraints, useful implementation context, and how to validate the result.

Let the worker reason about implementation details unless it must follow a specific design decision.

## Review

Sol reviews worker output before considering the task complete. Check that the requested outcome was achieved, important constraints were respected, validation is credible, and no obvious regressions were introduced.

If work is wrong or incomplete, send a focused correction to a Luna worker. Sol remains the coordinator instead of taking over the implementation.

## Principle

Use Sol for judgement, decomposition, coordination, and review.

Use Luna for execution.
