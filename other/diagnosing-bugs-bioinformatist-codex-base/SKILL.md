---
name: diagnosing-bugs
description: Disciplined diagnosis loop for hard bugs, regressions, flaky failures, and performance problems with unclear cause. Use for root-cause debugging after a concrete symptom exists; do not use for routine implementation or speculative cleanup.
---

# Diagnosing Bugs

Start from a concrete symptom and gather read-only evidence. A reproduction tightens hypotheses but is not a prerequisite for inspecting relevant code, history, configuration, or logs.

When exploring the codebase, read `CONTEXT.md` (if it exists) to get a clear mental model of the relevant modules, and check ADRs in the area you're touching.

## Redact

This skill has you show commands, outputs and captured artifacts. **Redact every secret first**: write `<REDACTED>` in its place. Build loops against env vars, so the credential stays in the environment rather than in what you show. Captured artifacts carry auth headers: quote only the lines that carry the signal.

If the redacted output is not enough to diagnose the bug, say so and ask the user.

## Scope

Diagnosis-only requests stop after reporting the supported cause, confidence, and next verification. Apply a fix or add a regression test only when implementation is authorized; keep changes within the approved scope.

## Phase 1: Build a feedback loop

**Prefer a tight, symptom-specific pass/fail signal when one is practical.** Scale reproduction work to the request, risk, and available environment. Read-only evidence can still support a useful diagnosis when no runnable loop is available.

Try the least invasive, highest-signal reproduction that fits the authorized scope. Stop when further experiments are disproportionate, require unavailable access, or would cross an authorization boundary; report the limitation.

### Ways to construct one, in roughly this order

1. **Failing test** at whatever seam reaches the bug: unit, integration, e2e.
2. **Curl / HTTP script** against a running dev server.
3. **CLI invocation** with a fixture input, diffing stdout against a known-good snapshot.
4. **Headless browser script** (Playwright / Puppeteer) that drives the UI and asserts on DOM/console/network.
5. **Replay an authorized captured trace.** If writes and the captured data are in scope, save a redacted request, payload, or event log and replay it through the code path in isolation.
6. **Temporary harness.** When implementation is authorized, use a minimal subset of the system that exercises the bug path without changing unrelated source or services.
7. **Property / fuzz loop.** For intermittent wrong output, use a bounded sample sized to the failure rate, cost, and risk; record the seed and observed rate.
8. **Bisection harness.** If the bug appeared between two known states (commit, dataset, version), automate "boot at state X, check, repeat" so you can `git bisect run` it.
9. **Differential loop.** Run the same input through old-version vs new-version (or two configs) and diff outputs.
10. **HITL bash script.** Last resort. If a human must click, drive _them_ with `scripts/hitl-loop.template.sh` so the loop is still structured. Captured output feeds back to you.

Build the right feedback loop, and the bug is 90% fixed.

### Tighten the loop

Treat the loop as a product. Once you have _a_ loop, **tighten** it:

- Can I make it faster? (Cache setup, skip unrelated init, narrow the test scope.)
- Can I make the signal sharper? (Assert on the specific symptom, not "didn't crash".)
- Can I make it more deterministic? (Pin time, seed RNG, isolate filesystem, freeze network.)

A 30-second flaky loop is barely better than no loop; a 2-second deterministic one is tight, a debugging superpower.

### Non-deterministic bugs

The goal is a reproduction rate high enough to distinguish hypotheses. Use a bounded number of attempts based on runtime and observed failure rate; add concurrency, stress, narrowed timing windows, or injected delays only when safe and within scope. Record both attempts and failures.

### When you genuinely cannot build a loop

Say so explicitly, list the evidence gathered and proportionate attempts made, and continue with labeled hypotheses where the evidence supports them. Ask only for missing access or a redacted artifact that is material to the diagnosis. Production instrumentation requires explicit authorization and must stay within the requested scope.

### When a runnable loop is available

Before relying on a runnable loop, name the command and run it when safe (show the invocation and its output, redacted). Prefer a loop that is:

