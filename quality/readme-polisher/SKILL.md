---
name: readme-polisher
description: Create or improve a GitHub README with clear positioning, setup, usage, architecture, and contribution guidance.
category: docs
version: 1.0.0
---

# README Polisher

## Purpose

Create or improve a GitHub README with clear positioning, setup, usage, architecture, and contribution guidance.

Use this skill to produce clear, actionable work. Avoid generic advice. Prefer concrete findings, explicit assumptions, and next steps that can be executed or reviewed.

## Use When

- Preparing a repo for GitHub
- Improving open-source presentation
- Documenting setup

## Required Context

Ask for missing context only when it blocks a correct answer. Otherwise, proceed with the best available information and clearly mark assumptions.

- Project name
- Purpose
- Stack
- Install commands
- Usage examples

## Workflow

1. Explain the project value in the first screen.
2. Provide quick start commands that can be copied.
3. Include architecture, configuration, testing, and deployment notes.
4. Add contribution and license information.
5. Avoid generic marketing copy.

## Guardrails

- Do not invent facts, files, commands, credentials, or project state.
- Separate confirmed information from assumptions.
- Prefer concise recommendations over long theoretical explanations.
- Make trade-offs explicit.
- When reviewing code or architecture, prioritize correctness, security, maintainability, and operational safety.
- When outputting commands, include only commands that are relevant to the current environment or clearly label them as examples.

## Output Contract

Always structure the final answer with these sections when applicable:

- README sections
- Quick start
- Usage
- Architecture
- Contribution notes

## Quality Bar

A strong result from this skill should be specific enough that a developer, reviewer, maintainer, or product owner can act on it without needing a second clarification round.
