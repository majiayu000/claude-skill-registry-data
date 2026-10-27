---
name: js-harvest
description: Crawl in-scope target, download every JS file + public sourcemap. Enumerates script tags, dynamic imports, webpack chunks, and .js.map siblings. Run after target-init when targets/<name>/raw/ is missing.
---

# js-harvest

## Purpose
Acquire every JavaScript asset the target ships, plus every sourcemap
that is publicly accessible, so later phases can analyze original
sources rather than minified bundles.

## Inputs
- `targets/<name>/status.json` with `scope.in` populated.

## Steps
1. Read scope. For each in-scope host, queue the bare host root as the
   first URL.
2. Use `chrome-devtools` MCP `navigate_page`, then
   `list_network_requests` and `evaluate_script` to enumerate:
   - every `<script src>` (including async/defer)
   - every dynamic `import()` (regex pass on inline JS as fallback)
   - every webpack chunk URL referenced by the first script
3. For each JS URL, fetch through chrome-devtools (so cookies + proxy
   apply). Save under `targets/<name>/raw/<host>/<path>.js`.
4. Sourcemap discovery for each JS:
   - `//# sourceMappingURL=...` pragma at file end
   - `SourceMap` / `X-SourceMap` response header
   - try `<url>.map` if pragma/header absent
5. Save discovered maps as siblings: `<path>.js.map`. If a map is
   referenced but returns 4xx, log to `status.json.harvest.missing_maps[]`.
6. Crawl follow-ups: respect a depth limit (default 2 hops on
   in-scope hosts only). Do not follow out-of-scope links — log them
   to `status.json.harvest.out_of_scope_skipped[]`.
7. Hidden-map + Sentry recon (T1.5). Run:
   ```
   python3 bin/sourcemap_recon.py targets/<name>
   ```
   This brute-forces common Webpack/Vite/Next/Nuxt hidden-map filenames
   next to each bundled `.js`, and pulls `.map` files from any in-scope
   Sentry release-artifact API. Brute-list and Sentry recipe are
   maintained in `wiki/tools/tlx/sourcemap-recon.md` (the spec). The
   script reads scope from `status.json.scope.in` and refuses
   out-of-scope hosts. Per-bundle attempt cap defaults to 40; 429s back
   off automatically. Sentry phase can be skipped with `--no-sentry`.

   After this phase, re-run `sourcemap-explode` to decode any newly
   recovered `.js.map` files into `targets/<name>/sources/`.

## Outputs
- `targets/<name>/raw/<host>/<path>.js[.map]`
- updated `status.json.phases.harvest`
- updated `status.json.phases.sourcemap_recon` (Step 7 only)

## Failure modes
- chrome-devtools MCP not responding → suggest `chrome-devtools-mcp:troubleshooting`.
- Auth-walled site (login redirect) → load Caido auth workflow first
  (`caido_login(workflow_id=...)`), then re-run.
- Hitting rate limits → back off; log; resume.
- `sourcemap_recon` 429-storm against a single host → script auto-pauses
  per attempt; if persistent, raise `--rate-limit-ms` (default 200) or
  drop `--max-attempts-per-bundle`.
- Sentry artifact API returns 401/403 (the common case for self-hosted
  with auth) → script silently skips; only misconfigured public
  instances enumerate.

## Result block
```json
"phases": {
  "harvest": { "status": "done", "ts": "<iso>",
    "files": N, "maps_public": M, "maps_missing": K,
    "hosts_seen": [...], "out_of_scope_skipped": [...] },
  "sourcemap_recon": { "status": "done", "ts": "<iso>",
    "bundles_processed": N, "maps_recovered": M, "maps_missing": K,
    "requests_total": R, "out_of_scope_hosts_skipped": [...],
    "sentry": { "hosts_seen": [...], "releases_enumerated": [...] },
    "found": [{ "url": "...", "saved_to": "...", "bundle": "..." }] }
}
```
