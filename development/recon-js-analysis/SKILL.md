---
name: recon-js-analysis
description: >
  Mine JavaScript for endpoints, params, secrets, and hidden functionality. Load on SPAs, heavy
  JS apps, after crawling, or "analyze the JS". Signals: bundled JS (webpack/main.*.js), API
  calls in JS, source maps, /static/js, front-end frameworks.
domain: recon
type: technique
stability: learning
modes: [bugbounty]
severity: medium
mitre: [T1592.002]
tools: [katana, linkfinder, jsluice, subjs, source-map-explorer]
schema_version: 1
---

# JavaScript analysis

## When it applies
The app is JS-heavy (SPA). The front-end bundle is a map of the backend: it references API
endpoints, parameters, feature flags, roles, and sometimes secrets — much of it not linked in the UI.

## Why it works
Client code must know how to call the server, so endpoints/params are embedded in JS. Bundlers
also occasionally ship source maps (full original source) and developers leave keys/comments.

## Method
1. **Collect all JS**: `katana -jc`, `subjs`, or crawl; grab every `.js` (incl. lazy-loaded chunks).
2. **Extract endpoints/params**: `linkfinder`/`jsluice` pull URLs, paths, and param names from bundles.
3. **Hunt secrets & flags**: grep for `apiKey|token|secret|internal|admin|debug`, feature flags,
   and role checks done client-side (server may not enforce them → BOLA/BFLA leads).
4. **Source maps**: if `.map` files ship, reconstruct original source (`source-map` tools) → full whitebox-ish view.
5. **Feed results**: new endpoints → `api-*`; client-only auth checks → `api-bola`; secrets → validate.

## Gotchas
- Client-side "admin" gating usually isn't enforced server-side — test the endpoints directly.
- De-obfuscate/beautify minified bundles before grepping (`js-beautify`).
- Lazy-loaded chunks hide the juicy routes — enumerate all chunk files, not just `main.js`.

## Verify success
Endpoints/params/secrets extracted from JS that weren't in the UI — new, testable surface.

## References
LinkFinder/jsluice; katana; "JS recon" bug-bounty methodology.
