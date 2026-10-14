---
name: kiss-yagni
description: "Trigger: KISS, YAGNI, overengineering, speculative abstraction. Keep refactor plans simple and non-speculative."
license: Apache-2.0
metadata:
  author: gentle-ai
  adapted_by: andresnator
  source: gentle-ai/plan-refactor
  version: "1.0.1"
  status: testing
---

## Activation Contract
Load this skill when reviewing refactor plans for: KISS, YAGNI, overengineering, speculative abstraction.

## Hard Rules

- Prefer explicit code until variation is proven.
- Reject abstractions for hypothetical future cases.
- Recommend deletion of unused speculative structure only when safe and validated.
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
