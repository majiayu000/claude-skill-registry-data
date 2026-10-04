---
name: release-brief-writer
description: Create release notes that communicate value, changes, risks, and upgrade instructions.
category: docs
version: 1.0.0
---

# Release Brief Writer

## Purpose

Create release notes that communicate value, changes, risks, and upgrade instructions.

Use this skill to produce clear, actionable work. Avoid generic advice. Prefer concrete findings, explicit assumptions, and next steps that can be executed or reviewed.

## Use When

- Publishing a release
- Announcing changes
- Preparing stakeholder updates

## Required Context

Ask for missing context only when it blocks a correct answer. Otherwise, proceed with the best available information and clearly mark assumptions.

- Change list
- Audience
- Version
- Known issues

## Workflow

1. Lead with user-visible value.
2. Explain important changes without oversharing internals.
3. Document upgrade or migration steps.
4. Mention known issues and compatibility notes.
5. Keep wording concise and professional.

## Guardrails

- Do not invent facts, files, commands, credentials, or project state.
- Separate confirmed information from assumptions.
- Prefer concise recommendations over long theoretical explanations.
- Make trade-offs explicit.
- When reviewing code or architecture, prioritize correctness, security, maintainability, and operational safety.
- When outputting commands, include only commands that are relevant to the current environment or clearly label them as examples.

## Output Contract

Always structure the final answer with these sections when applicable:

- Summary
- Highlights
- Upgrade notes
- Known issues
- Validation notes

## Quality Bar

A strong result from this skill should be specific enough that a developer, reviewer, maintainer, or product owner can act on it without needing a second clarification round.
