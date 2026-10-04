---
name: skill-authoring-forge
description: Design new reusable AI skills with clear triggers, workflow, guardrails, and output contracts.
category: strategy
version: 1.0.0
---

# Skill Authoring Forge

## Purpose

Design new reusable AI skills with clear triggers, workflow, guardrails, and output contracts.

Use this skill to produce clear, actionable work. Avoid generic advice. Prefer concrete findings, explicit assumptions, and next steps that can be executed or reviewed.

## Use When

- Creating a new SKILL.md
- Improving an existing skill
- Standardizing agent behavior

## Required Context

Ask for missing context only when it blocks a correct answer. Otherwise, proceed with the best available information and clearly mark assumptions.

- Skill goal
- Target users
- Task type
- Expected output

## Workflow

1. Write a precise description for automatic activation.
2. Define when to use and when not to use the skill.
3. Specify required inputs and assumptions.
4. Create deterministic workflow steps.
5. Define a stable output format.

## Guardrails

- Do not invent facts, files, commands, credentials, or project state.
- Separate confirmed information from assumptions.
- Prefer concise recommendations over long theoretical explanations.
- Make trade-offs explicit.
- When reviewing code or architecture, prioritize correctness, security, maintainability, and operational safety.
- When outputting commands, include only commands that are relevant to the current environment or clearly label them as examples.

## Output Contract

Always structure the final answer with these sections when applicable:

- Skill name
- Description
- Workflow
- Guardrails
- Output contract

## Quality Bar

A strong result from this skill should be specific enough that a developer, reviewer, maintainer, or product owner can act on it without needing a second clarification round.
