---
name: skill-quality-inspector
description: Review AI skills for ambiguity, weak activation triggers, missing guardrails, and poor output contracts.
category: strategy
version: 1.0.0
---

# Skill Quality Inspector

## Purpose

Review AI skills for ambiguity, weak activation triggers, missing guardrails, and poor output contracts.

Use this skill to produce clear, actionable work. Avoid generic advice. Prefer concrete findings, explicit assumptions, and next steps that can be executed or reviewed.

## Use When

- Auditing a skills repository
- Preparing skills for public release
- Refining agent workflows

## Required Context

Ask for missing context only when it blocks a correct answer. Otherwise, proceed with the best available information and clearly mark assumptions.

- One or more SKILL.md files
- Repository standard
- Target agent environment

## Workflow

1. Check whether the description is specific enough for activation.
2. Detect vague instructions or conflicting behavior.
3. Verify that workflow steps are ordered and actionable.
4. Ensure safety, privacy, and scope boundaries are explicit.
5. Recommend concrete edits rather than generic feedback.

## Guardrails

- Do not invent facts, files, commands, credentials, or project state.
- Separate confirmed information from assumptions.
- Prefer concise recommendations over long theoretical explanations.
- Make trade-offs explicit.
- When reviewing code or architecture, prioritize correctness, security, maintainability, and operational safety.
- When outputting commands, include only commands that are relevant to the current environment or clearly label them as examples.

## Output Contract

Always structure the final answer with these sections when applicable:

- Score
- Blocking issues
- Recommended edits
- Improved description
- Release readiness

## Quality Bar

A strong result from this skill should be specific enough that a developer, reviewer, maintainer, or product owner can act on it without needing a second clarification round.
