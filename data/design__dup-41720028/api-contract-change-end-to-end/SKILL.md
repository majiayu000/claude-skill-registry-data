---
name: api-contract-change-end-to-end
description: Use this when changing REST endpoints so Rust DTOs, UI DTOs, OpenAPI, and docs stay in sync.
---

## Goal

Make API changes once, but keep all consumers consistent (CLI/server, UI, docs).

## Checklist

1) Locate the endpoint
- Routing/handlers: `src/routes.rs`, `src/api_server.rs`, `src/web_server.rs`

2) Update Rust contract types
- DTOs: `src/api_types.rs`
- If you adjust validation/errors, keep behavior consistent with existing API error shapes (`src/errors.rs`).

3) Update UI types + API client
- DTOs: `view/api/types.ts` (explicit note at top: aligned with `src/api_types.rs`)
- Calls: `view/api/client.ts`

4) Update OpenAPI + help docs
- REST schema: `docs/openapi.json`
- If it’s user-visible, update relevant guides under `docs/help/*` (often `docs/help/api-quick-reference.md`, plus the feature-specific page).

5) Add/adjust tests
- Rust behavior: `tests/*.rs` (integration-heavy, many use `assert_cmd`).
- UI behavior: `npm run test:ui` (Vitest).
- Cross-cutting behavior: consider adding/updating smoke coverage under `smoke/tests/`.

6) Verify locally (CI parity)
- `npm run lint`
- `npm test`
- `npm run smoke`

## Notes

- Treat this repo as “contract-synchronized”: changing just one of Rust/UI/OpenAPI will likely break users or tests.
- Prefer incremental changes that preserve backwards compatibility for existing clients when practical.
