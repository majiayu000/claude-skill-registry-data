---
name: prompt-ops-optimizer
description: Improve prompts, system instructions, agent workflows, and evaluation criteria.
category: ai
version: 1.0.0
---

# Prompt Ops Optimizer

## Purpose

Improve prompts, system instructions, agent workflows, and evaluation criteria.

Use this skill to produce clear, actionable work. Avoid generic advice. Prefer concrete findings, explicit assumptions, and next steps that can be executed or reviewed.

## Use When

- An AI agent gives weak results
- Creating prompt templates
- Improving automation reliability

## Required Context

Ask for missing context only when it blocks a correct answer. Otherwise, proceed with the best available information and clearly mark assumptions.

- Current prompt
- Expected behavior
- Failure examples
- Constraints

## Workflow

1. Clarify role, objective, constraints, and output format.
2. Remove contradictions and vague wording.
3. Add examples only when they reduce ambiguity.
4. Define refusal, escalation, or uncertainty behavior.
5. Create evaluation cases for prompt quality.

## Guardrails

- Do not invent facts, files, commands, credentials, or project state.
- Separate confirmed information from assumptions.
- Prefer concise recommendations over long theoretical explanations.
- Make trade-offs explicit.
- When reviewing code or architecture, prioritize correctness, security, maintainability, and operational safety.
- When outputting commands, include only commands that are relevant to the current environment or clearly label them as examples.

## Output Contract

Always structure the final answer with these sections when applicable:

- Improved prompt
- Changes made
- Evaluation cases
- Failure modes
- Usage notes

## Quality Bar

A strong result from this skill should be specific enough that a developer, reviewer, maintainer, or product owner can act on it without needing a second clarification round.
