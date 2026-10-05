---
name: diagnose
description: Evidence-led diagnosis for hard bugs and performance regressions, using the full reproduce → minimise → hypothesise → instrument → test → fix → prevent loop when possible and a bounded, non-mutating assessment when reproduction is unsafe, unavailable, production-only, or outside the user's authority. Use when the user asks to diagnose or debug a failure or regression; do not broaden an assessment-only request into implementation.
---

# Diagnose

A discipline for hard bugs. Prefer the full loop and skip phases only when the
selected mode or available evidence justifies it.

When exploring the codebase, use the project's domain glossary to get a clear mental model of the relevant modules, and check ADRs in the area you're touching.

Example: [intermittent checkout total regression](examples/intermittent-checkout-total.md).

## Select The Mode

Use **Full Diagnosis Mode** when the failure can be exercised safely and the
user has authorized changes needed to test and fix it. Follow the complete
reproduce → minimise → hypothesise → instrument → test → fix → prevent loop.

Use **Bounded Diagnosis Mode** when reproduction is unsafe, unavailable,
non-reproducible, production-only, or the user authorized read-only analysis
only. In this mode:

- inspect available code, configuration, logs, traces, tests, and history
  without mutating the target system or repository
- separate **observed evidence** from **inference / hypotheses**
- give each conclusion a confidence level and state its evidence basis
- name the exact experiment, artifact, access, or runtime observation still
  needed to verify each material hypothesis
- stop and report when stronger proof requires a mutation, production action,
  unavailable environment, or authority the user did not grant
- never claim reproduction, a confirmed root cause, a verified fix, or GREEN
  validation unless it was actually observed

Bounded mode produces a diagnosis report and verification plan, not an
implementation. If the user asked only to assess, do not patch, instrument, or
fix; request expanded authority only when it is necessary to continue.

Phase 0 applies to both modes and is read-only by default. Phases 1–6 define
Full Diagnosis Mode. Do not enter them from bounded mode unless the missing
evidence and authority become available.

## Phase 0 — Establish runtime visibility

Before reasoning about a live failure, establish what runtime evidence can be
observed under the user's authority. Treat repository code and configuration as
static evidence, never as proof of what the current running instance loaded or
executed.

1. Record the read-only evidence boundary and separate it from any mutation
   such as restarting, replaying traffic, changing state, or adding
   instrumentation. Do not perform a mutation without matching authorization.
2. Inventory only available, authorized sensors: processes and services,
   ports or sockets, targeted logs, HTTP or health endpoints, browser/HAR
   evidence, database audit evidence, container/orchestrator state, metrics,
   and traces.
3. Identify the observed runtime using PID or workload identity, `start_time`,
   build/commit/version, and a redacted config fingerprint where available.
4. Correlate observations with explicit time zone and timestamps plus available
   `run_id`, `request_id`, or `trace_id` values.
5. Prove freshness: confirm the evidence belongs to the current instance and
   time window. A restart claim is not evidence that an old or zombie process
   stopped listening, that a replacement started, or that stale/old logs belong
   to the replacement.
6. Preserve a minimal redacted evidence bundle and classify every visibility
   gap as `unavailable`, `unauthorized`, or `unsupported`.

Read [runtime-evidence-acquisition.md](references/runtime-evidence-acquisition.md)
when the diagnosis depends on a running process, service, deployed build,
restart, live request, or production observation. Keep the selected mode's
authority boundary unchanged after reading it.

## Phase 1 — Build a feedback loop

**This is the skill.** Everything else is mechanical. If you have a fast, deterministic, agent-runnable pass/fail signal for the bug, you will find the cause — bisection, hypothesis-testing, and instrumentation all just consume that signal. If you don't have one, no amount of staring at code will save you.

Spend disproportionate effort here. **Be aggressive. Be creative. Refuse to give up.**

### Ways to construct one — try them in roughly this order

1. **Failing test** at whatever seam reaches the bug — unit, integration, e2e.
2. **Curl / HTTP script** against a running dev server.
3. **CLI invocation** with a fixture input, diffing stdout against a known-good snapshot.
4. **Headless browser script** (Playwright / Puppeteer) — drives the UI, asserts on DOM/console/network.
5. **Replay a captured trace.** Save a real network request / payload / event log to disk; replay it through the code path in isolation.
6. **Throwaway harness.** Spin up a minimal subset of the system (one service, mocked deps) that exercises the bug code path with a single function call.
7. **Property / fuzz loop.** If the bug is "sometimes wrong output", run 1000 random inputs and look for the failure mode.
8. **Bisection harness.** If the bug appeared between two known states (commit, dataset, version), automate "boot at state X, check, repeat" so you can `git bisect run` it.
9. **Differential loop.** Run the same input through old-version vs new-version (or two configs) and diff outputs.
10. **HITL bash script.** Last resort. If a human must click, drive _them_ with `scripts/hitl-loop.template.sh` so the loop is still structured. Captured output feeds back to you.

Build the right feedback loop, and the bug is 90% fixed.

