---
name: ln-diagnose
description: "Scientific debugging for bugs, flakes, failures, and performance regressions. Use when something is broken, throwing, failing, slow, nondeterministic, or when the user says diagnose/debug this. Builds a trusted repro loop, tests falsifiable hypotheses, installs a regression oracle, and routes durable findings back into ln-* planning."
argument-hint: "[bug report, failing command, error, or regression description]"
---

# Ln Diagnose

Debug by scientific method: trusted repro loop, falsifiable hypotheses, one-variable probes, regression oracle. Do not fix by inspection unless the cause is already proven.

## Input

Bug, failure, flake, or regression to diagnose: $ARGUMENTS

Orient first:

1. Read `memory/SPEC.md` if present; use its lexicon and live invariants.
2. Read `memory/PLAN.md` if present; identify the containing frontier item if one exists.
3. Read `HANDOFF.md` if present.
4. For runtime/UI failures, read the relevant project praxis doc before inspecting logs or driving browsers.

Write a 2-4 bullet orientation note: symptom, suspected seam, current feedback loop, proof standard.

## 1. Build the repro loop

This is the skill. A fast deterministic pass/fail loop makes the rest mechanical. No loop, no diagnosis.

Try, in rough order:

1. failing unit/integration/e2e test at the seam that reaches the bug
2. CLI/script with fixture input and asserted output
3. HTTP/curl script against a running server
4. browser automation asserting DOM, console, or network
5. replayed artifact: request, trace, event log, fixture, HAR
6. throwaway harness around the smallest subsystem that exercises the path
7. property/fuzz loop for intermittent wrong output
8. bisection/differential loop across commits, versions, datasets, or configs
9. structured HITL loop only when a human must observe or click

Improve the loop before moving on: faster, sharper assertion, less flake. Pin time, randomness, network, filesystem, and concurrency. For nondeterministic bugs, raise reproduction rate with repetition/stress until it is debuggable.

If no loop can be built, stop. Report what you tried and ask for access, logs, traces, fixtures, timestamped recordings, or permission for temporary instrumentation.

## 2. Reproduce the user's bug

Run the loop. Confirm it demonstrates the reported bug, not a nearby failure.

Capture:

- command/script/test used
- exact symptom: error, diff, timing, screenshot, console/network evidence
- reproduction rate for flakes
- saved replay artifact, if any

Lack of reproduction is allowed only as an explicit diagnosis result.

## 3. Rank falsifiable hypotheses

Generate 3-5 hypotheses before testing any one of them. Each hypothesis must predict an observation:

```md
If [cause] is true, then [probe/change] will make [specific observation] happen.
```

Prefer hypotheses that distinguish seams or invariants from `memory/SPEC.md`. Show the ranking to the user when they are present; proceed if they are AFK.

## 4. Probe one variable at a time

Every probe maps to one prediction. Prefer debugger/REPL inspection, then targeted boundary logs, then temporary assertions/counters.

Tag temporary instrumentation with a unique prefix like `[DEBUG-a4f2]`. Cleanup must be grep-able. Never "log everything and grep".

Performance branch: measure first. Establish a baseline timing/profiler/query-plan signal, then bisect or compare. Do not optimize before the measurement identifies the seam.

## 5. Choose the fix route

Before coding, choose the route:

- **Direct fix / `ln-build`** — cause is proven and the change stays inside a settled seam.
- **`ln-scope` or `ln-spec`** — the fix changes a seam, invariant, requirement, assumption, or frontier shape.
- **`ln-spike` or `ln-design`** — diagnosis answered one question but the fix shape remains uncertain.
- **`ln-review` / `ln-refactor`** — no correct regression seam exists, or architecture contributed to the bug.

Install the regression oracle before the fix when a correct seam exists. A correct seam reproduces the real bug pattern as it occurs at the call site. Shallow tests that cannot fail for the original bug are false confidence.

## 6. Cleanup and postmortem

Before declaring done:

- [ ] original repro loop no longer reproduces the bug, or non-repro is the diagnosis
- [ ] regression oracle exists and passes, or absence of a correct seam is documented
- [ ] all `[DEBUG-...]` instrumentation is removed
- [ ] throwaway harnesses are deleted or visibly temporary
- [ ] confirmed causal hypothesis is stated in the report / commit message

Ask: what would have prevented this bug? Route missing invariants, unclear seams, weak oracles, and bad module shapes into the appropriate `ln-*` skill.

## Canonical reconciliation

Reconcile only durable truth:

- New/retired assumption → update `memory/SPEC.md` §Assumptions.
- New seam-level invariant or oracle gap → update `memory/SPEC.md` or route to `ln-oracles`.
- Frontier status changed → update `memory/PLAN.md`.
- Local bug with no durable implication → no canonical update beyond tracked PLAN status.

Do not create `CONTEXT.md`, ADRs, or alternate planning docs. Canonical docs are `memory/SPEC.md` and `memory/PLAN.md`.

## Output

```md
## Diagnosis: [symptom]

**Repro loop:** [command/script/test and reproduction rate]
**Confirmed cause:** [one sentence]
**Evidence:** [key observations]
**Fix route:** [direct fix | ln-scope | ln-build | ln-spike | ln-review | ln-refactor]
**Regression oracle:** [test/harness or why unavailable]
**Canonical updates:** [none | specific SPEC/PLAN changes needed]
```

## Routing

After diagnosis, present these options to the user (use `tool-ask-question`):

| #   | Label            | Target       | Why |
| --- | ---------------- | ------------ | --- |
| 1   | Scope the fix    | `ln-scope`   | The fix needs a buildable card or durable seam update |
| 2   | Build the fix    | `ln-build`   | The fix is settled and ready for red-green-refactor |
| 3   | Spike deeper     | `ln-spike`   | A hard question remains after reproduction |
| 4   | Review structure | `ln-review`  | No good seam/regression oracle exists or architecture contributed |
| 5   | Back to triage   | `ln-consult` | Diagnosis changed priority or scope |

Recommended: **2** only when cause and seam are proven; otherwise **1**.

---
*Adapted from [mattpocock/skills/engineering/diagnose](https://github.com/mattpocock/skills/tree/main/skills/engineering/diagnose).*
