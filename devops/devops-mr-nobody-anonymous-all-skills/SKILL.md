---
name: devops
description: DevOps practices — CI/CD, infrastructure, deployment, observability, and incident response.
category: development
aliases:
- ci-cd
- deploy
- sre
- ops
triggers:
- set up CI
- deploy this
- infrastructure help
- CI/CD
- devops
keywords:
- devops
- ci
- cd
- deploy
- pipeline
- observability
- incident
- sre
dependencies: []
risk: medium
version: 1.0.0
source: custom
enabled: true
author: Mr-Nobody-Anonymous
tags:
- deploy
- development
- devops
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

# DevOps

## Purpose

Help the user with DevOps: CI/CD pipelines, infrastructure-as-code, deployments,
observability, and incident response.

## Safety

- Never write secrets into pipelines
- Confirm before destructive deploy actions
- Pin third-party action versions

## Source

Custom skill, written for this library.

## Notes

Pairs with `github`, `secure-coding`, `architecture`.

## When to Use

Use when the request matches the documented devops capability or its declared triggers.

## When NOT to Use

Do not use when the request is outside this capability, required context is unavailable, or a safer specialized skill applies.

## Capabilities

- Apply the devops workflow consistently.
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

Requests that should activate this skill include: "set up CI"; "deploy this"; "infrastructure help".
