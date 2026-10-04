---
name: legacy-decoder
description: Analyze legacy code and explain behavior, dependencies, hidden rules, and modernization opportunities.
category: engineering
version: 1.0.0
---

# Legacy Decoder

## Purpose

Analyze legacy code and explain behavior, dependencies, hidden rules, and modernization opportunities.

Use this skill to produce clear, actionable work. Avoid generic advice. Prefer concrete findings, explicit assumptions, and next steps that can be executed or reviewed.

## Use When

- Working with old systems
- Porting scripts
- Replacing spreadsheet or desktop tools

## Required Context

Ask for missing context only when it blocks a correct answer. Otherwise, proceed with the best available information and clearly mark assumptions.

- Legacy files
- Runtime behavior
- Known business process
- Expected outputs

## Workflow

1. Find entry points and execution order.
2. Identify implicit rules, magic values, and hidden data contracts.
3. Separate business logic from framework or UI code.
4. Document dependencies and side effects.
5. Suggest a safe modernization path.

## Guardrails

- Do not invent facts, files, commands, credentials, or project state.
- Separate confirmed information from assumptions.
- Prefer concise recommendations over long theoretical explanations.
- Make trade-offs explicit.
- When reviewing code or architecture, prioritize correctness, security, maintainability, and operational safety.
- When outputting commands, include only commands that are relevant to the current environment or clearly label them as examples.

## Output Contract

Always structure the final answer with these sections when applicable:

- Behavior summary
- Business rules
- Dependencies
- Risks
- Modernization plan

## Quality Bar

A strong result from this skill should be specific enough that a developer, reviewer, maintainer, or product owner can act on it without needing a second clarification round.
