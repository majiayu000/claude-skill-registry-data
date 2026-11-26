---
name: work-queue
description: "Drains the ready and changes-requested issue queue unattended, running implement then work-review on each eligible issue under a single-flight lock, up to a per-run cap. Use when asked to drain the queue, batch-process ready issues, or run the work loop unattended."
disallowed-tools:
  - AskUserQuestion
---

# work-queue

Drain the ready and changes-requested issues unattended, one at a time, under a lock.

## When to use

- Asked to batch-process, drain or auto-run the work loop.
- A single named issue: use `implement` or `work-review` directly instead.

## Steps

1. Config `work` is `false`: stop, tell the user the work loop is disabled for this repository.
2. Acquire the single-flight lock: `mkdir` at
   `$(git rev-parse --git-common-dir)/agent-skills/work.lock`. Held: stop, report the lock as
   held.
3. Stamp the owner file inside the lock directory with host and a `refreshed` epoch timestamp,
   written through a temp file and renamed into place.
4. Build the queue: every issue `ready` or `changes requested`, without `needs triage`, ordered
   by config `priority`.
5. `needs triage` next to `ready` or `changes requested`: skip the issue, name the contradiction
   in the report, do not label or touch it.
6. Nothing eligible: release the lock, report an empty run.
7. Loop up to config `work.cap` issues: run `implement` on the issue, then `work-review` on the
   same issue once it reaches `review requested` and CI on its head commit has finished. A
   reviewer that reports `boundary`: run the review again as `reviewer-boundary`. Small issues
   with no overlap in files may share one `implementer`, see `agents`.
8. Re-stamp the owner file's `refreshed` timestamp once per iteration.
9. Continue on `blocked`, `changes requested` or `needs human`. Stop the whole run only on a hard
   error.
10. After the cap, or when nothing eligible remains: release the lock with `rm -rf`, explicitly,
    not on a trap.
11. Report a table: issue, outcome, pull request.
12. Any open question that would need a human: comment it on the issue, never ask the user.

## Guardrails

- `disallowed-tools: AskUserQuestion`. This skill never asks, it comments on the issue instead.
- The queue is built from `ready` and `changes requested` only. An issue parked at `needs human`
  or `blocked` is never in it, so a non-independent review's terminal state stops the loop for
  real instead of spinning on the same issue.
- One lock per checkout. A held lock stops the run, it is never broken.
- A `refreshed` timestamp older than three hours marks the lock stale: `rm -rf` it and retake.
  Younger: the run is live, stop and report.
- The cap is a hard limit on the run, applied after ordering.
- Contradictory labels are reported, never resolved by picking one.
- This skill never sets `ai: ready` and never removes `needs triage`. The rule that lets a
  request naming the work do so, see `implement` step 1, never applies here.

## Config

Reads `.agent-skills.json` through the snippet in `~/.claude/skills/README.md`.

- `work`: `false` disables the work loop entirely.
- `work.cap`: maximum issues one run works. Default `5`.
- `priority`: ordering for the queue.
- `labels.needsTriage`, `labels.ready`, `labels.changesRequested`: defaults in
  `~/.claude/skills/README.md`.

## References

- Claim, implement and push: `implement` skill.
- Review and verdict: `work-review` skill.
