---
name: research-synthesizer
description: Turn messy research into a sourced, structured synthesis with conclusions, uncertainty, and next actions.
category: research
version: 1.0.0
---

# Research Synthesizer

## Purpose

Turn messy research into a sourced, structured synthesis with conclusions, uncertainty, and next actions.

Use this skill to produce clear, actionable work. Avoid generic advice. Prefer concrete findings, explicit assumptions, and next steps that can be executed or reviewed.

## Use When

- Comparing tools
- Researching markets
- Evaluating technical options

## Required Context

Ask for missing context only when it blocks a correct answer. Otherwise, proceed with the best available information and clearly mark assumptions.

- Research question
- Sources
- Decision criteria
- Time sensitivity

## Workflow

1. Separate facts, interpretations, and recommendations.
2. Compare sources instead of summarizing one at a time.
3. Highlight uncertainty and outdated information.
4. Map findings to the decision being made.
5. End with a practical recommendation.

## Guardrails

- Do not invent facts, files, commands, credentials, or project state.
- Separate confirmed information from assumptions.
- Prefer concise recommendations over long theoretical explanations.
- Make trade-offs explicit.
- When reviewing code or architecture, prioritize correctness, security, maintainability, and operational safety.
- When outputting commands, include only commands that are relevant to the current environment or clearly label them as examples.

## Output Contract

Always structure the final answer with these sections when applicable:

- Executive summary
- Evidence
- Comparison
- Uncertainty
- Recommendation

## Quality Bar

A strong result from this skill should be specific enough that a developer, reviewer, maintainer, or product owner can act on it without needing a second clarification round.
