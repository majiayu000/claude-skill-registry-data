---
name: debug
description: "Use when something is broken, throwing, failing, flaky or slow, a test fails unexpectedly, the user says \"debug\" or \"diagnose\", or a fix didn't work."
license: MIT
metadata:
  reviewed: "2026-10-18"
  sources: "mattpocock/skills diagnosing-bugs, diagnose; obra/superpowers 7.0.0 skills/systematic-debugging (+ root-cause-tracing.md, condition-based-waiting.md, defense-in-depth.md, find-polluter.sh); cursor/plugins pstack 0.15.25 principle-fix-root-causes, principle-attack-the-premise, poteto-mode playbooks/bug-fix, playbooks/perf-issue; garrytan/gstack investigate; MCT (local) skills/debugging-loop"
---

# Debug

The feedback loop is the skill. With a tight signal that goes red on *this* bug, bisection, hypotheses and instrumentation just consume it. Without one, reading code builds theories, not fixes. Spend disproportionate effort on phase 1.

Redact secrets in every command, output and artifact you show (`<REDACTED>`). Build loops on environment variables so credentials stay out of the transcript.

## 1. Build a red loop

Ways to get one, roughly in this order:
1. A failing test at whatever seam reaches the bug (unit, integration, e2e).
2. A curl or HTTP script against the running dev server.
3. A CLI run on a fixture, diffed against known-good output.
4. A headless browser script asserting on DOM, console or network.
5. A replay of a captured payload, request or event log through the code path.
6. A throwaway harness: the smallest slice of the system that hits the path with one call.
7. A property or fuzz loop for "sometimes wrong" output.
8. A bisection harness between a good and a bad state (`git bisect run <loop>`).
9. A differential run: same input through old vs. new, or two configs, diffed.
10. A human-in-the-loop script, last: a bash script that prints each step for the user and reads their observation back.

**Tighten it.** Faster (cache setup, narrow scope), sharper (assert the exact symptom, not "didn't crash"), deterministic (pin time, seed randomness, isolate filesystem and network).

**Flaky bugs**: raise the reproduction rate until it's debuggable (loop the trigger 100 times, parallelize, add load, narrow the timing window). For tests that guess at timing, read `references/condition-based-waiting.md`. For state that one test leaks into others, bisect with `scripts/find-polluter.sh`.

**No loop possible**: say so, list what you tried, and ask for access to an environment that reproduces it, a captured artifact (HAR, log dump, recording with timestamps), or permission to add temporary instrumentation.

Done when: you can name one command, already run, with its output shown, that is red on the user's exact symptom, gives the same verdict every run, finishes in seconds, and runs unattended.

## 2. Reproduce and minimise

Run the loop and confirm it's the user's failure, not a neighbor that happens to fail nearby. Capture the exact symptom (message, wrong value, timing) so the fix can be checked against it. Read the whole error and stack trace. Check what changed: `git log --oneline -20 -- <files>`, the diff, dependencies, config, environment. Find working code that does something similar and list every difference.

Then cut inputs, callers, config and steps one at a time, re-running after each cut.

Done when: every remaining element is load-bearing; removing any one turns the loop green.

## 3. Hypothesise

Write 3–5 ranked hypotheses before testing any; a single hypothesis anchors on the first plausible idea. Each states its prediction: "If X is the cause, changing Y makes it disappear and changing Z makes it worse." A hypothesis without a prediction is a hunch; sharpen it or drop it.

Common shapes: race on shared state (intermittent), null propagating from an optional, partial update corrupting state, integration boundary (timeout, unexpected response), config drift between environments, stale cache, persisted state that only bites after a restart (config, lock files, serialized state).

Show the ranked list in one line each; the user may re-rank it instantly. Continue with your ranking without waiting.

Done when: every hypothesis has a prediction that one probe can test.

## 4. Instrument

One probe per prediction, one variable at a time. Prefer a debugger or REPL; otherwise targeted logs at the boundaries that separate the hypotheses. Tag every temporary log with one prefix, e.g. `[DEBUG-a4f2]`, so cleanup is one grep.

- Across components (CI → build → deploy, API → service → DB): log what enters and leaves each boundary once to find the layer that breaks.
- Deep in a call stack: trace the bad value backward to where it originated. Read `references/root-cause-tracing.md`.

Done when: one hypothesis survives with runtime evidence and the others are ruled out.

## 5. Fix at the root

The root is the first place the system did something it shouldn't. Ask whether the state that triggered the symptom is legitimate. If it is, the code that broke on it is the root: handle the state there. If it isn't, a guard where it broke hides the bug, so find what produced the state. Guards, retries, swallowed errors and clamped values are where bugs usually hide.

Fix in the shared function that every caller routes through, not at the one call site that surfaced it. Grep for the same pattern and fix every instance.

**Regression test first, at a correct seam**, one that exercises the real bug pattern as it happens at the call site. Watch it fail, apply the fix, watch it pass, then re-run the original, un-minimised loop. If no correct seam exists, that is a finding: record it and suggest the `architecture` skill.

- Add a regression test where a clean seam exists. Otherwise the phase-1 loop can serve as the regression check; say why a test was impractical.
- If bad data could re-enter through other paths, add validation at each layer it crosses. Read `references/defense-in-depth.md`.
- Truly environmental or external causes get handling (retry, timeout, a clear error) plus a signal for next time, and only after phases 1–4 point there.

Done when: the regression test (or the loop) went red before the fix and green after it, this turn.

## 6. Clean up and report

- [ ] The original loop is green.
- [ ] The regression test passes, or the missing seam is recorded.
- [ ] `grep -rn "DEBUG-a4f2" .` finds nothing.
- [ ] Throwaway harnesses are deleted or moved to a clearly marked debug location.

Report the symptom, the root cause (the hypothesis that survived), the fix with `file:line`, and the red-then-green output. If the deciding fact took a deep dig, propose the cheap, always-on signal (a log line, an assertion, a clearer error) that would have shown it at first look.

## Perf branch

Logs mislead for performance. Measure a baseline first (timing harness, profiler, query plan, trace), then bisect against it. Try fixes cheapest first, and stop when the target is met: don't do the work at all; don't do it twice (cache); do less; do it later; do it concurrently; do it cheaper. Before trusting a number, explain it: what limits it, and does it measure the work you think it does? Report baseline, after, delta, and where the artifact lives.
