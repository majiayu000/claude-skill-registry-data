---
name: manager-loop
description: >
  Run a large batch of independent work items (a fleet-wide harvest, a
  multi-repo sync-down, an overnight backlog) as a persistent coordinator
  loop instead of one item at a time. Use when there are enough independent
  units of work that dispatch-review-merge would otherwise repeat many times
  in a row, or when the batch should keep making progress across a heartbeat
  interval instead of stalling until the next message.
---

# Manager Loop

One coordinator, many workers, a heartbeat instead of a human trigger between
steps. The coordinator never implements — it dispatches, watches, routes
feedback, and gates merges. Each worker gets its own git worktree, branch,
and PR, and is told explicitly to keep going until the deliverable is
actually mergeable, not just "implemented."

This is the outer loop that runs many `evaluator-optimizer` convergence
loops in parallel (each worker converging its own PR against a pass/fail
bar), with `advisor-checkpoint` as the review step when a worker's approach
needs a second opinion before or after the work lands.

## When to use it

Fits a batch with several genuinely independent units — files, projects, or
PRs that don't depend on each other's outcome. Doesn't fit a single task
with one thread of work (there's nothing to coordinate), or units so
interdependent that running them one at a time, in order, with full context
carried forward is actually required.

For a single feature-level task with several sequential subtasks (one branch,
one PR, tasks that build on each other) rather than a batch of independent
units, use `superpowers:subagent-driven-development` instead — same session,
fresh subagent per subtask, code review between each. Reach for this skill
only once the work is actually a multi-unit batch; standing up worktrees,
branches, and PRs per subtask for what is really one feature is the heavier
tool for the wrong job.

## The shape

1. **Dispatch.** For each unit of work, spin up a worker on its own
   worktree and branch — a background `Agent` call. Give it the deliverable,
   the acceptance bar (tests/build/lint that must pass), and an explicit
   directive: don't stop at "I implemented it" — keep going until the branch
   is actually mergeable (green build, green tests, PR open), and report
   back rather than declaring done if genuinely blocked. This is the fix for
   a worker that stops early at a plausible-looking first draft.
2. **Heartbeat instead of waiting on the human.** Don't sit idle between a
   worker's completion notification and your next action. Use
   `ScheduleWakeup` to re-enter at an interval matched to how fast the batch
   actually moves — checking in-flight PRs, build status, and whether a
   worker is stuck, the same way you'd poll CI. This is what turns "dispatch
   one thing, wait for a message, dispatch the next" into a loop that keeps
   moving on its own between check-ins. When you report batch status at a
   heartbeat, ground it in what you actually checked this cycle (PR state,
   CI status, the worker's own report) — don't assert a unit is done or
   still on track without a result from this session backing that claim.
3. **Route feedback back to the worker, don't re-implement it yourself.**
   When a PR needs a change (a review finding, a failed check), resume the
   *same* worker via `SendMessage` with the specific feedback, rather than
   fixing it in a fresh agent with no context or fixing it yourself in the
   coordinator's own thread. The worker already has the worktree and the
   history; re-dispatching loses both.
4. **Gate the merge.** Require the objective checks (build, tests, lint) to
   pass before a worker's PR is mergeable — same rule as
   `evaluator-optimizer`. Then still read the diff yourself before merging.
   A green build proves the code compiles and the tests it wrote pass; it
   doesn't prove the approach was right, that nothing was overreached, or
   that a subtler failure mode was missed. The loop moves work forward — it
   doesn't replace the review.

## What this doesn't fix

Worker threads still stall on genuinely ambiguous problems, still misread
instructions, and still produce plausible-but-wrong work that passes its own
tests without actually being correct — the same failure modes any single
agent has, just now happening in parallel across more surface area. Watch
for a worker whose "done" claim doesn't survive your own read of the diff,
and don't let batch throughput become a reason to skip that read.
