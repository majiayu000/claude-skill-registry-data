---
name: dependency-inversion
description: "Trigger: dependency inversion, DIP, ports, interfaces, adapters. Detect concrete dependency risks at boundaries."
license: Apache-2.0
metadata:
  author: gentle-ai
  adapted_by: andresnator
  source: gentle-ai/plan-refactor
  version: "1.0.0"
  status: in-progress
---

## Activation Contract
Load this skill when reviewing refactor plans for: dependency inversion, DIP, ports, interfaces, adapters.

## Hard Rules

- Flag direct dependencies on frameworks, gateways, clients, persistence, or external systems when they hurt testing or coupling.
- Introduce ports/interfaces only for real variation, test seams, or architectural boundaries.
- Do not wrap stable internal classes by default.
- Preserve observable behavior; label functional changes as follow-up.
- Require evidence for every recommendation, or mark it as a hypothesis.

## Decision Gates

| Signal | Action |
|---|---|
| Concrete evidence exists | Create a finding with file, lines, symbol, benefit, validation, and rollback. |
| Evidence is incomplete | Mark as hypothesis and lower confidence. |
| Recommendation is cosmetic or speculative | Omit it unless maintainability benefit is clear. |

## Execution Steps

1. Inspect the target and nearby tests only as needed for this lens.
2. Identify findings that match this skill's responsibility.
3. Recommend the smallest safe behavior-preserving refactor.
4. Add validation and rollback steps for each recommendation.

## Output Contract

Return structured findings for the calling reviewer. Return `no_findings` when this lens has no material issue.

## References

None.
