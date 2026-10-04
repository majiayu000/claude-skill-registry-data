---
name: type-safety-chain
description: Implements or verifies the six-layer chain from Drizzle schema through Zod, services, API routes, and React hooks. Use when regenerating after DB changes, fixing alignment scripts, or bootstrapping the same architecture in a new folder.
---

# Type safety chain (Cursor)

## Canonical source

All phases, SQL for Supabase MCP verification, generator script behavior, and layer rules are in **`.claude/skills/type-safety-chain/SKILL.md`**. Open and follow that file for any non-trivial chain work.

## Quick reference

| Layer | Location |
|-------|-----------|
| 1 DB schema | `src/lib/database/schema.ts` |
| 2 Zod | `src/lib/schemas/` |
| 3 Services | `src/lib/services/simplified/` |
| 4 Routes | `src/app/api/simplified/` |
| 5 Hooks | `src/hooks/simplified/` |
| 6 UI | `src/components/simplified/` (optional; `pnpm validate:all:with-ui`) |

Run `pnpm validate:all` after regenerating (layers 1–5). Use **`pnpm validate:all:with-ui`** when Layer 6 exists. Docs: **`_docs/_build/architecture/type-safety-chain.md`**, **`_docs/_build/type/README.md`**. Error-check workflow: **`.cursor/skills/validate/SKILL.md`**.

If Supabase MCP is available, use it to compare live tables to `schema.ts` as described in the Claude skill.

**Multi-tenant:** After schema or seed changes, confirm `organization_id` columns and tenant-scoped data per org. Canonical rules: **`.cursor/rules/multi-tenancy.mdc`** and the **Multi-tenancy** section in **`.claude/skills/type-safety-chain/SKILL.md`**.
