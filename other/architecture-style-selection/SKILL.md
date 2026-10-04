---
name: architecture-style-selection
kind: skill
status: ready
provenance:
  principles:
  - P037
  claims:
  - C01089
  - C01090
  evidence:
  - E00170
  - E00171
  source_anchors:
  - 8afa2d6eafa0-c0046
  authored_from_digest: 1938e3cf75a69f3c157f8b563dce1251f4bbe5f9953cfd662ced302a089bfd82
---

# Architecture style selection

## Purpose

Select an architecture style by its characteristic profile, not by default or fashion. Each style
— layered, event-driven, microkernel, microservices, space-based — carries a distinct profile of
strengths and weaknesses rated across characteristics such as agility, ease of deployment,
testability, performance, and scalability. No style is universally best; the right one is the one
whose profile matches the application's prioritized requirements.

## When to use

- The caller is choosing or comparing top-level architecture styles for a system.
- A style is proposed without reference to the qualities it must deliver.
- The caller wants a default or "modern" style applied without analysis.

Do not invoke when the style is fixed by external constraint and only within-style design remains.

## Procedure

1. **Get the ranked characteristics.** Start from the prioritized characteristics
   (`identify-architecture-characteristics`). Style selection is meaningless without knowing which
   qualities matter most.
2. **Read each candidate style's profile.** For each style under consideration, look up its
   rating across the characteristics in the style-characteristics matrix.
3. **Match profile to priorities.** Compare how each style scores on the top-ranked
   characteristics. Favor the style that is strong where the system's priorities are highest.
4. **Surface the sacrifice.** Every style trades some characteristics for others; name what the
   leading candidate is weak at and confirm those weaknesses fall on lower-priority
   characteristics. If a top priority lands on a style's weakness, that style is a poor fit
   despite its popularity.
5. **Reject the default-choice reflex.** If a style is proposed only because it is common or
   fashionable, replace that justification with a profile-to-priorities match (or a deliberate,
   stated exception).
6. **Recommend, with residual trade-off.** Recommend the best-matching style and state the
   residual consequence the caller accepts. When comparing, present a side-by-side of the styles
   on the characteristics each favors before the forces-weighted pick.

## Inputs

- The candidate architecture styles and the system's ranked architecture characteristics and
  constraints.

## Output

A style recommendation (or side-by-side comparison) justified by matching each style's
characteristic profile to the caller's prioritized requirements, with the residual trade-off
named. Never a universal "best style."

## References

- [Architecture style characteristics matrix](../../references/architecture-style-characteristics-matrix.md)
  — the styles-by-characteristics rating table this skill reads.

## Provenance

Distilled from principle(s) **P004**, claims **C00219/C00220**, evidence **E00048/E00049**, anchored in the cited architecture sources (`sources/anchors/`). Source is `distillation-only`: content is paraphrased, never quoted verbatim.
