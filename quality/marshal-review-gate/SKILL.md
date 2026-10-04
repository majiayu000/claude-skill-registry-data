---
name: marshal-review-gate
description: >
  Gate a candidate diff behind an independent, multi-reviewer consensus before integrating it. Spawn
  several biased reviewers (architect, quality, tests) that each judge the SAME diff in isolation,
  then apply a fixed truth table - integrate only when no reviewer rejects and at least one approves.
  Use when a single-pass review (marshal-orchestrate step 4) is not enough: a high-stakes merge, or
  when you want a quorum instead of one opinion. The engine runs the agents; this playbook is the
  judgment.
---

# Gating a merge behind reviewer consensus

> **Prefer a declared team when one exists.** `run_team` (see `marshal-adversarial-review`) does
> step 2 below as one call: it fans the reviewers out in isolation, refuses any reviewer that is not
> read-only, and returns one report per reviewer plus a unified one. It deliberately does **not**
> apply the truth table in step 4 — you read the reports and decide, which is what the sealed
> `REVIEW:` line here is a cruder approximation of. Use the hand-rolled loop when you need a one-off
> panel no team file declares, or want to vary the rubric per run.

You already have a worker run that **succeeded** and a diff you could merge. `succeeded` means the
process exited cleanly (plus the workspace's config-level `verify:` gate, if one is set - that
mechanical gate runs before this review gate ever sees the run), not that the code is correct - so
before a high-stakes integrate you gate it behind several **biased, independent** reviewers and a
fixed rule, instead of one judgment call. The
loop is **collect → review (in isolation) → decide by truth table → fix or integrate.**

This is not "run the same review prompt three times and average." It is biased, independent,
multi-angle convergence: each reviewer holds one prior, judges one lens, and seals its verdict
without seeing the others.

## When to use
- After a run succeeded (`marshal-orchestrate` step 3) and the change is risky or valuable enough to
  want more than your own single read - a public API, a migration, a security-sensitive path.
- Not a replacement for reading the diff yourself; a structured second/third opinion that a worker
  cannot hand-wave past.

## The three rules that make it work
- **Biased.** Each reviewer holds ONE prior and judges only that lens. Never ask one agent for
  "overall quality" - that collapses back to a single opinion.
- **Independent.** Reviewers must not see each other's verdicts. Spawn them together so they run in
  parallel isolation; never feed one reviewer another's output.
- **Sealed.** Each reviewer ends with exactly one parseable line: `REVIEW: approve|reject|comment -
  <reason>`. A `reject` must cite concrete evidence (a rule clause, a named smell, a missing test),
  not a vibe.

## 1. Get the candidate diff
`collect_run(candidate_run_id)` returns the diff + changed files, read-only. This exact diff is what
every reviewer judges.

## 2. Spawn the reviewers (no-peek, read-only)
Route to read-only clients and put the SAME diff + the lens rubric + the required verdict line into
each reviewer's `goal`. Run them together with one call so they cannot see each other:

```
run_many([
  {client: <read-only client>, goal: ARCHITECT_RUBRIC + diff, task_id: "review.<candidate>"},
  {client: <read-only client>, goal: QUALITY_RUBRIC   + diff, task_id: "review.<candidate>"},
  {client: <read-only client>, goal: TESTS_RUBRIC     + diff, task_id: "review.<candidate>"},
])
```

Share one `task_id` across the three so `usage()` / `report()` group the review as one unit. The
lenses:
- **architect** - does it honor the project's rules and scope? Prefer deletion. Reject only with a
  cited rule/clause, never "architectural smell."
- **quality** - readability, naming intent, dead code, over/under-engineering, function size.
- **tests** - real behaviour tests on the changed lines; no skipped tests, no loosened assertions,
  no mock-only pseudo-coverage.

## 3. Parse the verdicts
From each run's text take the single `REVIEW:` line -> `approve` / `reject` / `comment`. A run you
cannot parse, or that `failed` / `timed_out`, is **not** an approval: re-spawn it. Never count a
missing verdict as approve.

## 4. Apply the truth table
With all three reviewers present and judging the same diff:

| verdicts | decision |
|---|---|
| any `reject` | **FIX** (go to step 5) |
| 0 reject, 0 approve (all comment) | **HOLD** - needs your explicit approval; comments alone don't merge |
| 0 reject, >= 1 approve | **INTEGRATE** (go to step 6) |

A `reject` is blocking; a `comment` is advisory. Do not let advisory comments block a merge, and do
not let an all-comment result auto-merge.

## 5. Fix loop (on any reject)
Dispatch ONE fix task that addresses **only** the reject reasons (quote them verbatim in the goal);
comments are optional context, not demands. Then re-run the gate on the new candidate run. Cap at
~2-3 fix rounds. Stop and bring it to a human if the same reason rejects twice, or if two reviewers
demand opposite changes (a conflict no fix can satisfy) - never loop forever.

## 6. Integrate
Only after **INTEGRATE**: `integrate(candidate_run_id, cleanup?)`, one run at a time. See
`marshal-orchestrate` step 5 for handling `merged` / `conflict` / `blocked` / `empty` / `error`.
Worktree isolation means main is untouched until this step.

Then judge the **reviewers**, not just the candidate: `set_outcome(<reviewer_run_id>, "advisory")`
for each gate reviewer whose verdict you used. A reviewer merges nothing, so `advisory` is what
fits - `abandoned` reads as giving up and would count a review you relied on against that client's
integration rate. Without this the gate's own reviewers never accumulate a `routing` record, and
you cannot tell which of them is worth the spend.

## Invariants to respect
- Reviewers are headless - the rubric + diff in the prompt is all they get; no questions are possible.
- Independent means parallel + isolated; never show a reviewer a peer's verdict.
- A reject needs cited evidence; a comment never blocks; an all-comment result never auto-merges.
- `succeeded` is not `correct`; integrate one run at a time; main is untouched until integrate.
