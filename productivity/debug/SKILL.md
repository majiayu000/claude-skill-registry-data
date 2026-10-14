---
name: debug
description: "A check fails or behavior is wrong and the cause isn't obvious — reproduce, isolate the root cause, fix narrowly, and prove it."
---

# Debug

Find the causal defect, not just a patch that hides the symptom.

- Capture a pass/fail signal for the reported behavior. Preserve the original
  scenario while shrinking a reproduction; the small case must still explain it.
  For intermittent failures, record conditions and observed frequency instead of
  imposing an arbitrary flake threshold. If reproduction is unavailable, seek
  decisive traces and name what remains unproven.
- Trace callers, state, guards, sinks and configuration. Compare known-good
  behavior and recent changes when available. Rank plausible explanations by
  what observable evidence would distinguish them, then test the most informative
  one. Change one causal variable at a time where possible.
- Keep probes identifiable. Probes and their cleanup need permission to write,
  even for files you created. An approved tool call does not widen which files
  you may change. Prefer
  existing tests, in-memory checks or focused traces over new files and noisy
  logging; ask before creating an extra file. Measure performance against a
  comparable baseline. Redact secrets before sharing commands, logs or artifacts,
  and say when redaction limits diagnosis.
- Fix the shared cause where it belongs and inspect sibling callers. Do not
  compensate separately in every path or keep retrying an unchanged theory.
  Repeated failure calls for a new hypothesis, decomposition or escalation—not a
  success verdict because an attempt budget ran out.
- Re-run the exact original signal and relevant regression checks. Assert the
  visible result, not merely that nothing threw. Inspect the real rendered/output
  surface for visual or generated-artifact bugs; synthetic checks alone leave that
  requirement unverified. If no honest test seam exists, report the design gap.

Deliver: cause, distinguishing evidence, fix and regression results, removed
probes and remaining uncertainty. Hand the uncommitted change to independent
verification. Keep a durable lesson in its existing owner only when it changes
current guidance; no mandatory debug diary.
