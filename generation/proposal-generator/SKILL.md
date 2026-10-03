---
name: proposal-generator
description: Build agency proposal workflows for scopes, offers, pricing narratives, and next-step packaging. Use when the user needs a proposal draft, scope framing, statement-of-work structure, or reusable proposal-generation logic.
---

# proposal-generator

## Purpose

- Turn a service brief into a proposal structure the team can refine.
- Keep proposals consistent across scope, pricing narrative, and next steps.

## Triggers

- The user wants a proposal drafted from discovery notes.
- The user wants a repeatable proposal skeleton for a service line.
- The user wants scope, deliverables, and next steps packaged clearly.

## Inputs

### Required

- client problem or objective
- service scope or offer definition

### Optional

- pricing model
- timeline assumptions
- discovery notes, constraints, or exclusions

## Outputs

- proposal outline
- scope and deliverables draft
- assumptions, exclusions, and next-step section

## Guardrails

- Do not fabricate pricing authority or legal terms.
- Keep assumptions and exclusions explicit.
- Escalate when legal review, procurement requirements, or custom commercial terms are involved.

## Failure Modes

- scope is underspecified
- pricing story is disconnected from outcomes
- exclusions are missing and create delivery risk
- next steps are vague or non-actionable

## QA Steps

1. Confirm the proposal maps to a real client objective.
2. Check deliverables and assumptions do not conflict.
3. Check exclusions and next steps are explicit.
4. Check the proposal can be reviewed without needing hidden context.
