---
name: "diagnose"
description: "Gated diagnosis loop for hard bugs and performance regressions. Build a tight red-capable feedback loop first, reproduce and minimise, rank falsifiable hypotheses, instrument one variable at a time, then fix with a regression test. Use when the user says diagnose or debug this, or reports something broken, throwing, failing, hanging, or slow."
---

# Diagnose

A discipline for hard bugs. The phases are gates, not suggestions. Skip one
only with an explicit reason.

**You own this.** Delegate investigation and the fix to subagents if it helps,
but stay in the lead and review every diff yourself.

**Be scientific.** Every shipped line traces to runtime evidence. A
belt-and-suspenders change that "might help" is an untested hypothesis, not a
fix, and it does not ship. When evidence refutes a hypothesis, revert what that
hypothesis motivated. The smallest change the evidence justifies ships, nothing
more. This is the **fix-root-causes** principle
(`principles/fix-root-causes.md`) in operation.

When exploring the codebase, read `CONTEXT.md` if it exists, and check ADRs in
the area you are touching. `get_architecture` and `trace_path` from
`codebase-memory` beat grepping for the call chain when the repo is indexed.

## Redact

This skill has you show commands, outputs, and captured artifacts. **Redact
every secret first**: write `<REDACTED>` in its place. Build loops against env
vars so the credential stays in the environment rather than in what you show.
Captured artifacts carry auth headers; quote only the lines that carry signal.

If the redacted output is not enough to diagnose the bug, say so and ask.

## Phase 1: Build a feedback loop

**This is the skill.** Everything else is mechanical. If you have a **tight**
pass/fail signal that goes red on *this* bug, you will find the cause;
bisection, hypothesis-testing, and instrumentation all just consume it. Without
one, no amount of staring at code will save you.

Spend disproportionate effort here. **Be aggressive. Be creative. Refuse to
give up.**

**Drive it yourself.** Reproduce on the real surface rather than handing the
reproduction back to the user. A debug protocol that says "ask the user to
try X" does not override this; you drive the instrumented runtime. Ask only
with a stated, specific reason the surface cannot be reached from here, and
only after driving it as far as it goes. If it will not reproduce directly,
force it: synthesize the trigger, tighten conditions, instrument until it
fires. A bug you cannot reproduce is a bug you cannot prove fixed.

### Ways to construct one, in roughly this order

1. **Failing test** at whatever seam reaches the bug: unit, integration, e2e.
2. **Curl / HTTP script** against a running dev server.
3. **CLI invocation** with a fixture input, diffing stdout against a known-good snapshot.
4. **Headless browser script** driving the UI and asserting on DOM, console, or network. The `claude-in-chrome` skill covers this surface.
5. **Replay a captured trace.** Save a real request, payload, or event log to disk; replay it through the code path in isolation.
6. **Throwaway harness.** A minimal subset of the system (one service, mocked deps) that exercises the bug path in one function call.
7. **Property / fuzz loop.** For "sometimes wrong output", run 1000 random inputs and look for the failure mode.
8. **Bisection harness.** If it appeared between two known states, automate "boot at state X, check, repeat" so `git bisect run` can consume it.
9. **Differential loop.** Same input through old-version vs new-version, or two configs, and diff.
10. **HITL bash script.** Last resort. If a human must click, drive *them* with [scripts/hitl-loop.template.sh](scripts/hitl-loop.template.sh) so the loop stays structured and its output feeds back to you.

Build the right feedback loop and the bug is 90% fixed.

### Tighten it

Treat the loop as a product. Once you have *a* loop:

- Faster? Cache setup, skip unrelated init, narrow the scope.
- Sharper signal? Assert the specific symptom, not "didn't crash".
- More deterministic? Pin time, seed RNG, isolate the filesystem, freeze the network.

A 30-second flaky loop is barely better than none. A 2-second deterministic one
is a superpower.

### Non-deterministic bugs

The goal is not a clean repro but a **higher reproduction rate**. Loop the
trigger 100×, parallelise, add stress, narrow timing windows, inject sleeps. A
50%-flake bug is debuggable; 1% is not. Keep raising the rate until it is.

### When you genuinely cannot build a loop

Stop and say so. List what you tried. Ask for one of: access to an environment
that reproduces it, a redacted captured artifact (HAR, log dump, core dump,
screen recording with timestamps), or permission to add temporary production
instrumentation. **Do not proceed to hypothesise without a loop.**

### Gate: a tight loop that goes red

Phase 1 is done when you can name **one command** you have **already run at
least once** (show the invocation and its redacted output), and that is:

