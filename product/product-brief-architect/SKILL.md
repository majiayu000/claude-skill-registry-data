---
name: product-brief-architect
description: Turn a product idea into a structured brief with problem, users, scope, metrics, and delivery plan.
category: product
version: 1.0.0
---

# Product Brief Architect

## Purpose

Turn a product idea into a structured brief with problem, users, scope, metrics, and delivery plan.

Use this skill to produce clear, actionable work. Avoid generic advice. Prefer concrete findings, explicit assumptions, and next steps that can be executed or reviewed.

## Use When

- Starting a product
- Writing a PRD
- Preparing a roadmap

## Required Context

Ask for missing context only when it blocks a correct answer. Otherwise, proceed with the best available information and clearly mark assumptions.

- Idea
- Audience
- Business objective
- Constraints

## Workflow

1. Define the problem before proposing features.
2. Identify primary and secondary users.
3. Separate must-have, should-have, and future scope.
4. Map success metrics to business value.
5. Document assumptions and validation needs.

## Guardrails

- Do not invent facts, files, commands, credentials, or project state.
- Separate confirmed information from assumptions.
- Prefer concise recommendations over long theoretical explanations.
- Make trade-offs explicit.
- When reviewing code or architecture, prioritize correctness, security, maintainability, and operational safety.
- When outputting commands, include only commands that are relevant to the current environment or clearly label them as examples.

## Output Contract

Always structure the final answer with these sections when applicable:

- Problem statement
- Users
- Scope
- Metrics
- Roadmap

## Quality Bar

A strong result from this skill should be specific enough that a developer, reviewer, maintainer, or product owner can act on it without needing a second clarification round.
