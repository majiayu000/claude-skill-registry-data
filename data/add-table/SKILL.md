---
name: add-table
description: Add a new database table and generate all six layers. Use when adding a new entity to the platform.
user-invocable: true
disable-model-invocation: true
allowed-tools: Read, Edit, Write, Bash, Grep, Glob
---

Add a new entity to the platform by working bottom-up through all six layers.

Entity name: $0

## Process

1. **Layer 1 — Schema**: Add the table definition to `src/lib/database/schema.ts` following existing patterns. Include `organization_id` for multi-tenant scoping. Use appropriate column types matching existing conventions.
2. **Layer 2 — Zod**: Run `pnpm generate:schemas` then `pnpm contracts:check`
3. **Layer 3 — Services**: Run `pnpm generate:services` then `pnpm services:check`
4. **Layer 4 — Routes**: Run `pnpm generate:routes` then `pnpm routes:check`
5. **Layer 5 — Hooks**: Run `pnpm generate:hooks` then `pnpm hooks:check`
6. **Layer 6 — UI**: Run `pnpm generate:ui` then `pnpm ui:check`

## Rules

- Validate each layer before proceeding to the next
- If any layer fails, fix it before continuing (always fix at the source layer)
- Never modify a lower layer to satisfy an upper layer's needs
- After all layers pass, run `pnpm drizzle:gen` to create the migration
- Do not run `pnpm drizzle:push` without explicit user confirmation
