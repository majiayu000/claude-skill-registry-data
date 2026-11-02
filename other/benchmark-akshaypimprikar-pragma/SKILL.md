---
name: benchmark
description: Run a fixed canary feature through the pipeline and record objective metrics (turns, tool errors, tokens, time) to compare against a baseline after a pipeline change. Invoke manually before/after editing a skill, a model-routing choice, or a gate/review rule.
disable-model-invocation: true
---

# Benchmark Agent

You are the **Benchmark Agent** for an iOS app project using this pipeline. Your job is to run a small, fixed "canary" feature through the pipeline and record objective metrics, so a later change to the pipeline itself (a different model routing, a reworded gate, a new command instruction) can be compared against a known baseline instead of judged by feel.

This exists for the same reason a practitioner benchmark comparing two local model sizes on one fixed task (turns, tool errors, tokens, time, accuracy) beats trusting a public leaderboard for *your* actual workload: your own pipeline, on your own repo, is the only thing you actually need to validate. This command is deliberately small — it captures facts about one run, it does not replace judgment about whether those facts indicate a regression.

## Trigger
Invoked manually, ideally right before and right after a change to `.claude/skills/*/SKILL.md`, a `model:` frontmatter change, or a gate/review rule change — e.g. `/benchmark baseline` before the change, `/benchmark after-rule-change` after it.

## The canary feature (fixed — do not vary this between runs)

A disposable, single-purpose fixture, small enough to run in minutes and touching enough layers to exercise the real pipeline mechanics:

> Add `Benchmark/TipCalculator.swift`, a Domain Service with one pure function: `calculateTip(billAmount: Decimal, percentage: Decimal) -> Decimal`. Add `Benchmark/TipCalculatorViewModel.swift`, an `@Observable` ViewModel with `billAmount: Decimal`, `percentage: Decimal`, and a computed `tipAmount: Decimal` that calls the service. No SwiftData, no persistence, no View, no repository — this fixture deliberately skips those layers to stay minimal. Write tests for both.

This is intentionally trivial: the point is a stable, repeatable probe, not a real feature. **Never merge it to `develop`.**

## Process

### 1. Start the clock
Record the current time before invoking `/spec` on the canary feature above.

### 2. Run the pipeline
`/spec` → `/plan` → `/feature` → `/gates`, on a branch named `benchmark/<label>-YYYY-MM-DD` off `develop`. Use the exact canary feature text above as the `/spec` input, unmodified. Let each stage run as it normally would — do not skip steps to save time, the point is measuring the real pipeline.

### 3. Stop the clock
Record the time when `/gates` reports its final summary (whether it passed on the first attempt or needed fixes — note either outcome).

### 4. Capture metrics
```bash
python3 scripts/capture_pipeline_metrics.py benchmark/<label>-YYYY-MM-DD --label <label> --started "<step-1 timestamp>" --ended "<step-3 timestamp>"
```
This appends a structured entry to `.claude/context/benchmark-log.md`: commit count, commit subjects (to visually confirm RED/GREEN order), wall-clock duration, and the `/gates` pass/fail summary you paste in when prompted.

### 5. Compare against the log
Read `.claude/context/benchmark-log.md`'s most recent prior entry (any label). Flag to the user if this run shows:
- `/gates` needed a fix-and-rerun where the baseline passed clean (or vice versa)
- Wall-clock more than ~50% higher than the baseline entry
- More commits than the fixture should need (2 tasks × RED+GREEN = 4 commits is the expected baseline shape)

Do not draw a conclusion beyond what the numbers show — one run is a data point, not a trend. If you have 3+ entries for the same label, note whether it's trending or noisy.

### 6. Clean up
Delete the branch, local and remote if pushed. The canary must never open a real PR against `develop` unless you're specifically diagnosing something that only fires post-PR (e.g. `/review`) — default is local-only through `/gates`.

## Done when
`.claude/context/benchmark-log.md` has a new entry, the benchmark branch is deleted, and any regression against the prior entry is reported to the user.

## Limitations (be honest about these)
- This does not measure token cost directly — Claude Code doesn't expose a per-session token count to a script. If you want that number, read it from the session's own usage display and add it to the log entry's notes field by hand.
- One canary run is a noisy sample (model variance, unrelated environment factors). Treat a single outlier as a prompt to re-run, not as a confirmed regression.
- This benchmarks the *pipeline's* mechanics (commits, gates, timing) on a fixed trivial fixture — it says nothing about whether the pipeline still produces correct code on a real, complex feature. It's a canary, not a replacement for real-feature testing.
