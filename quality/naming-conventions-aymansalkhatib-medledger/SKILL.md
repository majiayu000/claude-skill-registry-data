---
name: naming-conventions
description: Source of truth for naming — folders, files, classes, methods, DTOs, DB tables/columns/indexes, HTTP paths, migrations. Use when creating, renaming, or reviewing names. Triggers "/naming-conventions", "rename", "is this name correct".
user-invocable: true
argument-hint: '[check <path>] | [propose <thing>] | [show <category>]'
allowed-tools: Read, Grep, Glob
---

# Naming Conventions

Source of truth for every name in this codebase. If a rule here conflicts with an older file, **the file is wrong** — open a renaming PR.

## Quick Reference

| Thing                   | Case               | Number   | Example                                       |
| ----------------------- | ------------------ | -------- | --------------------------------------------- |
| Module folder           | `kebab-case`       | plural   | `src/modules/holdings/`                       |
| Sub-folder              | `kebab-case`       | plural   | `controllers/`, `dto/`, `entities/`           |
| File name               | `kebab-case`       | singular | `holding.entity.ts`, `create-transfer.dto.ts` |
| Class                   | `PascalCase`       | singular | `HoldingEntity`, `CustodyController`          |
| Interface (DI contract) | `PascalCase` + `I` | singular | `IWebhookDispatcher`                          |
| Type alias              | `PascalCase`       | singular | `LedgerDelta`, `DoseWindow`                   |
| Enum type               | `PascalCase`       | singular | `ErrorCode`, `AuditEventType`                 |
| Enum member             | `UPPER_SNAKE`      | —        | `ErrorCode.INSUFFICIENT_STOCK`                |
| Function / method       | `camelCase`        | verb     | `findById`, `recordAdministration`            |
| Variable / property     | `camelCase`        | noun     | `holdingId`, `recordedAt`                     |
| Boolean                 | `camelCase`        | `is/has` | `isReplayed`, `hasVariance`                   |
| Constant (truly global) | `UPPER_SNAKE`      | —        | `DOSE_WINDOW_HOURS`                           |
| DB table                | `snake_case`       | plural   | `holdings`, `ledger_entries`                  |
| DB column               | `snake_case`       | singular | `holding_id`, `created_at`, `dose_mg`         |
| DB FK column            | `<entity>_id`      | singular | `holding_id`, `drug_id`                       |
| DB enum type            | `<col>_enum`       | singular | `audit_event_type_enum`                       |
| DB index                | `idx_<tbl>_<cols>` | —        | `idx_administrations_patient_id`              |
| DB unique index         | `uq_<tbl>_<cols>`  | —        | `uq_idempotency_keys_key`                     |
| Migration class         | `PascalCase`       | —        | `CreateLedgerSchema1747600000001`             |
| HTTP path segment       | `kebab-case`       | plural   | `/custody/transfers`, `/administrations`      |

The rule: **plural for collections (folders, tables, URL paths); singular for the thing itself (class, file, column).**

## Reserved verbs (do not invent synonyms)

| Concept          | Verb                                                                          | Not                              |
| ---------------- | ----------------------------------------------------------------------------- | -------------------------------- |
| Read one         | `findById`, `findOne`                                                         | `get`, `fetch`, `lookup`, `read` |
| Read many        | `findAll`                                                                     | `list`, `getMany`, `index`       |
| Read or 404      | `findByIdOrFail`                                                              | `getOrThrow`, `requireById`      |
| Predicate        | `is<State>`, `has<Thing>`                                                     | `check`, `verify`                |
| Throw-on-failure | `assert<Constraint>`                                                          | `validate`, `ensure`             |
| Create draft     | `create` (repo)                                                               | `build`, `make`                  |
| Persist          | `save` (repo)                                                                 | `store`, `persist`               |
| Update           | `update` (svc) / `mergeAndSave` (repo)                                        | `edit`, `modify`                 |
| Remove           | `remove` (controller) / `delete` (svc) / `deleteById` (repo)                  | `destroy`, `purge`               |
| Domain action    | domain verb: `transfer`, `administer`, `waste`, `reconcile`, `replay`, `seed` | `process`, `handle`              |

## Details

- Folders, files, classes, interfaces, types, enums, variables → @code-naming.md

Other categories (methods, DTOs, DB columns, routes) are covered by the Quick Reference + Reserved verbs tables above.

## When in doubt

1. Find an existing analogous thing in the codebase — copy its shape.
2. Check this document.
3. Open the PR with the proposed name and a one-line rationale.

Prefer **rename now** over **let it accumulate** — every additional caller makes the rename more expensive.

## Skill usage modes

`/naming-conventions [arg]`:

- `check <path>` — read the file, report each name that violates a rule, cite rule + proposed name. No edits.
- `propose <thing>` — given a short description, output the proposed file path, class name, method names, table/column names. No files written.
- `show` — print `code-naming.md` (folders, files, classes, enums, variables).
- No args — print the Quick Reference table and stop.

Never apply renames silently. Renames cascade — run a project-wide report first and confirm scope with the user before editing.
