---
name: spark-feature-planning
description: Use when a Spark feature needs repository-first research, explicit option selection, and an owner-aligned implementation plan before code changes.
---

# Spark feature planning

Turn a requested capability into an evidence-backed decision and the smallest
plan that can prove it.

## Procedure

1. Reconstruct the user problem and current behavior from the owning code, specifications, package README, nearby tests, and machine-readable inventory.
2. Separate repository facts, external facts, assumptions, constraints, and unresolved product decisions. Research only questions whose answers can change the selection or acceptance boundary; prefer primary sources for external claims.
3. Compare the status quo and viable options against owner fit, semantic duplication, dependency direction, compatibility cost, lifecycle and failure modes, operational burden, and validation cost.
4. Select one option only when the evidence and confirmed constraints distinguish it. Explain why rejected options lose without inventing future requirements.
5. Produce a dependency-ordered plan whose first slice proves the highest-risk behavior. Name the owner, affected surfaces, observable acceptance criteria, failure cases, compatibility evidence, documentation owner, and validation commands.
6. Keep adjacent cleanup and speculative extensibility out of the feature plan. Record them as rejected or out of scope rather than prebuilding them.

Stop with `needs-decision` when a missing product choice changes user-visible
behavior, authority, ownership, or irreversible cost. Return `problemEvidence`,
`options`, `selection`, `plan`, `acceptanceCriteria`, `risks`, `outOfScope`,
`validationCommands`, `openQuestions`, and `verdict`.
