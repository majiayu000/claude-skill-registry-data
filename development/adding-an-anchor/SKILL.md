---
name: adding-an-anchor
description: Use when adding a new anchor integration to this project — creating an anchor client, its server singleton, API wrappers, proxy routes, and flow pages, or deciding whether a new anchor belongs in ANCHORS vs HONORABLE_MENTIONS.
---

# Adding a new curated anchor

Each curated anchor owns its own client, server-side instance singleton, client-side API wrapper, API routes, and bespoke flow pages. Nothing is shared — see the per-provider isolation decision in `CLAUDE.md`.

1. **`src/lib/anchors/<name>/{client,types,index}.ts`** — shaped however the anchor's API actually works. No interface to satisfy. Define your own error class. Include the `debug?: boolean` flag described in `CLAUDE.md` and cover both logging behaviors with tests.
2. **`src/lib/server/<name>Instance.ts`** — singleton getter reading env vars, passing `debug: dev` from `$app/environment`.
3. **`src/lib/api/<name>.ts`** — client-side fetch wrappers per route. Mirror the per-provider shape in `etherfuse.ts` / `testanchor.ts`.
4. **`src/routes/api/anchor/<name>/<operation>/+server.ts`** — one route per operation.
5. **`src/routes/anchors/<name>/+page.svelte`** (landing) and `<name>/<flow>/+page.svelte` per flow. Compose primitives from `src/lib/components/`. Use `AnchorRegionSelector` for the region section. Don't try to share flow logic with another anchor in this PR — let it duplicate.
6. Add the provider to `src/lib/constants.ts` (`PROVIDER`).
7. Add to `src/lib/config/anchors.ts` (`ANCHORS`).
8. Add to `src/lib/config/regions.ts` if the anchor serves a region.
9. Add tests under `tests/anchors/<name>/`.
10. Document in `src/lib/anchors/<name>/README.md`.

## If it doesn't clear the bar

Add it to `HONORABLE_MENTIONS` in `src/lib/config/anchors.ts` instead — no client code needed. Give it a `scorecard` (via `makeCriteria`) so its gaps render. For a candidate you're still researching rather than rejecting, use the `assessing-an-anchor` skill.

## Adding SEP support

If the anchor needs a SEP this project doesn't implement yet: create `src/lib/anchors/sep/sep<N>.ts` modeled on the existing modules (pure functions, optional `fetchFn`), add types to `sep/types.ts`, export from `sep/index.ts`, and cover it under `tests/anchors/sep/`.
