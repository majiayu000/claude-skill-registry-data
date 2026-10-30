---
name: breath-of-fire
description: Zuko's breath of fire for performance work. Use for slowness, high latency, memory growth, CPU spin, bundle size, cloud cost, "make this faster", or the old perf-issue playbook. Captures a baseline trace, finds the real limit, fixes the cheapest thing that meets the target, and reports a number it can explain.
---

# Zuko's breath of fire

Zuko's fire was wild until Iroh taught him that real power comes from the breath. Performance work is the same. Rage at the code and you burn things down. Breathe, measure, and the heat goes exactly where you aim it.

You own the measurement story. Plan, review, and verify the numbers. Tie every fix to a measurement. Never read source in place of measuring.

On Codex, read [avatar-mode/references/codex.md](../avatar-mode/references/codex.md) for tool equivalents.

## Steps

1. **Set the target.** Name the metric, the workload, and the number that counts as done ("p95 under 200 ms on the checkout request with 1k items"). No target means no stopping point.
2. **Capture the baseline.** Run the real workload on the surface where it is slow, through the project's verification skill (generate one with `vital-signs`) or Claude Code's `run` skill. Use a realistic build (release mode, production-like data) and repeat enough times to see the spread. Save the raw artifact (trace, profile, or timing output) to a path you will cite.
3. **Vet the number with `steady-flame`.** Do this for the baseline and for every number after it. Check that it measures the work you think, that the variance is small next to the change you expect, and that the build, data, and machine stayed the same between runs.
4. **Find the limit.** Use `seismic-sense` to ground your hypotheses in how the code actually runs. Then profile, trace, or instrument to see where time or memory goes. Name the bottleneck with evidence. Never claim a performance ceiling you have not run.
5. **Work the mantras in order, cheapest first.** Stop at the first one that meets the target.
   1. Do not do it at all. Stop work whose result nothing uses, rather than making it cheaper.
   2. Do it once, not again (cache, memoize, dedupe).
   3. Do less of it (batch, paginate, narrow the query).
   4. Do it later (lazy, deferred).
   5. Do it where no one waits (background, precompute).
   6. Do it concurrently.
   7. Do it cheaper (a better algorithm or data structure).
6. **Plan the fix from the trace.** If the fix crosses a function boundary, run `war-room` first. When the top-level session runs this skill, dispatch the implementation to `team-avatar:zuko` on Zuko's model from the avatar-setup sheet, with an effort level that fits the job, then review the diff yourself. When you are already a dispatched character, implement it yourself.
7. **One change per measurement.** Change one thing, capture a post-fix artifact with the same harness, and keep the change only if the number moves past the noise. Revert changes that do not pay. Verify each attempt before you try the next (Sequence Work into Verifiable Units, Fire in `four-elements`).
8. **Parse and compare the artifacts.** Load the before and after artifacts into something you can query (JSON into sqlite, or a plain diff of the reduced output). Compare them directly. "Inconclusive" or a measurement on the wrong surface is not a pass. Flag it.
9. **Explain the result.** Report baseline, after, delta, and spread. Say why the number moved, in terms of the bottleneck from step 4. If you cannot explain it, it is not done (Explain the Number, Earth in `four-elements`).
10. **Cite the measurement in the PR** and hand to `yip-yip`.

## Where else to go

- Sustained improvement of one metric against a target, over many attempts, is `dragon-dance`, not this one-off fix.
- A symptom you cannot yet place (a leak, an idle CPU spin, a handed-over profile) goes to `ember-trace` first for a diagnosis.
- A choice between libraries, configs, or designs on performance goes through `steady-flame` before anyone picks a winner.

## Rules

- A number without its workload, build, and spread is not a result.
- Correctness first. A faster wrong answer is a bug (`healing-water`).
- Keep the benchmark script. It is the lever the next engineer reruns.
- Ship the fix. Do not stop to ask whether an unstated detail matters, such as how many times a callback runs. Read the callers and tests instead. If nothing observes that detail, make the change, pin the behavior that is observed with a test, and name the detail you changed in the reply so the user can push back. Hold back only when a caller or test truly depends on it (Never Block on the Human, Fire in `four-elements`).

## Reply

Baseline number, post-fix number, delta, and the artifact path.
