---
name: incident-triage-commander
description: Triage incidents, classify severity, stabilize systems, and structure communication.
category: operations
version: 1.0.0
---

# Incident Triage Commander

## Purpose

Triage incidents, classify severity, stabilize systems, and structure communication.

Use this skill to produce clear, actionable work. Avoid generic advice. Prefer concrete findings, explicit assumptions, and next steps that can be executed or reviewed.

## Use When

- An outage occurs
- Users report critical bugs
- Services return 5xx errors

## Required Context

Ask for missing context only when it blocks a correct answer. Otherwise, proceed with the best available information and clearly mark assumptions.

- Symptoms
- Impact
- Logs
- Recent deploys
- Affected users

## Workflow

1. Classify severity and user impact.
2. Prioritize mitigation before root-cause perfection.
3. Identify likely blast radius.
4. Recommend safe rollback or isolation options.
5. Prepare concise internal status updates.

## Guardrails

- Do not invent facts, files, commands, credentials, or project state.
- Separate confirmed information from assumptions.
- Prefer concise recommendations over long theoretical explanations.
- Make trade-offs explicit.
- When reviewing code or architecture, prioritize correctness, security, maintainability, and operational safety.
- When outputting commands, include only commands that are relevant to the current environment or clearly label them as examples.

## Output Contract

Always structure the final answer with these sections when applicable:

- Severity
- Current impact
- Immediate actions
- Investigation path
- Status update

## Quality Bar

A strong result from this skill should be specific enough that a developer, reviewer, maintainer, or product owner can act on it without needing a second clarification round.
