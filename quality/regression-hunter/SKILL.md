---
name: regression-hunter
description: Find likely regressions introduced by a change and recommend targeted validation.
category: quality
version: 1.0.0
---

# Regression Hunter

## Purpose

Find likely regressions introduced by a change and recommend targeted validation.

Use this skill to produce clear, actionable work. Avoid generic advice. Prefer concrete findings, explicit assumptions, and next steps that can be executed or reviewed.

## Use When

- After code changes
- Before release
- When bugs appear after deployment

## Required Context

Ask for missing context only when it blocks a correct answer. Otherwise, proceed with the best available information and clearly mark assumptions.

- Diff
- Affected modules
- Recent incidents
- Test results

## Workflow

1. Identify touched surfaces and indirect dependencies.
2. Map changed behavior to user workflows.
3. Look for backward compatibility risks.
4. Recommend specific regression tests.
5. Prioritize high-impact scenarios.

## Guardrails

- Do not invent facts, files, commands, credentials, or project state.
- Separate confirmed information from assumptions.
- Prefer concise recommendations over long theoretical explanations.
- Make trade-offs explicit.
- When reviewing code or architecture, prioritize correctness, security, maintainability, and operational safety.
- When outputting commands, include only commands that are relevant to the current environment or clearly label them as examples.

## Output Contract

Always structure the final answer with these sections when applicable:

- Regression risks
- Affected workflows
- Targeted tests
- Manual checks
- Confidence level

## Quality Bar

A strong result from this skill should be specific enough that a developer, reviewer, maintainer, or product owner can act on it without needing a second clarification round.
