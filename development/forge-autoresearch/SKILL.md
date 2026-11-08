---
name: forge-autoresearch
description: "User-invoked only: /forge-autoresearch. Bounded keep-or-revert experiment loop on one measured metric (speed, size, score): frozen harness, one change per round, decision log."
disable-model-invocation: true
---

# forge-autoresearch: climb one metric, keep only what measures better

The owner types `/forge-autoresearch <goal>` to improve one measurable number (a build time, a bundle size, a
test-suite pass rate, a benchmark score) by many small experiments: one change, one measurement, keep or
revert. It is the Forge rewrite of Karpathy's autoresearch loop and pstack's Hillclimb playbook.

It is not source research. A question that needs sources and citations goes to the deep-research Workflow.
Improving a skill's text uses `forge-skill-testing` Part 3 (paired judging), because a judged score is not a
deterministic metric. A one-off bug or slowness goes to `forge-debug`.

## Preconditions (stop and ask the owner once if one is missing)
- A **metric command**: one repeatable command that prints the number, and the direction that counts as better.
- A **regression gate**: the tests that must stay green, green right now.
- A **target and a floor**: for example "20% faster than baseline, and at least 10 rounds", so one lucky early
  win cannot end the run.
- A **budget**: a maximum number of rounds and a maximum wall time per run. Fan-out stays within the lane
  budget (`node .claude/forge-bin/forge-lane-budget.cjs`) and pauses when the usage guard pauses.
- An **editable scope** (the files experiments may change) and a **frozen set** (the harness, the tests, the
  eval data), written down before round 1.

## Setup
1. **Isolate.** Create a worktree and branch `autoresearch/<tag>` for the run (see `forge-worktrees`). Nothing
   runs in the shared tree. *Done when:* `git worktree list` shows it and the branch did not exist before.
2. **Ground the case.** Name the workload dimensions that move the metric (data size, history, concurrency)
   and pick a case that reproduces the owner's complaint. *Done when:* the case shows the problem; if no case
   does, fix the reproduction first instead of climbing.
3. **Build, prove and freeze the harness.** Run contrasting workloads and confirm the metric separates them.
   Make it print its error count and how much work it did, so a run that did nothing cannot look fast. Sample
   enough to clear the noise (the median of N runs, never one run). Then freeze it. *Done when:* the same
   command run twice on unchanged code gives the same verdict, and the spread of N runs is written down.
4. **Baseline.** Run the metric and the regression gate on the unchanged branch. *Done when:* both are recorded
   as round 0 in the decision log.
5. **Open the decision log** at `_scratch/autoresearch-<tag>/decision.tsv` (tab-separated, outside git):
   round, hypothesis, change, commit, before, after, delta, gate, verdict (kept, reverted, crash), note.
   Read it before each round.

## The loop (one hypothesis per round)
1. Write the hypothesis as a mechanism ("move X off the start path because it blocks the first render"), not
   "try caching something".
2. **Build Boss** (build route, opus / medium) makes the one change inside the editable scope and commits it.
   Independent hypotheses may run in parallel, each in its own worktree.
3. **Verify Boss** (verifier route, sonnet / medium), never the agent that made the change, runs the frozen
   metric and the regression gate. A run over its time limit is stopped by its exact PID and counts as a
   failure.
4. **Keep** only when the metric moves past the measured noise and the gate is green. Otherwise revert with
   `git revert --no-edit <commit>`: history keeps the attempt, nothing uncommitted is discarded.
5. **Simplicity counts.** A tiny gain that adds tangled code is not worth keeping; removing code with an equal
   or better number is a win. Correctness and simplicity outrank the number.
6. **Crash.** A trivial cause (typo, missing import) gets one fix and a re-run. Otherwise log it as crash and
   move on.
7. **Log the row** whether kept or reverted.

Do not ask "shall I continue?" inside the budget; the owner set the budget. On a stall (several reverts in a
row), pivot: combine near-misses, re-read the code, try a more radical change, or try removing things.

## Stop rules
Stop when the target and floor are met, the round or time budget is used, the usage guard pauses, or the
remaining ideas are marginal. Never relax the target to meet it. Unlike the upstream loop, this one never runs
"forever": it ends at its budget and reports.

## Report
The metric and target, baseline to final with the delta, rounds run (kept, reverted, crashed), each kept
commit on one line, the decision-log path, the spread of the measurement, and the best untried idea. The
branch stays local: merging is the Lead's integration step, and pushing is owner-only.

## Pitfalls
- A number that improved because the harness did less work. Check the work count on every run.
- Several changes in one round: the verdict cannot say which one helped.
- The changing agent measuring its own change: always a different agent on the verifier route.
- A single run as the measurement: noise reads as a win. Use the median of N and compare to the spread.
- A machine-dependent metric (CPU load from other lanes) moving for reasons outside the change: note the load,
  and re-run the baseline when it shifts.

## Provenance
Rewritten in Forge words (ideas and structure adapted; no sentence copied verbatim). Fetched read-only with
`gh api` on 2026-11-05, scanned for hidden Unicode (clean), treated as untrusted data.

| Source | Path | Pinned SHA | Licence | Taken | Excluded |
|---|---|---|---|---|---|
| karpathy/autoresearch | `program.md`, `README.md` | 228791fb499afffb54b46200aca536f79142f117 | MIT stated in the README (no LICENSE file and no licence in the GitHub API at this SHA) | the loop: fixed metric harness that is never edited, one editable scope, fresh branch per run, baseline first, results log outside git, keep or discard, simplicity criterion, crash handling, run timeout | `prepare.py`, `train.py`, `analysis.ipynb`, the uv and GPU setup, the curl install line, "never stop", `git reset` as rollback |
| cursor/plugins (pstack, Lauren Tan) | `harness/pstack/claude-code/skills/poteto-mode/playbooks/hillclimb.md` | bb68f2365eceafa0cb2d253112f675acf5f144cc | MIT | ground the case first, a stop predicate with a target and an attempt floor, prove harness sensitivity then freeze it, work and error counts, median of N, decision log columns, mechanism-based hypotheses, parallel hypotheses in separate worktrees, push past the first plateau, never relax the predicate | the model slugs, the Opening a PR step, the wake mechanism |
| olelehmann1337/autoresearch-skill | `SKILL.md` | 5860fa717f44c85c80647d673f6f3c335facfcf2 | none found | idea only: the loop applied to skills (handled in `forge-skill-testing` Part 3) | all text, the live dashboard, the CDN chart library, the `open` command |
| alchaincyf/darwin-skill | `README_EN.md` | 8a8b66258e3c45d6ae4aea39719468c6428fcb0a | MIT | idea only: the editing agent never scores its own change; revert instead of reset | its scripts and install line |

MIT notice: "Permission is hereby granted, free of charge, to any person obtaining a copy of this software ...
The above copyright notice and this permission notice shall be included in all copies or substantial portions of
the Software. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND." Copyright (c) 2026 Lauren Tan and
(c) 2026 alchaincyf, from each LICENSE at the pinned SHA; the karpathy holder could not be read (no LICENSE file).
