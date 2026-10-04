---
name: observability-for-scale-review
kind: skill
status: ready
provenance:
  principles:
  - P010
  - P009
  claims:
  - C01899
  - C01933
  - C00668
  - C00670
  evidence:
  - E00263
  - E00266
  - E00164
  - E00165
  source_anchors:
  - 760c81171459-c0022
  - 760c81171459-c0025
  - 8afa2d6eafa0-c0005
  authored_from_digest: b698e2d7c96f2f64f41411b24f53ec144e55fde627486c0b0cdbb87c98996be3
---

# Observability for scale review

## Purpose

Check that a scalable or highly-available design can actually be *seen* to be working. Resilience
and fault tolerance do not justify blind faith that a system is up; a fault-tolerant architecture
with no monitoring is failing silently waiting to happen. This skill reviews whether failures are
detected end-to-end and early, before they reach user-facing services.

## When to use

- A scalable or highly-available design has no end-to-end monitoring, or assumes it is "obviously" up.
- The caller is reviewing how a system's health and failures are detected.
- A team treats fault tolerance as a substitute for monitoring.

Do not invoke for a pure design question with no runtime/operational dimension.

## Procedure

1. **Challenge the blind-faith assumption.** If the argument is "it's fault tolerant, so it's fine",
   reject it: assuming an HA system is available without verifying it is unjustified.
2. **Map detection coverage end-to-end.** Trace how each tier's health is observed, from
   infrastructure up to the user-facing service. Look for tiers that emit nothing.
3. **Find the bottom-up gap.** Operations-driven, bottom-up monitoring is necessary but incomplete —
   it tends to cover the operators' immediate needs and miss the service-level view. Flag where only
   low-level signals exist.
4. **Trace failure propagation.** For a representative component failure, ask whether it would be
   caught before it propagates and degrades the facing service. If not, that is the gap to close.
5. **Recommend top-down coverage.** Add monitoring that observes the user-facing service and works
   downward, complementing bottom-up checks, so failures are caught early and localized.
6. **Tie to the scalability goal.** Frame observability as a scalability/availability characteristic:
   a system you cannot see is not reliably scalable in practice.

## Inputs

- The current monitoring/alerting coverage per tier and how a component failure surfaces today.

## Output

A review that identifies blind spots in end-to-end detection, distinguishes necessary bottom-up
monitoring from the missing top-down service view, and recommends coverage so failures are caught
before they reach users.

## Provenance

Distilled from principle(s) **P006/P007**, claims **C00419/C00453/C00470/C00471**, evidence **E00083/E00086/E00088/E00089**, anchored in the cited architecture sources (`sources/anchors/`). Source is `distillation-only`: content is paraphrased, never quoted verbatim.
