---
name: wu-inpage-unicode-api
description: Implement or review WU-API-001 — the InPage↔Unicode npm package and beta developer API for WriteUrdu. Wraps the existing js/inpage-unicode-core.js engine for external distribution; does not touch the browser tool, the mapping tables, or any WU-PLAT-002H activation surface.
---

# WriteUrdu InPage↔Unicode developer API & npm package

Read first:

1. `specs/WU-API-001-inpage-unicode-developer-api.md`
2. `docs/WU-API-001A-INPAGE-UNICODE-NPM-BETA-IMPLEMENTATION-PLAN-2026-09-06.md`
3. `specs/archive/implemented/WU-TOOLS-EXPANSION-005-inpage-unicode-converter.md`
4. `docs/WU-INPAGE-MAPPING-RESEARCH-2026-08-17.md`
5. current `js/inpage-unicode-core.js` and `tests/inpage-unicode-core.test.js`
6. one existing public POST route for house style: `functions/api/document-translate.js`

## Core rule

**This is a distribution wrapper, not a new engine.** The mapping tables and conversion functions in `js/inpage-unicode-core.js` are the single source of truth. Never fork, duplicate, or re-derive the mapping tables in the npm package or the API route — both must call the same module.

This work is a documented, founder-approved exception to the `BACKLOG.md` P0.1 feature-breadth freeze (see spec §3). It must stay isolated: do not touch the Basic/Rich Editor, mobile viewport code, activation telemetry, or any file under active `WU-PLAT-002H` review. If a step here starts requiring changes to one of those files, stop — that means the isolation assumption broke and this needs re-filing under normal backlog review, not a workaround.

## Step 1 — verify the module boundary before writing anything

Confirm whether Cloudflare Pages Functions' build can `import` `js/inpage-unicode-core.js`'s UMD export directly (CJS interop). If it cannot:

- add a small `functions/lib/inpage-unicode.mjs` that re-exports the same functions;
- it must call into the existing module, not redefine mapping tables.

Do the same check for npm packaging: the UMD wrapper already supports `require()` (`module.exports`), so packaging should need no logic changes — only `package.json` + `README.md`.

## Step 2 — npm package (ship first; no server, no cost, no risk)

- New `package.json` for `@write-urdu/inpage-unicode` — `main` points at the existing core file (or the `.mjs` re-export from Step 1); zero new dependencies.
- README: both-direction usage examples, explain `converted`/`unsupported`/`warnings` fields, link to the live browser tool and (later) the hosted API.
- npm scope/org and license are resolved: published under the `write-urdu` org, MIT licensed (see `packages/inpage-unicode/LICENSE`). Keep both in sync on any future version bump.
- Do not publish until `tests/inpage-unicode-core.test.js` passes against the packaged entry point exactly as it does today.

## Step 3 — beta API route

New route: `functions/api/v1/inpage-unicode/convert.js` (first route under a `/v1/` namespace in this repo — don't retrofit existing routes into it).

Required shape, matching this repo's existing house style (see `document-translate.js`), not another repo's:

- `env.INPAGE_API_ENABLED !== 'true'` → 503, same kill-switch convention as `DOCUMENTS_ENABLED`/`AUTH_ENABLED`.
- Single shared bearer secret `INPAGE_API_BETA_SECRET`, constant-time compare — write a small local helper, do not port one from another repo.
- CORS: this is the first cross-origin route in the repo — add explicit `Access-Control-Allow-Origin`/`-Methods`/`-Headers` and an `onRequestOptions` handler. Every other `/api/*` route is same-origin only; do not add CORS to those by copy-paste, and do not skip it here.
- Body-size cap and text-length cap enforced before parsing further (mirror `document-translate.js`'s guard order: declared `Content-Length` first, then actual body length).
- Response passes through `decodeLegacyText`/`encodeUnicodeText`'s existing return fields (`text`, `converted`, `unsupported`, `warnings`, `profile`) — do not re-shape them into a different envelope.
- Errors as `{ ok: false, error: '<snake_case_code>' }`, matching every other route in `functions/api/` — do not import another project's error-code vocabulary (e.g. InvoiceCraftly's `SCREAMING_SNAKE` enum).
- Never log or persist request/response text, matching the rule already enforced on `functions/lib/documents.mjs`.

## Step 4 — tests

- Leave `tests/inpage-unicode-core.test.js` untouched — it stays the engine's source of truth regardless of how the API/package wraps it.
- Add `tests/inpage-unicode-api-contract.test.js`: static source assertions (kill switch present, bearer check present, no console logging, CORS headers present, delegates to the shared engine rather than a duplicated map) plus a runtime handler test with a fake `Request`/`env` covering: missing/wrong secret → 401; oversized body → 413; malformed JSON → 400; both conversion directions → 200 with the expected fields.
- Add the new test file to `scripts/run-contract-tests.js`'s list.
- Run full `npm test` before considering this done — zero regression on the existing browser tool's contract test.

## Step 5 — cross-sell surface (marketing, not engineering)

- Add a small "Use this via API →" link/section on the existing `/tools/inpage-unicode-converter/` page, pointing at a short reference doc for the new route/package. Keep it out of the active-writing/editor surfaces — this is a tools page, not a P0.1-governed activation surface.
- Do not create a full developer-portal page in this slice (non-goal, spec §6).

## Rollback

Set `INPAGE_API_ENABLED=false`. The npm package is unaffected (it has no server dependency). The browser tool and its existing route are never touched by this work, so nothing here can regress them.

## Stop conditions

Stop and fix if:

- the mapping tables get duplicated or diverge between the package, the API route, and the browser tool;
- any change touches `js/inpage-unicode-core.js`'s existing exported behavior, or `tests/inpage-unicode-core.test.js` needs to change to keep passing;
- the new route becomes same-origin-only (defeats the point), or CORS leaks onto an existing internal route;
- request/response text is logged anywhere;
- work expands into real API keys, a Durable Object, billing, or a full docs portal — those are explicitly out of scope until Phase A/B show real usage (spec §11).
