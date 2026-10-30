---
name: loop
description: >-
  Load when the user asks for a repeating autonomous mode: "loop 10 30m <prompt>",
  "loop 99 6666 <prompt>", "work cycle after cycle", "keep going until it's done",
  "continue on your own, don't stop", "find new solutions turn after turn",
  "infinite loop", "autonomous until the result". Each iteration is a full work
  cycle (re-state → prior knowledge → research → act → verify → checkpoint), the
  next iteration starts with a NEW angle or hypothesis, and the agent makes its
  own decisions. Stop: N iterations / M minutes / a readiness criterion / 2
  iterations without progress. NOT for a single task (task-cycle) or unattended
  assigned-goal work (autonomous-work).
license: Proprietary
metadata:
  inspiration: "can1357/oh-my-pi, ByBrawe/opencode-loop, disler/infinite-agentic-loop — loop mechanics; rules and text are our own"
  rewritten: 2026-10-03 — an earlier toolchain's assumptions (a research sqlite
    store, a task script, a cycle file) replaced with this kit's memory layers
---

# loop — repeating autonomous iterations

The agent does not "answer and stop": it goes iteration after iteration — a full
work cycle → a checkpoint on disk → immediately the next iteration with a new
angle. It stops only on explicit criteria, not out of the habit "answered — enough".

## Invocation format

```text
loop [N] [M] [prompt]
```

| Argument | Rule |
|---|---|
| N | number of iterations (integer) |
| M | minute limit (integer or with `m`/`h` suffix). Both N and M set — stop at whichever comes first |
| prompt | task/goal, rest of the line. Not set — **continue from the last checkpoint** |

Limits are owner-supplied, never invented: when neither N nor M is given, the run
is bounded by the readiness criterion and the no-progress stop only, and the
opening message says exactly that. Do not silently substitute a default budget.

Examples:

```text
loop 10 30m run an audit and close findings one by one
loop 99 6666 invent improvements and ship them turn after turn
loop improve the release checklist   # no N/M → readiness + no-progress stops
loop                                 # continue from the last checkpoint
```

These are plain requests to the agent, not slash commands: the trigger is the
owner saying "keep going until done" / "work in cycles", not a client command.

## When to use / NOT to use

**Use:** the user explicitly asks for a loop; "do N iterations"; "keep going
until it's done"; a series of sequential improvements where each next step
depends on the previous result.

**NOT to use:** a single task — the `task-cycle` skill; unattended assigned-goal
work with its own stop contract — `loops/parts/autonomous-work`; parallel
decomposition of ONE task by subagents — a host tool capability this loop does not
own, so when the host exposes `spawn_agents` fan out directly instead of through
a loop request (fan-out is not iteration); a trivial request — just do it.

## Workflow

**0. Initialization (once).**

1. Record the task as a Memora node under `root/skill/loops` (project branch when
   the work belongs to a project) and mirror the open steps in `write_todos`.
2. Write the start checkpoint (format below) into that node, with the plan for
   the first iterations.
3. Record the start time: `date +%s` (for the M limit, not by feel).
4. Define the readiness criterion: what must be visible at the end
   (green tests, N findings closed, empty backlog, a concrete file/state).
   If the criterion cannot be formulated — ask the owner before iterating.

**1. Iteration (repeats).** Each iteration is a compact work cycle:

1. **Iteration angle:** one phrase — what this iteration does and HOW it
   differs from the previous one (new hypothesis, other source, other tool,
   other order). Repeating the previous iteration is forbidden.
2. **Prior knowledge:** targeted lookups in Memora (this branch and the domain
   that matches the topic), then `knowledge/` and project docs — so we don't
   repeat or argue with our own conclusions.
3. **Action:** research per the step type → edits/experiment →
   **verification** (the project's real checks plus the usage path; "it built"
   ≠ "it works").
4. **Findings:** record what you chose, why, what you rejected, links — as a
   Memora node (bidirectional `supersedes` when it replaces an earlier one).
   Iterations without a record are wasted iterations.
5. **Checkpoint delta:** append the checkpoint (format below) — short, only
   non-obvious.
6. **Summary to the owner:** 1-2 lines — iteration X/N done, what was done,
   what's next.

**2. Transition to the next iteration.**

- Progress exists → the next iteration develops the previous one (the next
  finding, the next plan step).
- No progress for 2 iterations in a row → **change the angle** (another
  hypothesis, another source, another tool); do not hammer the same thing a
  third time (an error twice = change the method).
- Before starting an iteration, check the limits: iterations done ≥ N? Minutes
  elapsed ≥ M (`date +%s` against start)? Readiness criterion reached AND
  verified? Yes → phase 3, no → iterate.

**3. Stop and final.**

1. Close the task node in Memora with a one-two line result and the stop reason.
2. Final report to the owner: what was done across all iterations, what remains,
   how to continue (a loop request with no arguments resumes from the last
   checkpoint).
3. Stop always with a named reason: which criterion exactly fired.

## Progress detector & retry policy

- **Repeat fingerprint:** hash (step+result) per turn; 2 identical turns with no
  new information = stop criterion → change angle.
- **Retries by class:** validation/auth/permanent → STOP; 429/timeout → 2-3
  retries with backoff+jitter; safety/irreversible → owner confirmation;
  everything else → 1 retry.
- **Budgets:** owner-supplied N/M only — never invented; exceeding any stated
  limit = stop with reason. Expensive operations get a cost mention before, not
  after.

## Checkpoint format

```text
loop: iteration X/N (or X iterations, M min)
done: <what this iteration completed>
decisions: <what you chose and rejected, one line>
next: <the next iteration's angle — one line>
files: <what changed>
```

~100 words limit. The checkpoint is the fuel of resumption: reading the node
back must restore context after a session restart or compaction.

## Success criteria

- N iterations (or M minutes) completed, each with a finding and a checkpoint
  (check: the Memora node has ≥ N+1 entries).
- Or earlier: the readiness criterion reached AND verified by a check
  (not claimed in words).
- Each iteration differs from the previous one — visible from the checkpoints.
- Stop always with a reason; the task record is closed.

## Failure modes

| Symptom | What to do |
|---|---|
| Repeats the same iteration | The angle-change rule after 2 no-progress iterations — apply, don't discuss |
| Context running out (>50-60%) | Don't start a new iteration: checkpoint + tell the owner "say loop — I'll continue from the checkpoint" |
| Owner doesn't see progress | 1-2 line summary after EVERY iteration — mandatory, not optional |
| Stopped without a reason | Stop only by phase 3 criteria; the reason goes in the report |
| Decisions not recorded | Every iteration must leave a finding; otherwise knowledge dies with the context |

## Gotchas

- Keep the iteration counter EXPLICIT in every checkpoint (iteration X/N) —
  from memory the agent errs in both directions.
- Minutes — by `date +%s`, not by felt time.
- Expensive/irreversible/outward-facing actions — owner confirmation even
  inside the loop (the irreversibility gate). Never Destroy outranks any loop.
- Secrets — placeholders only, even in checkpoints.
- "Readiness criterion reached" — only after verification by a check;
  a green check that doesn't verify the feature is not done.
- Iterations don't have to be big: a small verified step beats a large
  unverified one.
- If the owner asks for 99 iterations and 6666 minutes: a BIG
  autonomous mode. Checkpoints are critical: without them everything is lost on
  context overflow.

## References

- The cycle behind one iteration and its gates: `task-cycle` and `AGENTS.md` §
  Engineering cycle.
- Unattended assigned goal, checkpoints and valid stops: `loops/parts/autonomous-work`.
- Loop patterns and design interviews: `loops/parts/loop-library`.
