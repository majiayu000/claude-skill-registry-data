---
name: spec-clarify
description: Ask targeted questions to clarify scope, edge cases, and acceptance before coding.
---

# Spec Clarify

## Objective
- Surface ambiguities and edge cases early.
- Confirm inputs, outputs, and constraints before implementation.

## When to use
- Requirements are vague, conflicting, or incomplete.
- Before starting on a new feature or significant change.

## Inputs
- User request and any provided specs.
- AGENTS.md and applicable rules.
- Existing behavior inferred from code/tests.

## Process
1) Restate the goal and current understanding.
2) List assumptions explicitly.
3) Ask precise questions on inputs/outputs, data shapes, edge cases, and metrics.
4) Highlight risks of proceeding without answers.
5) Propose a minimal path once questions are resolved.

## Outputs
- Concise list of questions and assumptions.
- Risks of proceeding without answers.
- Suggested next step once clarified.

## Edge cases
- If blocking ambiguity exists, do not proceed to implementation; ask first.
- Keep questions specific and answerable; avoid broad surveys.
