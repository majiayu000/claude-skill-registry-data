---
name: openapi-codegen
description: How to consume a new backend API surface via Orval-generated OpenAPI clients — only relevant once the project has a real OpenAPI spec to generate from.
disable-model-invocation: true
---

This template ships with a hand-written mock API (`src/mocks/handlers.ts`, MSW) and no OpenAPI
spec — this skill only becomes relevant once the project this template was cloned into has a
real backend with a published OpenAPI document. It is manual-invocation-only (`/openapi-codegen`)
so it never loads by accident while there is nothing to generate from.

When there is a real spec:

1. Add `orval` (already pinned as a compatible default in `docs/CUSTOMIZING.md`) and an
   `orval.config.ts` pointing at the spec (a URL or a committed `.json`/`.yaml` file).
2. Generate into `src/lib/generated/` (gitignored or committed — decide per project; committing
   makes diffs reviewable, gitignoring keeps CI as the source of truth) — configure Orval's
   `client` output mode to `react-query` so it emits `useQuery`/`useMutation` hooks directly,
   consistent with the `server-state-tanstack-query` skill's conventions.
3. Never hand-edit a generated file — if the generated hook shape doesn't fit a call site,
   wrap it in a thin hand-written hook in `src/lib/queries.ts` instead.
4. Re-run generation as a `pnpm` script (`orval`) wired into `scripts/verify.sh`'s typecheck
   step's prerequisites if the project's CI needs generated types to be fresh — otherwise
   generation is a manual step run when the spec changes.
5. Validate the generated response shape against a Zod schema at the boundary if Orval's
   output doesn't already do so — Orval generates TypeScript types, not runtime validation, by
   default.
