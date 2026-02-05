---
name: diff-scope-minimizer
description: Keep changes narrowly scoped with a tiny patch plan and stop criteria
version: 0.1.0
tags: [refactor, productivity]
triggers:
  - small diff
  - minimal change
  - refactor plan
---

# Diff Scope Minimizer

## Purpose
Focus on the smallest viable change to solve the problem and reduce churn.

## Behavior
1. Propose a 3–5 step patch plan with target files.
2. Estimate diff size (files/lines) and define stop criteria.
3. Re-evaluate after each step; stop if criteria met.

## Guardrails
- Avoid touching unrelated files.
- If diff grows >2× estimate, pause and re-plan.

## Integration
- `/lazy task-exec` before edits; Coder and Refactor agents.

## Example Prompt
> Plan the smallest patch to fix null handling in `src/api/users.py`.