- [ ] **Red-capable**: it drives the actual bug code path and asserts the **user's exact symptom**, so it can go red on this bug and green once fixed. Not "runs without erroring"; it must be able to _catch this specific bug_.
- [ ] **Deterministic**: same verdict every run (flaky bugs: a pinned, high reproduction rate, per above).
- [ ] **Fast**: seconds, not minutes.
- [ ] **Agent-runnable**: you can run it unattended; a human in the loop only via `scripts/hitl-loop.template.sh`.

Read-only inspection may precede a red-capable command. Do not claim reproduction or a confirmed cause until the evidence supports it.

## Phase 2: Reproduce + minimise

Run the loop. Watch it go red as the bug appears.

Confirm:

- [ ] The loop produces the failure mode the **user** described, not a different failure that happens to be nearby. Wrong bug = wrong fix.
- [ ] The failure is reproducible across multiple runs (or, for non-deterministic bugs, reproducible at a high enough rate to debug against).
- [ ] You have captured the exact symptom (error message, wrong output, slow timing) so later phases can verify the fix actually addresses it.

### Minimise

Once it's red, shrink the repro to the **smallest scenario that still goes red**. Cut inputs, callers, config, data, and steps **one at a time**, re-running the loop after each cut, and keep only what's load-bearing for the failure.

Why bother: a minimal repro shrinks the hypothesis space in Phase 3 (fewer moving parts left to suspect) and becomes the clean regression test in Phase 5.

Done when **every remaining element is load-bearing**: removing any one of them makes the loop go green.

If reproduction is possible, minimise it proportionally; otherwise continue diagnosis from the available evidence and record the limitation.

## Phase 3: Hypothesise

Generate and rank the distinct hypotheses justified by the evidence. Consider alternatives before committing to the first plausible cause, but do not invent hypotheses to meet a quota.

Each hypothesis must be **falsifiable**: state the prediction it makes.

> Format: "If <X> is the cause, then <changing Y> will make the bug disappear / <changing Z> will make it worse."

If you cannot state the prediction, the hypothesis is a vibe: discard or sharpen it.

Report the ranked hypotheses and why they differ. Run safe, in-scope read-only probes without waiting; ask the user first only when a test needs a material choice, new access, or additional authorization.

## Phase 4: Probe or instrument within scope

Each probe must map to a specific prediction from Phase 3. **Change one variable at a time.**

Tool preference:

1. **Debugger / REPL inspection** if the env supports it. One breakpoint beats ten logs.
2. **Targeted logs** at the boundaries that distinguish hypotheses.
3. Never "log everything and grep".

Add debug logging only when source changes are authorized. Tag each added log with a unique prefix such as `[DEBUG-a4f2]`, track the changed paths, and remove only that temporary instrumentation before handoff.

**Perf branch.** For performance regressions, logs are usually wrong. Instead: establish a baseline measurement (timing harness, `performance.now()`, profiler, query plan), then bisect. Measure first, fix second.

## Phase 5: Authorized fix + regression test

When implementation is authorized, write the regression test **before the fix**, but only if there is a **correct seam** for it.

A correct seam is one where the test exercises the **real bug pattern** as it occurs at the call site. If the only available seam is too shallow (single-caller test when the bug needs multiple callers, unit test that can't replicate the chain that triggered the bug), a regression test there gives false confidence.

**If no correct seam exists, that itself is the finding.** Note it. The codebase architecture is preventing the bug from being locked down. Flag this for the next phase.

If a correct seam exists:

1. Turn the minimised repro into a failing test at that seam.
2. Watch it fail.
3. Apply the fix.
4. Watch it pass.
5. Re-run the Phase 1 feedback loop against the original (un-minimised) scenario.

## Phase 6: Verify and report authorized changes

For an authorized implementation, verify proportionally before declaring done:

- [ ] The original repro no longer reproduces when a runnable loop exists
- [ ] The authorized regression test passes, or the absence of a correct seam is documented
- [ ] Temporary instrumentation added during this task is removed and its unique prefix no longer appears
- [ ] Temporary artifacts created during this task are reported and removed only when that cleanup is authorized
- [ ] The supported root cause and verification evidence are reported to the user