- [ ] **Red-capable.** Drives the actual bug path and asserts the **user's exact symptom**. Not "runs without erroring": it must be able to catch *this* bug and go green once fixed.
- [ ] **Deterministic.** Same verdict every run, or a pinned high reproduction rate.
- [ ] **Fast.** Seconds, not minutes.
- [ ] **Agent-runnable.** You can run it unattended.

If you catch yourself reading code to build a theory before this command
exists, **stop**. Jumping to a hypothesis is the exact failure this skill
prevents. No red-capable command, no Phase 2.

## Phase 2: Reproduce and minimise

Run the loop. Watch it go red.

- [ ] It produces the failure the **user** described, not a nearby one. Wrong bug, wrong fix.
- [ ] Reproducible across runs, or at a high enough rate to debug against.
- [ ] The exact symptom is captured, so later phases can prove the fix addressed it.

**Minimise.** Shrink to the smallest scenario that still goes red. Cut inputs,
callers, config, data, and steps **one at a time**, re-running after each cut.
Done when every remaining element is load-bearing: removing any one makes it go
green.

This is not busywork. A minimal repro shrinks the hypothesis space in Phase 3
and becomes the clean regression test in Phase 5.

## Phase 3: Hypothesise

Generate **3 to 5 ranked hypotheses before testing any of them.** Generating
one at a time anchors you on the first plausible idea.

Each must be **falsifiable**, stated as a prediction:

> "If X is the cause, then changing Y makes the bug disappear / changing Z makes it worse."

If you cannot state the prediction, it is a vibe. Discard or sharpen it.

Seed the list from the **how** skill over the affected subsystem and the
**why** skill for regression history. Something that worked last month and
fails now has a commit behind it.

**Show the ranked list before testing.** The user often re-ranks it instantly
("we just deployed a change to #3") or names ones already ruled out. Cheap
checkpoint, big saving. Don't block on it: proceed with your ranking if they
are away.

## Phase 4: Instrument

Each probe maps to a specific prediction from Phase 3. **Change one variable at
a time.**

1. **Debugger or REPL** if the environment supports it. One breakpoint beats ten logs.
2. **Targeted logs** at the boundaries that distinguish hypotheses.
3. Never "log everything and grep".

**Tag every debug log** with a unique prefix, `[DEBUG-a4f2]`. Cleanup becomes
one grep. Untagged logs survive forever.

Binary-search the space: each pass, take the split that eliminates the most
remaining candidates. Confirm the surviving **mechanism** with runtime evidence
before designing any fix. A design grounded on a plausible-but-unconfirmed
cause can be unanimously wrong while the real cause sits one subsystem over.

**Perf branch.** For performance regressions, logs are usually the wrong tool.
Establish a baseline measurement (timing harness, profiler, query plan), then
bisect. Measure first, fix second, and tie every change to a measurement.

## Phase 5: Fix and regression test

Write the regression test **before the fix**, but only if there is a **correct
seam** for it.

A correct seam exercises the **real bug pattern** as it occurs at the call
site. If the only available seam is too shallow (a single-caller test when the
bug needs multiple callers, a unit test that cannot replicate the triggering
chain), a test there gives false confidence.

**If no correct seam exists, that is itself the finding.** Note it. The
architecture is preventing the bug from being locked down.

If a correct seam exists:

1. Turn the minimised repro into a failing test there. See the **tdd** skill for the loop, including when a test is not worth writing.
2. Watch it fail.
3. Apply the smallest fix the evidence justifies. If it crosses a function boundary, run **architect** first.
4. Watch it pass.
5. Re-run the Phase 1 loop against the original, un-minimised scenario.

**Stage the commits so the failing repro lands before the fix**, so the history
tells the story. That is the **sequence-verifiable-units** principle
(`principles/sequence-verifiable-units.md`) in its canonical form.

## Phase 6: Cleanup

Required before declaring done:

- [ ] Original repro no longer reproduces. Re-run the Phase 1 loop.
- [ ] Regression test passes, or the absence of a seam is documented.
- [ ] All `[DEBUG-...]` instrumentation removed. Grep the prefix.
- [ ] Throwaway prototypes deleted, or moved somewhere clearly marked.
- [ ] The hypothesis that turned out correct is stated in the commit or PR, so the next person learns from it.

**Reply:** what was broken, the root cause, the fix, and how you verified.
Paste the failing-then-passing output verbatim. "Inconclusive" or a
wrong-surface check is not a pass; flag it as such.
