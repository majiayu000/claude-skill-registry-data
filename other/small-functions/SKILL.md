---
name: small-functions
description: "Trigger: small functions, long method, extract method. Detect oversized functions and extractable blocks."
license: Apache-2.0
metadata:
  author: gentle-ai
  adapted_by: andresnator
  source: gentle-ai/plan-refactor
  version: "1.0.0"
  status: in-progress
---

## Activation Contract
Load this skill when reviewing refactor plans for: small functions, long method, extract method.

## Hard Rules

- Flag methods with multiple abstraction levels, nested branches, or distinct phases.
- Prefer Extract Method when a block has a meaningful domain name.
- Prefer Split Phase when parsing/validation/calculation/persistence are interleaved.
- Keep recommendations behavior-preserving and incremental.
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
