---
name: diagnosing-bugs
description: Reproduction signals, chronology, and hypothesis testing for hard, elusive, or intermittent bugs. Use when a diagnosis needs stronger evidence than ordinary debugging provides.
---

# Diagnosing Bugs

The active harness process owns whether the work is read only, includes repair, or belongs to a performance route. This skill contributes diagnostic technique and never expands that authority.

Use this method for bugs that do not yield to a direct repair. Keep confirmed facts, falsified hypotheses, and open questions separate throughout the investigation.

## Establish the failure

Start from the exact reported outcome. Identify the affected surface, the last known good state, and the evidence that distinguishes the reported bug from nearby failures.

For a regression or incident, reconstruct the chronology before naming a root cause. Resolve the last known good and first known bad from reports, deployments, logs, issue attachments, and configuration or data changes. A confirmed cause must explain both the failure mechanism and why the failure appeared when it did. If the faulty code predates the incident, identify the later trigger or leave the cause open.

Build the tightest practical signal for that outcome. Prefer, in order:

1. A focused failing test at the real seam.
2. A request or CLI command with a fixed input and observable output.
3. A browser flow that checks the user-visible symptom.
4. A captured request, event, trace, or production artifact replayed locally.
5. A measurement harness for a performance regression.
6. Targeted logs or traces at the boundary where the outcome becomes wrong.

A full local reproduction is best, but it is not always available. Continue from exact logs, traces, runtime evidence, code paths, and historical diffs when they can falsify theories. State the proof limit. Do not turn missing reproduction into permission to guess, and do not stop while useful evidence remains available.

## Narrow the boundary

Trace the actual object, request, state transition, or timing path. Minimize the failing case when possible. Compare old and new behavior under the same input. For intermittent work, increase the reproduction rate with repeated runs, controlled timing, or recorded inputs.

Record:

1. Confirmed facts.
2. Falsified explanations.
3. Ranked open hypotheses, each with a prediction that would distinguish it.
4. The next cheapest probe that can change the ranking.

Do not present a plausible historical diff as the cause until the exact failure or direct instrumentation connects it to the outcome.

## Probe and repair

Change one variable at a time. Place instrumentation only where it separates live hypotheses. Tag temporary logs so one search removes them later. For performance work, measure before and after under the same conditions.

Fix the owning boundary rather than masking the symptom. When the request includes a repair, add a regression test only when there is a correct seam and the changed behavior is application behavior. Follow project rules for operational logging, telemetry, and one-off support changes.

## Prove the result

Re-run the original signal against the full reported scenario. A narrow test proves only its seam. A browser check proves only the observed browser flow. State what each check establishes.

Before finishing:

1. Remove temporary instrumentation and throwaway harnesses.
2. State the confirmed cause, or label the best remaining explanation as a hypothesis.
3. Report the original outcome, the verification result, and any untested boundary.
4. Record a structural prevention only when the evidence supports one.
