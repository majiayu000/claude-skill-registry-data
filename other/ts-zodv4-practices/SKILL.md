---
name: ts-zodv4-practices
description:
  Zod 4 validation and shared-contract practices for TypeScript. Use when writing, reviewing, or
  refactoring schemas, Zod 4 APIs, coercion, parsing, transforms, refinements, discriminated unions,
  or shared module contracts.
license: MIT
metadata:
  author: AutanaSoft
  organization: AutanaSoft
  version: '0.2.0'
  date: '2026-07'
---

# TypeScript Zod v4 Practices

Framework-independent Zod 4 validation and contract rules. Read the relevant atomic card in
`references/`.

## When to Apply

- Write, review, or refactor Zod 4 schemas.
- Validate external APIs, forms, environment variables, or payloads.
- Choose parsing behavior, model transforms, refinements, unions, or nullability.
- Organize contracts shared between modules, applications, and persistence.

## Rule Categories by Priority

| Priority | Category                   | Impact | Prefix       |
| -------- | -------------------------- | ------ | ------------ |
| 1        | Zod 4 API and parsing      | HIGH   | `zod-`       |
| 2        | Shared contract boundaries | HIGH   | `contracts-` |

## Quick Reference

- Zod 4 API and parsing: `zod-use-top-level-validators`, `zod-customize-errors-with-error`,
  `zod-derive-types-in-schema-owner`, `zod-use-input-output-for-transforms`,
  `zod-choose-parse-or-safe-parse`, `zod-limit-coercion-to-boundaries`,
  `zod-model-nullability-explicitly`, `zod-prefer-discriminated-unions`,
  `zod-compose-existing-schemas`, `zod-keep-refinements-pure`, `zod-keep-transforms-pure`
- Shared contract boundaries: `contracts-assign-canonical-owner`,
  `contracts-import-canonical-schema-and-type`, `contracts-keep-infrastructure-out-of-schemas`,
  `contracts-separate-application-and-persistence`, `contracts-export-schema-and-type-public-api`

## How to Use

Read the applicable card: `references/<prefix>-<slug>.md`.
