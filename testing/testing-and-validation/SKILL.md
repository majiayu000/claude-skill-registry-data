---
name: testing-and-validation
description: Shared testing and validation guidance for choosing the right checks, improving confidence, and reporting residual risk clearly.
compatibility: opencode
metadata:
  audience: engineers
  purpose: validation-guidance
---
## What I do

Provide consistent guidance for validating changes and improving delivery confidence.

## Core principles

- Run the most relevant validation available for the change.
- Prefer focused, high-signal tests over broad, expensive rituals.
- Tie validation to the behavior being changed.
- Distinguish verified behavior from assumed behavior.
- Report residual risk clearly when validation is incomplete.

## Practical guidance

- Add or update automated tests when the change materially affects behavior.
- Prefer unit tests for isolated logic, integration tests for boundaries, and end-to-end checks for user-critical flows.
- If full validation is not possible, explain what was checked and what remains uncertain.
- Watch for brittle tests, missing fixtures, poor observability, and unverified failure paths.

## When to use me

Use this skill whenever code changes need validation, test design, or quality assessment.
