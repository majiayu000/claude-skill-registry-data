---
name: failure-forensics
shapes: [failure-forensics]
description: >
  Read the wreckage before rebuilding. Use for incident post-mortems, "what
  happens when everything goes wrong at once?", flaky or anomalous cases being
  filtered out as noise, "that's weird" moments nobody wrote down, oscillating
  or unstable feedback behavior, and designs whose only failure mode is crash.
---

# Failure Forensics

**Problem shape:** something failed (or will fail) and the evidence is being
averaged away, cleaned up, or explained by its most convenient story. The move:
treat anomalies as data, reconstruct the timeline at the right timescale, and
design the degraded state as a first-class behavior.

## Relevant geniuses

| Agent | Use when |
|---|---|
| [hamilton](../../agents/genius/hamilton.md) | overload and simultaneous failure scenarios; priority shedding by criticality; the degraded mode is undesigned; "users will never do that" |
| [mcclintock](../../agents/genius/mcclintock.md) | aggregate metrics look smooth but one specific case is weird; a class of observations is being trimmed as noise |
| [fleming](../../agents/genius/fleming.md) | anomalies keep appearing during routine work and being cleaned up; "that's weird" said and never investigated |
| [ginzburg](../../agents/genius/ginzburg.md) | reconstruct what happened from marginal traces and involuntary evidence (logs, timestamps, artifacts nobody meant to leave) |
| [braudel](../../agents/genius/braudel.md) | the incident needs three-timescale decomposition — event, cycle, structure — before a root cause is named |
| [wu](../../agents/genius/wu.md) | the failure hides under an assumption everyone considered too obvious to test |
| [maxwell](../../agents/genius/maxwell.md) | the system oscillates, overshoots, or hunts — feedback stability and gain-margin diagnosis |

## Invocation

1. Pick the best-fit agent above. If two or more fit, run
   `tools/genius-invoker.sh route "<problem>"` and take the top ranked match.
2. Load it: `tools/genius-invoker.sh invoke <agent> "<problem>"`, then read
   `agents/genius/<agent>.md` in full.
3. Apply the agent's `<workflow>` step by step and answer in its
   `<output-format>`. Reproduce before claiming a cause; classify the cause
   before proposing the fix (coding-standards §6 root-cause protocol).
4. Typical chain: ginzburg reconstructs the timeline → braudel separates
   timescales → hamilton designs the degraded state. Run via
   `tools/genius-invoker.sh compose ginzburg hamilton -- "<problem>"`.
5. If no shape above matches, use a standard team agent instead.

## Refuse when

- No reproduction and no trace evidence exist — forensics reads records, it
  does not invent narratives.
- The requested output is a fix at the throw site with no cause classification.
