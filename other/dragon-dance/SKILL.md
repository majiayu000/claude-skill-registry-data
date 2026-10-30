---
name: dragon-dance
description: Zuko's dragon dance for sustained, scientific improvement of one metric. Zuko and Aang learned the Dragon Dance from Ran and Shaw one form at a time, each form proven before the next. Use for hillclimb, "hillclimb this", "keep improving X until Y", or any loop of hypotheses with before-and-after measurement, a decision log, and one commit per accepted win. A one-off speedup is `breath-of-fire`.
---

# Zuko's dragon dance

Ran and Shaw did not hand Zuko and Aang the true fire all at once. The masters taught the Dragon Dance form by form, and the two learned each form in full before the next began. The fire came from the dance as a whole. Hillclimbing is the same. One change, one measurement, keep or revert, then the next form. Never stack untested changes, and never claim a win from reading code (Prove It Works, Earth in `four-elements`).

You own the metric and the experiment's integrity. Supervise and review. Dispatch the attempts. A one-off fix is `healing-water` or `breath-of-fire`. This is the loop.

On Codex, read [avatar-mode/references/codex.md](../avatar-mode/references/codex.md) for tool equivalents.

## Steps

1. **Ground the workload before choosing the metric.** Run `seismic-sense` over the target. Name the realistic workload dimensions that can move the result (data size, history, state, concurrency), and select a case that reproduces the user's complaint. If no case reproduces it, fix the repro instead of hillclimbing. Then fix one metric, the direction that counts as better, and a checkable stop predicate that pairs a target with a floor on attempts, so a lucky early win cannot end the run. "At least 50% better than baseline and at least 10 iterations" has this shape. Use the user's numbers when given. Otherwise agree on them.
2. **Build the harness, prove its sensitivity, then freeze it** (Build the Lever, Fire in `four-elements`). Run contrasting realistic workloads and confirm the target case reproduces the symptom while easier cases separate as expected. If the harness cannot tell them apart, revise the workload or the metric. Vet the harness with `steady-flame` before you freeze it, and make it print its error count and a count of the work done. Once frozen, one repeatable command emits the metric, sampled enough to clear the noise (median of N, never a single run). Record the baseline metric and a green run of the regression gate (the tests that must keep passing) before any change.
3. **Open the decision log** with `battle-map`. Keep a `decision.tsv` with one row per attempt and these columns: id, hypothesis, change, before, after, delta, tests, verdict (kept or reverted), note. Read it before each attempt. Keep it out of the tree (gitignored).
4. **Ground each hypothesis in the model from step 1.** Each one names a specific mechanism ("defer X off the boot path because it blocks first paint"), not "try memoizing something". For a performance metric, order hypotheses by the mantras in `breath-of-fire` step 5. Borrow only their order, not that step's stop rule.
5. **Loop, one hypothesis per form.**
   - When the top-level session runs this skill, dispatch each change to `team-avatar:zuko` on Zuko's model from the avatar-setup sheet, with a tight scope and an effort level that fits the job. Supervise and review the diff rather than typing it (Guard the Context Window, Fire in `four-elements`). When several independent hypotheses are live, dispatch them in parallel, each in its own git worktree, so no two writers share a checkout. When you are already a dispatched character, run the attempts yourself, one after another.
   - Measure before and after with the frozen harness, and run the regression gate.
   - Accept only when the metric moves past the noise and the gate stays green. Otherwise revert the change in full. A tweak that "might help" is not kept.
   - One commit per accepted fix. Stage only the files you changed (`git add <files>`, never `-A`). Log the row either way, kept or reverted.
   - Each iteration ends in a check before the next begins (Sequence Work into Verifiable Units, Fire in `four-elements`). If the run is unattended, borrow only the wake mechanism from `night-watch`, not its stop rule.
6. **Push past the first plateau.** On a stall (several rejects in a row), pivot category, combine near-misses, reread the source, or try something more radical before you conclude the hill is climbed. Correctness and simplicity outrank the number. Revert a win that breaks behavior, and keep a simplification that holds the number (Laziness Protocol, Air in `four-elements`).
7. **Stop when the predicate is met,** or when the remaining ideas are marginal and not worth their cost. Never relax the predicate to meet it, and never quit while cheap untried hypotheses remain. If you are stuck, say so instead of spinning.
8. **Hand to `yip-yip`** with the accepted commits stacked in the order they landed.

## Reply

The metric and the target, baseline to final with the percent delta, iterations run (kept and reverted), each accepted fix on one line, the `decision.tsv` path, and the best idea you would try next if pushed further.