### Iterate on the loop itself

Treat the loop as a product. Once you have _a_ loop, ask:

- Can I make it faster? (Cache setup, skip unrelated init, narrow the test scope.)
- Can I make the signal sharper? (Assert on the specific symptom, not "didn't crash".)
- Can I make it more deterministic? (Pin time, seed RNG, isolate filesystem, freeze network.)

A 30-second flaky loop is barely better than no loop. A 2-second deterministic loop is a debugging superpower.

### Non-deterministic bugs

The goal is not a clean repro but a **higher reproduction rate**. Loop the trigger 100×, parallelise, add stress, narrow timing windows, inject sleeps. A 50%-flake bug is debuggable; 1% is not — keep raising the rate until it's debuggable.

### When you genuinely cannot build a loop in Full Diagnosis Mode

Stop the full loop and say so explicitly. List what you tried. Ask the user for:
(a) access to whatever environment reproduces it, (b) a captured artifact (HAR
file, log dump, core dump, screen recording with timestamps), or (c) permission
to add temporary production instrumentation. Do **not** proceed to a verified
fix without a loop. If bounded mode applies, report ranked hypotheses under its
evidence and confidence rules instead.

Do not proceed to Phase 2 in full mode until you have a loop you believe in.

## Phase 2 — Reproduce + Minimise

Run the loop. Watch the bug appear.

Confirm:

- [ ] The loop produces the failure mode the **user** described — not a different failure that happens to be nearby. Wrong bug = wrong fix.
- [ ] The failure is reproducible across multiple runs (or, for non-deterministic bugs, reproducible at a high enough rate to debug against).
- [ ] You have captured the exact symptom (error message, wrong output, slow timing) so later phases can verify the fix actually addresses it.

Do not proceed until you reproduce the bug.

Minimise the reproducer while preserving the exact symptom. Remove unrelated
inputs, services, timing, and state one at a time; rerun the loop after each
reduction. Keep the original scenario so the eventual fix can be verified
against both the minimal case and the user's real failure.

## Phase 3 — Hypothesise

Generate **3–5 ranked hypotheses** before testing any of them. Single-hypothesis generation anchors on the first plausible idea.

Each hypothesis must be **falsifiable**: state the prediction it makes.

> Format: "If <X> is the cause, then <changing Y> will make the bug disappear / <changing Z> will make it worse."

If you cannot state the prediction, the hypothesis is a vibe — discard or sharpen it.

**Show the ranked list to the user before testing.** They often have domain knowledge that re-ranks instantly ("we just deployed a change to #3"), or know hypotheses they've already ruled out. Cheap checkpoint, big time saver. Don't block on it — proceed with your ranking if the user is AFK.

## Phase 4 — Instrument + Test Hypotheses

Each probe must map to a specific prediction from Phase 3. **Change one variable at a time.**

Run each probe and record whether the observed result supports or falsifies its
hypothesis. Do not promote a plausible explanation to root cause from code
inspection alone.

Tool preference:

1. **Debugger / REPL inspection** if the env supports it. One breakpoint beats ten logs.
2. **Targeted logs** at the boundaries that distinguish hypotheses.
3. Never "log everything and grep".

**Tag every debug log** with a unique prefix, e.g. `[DEBUG-a4f2]`. Cleanup at the end becomes a single grep. Untagged logs survive; tagged logs die.

**Perf branch.** For performance regressions, logs are usually wrong. Instead: establish a baseline measurement (timing harness, `performance.now()`, profiler, query plan), then bisect. Measure first, fix second.

## Phase 5 — Regression Test + Fix

Write the regression test **before the fix** — but only if there is a **correct seam** for it.

A correct seam is one where the test exercises the **real bug pattern** as it occurs at the call site. If the only available seam is too shallow (single-caller test when the bug needs multiple callers, unit test that can't replicate the chain that triggered the bug), a regression test there gives false confidence.

**If no correct seam exists, that itself is the finding.** Note it. The codebase architecture is preventing the bug from being locked down. Flag this for the next phase.

If a correct seam exists:

1. Turn the minimised repro into a failing test at that seam.
2. Watch it fail.
3. Apply the fix.
4. Watch it pass.
5. Re-run the Phase 1 feedback loop against the original (un-minimised) scenario.

## Phase 6 — Cleanup + Prevent

Required before declaring done:

- [ ] Original repro no longer reproduces (re-run the Phase 1 loop)
- [ ] Regression test passes (or absence of seam is documented)
- [ ] All `[DEBUG-...]` instrumentation removed (`grep` the prefix)
- [ ] Throwaway prototypes deleted (or moved to a clearly-marked debug location)
- [ ] The hypothesis that turned out correct is stated in the commit / PR message — so the next debugger learns

**Then ask: what would have prevented this bug?** If the answer involves architectural change (no good test seam, tangled callers, hidden coupling) hand off to the `architecture-review` skill with the specifics. Make the recommendation **after** the fix is in, not before — you have more information now than when you started.
