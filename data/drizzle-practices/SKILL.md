---
name: drizzle-practices
description:
  Drizzle ORM persistence practices. Use when writing, reviewing, or refactoring schemas,
  migrations, transactions, persistence contracts, or data access.
license: MIT
metadata:
  author: AutanaSoft
  organization: AutanaSoft
  version: '0.1.0'
  date: '2026-05'
---

# Drizzle Practices

Rules for Drizzle ORM schemas, persistence contracts, migrations, transactions, and data access.

## When to Apply

- Work with Drizzle schemas, relationships, migrations, or persistence contracts.
- Refactor data-access boundaries, repositories, transactions, or database clients.

## Rule Categories by Priority

| Priority | Category         | Impact | Prefix |
| -------- | ---------------- | ------ | ------ |
| 1        | Database and ORM | HIGH   | `db-`  |

## Quick Reference

- Organize application Drizzle access - `db-organize-app-drizzle-access`
- Define Drizzle schema contracts in the database module - `db-define-drizzle-schema-contracts`
- Use transactions - `db-use-transactions`
- Use versioned migrations - `db-use-versioned-migrations`

## How to Use

Read the card that applies: `references/db-<slug>.md`.
