---
name: bug-forensics
description: Diagnose bugs through evidence, hypotheses, reproduction paths, and targeted fixes.
category: quality
version: 1.0.0
---

# Bug Forensics

## Purpose

Diagnose bugs through evidence, hypotheses, reproduction paths, and targeted fixes.

Use this skill to produce clear, actionable work. Avoid generic advice. Prefer concrete findings, explicit assumptions, and next steps that can be executed or reviewed.

## Use When

- Debugging errors
- Investigating production bugs
- Analyzing logs

## Required Context

Ask for missing context only when it blocks a correct answer. Otherwise, proceed with the best available information and clearly mark assumptions.

- Error message
- Logs
- Recent changes
- Reproduction steps

## Workflow

1. Separate symptoms from root causes.
2. Build ranked hypotheses with evidence.
3. Suggest minimal reproduction steps.
4. Recommend safe diagnostic commands.
5. Propose a fix and validation path.

## Guardrails

- Do not invent facts, files, commands, credentials, or project state.
- Separate confirmed information from assumptions.
- Prefer concise recommendations over long theoretical explanations.
- Make trade-offs explicit.
- When reviewing code or architecture, prioritize correctness, security, maintainability, and operational safety.
- When outputting commands, include only commands that are relevant to the current environment or clearly label them as examples.

## Output Contract

Always structure the final answer with these sections when applicable:

- Most likely cause
- Evidence
- Hypotheses
- Debug steps
- Fix plan

## Quality Bar

A strong result from this skill should be specific enough that a developer, reviewer, maintainer, or product owner can act on it without needing a second clarification round.
