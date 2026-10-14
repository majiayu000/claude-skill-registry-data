---
name: null-safety
description: "Trigger: null safety, nullability, Optional, NPE. Detect null hazards and conservative Java null-safety refactors."
license: Apache-2.0
metadata:
  author: gentle-ai
  adapted_by: andresnator
  source: gentle-ai/plan-refactor
  version: "1.0.1"
  status: testing
---

## Activation Contract
Load this skill when reviewing refactor plans for: null safety, nullability, Optional, NPE.

## Hard Rules

- Flag dereferences without clear guarantees, nullable returns, and ambiguous null semantics.
- Prefer boundary checks, NonNull annotations where used, clear defaults, or Null Object only when justified.
- Do not introduce Optional in fields, parameters, or DTOs without explicit reason.
- Preserve observable behavior; label functional changes as follow-up.
- Require evidence for every recommendation, or mark it as a hypothesis.

## Decision Gates

| Signal | Action |
|---|---|
| Concrete evidence exists | Create a finding with `file:line` evidence and the smallest safe refactor. |
| Evidence is incomplete | Mark as hypothesis and lower confidence. |
| Recommendation is cosmetic or speculative | Omit it unless maintainability benefit is clear. |

## Execution Steps

1. Inspect the target and nearby tests only as needed for this lens.
2. Identify findings that match this skill's responsibility.
3. Recommend the smallest safe behavior-preserving refactor.
4. Note validation and rollback implications where material; the calling agent decides where they land.

## Output Contract

Return findings in the calling agent's output contract — that contract wins over any field list here. Every finding carries `file:line` evidence or is marked hypothesis. Return `no_findings` when this lens has no material issue.

## References

None.
