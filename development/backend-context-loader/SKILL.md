---
name: backend-context-loader
description: "Load the minimal Cookmate backend context fast. Use only for backend tasks to avoid repeated discovery: Prisma schema, domain modules, repositories, route patterns, shared route helpers."
---
# Context Loader (Cookmate backend)

Goal: cut token/time spent rediscovering the repo. Load these in order, skim only what’s needed.

## Quick sequence
1) Prisma model source: `apps/api/prisma/schema.prisma`.
2) Domain modules: `packages/domain/src/**` (check entity folders + `index.ts` exports).
3) Repositories: `apps/api/src/infra/db/repositories/**` (map to models/domains).
4) Route patterns: `apps/api/src/interfaces/http/routes/collections/**` (+ `collections/members` for sub-entity prefixing).
5) Shared libs: `apps/api/src/shared/lib/route/**`, `apps/api/src/shared/utils/handle-error.ts`, `apps/api/src/shared/enums/http-status.enum.ts`.

## Fast commands (prefer to keep context small)
- List files quickly: `rg --files apps/api/src/interfaces/http/routes/collections`
- Search patterns: `rg "CollectionEntity" apps/api/src`
- Preview: `sed -n '1,160p' path`

## Notes
- Sub-entities: use `collections/members` as the reference for prefixes (`/:parentId/...`).
- Stay concise: only open files relevant to the task; avoid full dumps.
