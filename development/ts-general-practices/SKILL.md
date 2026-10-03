---
name: ts-general-practices
description:
  Framework-independent TypeScript practices. Use when writing, reviewing, or refactoring type
  safety, type-only imports, generics, utility types, or unknown-data boundaries.
license: MIT
metadata:
  author: AutanaSoft
  organization: AutanaSoft
  version: '0.1.0'
  date: '2026-05'
---

# TypeScript General Practices

Framework-independent TypeScript rules. Read the relevant atomic card in `references/` before
applying a convention.

## When to Apply

- Write or review TypeScript in an application, package, or monorepo.
- Refactor type safety, imports, generics, or unknown-data boundaries.

## Rule Categories by Priority

| Priority | Category               | Impact | Prefix |
| -------- | ---------------------- | ------ | ------ |
| 1        | TypeScript type safety | HIGH   | `ts-`  |

## Quick Reference

- Avoid `any` at unknown-data boundaries - `ts-avoid-any-at-unknown-boundaries`
- Derive types from runtime values - `ts-derive-types-from-runtime-values`
- Extract reusable object shapes - `ts-extract-reusable-object-shapes`
- Use type-only imports - `ts-use-type-only-imports`
- Use generics and utility types - `ts-use-generics-and-utility-types`

## How to Use

Read the applicable card: `references/ts-<slug>.md`.

## Full Compiled Document

Read `references/agent-context.md` for the compiled guide.
