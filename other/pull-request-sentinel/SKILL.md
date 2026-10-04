---
name: pull-request-sentinel
description: Review pull requests for correctness, maintainability, security, tests, and release risk.
category: quality
version: 1.0.0
---

# Pull Request Sentinel

## Purpose

Review pull requests for correctness, maintainability, security, tests, and release risk.

Use this skill to produce clear, actionable work. Avoid generic advice. Prefer concrete findings, explicit assumptions, and next steps that can be executed or reviewed.

## Use When

- Reviewing PRs
- Before merge
- Auditing generated code

## Required Context

Ask for missing context only when it blocks a correct answer. Otherwise, proceed with the best available information and clearly mark assumptions.

- Diff
- Issue/requirement
- Test results
- Project standards

## Workflow

1. Confirm the change solves the stated problem.
2. Look for regressions, missing tests, and risky side effects.
3. Review readability, naming, and architectural fit.
4. Check security, data handling, and permissions.
5. Return actionable comments with severity.

## Guardrails

- Do not invent facts, files, commands, credentials, or project state.
- Separate confirmed information from assumptions.
- Prefer concise recommendations over long theoretical explanations.
- Make trade-offs explicit.
- When reviewing code or architecture, prioritize correctness, security, maintainability, and operational safety.
- When outputting commands, include only commands that are relevant to the current environment or clearly label them as examples.

## Output Contract

Always structure the final answer with these sections when applicable:

- Verdict
- Blocking issues
- Non-blocking suggestions
- Security notes
- Test recommendations

## Quality Bar

A strong result from this skill should be specific enough that a developer, reviewer, maintainer, or product owner can act on it without needing a second clarification round.
