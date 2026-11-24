---
name: improve-worker
description: methodology for iterative improve loop workers.
version: 1.0.0
---

## Mindset

- **Correctness first, then efficiency** — never sacrifice correctness for speed. Verify correctness after every change.
- **Review existing code critically** — before writing any new code, audit the current implementation with a strict eye. Question every abstraction, every redundant operation, every boundary. Understanding what's suboptimal comes before proposing changes.
- **Zero progress is acceptable** — most optimization ideas will not pan out. An iteration that concludes "no viable improvement found" after rigorous analysis is a valid outcome. Do not force changes just to show progress. Record what was tried and the metrics result. No need to guess why it failed — the next iteration will read the record and think for itself.

## Research

When out of ideas for the next optimization, **search the web** for techniques used in similar workloads.

Rules:
- **Use established, trusted references** — prefer well-known, maintained libraries and official documentation as pattern references. Do NOT introduce unvetted third-party dependencies without explicit approval from the domain skill.
- **Learn the technique, implement it yourself** — the purpose of web research is to discover *approaches*, not to copy code.
- **Cite what you found** — in the iteration report, note what you searched for and any useful references discovered, so future iterations have context.

## Optimization Workflow: Profile First

Before writing any optimization code, follow this sequence:

1. **Collect a baseline measurement** — run a profiler or benchmark appropriate to the domain. Get a representative profile of the current state.
   Use repeated measurements with sufficient warmup before treating a benchmark as evidence.
2. **Read the data** — identify where time is spent: which operations, which phases.
3. **Compute efficiency** — how close is current performance to the theoretical limit? This tells you how much headroom exists.
4. **Identify the bottleneck** — is the system compute-bound, memory-bound, I/O-bound, or communication-bound?
5. **Target the bottleneck** — only then choose what to optimize. Optimizing a non-bottleneck wastes an iteration.

Do NOT guess what to optimize based on code reading alone. Measurement is the source of truth.

## Iteration Discipline

- **One change each time** — make only one logical change. Multiple unrelated changes make it impossible to attribute regressions.
- Record a failed approach and move on; revisit it only with new evidence.
- **Never loosen tests or tolerances** — tests exist to catch regressions. Weakening them is not an optimization. Fix the implementation, not the tests.
- Keep and run tests for live functions; deleting them hides regressions.
- **Never modify ground truth** — if a reference implementation exists, it is read-only. Do not alter it to make your implementation match.
- **Verify on real infrastructure** — complete the verification step on the target infrastructure before concluding the iteration. An iteration without verified results is a wasted iteration; the next worker will re-do the same work.
- **Only revert changes that make tip worse.** Revert regressions, broken tests, slower experiments, and scope cuts that leave the branch worse than before. Keep partial progress, completed milestones, and non-breaking refactors because they compose into the final deliverable. Tip must always stay releasable. Cleanup-only iters (dead code, readability) are valid output; iter may end with no commit.
- **Cleanup tasks must not increase LOC.**
- **Report compute cost** — every iteration report must summarize actual wall-clock cost for each tested configuration separately so the orchestrator can decide cost/benefit.
- **Scope changes need user approval, not worker judgement** — if measured throughput projects a runtime significantly above the task's stated budget, or if you encounter any obstacle that would require narrowing the deliverable (skipping slices, subsampling, dropping horizons, adding a default CLI flag that reduces work, etc.), do NOT silently trim scope. These are scope changes — they need the user to decide, not the worker. Surface the situation with concrete numbers (e.g. `observed 180 samples/s × 2.3M rows → projected 3h, task budget said 5-20 min`) and wait for the user's decision before proceeding. "Budget overshoot" is a signal to escalate to the user, not to redefine the deliverable.
