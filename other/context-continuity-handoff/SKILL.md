---
name: context-continuity-handoff
description: Create a concise handoff so another AI agent or developer can continue the work without losing context.
category: strategy
version: 1.0.0
---

# Context Continuity Handoff

## Purpose

Create a concise handoff so another AI agent or developer can continue the work without losing context.

Use this skill to produce clear, actionable work. Avoid generic advice. Prefer concrete findings, explicit assumptions, and next steps that can be executed or reviewed.

## Use When

- A session is ending
- A task is moving to another agent
- A project needs a continuation brief

## Required Context

Ask for missing context only when it blocks a correct answer. Otherwise, proceed with the best available information and clearly mark assumptions.

- Current state
- Decisions made
- Files changed
- Open issues

## Workflow

1. Summarize the objective in one paragraph.
2. List decisions that should not be re-litigated.
3. Capture exact files, commands, branches, and errors when available.
4. Separate completed work from pending work.
5. Provide a next-step sequence that is safe to execute.

## Guardrails

- Do not invent facts, files, commands, credentials, or project state.
- Separate confirmed information from assumptions.
- Prefer concise recommendations over long theoretical explanations.
- Make trade-offs explicit.
- When reviewing code or architecture, prioritize correctness, security, maintainability, and operational safety.
- When outputting commands, include only commands that are relevant to the current environment or clearly label them as examples.

## Output Contract

Always structure the final answer with these sections when applicable:

- Project context
- Completed items
- Pending items
- Known risks
- Next actions

## Quality Bar

A strong result from this skill should be specific enough that a developer, reviewer, maintainer, or product owner can act on it without needing a second clarification round.
