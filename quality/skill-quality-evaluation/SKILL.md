---
name: skill-quality-evaluation
description: "Evaluates skill quality, actionability, and usefulness before adding it to a shared library. Use when accepting new skills or reviewing a skill batch for duplicates and vague guidance."
---

# Skill Quality Evaluation

## Use when
A collection grows in count while new entries repeat broad advice, lack trigger conditions, or cannot be tested.

## Workflow
1. Check frontmatter name, trigger-specific description, intended inputs, decision procedure, concrete outputs, validation, and failure/guardrail behavior.
2. Run a few positive and negative trigger examples to test when the skill should and should not activate.
3. Score specificity, executable steps, evidence/validation, uniqueness, portability, and maintenance cost with written reasons.
4. Reject, merge, revise, or accept each candidate and preserve a short review note for traceability.

## Required output
A scored review table, revision requests, duplicate candidates, and an accept/merge/reject decision for each skill.

## Validation
- At least one positive and one negative trigger example are evaluated.
- Scores include written evidence rather than subjective star ratings alone.
- Skills with unsafe or unsupported instructions are blocked until revised.

## Guardrails
Do not optimize solely for the number of skills; a smaller reliable library is better than hundreds of near-duplicates.
