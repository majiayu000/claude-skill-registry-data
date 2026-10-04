---
name: api-contract-steward
description: Review REST, GraphQL, webhook, or internal API contracts for consistency, safety, and usability.
category: engineering
version: 1.0.0
---

# API Contract Steward

## Purpose

Review REST, GraphQL, webhook, or internal API contracts for consistency, safety, and usability.

Use this skill to produce clear, actionable work. Avoid generic advice. Prefer concrete findings, explicit assumptions, and next steps that can be executed or reviewed.

## Use When

- Designing endpoints
- Reviewing API changes
- Integrating systems

## Required Context

Ask for missing context only when it blocks a correct answer. Otherwise, proceed with the best available information and clearly mark assumptions.

- Endpoint list
- Payloads
- Authentication model
- Consumers

## Workflow

1. Check resource naming, HTTP semantics, and versioning.
2. Validate request/response schemas and error contracts.
3. Review auth, authorization, pagination, filtering, and idempotency.
4. Identify breaking changes and migration needs.
5. Improve developer experience and documentation.

## Guardrails

- Do not invent facts, files, commands, credentials, or project state.
- Separate confirmed information from assumptions.
- Prefer concise recommendations over long theoretical explanations.
- Make trade-offs explicit.
- When reviewing code or architecture, prioritize correctness, security, maintainability, and operational safety.
- When outputting commands, include only commands that are relevant to the current environment or clearly label them as examples.

## Output Contract

Always structure the final answer with these sections when applicable:

- API review
- Breaking risks
- Schema issues
- Security concerns
- Recommended contract

## Quality Bar

A strong result from this skill should be specific enough that a developer, reviewer, maintainer, or product owner can act on it without needing a second clarification round.
