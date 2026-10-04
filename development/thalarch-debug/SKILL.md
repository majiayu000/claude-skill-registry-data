---
name: thalarch-debug
description: >
  Performs causal root-cause debugging before fixes. Use for bugs, crashes, failing tests
  or builds, intermittent behavior, regressions, incorrect state, networking failures, or
  performance anomalies. Requires reproduction/evidence, a falsifiable hypothesis, minimal
  diagnostic experiments, and architecture reassessment after repeated failed hypotheses.
---

# Thalarch Debug

## Causal Debug Protocol

## Phase 1 — Reproduce and bound

Record:
- exact expected vs actual behavior;
- reproduction or failure evidence;
- frequency if intermittent;
- environment/version;
- earliest known good state when available.

## Phase 2 — Trace the causal chain

Trace backward from the symptom.

At each boundary ask:
- what entered?
- what exited?
- what state/config was assumed?
- where is the first violated contract?

Instrument boundaries rather than guessing downstream fixes.

## Phase 3 — Compare a working analogue

Find the closest known-working path and compare all meaningful differences.

Do not dismiss small differences without evidence.

## Phase 4 — Hypothesis

Write exactly one primary hypothesis:

`Cause: ...`
`Because: ...`
`Prediction if true: ...`
`Observation that disproves it: ...`

Then run the smallest experiment that separates this hypothesis from alternatives.

## Phase 5 — Fix source, prove regression

Prefer the earliest incorrect state or broken contract.

Where practical, demonstrate:
- fail before;
- pass after;
- nearby regression checks remain green.

## Breaker

After three failed hypotheses:
- stop patch accumulation;
- re-open assumptions;
- examine shared state, ownership, lifecycle, and architecture;
- use a fresh agent/context for the reassessment.
