---
name: technical-debt-radar
description: Detect technical debt and prioritize fixes by business risk, maintainability, and delivery impact.
category: engineering
version: 1.0.0
---

# Technical Debt Radar

## Purpose

Detect technical debt and prioritize fixes by business risk, maintainability, and delivery impact.

Use this skill to produce clear, actionable work. Avoid generic advice. Prefer concrete findings, explicit assumptions, and next steps that can be executed or reviewed.

## Use When

- Auditing a codebase
- Planning refactors
- Preparing roadmap items

## Required Context

Ask for missing context only when it blocks a correct answer. Otherwise, proceed with the best available information and clearly mark assumptions.

- Codebase notes
- Known pain points
- Incident history
- Delivery goals

## Workflow

1. Identify duplication, coupling, fragile areas, and unclear ownership.
2. Separate cosmetic issues from business-impacting debt.
3. Estimate risk, effort, and payoff.
4. Recommend staged remediation.
5. Tie debt items to measurable outcomes.

## Guardrails

- Do not invent facts, files, commands, credentials, or project state.
- Separate confirmed information from assumptions.
- Prefer concise recommendations over long theoretical explanations.
- Make trade-offs explicit.
- When reviewing code or architecture, prioritize correctness, security, maintainability, and operational safety.
- When outputting commands, include only commands that are relevant to the current environment or clearly label them as examples.

## Output Contract

Always structure the final answer with these sections when applicable:

- Debt inventory
- Priority ranking
- Impact
- Fix plan
- Deferred items

## Quality Bar

A strong result from this skill should be specific enough that a developer, reviewer, maintainer, or product owner can act on it without needing a second clarification round.
