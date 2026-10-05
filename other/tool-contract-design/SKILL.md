---
name: tool-contract-design
description: Use when defining or reviewing tool interfaces, skill payloads, executor-facing contracts, and structured request-response shapes in PonyBunny.
---

# Tool Contract Design

## Use this skill when
- adding a tool
- changing a payload schema
- reviewing request/response design
- diagnosing tool mismatch bugs

## Goals
- make tool usage explicit
- reduce ambiguity
- improve validation
- support safe execution and auditability

## Process
1. Define the tool purpose.
2. Define caller expectations.
3. Define input schema.
4. Define output schema.
5. Define error schema.
6. Define side effects.
7. Define audit fields.
8. Define compatibility concerns.

## Output contract
Return:
- purpose
- request schema
- response schema
- error schema
- side-effect notes
- validation rules
- compatibility notes
