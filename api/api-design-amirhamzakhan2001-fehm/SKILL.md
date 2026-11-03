---
name: api-design
description: REST API design patterns including resource naming, status codes, pagination, filtering, error responses,
  versioning, and rate limiting for production APIs. Use when designing or reviewing REST endpoints, resource names,
  status codes, pagination, or versioning.
category: backend
sources:
- repository: ecc
  original_path: skills/api-design/SKILL.md
  sha256: bfae53167acc91caff0ff9ab73a80ee3fd92caccdfa445c88302c3bf95255156
principles:
- core/think-before-coding
- core/simplicity-first
- core/surgical-changes
- core/goal-driven-execution
---

> **Library use:** Apply the [compatibility and execution contract](../../COMPATIBILITY.md). Source roles, memory claims, command names, hooks, and integrations are instructions or prerequisites—not installed capabilities.

# Api Design

REST API design patterns including resource naming, status codes, pagination, filtering, error responses, versioning, and rate limiting for production APIs. Use when designing or reviewing REST endpoints, resource names, status codes, pagination, or versioning.

## Required procedure

Read [the complete methodology](references/methodology.md) before performing this skill. It retains the full procedure, examples, constraints, and failure handling.

Procedure topics: API Design Patterns; When to Activate; Resource Design; URL Structure; Resources are nouns, plural, lowercase, kebab-case; Sub-resources for relationships; Actions that don't map to CRUD (use verbs sparingly); Naming Rules; GOOD; BAD; HTTP Methods and Status Codes; Method Semantics; Status Code Reference; Success.

## Related skills and principles

- [core/goal-driven-execution](../../core/goal-driven-execution/SKILL.md)
- [core/simplicity-first](../../core/simplicity-first/SKILL.md)
- [core/surgical-changes](../../core/surgical-changes/SKILL.md)
- [core/think-before-coding](../../core/think-before-coding/SKILL.md)

## Source provenance

- `ecc/skills/api-design/SKILL.md`
