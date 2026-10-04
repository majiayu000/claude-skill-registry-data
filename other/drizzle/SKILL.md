---
name: drizzle
description: Drizzle ORM patterns + database migration workflows
category: DB
level: library
engineer: db-engineer
gate: "bunx drizzle-kit check"
bundles: []
allowed-tools: Read, Glob, Grep
---


# Drizzle

Composition metadata carrier — frontmatter is the product (see
`commands/apply/references/skill-metadata-schema.md`). Body intentionally minimal. Do not
delete: `compose_stack` hard-fails without this registration.

For full schema design + query patterns, see `database-schema-designer`. For T3-monorepo wrapping
(turbo task, package layout), see `t3-code-patterns` § Database. For the migration-based-only
policy (never `db:push`), see `drizzle-best-practices` § Migration Safety.
