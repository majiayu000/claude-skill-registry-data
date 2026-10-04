---
name: backend
description: Build backend services — APIs, server logic, persistence, queues, and integration with other systems.
category: development
aliases:
- server
- api-server
- backend-dev
triggers:
- build a backend
- backend dev
- write an API
- server side
keywords:
- backend
- server
- api
- rest
- graphql
- persistence
- queue
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
author: Mr-Nobody-Anonymous
tags:
- api
- backend
- development
- rest
- server
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# Backend

## Purpose

Build and reason about backend services: HTTP APIs, persistence, async work, authentication,
and integration with other systems.

## Source

Custom skill, written for this library.

## Notes

Pairs with `architecture`, `databases`, `secure-coding`.

## When to Use

Use when the request matches the documented backend capability or its declared triggers.

## When NOT to Use

Do not use when the request is outside this capability, required context is unavailable, or a safer specialized skill applies.

## Capabilities

- Apply the backend workflow consistently.
- Produce a clear, reviewable result.
- Surface assumptions, constraints, and unresolved risks.

## Inputs

- The user's goal and desired output.
- Relevant source material, constraints, and environment details.
- Acceptance criteria when available.

## Workflow

1. Confirm the goal, scope, and constraints.
2. Inspect the available context before acting.
3. Apply the skill-specific guidance in this document.
4. Verify the result and report limitations or next steps.

## Tools

- No mandatory tool unless declared in frontmatter.
- Use only project-approved tools and documented optional dependencies.

## Examples

Requests that should activate this skill include: "build a backend"; "backend dev"; "write an API".

## Safety

- Preserve user data and existing work.
- Confirm before destructive or externally visible actions.
- Do not expose credentials or claim unverified results.
