---
name: plan-update
description: Make the smallest evidence-backed correction to implementation-plan mechanics. Use when implementation or validation proves incorrect ordering, prerequisites, phase scope, dependencies, steps, or validation gates.
---

# Plan Update

Correct an implementation plan without making product, architecture, or behavior decisions.

## Workflow

1. Identify the authoritative plan, exact mechanical defect, evidence, and affected phases.
2. Confirm that the correction is local. Use `plan-create` when multiple phases require broad replanning.
3. Use `spec-update` when the defect concerns product behavior, architecture semantics, a public contract, or acceptance meaning.
4. Stop for user direction when the correction materially expands authorized scope.
5. Apply the smallest correction in the plan's existing structure and style.
6. Verify affected dependencies, cross-references, acceptance criteria, and downstream phases remain consistent.

Do not use plans as progress logs, add speculative roadmap work, rewrite unrelated phases, or disguise scope expansion as maintenance.

Finish by reporting the defect, evidence, exact correction, affected phases, and whether implementation or validation can safely resume.
