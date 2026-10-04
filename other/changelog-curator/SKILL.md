---
name: changelog-curator
description: Generate clean changelogs from commits, pull requests, tickets, or release notes.
category: docs
version: 1.0.0
---

# Changelog Curator

## Purpose

Generate clean changelogs from commits, pull requests, tickets, or release notes.

Use this skill to produce clear, actionable work. Avoid generic advice. Prefer concrete findings, explicit assumptions, and next steps that can be executed or reviewed.

## Use When

- Preparing releases
- Summarizing changes
- Maintaining open-source history

## Required Context

Ask for missing context only when it blocks a correct answer. Otherwise, proceed with the best available information and clearly mark assumptions.

- Commits
- PRs
- Version
- Release date

## Workflow

1. Group changes into added, changed, fixed, deprecated, removed, and security.
2. Write for users and maintainers, not just commit authors.
3. Avoid exposing internal noise.
4. Call out breaking changes clearly.
5. Link to relevant issues when available.

## Guardrails

- Do not invent facts, files, commands, credentials, or project state.
- Separate confirmed information from assumptions.
- Prefer concise recommendations over long theoretical explanations.
- Make trade-offs explicit.
- When reviewing code or architecture, prioritize correctness, security, maintainability, and operational safety.
- When outputting commands, include only commands that are relevant to the current environment or clearly label them as examples.

## Output Contract

Always structure the final answer with these sections when applicable:

- Version heading
- Grouped changes
- Breaking changes
- Migration notes
- Credits

## Quality Bar

A strong result from this skill should be specific enough that a developer, reviewer, maintainer, or product owner can act on it without needing a second clarification round.
