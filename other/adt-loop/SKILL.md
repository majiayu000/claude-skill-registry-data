---
name: loop
description: Default execution rhythm — inspect → act → verify → checkpoint — applied iteratively until the task is done or a clear blocker emerges. Use when working through a known plan, draining a queue (PRs, issues, dependency bumps), or executing a multi-step recipe where each step's output informs the next. Each iteration must produce a concrete artifact (commit, comment, decision) and a one-line state update. Stop on first unrecoverable error rather than retrying blindly. Pair with `ship` for merge-bound work and `handoff` if budget runs out mid-loop.
triggers:
  - loop
  - execute this plan
  - keep going safely
  - work through these
  - drain the queue
  - keep cycling
  - run iteratively
---

# loop

This is the default working mode once the path is known.

## Cycle

1. Inspect the smallest missing evidence.
2. Act on the smallest coherent change.
3. Verify with narrow checks first.
4. Checkpoint the result.
5. Repeat until done or blocked.

## Stop conditions

Stop and re-route if:
- the evidence no longer supports the current path
- the diff grows beyond the intended scope
- the same failure repeats without progress
- the work becomes multi-step enough to require `plan`
- context budget exceeds 75% → emit `handoff`, then stop the loop
- cumulative tool-result bytes >50KB without progress → summarize + drop noise before next iteration

## Parallel mode

If a `Monitor` task is running (CI settle, build, long test), do NOT busy-wait. Pick up an independent priority — refactor a different file, draft a memory note, answer an open review thread — and resume the original loop when the monitor fires its event.

Rule: at most one Monitor active per loop; otherwise events collide.
