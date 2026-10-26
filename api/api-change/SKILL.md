---
name: api-change
description: "Propagates a FastAPI route or schema change to the generated TypeScript client and API docs. Use when editing apps/api/fastapi/src/**/router.py, routes.py, schemas.py or routers/, or when a web app needs a field or endpoint that @barrelsgd/api-client doesn't have yet."
---

# FastAPI Contract Change

This is the procedure the repo's own Blast-Radius Gate table names in one
cell ("A FastAPI route or schema → regen `openapi.json` → `pnpm
generate:api-client` → `pnpm check:drift`; `docs/api/contracts.md`") — this
skill is that cell, spelled out. `packages/api-client/src/gen/` is Never-tier
(mechanically blocked by `.claude/hooks/protect-files.mjs`) — you cannot hand-edit
around this procedure even if it would be faster.

## When this applies

Any edit under `apps/api/fastapi/src/**/router.py`, `routes.py`, `schemas.py`,
`schemas/`, or `routers/` (the same file patterns
`scripts/guardrails/check-blast-radius.mjs` treats as FastAPI contract files),
or `apps/api/fastapi/src/main.py`. Also applies in reverse: a web app needs a
field or endpoint `@barrelsgd/api-client` doesn't expose yet.

Compatible route and OpenAPI changes required by an authorized task can proceed
with the complete procedure below. Ask first for breaking contracts, widened
public access or permissions, or work outside the authorized scope, as defined
in `AGENTS.md`; do not request existing session authorization again.

## Procedure

1. **Make the FastAPI change** (route, schema, or model) in
   `apps/api/fastapi/src/`.
2. **Regenerate `openapi.json`** (from `apps/api/fastapi`):
   ```bash
   PROJECT_NAME='Barrels Grenada' uv run --frozen --package fast-back python -c "from src.main import app; import json; json.dump(app.openapi(), open('openapi.json', 'w'), indent=2)"
   ```
3. **Regenerate the TypeScript client** (from repo root):
   ```bash
   pnpm generate:api-client
   ```
4. **Verify no drift**:
   ```bash
   pnpm check:drift
   ```
   A failure here means step 2 or 3 was skipped or produced something
   inconsistent — fix forward, don't hand-edit `packages/api-client/src/gen/`
   to make drift-check pass.
5. **Update `docs/api/contracts.md`** if the change is a new endpoint, a
   breaking field change, or anything else that document already describes.
6. **Update every consumer** of the changed types/endpoints across the web
   apps — grep for the generated hook/client function name
   (`@barrelsgd/api-client`'s generated names follow the FastAPI
   operation ID). This is the Blast-Radius Gate step; `pnpm guardrails:staged`
   only checks that the contract-file change and a client regen both happened,
   not that every consumer was updated.
7. **Commit `openapi.json` and the generated client changes together** (per
   `docs/api/contracts.md`) — never split them across commits.

## Verification

- `pnpm check:drift` passes.
- `pnpm type-check` passes (a removed/renamed field surfaces here across every
  consuming app).
- `pnpm guardrails:staged` passes (checks the contract-file/client-regen
  pairing mechanically).
- Every consumer found in step 6 is updated, or explicitly reported to the
  user per the Scope Gate if it's outside what was asked.

## What NOT to do

- Don't hand-edit anything under `packages/api-client/src/gen/` — it's
  Never-tier and mechanically blocked.
- Don't regenerate the client without first regenerating `openapi.json` — the
  client would just re-encode the stale contract.
- Don't skip `docs/api/contracts.md` for a breaking change because "the code
  is the source of truth" — the doc is what the next agent (or the next
  session of you) reads before touching this surface again.
