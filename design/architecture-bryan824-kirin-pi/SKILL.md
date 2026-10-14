---
name: architecture
description: "When structure is the problem — improve an existing architecture without changing its goals, or rethink it from first principles when the user explicitly asks."
---

# Architecture

Choose a better system shape before designing implementation details. Keep repository
files unchanged. Write a report file only when the user requests one.

First name the posture:

- **Improve** — preserve product goals, domain language, public contracts, and accepted constraints.
- **Rethink** — challenge inherited constraints and propose a bold target only when the user explicitly asks for an overhaul.

For either posture:

- Read current docs, contracts, tests, consumers, and recent friction before judging structure.
- Separate real constraints from inertia. Public promises, persisted data, compliance, and explicit user direction are real; internal callers and stale layouts are movable.
- Judge interfaces by what callers must know versus behavior hidden behind them — everything a caller must know counts, invariants, ordering, error modes and all, not just the type signature. Depth is a property of the interface, never of the implementation: deep does not mean monolithic, and private seams are fine. Depth gives callers leverage, meaning more behavior per unit of interface they must learn, and gives maintainers locality, meaning changes and bugs concentrate in one place. Say which of the two a candidate delivers.
- Testability is evidence about a boundary, not a ban on internal tests. Exercise caller-facing behavior and use narrower seams when they expose important failures honestly. Excessive setup or mocking can indicate coupling; explain the cause before reshaping the module.
- Apply the deletion test: if removing a layer removes complexity, delete it; if complexity leaks into callers, deepen the boundary.
- A seam earns its cost through caller leverage, maintenance locality, a trust boundary or testability—not an implementation count. One adapter can isolate a real dependency; speculative variation is not a reason to add one.
- Prefer a change proven through one behavior seam. Relocated complexity is not improvement.

For **Improve**, rank evidence-backed candidates by leverage versus blast radius. Recommend one only when evidence supports a change; no worthwhile candidate is a valid result.

For **Rethink**, produce a target model, a kill list, assumptions, and falsifiers. Keep inherited pieces only when evidence says they still earn their place.

Compare alternative interfaces only when that choice matters. Lead with the recommendation and name the fragile assumption.

## Optional discovery and report mode

Use this mode when the user asks for improvement candidates before choosing a refactor.
Do not require it for an already chosen change.

1. Scope to the upcoming change or named pain point. Otherwise, inspect recent history
   for frequently changed areas, then confirm friction in current callers and tests.
   Churn alone is not evidence of a defect.
2. Present a small set of distinct candidates, or none; do not fill a quota.
   Each cites paths and a concrete caller/test trace, shows a compact before/after
   diagram, and explains what changes or disappears. Include contract/test impact,
   dependency limits, blast radius, confidence, and assumptions. Describe changed
   responsibilities, not proposed interfaces.
3. Default to a compact chat report. If the user requests HTML, create a uniquely
   named static file in the OS temp directory, outside the repository. Provide its
   absolute path.
   Use inline CSS/SVG with escaped text, no scripts or external resources.
   Check its rendering with available browser tooling; otherwise disclose that
   rendering is unverified.
4. For report-only requests, stop without an interview. Otherwise, ask which candidate
   to explore, including none, and wait. Use the host's structured question tool when
   available. Selection permits discussion, not edits. Explore only the chosen candidate.

For unresolved behavior choices, use `design` when available; otherwise ask directly.
Use `plan` only when dependencies, risk, or handoff require it.

Deliver: posture, current constraints, candidate report or recommended architecture,
what disappears, contract/test impact, risks, and next step. Stop before implementation.
