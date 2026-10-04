---
name: dependency-risk-sentinel
description: Review dependencies for security, maintenance, licensing, bloat, and supply-chain risk.
category: security
version: 1.0.0
---

# Dependency Risk Sentinel

## Purpose

Review dependencies for security, maintenance, licensing, bloat, and supply-chain risk.

Use this skill to produce clear, actionable work. Avoid generic advice. Prefer concrete findings, explicit assumptions, and next steps that can be executed or reviewed.

## Use When

- Adding packages
- Auditing a repo
- Preparing production release

## Required Context

Ask for missing context only when it blocks a correct answer. Otherwise, proceed with the best available information and clearly mark assumptions.

- Package files
- Lockfiles
- Runtime environment
- License requirements

## Workflow

1. Check whether each dependency is necessary.
2. Review maintenance status and transitive risk.
3. Identify vulnerable, deprecated, or oversized packages.
4. Consider license compatibility.
5. Suggest safer built-in or smaller alternatives.

## Guardrails

- Do not invent facts, files, commands, credentials, or project state.
- Separate confirmed information from assumptions.
- Prefer concise recommendations over long theoretical explanations.
- Make trade-offs explicit.
- When reviewing code or architecture, prioritize correctness, security, maintainability, and operational safety.
- When outputting commands, include only commands that are relevant to the current environment or clearly label them as examples.

## Output Contract

Always structure the final answer with these sections when applicable:

- Dependency risks
- Remove/replace candidates
- Security notes
- License notes
- Upgrade plan

## Quality Bar

A strong result from this skill should be specific enough that a developer, reviewer, maintainer, or product owner can act on it without needing a second clarification round.
