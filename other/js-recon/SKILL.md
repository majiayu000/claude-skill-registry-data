---
name: js-recon
description: Analyze JavaScript bundles from any web app for API endpoints, GraphQL operations, hardcoded secrets, internal service hosts, per-environment config maps (prod/staging/QA), and admin/debug surface. Use whenever the user says "scan JS files", "analyze JS bundles", "analyze all JS", wants endpoints/secrets/API keys extracted from frontend code, or asks what an app's JS reveals — including single files, URL lists, whole SPAs, or static data catalogs.
---

# JS Recon Analyzer

Extract maximum intelligence from frontend JavaScript with zero requests to the target beyond the JS files themselves (they're public static assets).

## Workflow

1. **Collect bundle URLs.** Sources, in order of value: page HTML `<script src>` + `modulepreload` links, microfrontend manifests (`/micro-frontends/*/manifest.json`, import maps), URLs seen in proxy history, **wayback CDX hits** (archived bundles reveal endpoints the current build dropped), and the app's entry shims — **entry files often import bigger chunks** (`import"./vendor-XXX.js"`). Follow imports one level deep; the main logic hides in vendor/route chunks, not the 1KB entry shim. Also check for static data files: some sites ship whole catalogs as JS (`data/catalog.js` setting `window.SOMETHING=[...]` — one 5MB file can contain the entire dataset).
2. **Download** each bundle once to a local `js/` dir (static CDNs are usually not WAF-protected; app hosts might be — see curl_cffi note in bb-pipeline).
3. **Mine** with `scripts/mine_js.py js/*.js` — extracts, grouped:
   - REST/GraphQL path strings (quoted and backticked, with `${}` → `{ID}` normalization)
   - GraphQL `query`/`mutation` operation names
   - Secret patterns: AKIA*, AIza*, sk_live, private key blocks, raw JWTs, `pub…` Datadog client keys (flag as public-by-design)
   - Internal hosts: `*.svc.cluster.local`, `internalUrl`/`internalHost` values, RFC1918/hostnames that shouldn't be client-side
   - String-concatenation bases (e.g. `CUSTOMER_BASE_PATH` constants) — grep 200 chars of context to find the appended suffixes
4. **Build the dictionary**: normalize to `{ID}`-parameterized paths, group by service prefix, count occurrences. This becomes the endpoint test list for Phase 4 — not a fuzz wordlist.

## Deep passes beyond the extractor (do these manually on big finds)

- **Config object mining**: search for `ApiUrl:"`, `baseUrl:`, `authUrl`, `kycApiUrl`, `gateway` assignments — one bundle's config block often maps the whole per-region/per-tier topology (prod/staging/qa/sandbox hosts + feature toggles). Staging/QA hosts found this way are new attack surface; resolve + fingerprint them.
- **Auth-model reconstruction**: find the header-builder function (e.g. `const Ke=()=>{...Authorization:Bearer...}`) — does it add auth only-if-authenticated? Then anonymous calls are expected somewhere: find which resources the anonymous flow touches (lead vs signup tracks) — that's the pre-auth attack surface.
- **URL-concat sites**: for each API base var, locate `.concat(` and template-literal uses to recover the full endpoint shapes (path params, query params like `?searchTerm=`).
- **Turnstile/proof gates**: note where the app attaches bot-proof headers (`cf-turnstile-token`) — those endpoints are script-hostile; plan the browser-pass for them instead of curl.

## Reading the results (what history says matters)

- **Version numbers**: endpoints appear per TLD/environment with different versions — probing `v{n-1}`/`v{n+1}` on each service occasionally exposes legacy versions (expect mostly 404; log it and move on).
- **GraphQL operation names** are an API map without auth: mutations reveal state-changing surface (e.g. `updateCompanyDetails`, `uploadCompanyDocuments`) — the authz test plan writes itself.
- **i18n keys and component names** (`addressesEditAddress`, `OrderDetails`) reveal features whose backing endpoints you should hunt in route chunks.
- **Env-var remnants** (`VITE_*`) leak BFF path maps and feature flags.
- Zero secrets is the common case on mature programs — say so plainly and move on; the path dictionary is the real prize.

## Rules

- Never execute or eval extracted code; strings are data only.
- Treat extracted endpoints as leads — every one still needs an authorized test before it means anything.
- If the target's app host blocks scripted downloads (Cloudflare JA3), use `curl_cffi` with `impersonate="chrome"`/`"edge"`, or have the user's browser fetch and save the files.
