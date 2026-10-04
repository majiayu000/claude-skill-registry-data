---
name: architecture-lens
description: Review system architecture for boundaries, coupling, scalability, maintainability, and operational risk.
category: engineering
version: 1.0.0
---

# Architecture Lens

## Purpose

Review system architecture for boundaries, coupling, scalability, maintainability, and operational risk.

Use this skill to produce clear, actionable work. Avoid generic advice. Prefer concrete findings, explicit assumptions, and next steps that can be executed or reviewed.

## Use When

- Designing a system
- Before major refactors
- Before production deployment

## Required Context

Ask for missing context only when it blocks a correct answer. Otherwise, proceed with the best available information and clearly mark assumptions.

- Architecture proposal
- Repo structure
- Runtime diagram
- Constraints

## Workflow

1. Identify bounded contexts and ownership.
2. Review data flow, API boundaries, and dependency direction.
3. Evaluate scalability and operational failure modes.
4. Check whether the architecture matches team capacity.
5. Recommend simpler alternatives when complexity is unjustified.

## Guardrails

- Do not invent facts, files, commands, credentials, or project state.
- Separate confirmed information from assumptions.
- Prefer concise recommendations over long theoretical explanations.
- Make trade-offs explicit.
- When reviewing code or architecture, prioritize correctness, security, maintainability, and operational safety.
- When outputting commands, include only commands that are relevant to the current environment or clearly label them as examples.

## Output Contract

Always structure the final answer with these sections when applicable:

- Architecture assessment
- Strengths
- Weaknesses
- Risks
- Recommended changes

## Quality Bar

A strong result from this skill should be specific enough that a developer, reviewer, maintainer, or product owner can act on it without needing a second clarification round.
