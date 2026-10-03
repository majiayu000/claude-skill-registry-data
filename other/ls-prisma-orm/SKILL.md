---
name: ls-prisma-orm
description: Guide Prisma ORM work. Use for schema design, Prisma Client, migrations,
  Postgres setup, upgrades, driver adapters, and query review.
metadata:
  version: '1.0'
extensions:
  external_skill:
    source_kind: native-reference
    source_url: https://github.com/prisma/skills
    source_path: prisma-client-api/SKILL.md
    source_commit: dc08577cacd642af075e1017f0f7fe93177b06b4
    source_ref: main
    source_sha256: 47ea4fb63fe45534872026f59ed937a6b7fda83a3d7ef95710b0d84e4bbeb905
    license: MIT
    import_date: '2026-07-03'
    vetting_status: provenance-recorded-no-bundled-tooling-executed
---

# Prisma Orm

Use this skill when working on Prisma ORM tasks.

## Workflow

- Inspect `schema.prisma`, migrations, generated client, database provider, and package versions before edits.
- Plan migrations with rollback/data-safety expectations and run generation/tests after schema changes.
- Avoid leaking database URLs and production data in examples, logs, or generated artifacts.

## Boundaries

- Inspect the target repository before making changes.
- Prefer existing project patterns, declared package managers, and documented validation commands.
- Do not expose secrets, credentials, private user data, or production account identifiers in source, examples, or logs.
- When external APIs or current vendor behavior matter, verify against official docs before implementation.

## Provenance

- Source: `https://github.com/prisma/skills`
- Ref: `main` at `dc08577cacd642af075e1017f0f7fe93177b06b4`
- Source path: `prisma-client-api/SKILL.md`
- License classification: `MIT`
- Source SHA-256: `47ea4fb63fe45534872026f59ed937a6b7fda83a3d7ef95710b0d84e4bbeb905`
