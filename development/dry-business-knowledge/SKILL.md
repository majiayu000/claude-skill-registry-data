---
name: dry-business-knowledge
description: "Trigger: DRY, duplicated business knowledge, duplication. Distinguish harmful knowledge duplication from harmless similarity."
license: Apache-2.0
metadata:
  author: gentle-ai
  adapted_by: andresnator
  source: gentle-ai/plan-refactor
  version: "1.0.0"
  status: in-progress
---

## Activation Contract
Load this skill when reviewing refactor plans for: DRY, duplicated business knowledge, duplication.

## Hard Rules

- Prioritize duplicated rules, validations, formulas, permissions, mappings, or invariants.
- Do not merge coincidentally similar code with different meanings.
- State the business knowledge that would become single-sourced.
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
