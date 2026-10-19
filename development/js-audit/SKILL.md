---
name: js-audit
description: The deep JavaScript bundle auditor for bug bounty — extracts and interprets REST endpoints by function group, GraphQL operations, auth/authz mechanisms, hidden/debug/admin endpoints, upload surface, WebSockets, secrets, third parties, and business-logic signals, then maps them to concrete vulnerabilities (SQLi-prone spots, mass assignment, missing server-side validation, auth weaknesses, UI-only authz, client-controlled identity headers, input-validation bypass, rate-limit gaps) and emits manual testing steps. Use whenever the user says "analyze js files", "audit the JS", "deep JS analysis", "what's in the bundles", wants the full 10-section attack-surface report, or hands over any SPA/front-end during recon. Distinct from js-recon (harvesting) — this is the interpretation and attack-plan layer.
---

# JS Audit — Deep Bundle Analysis → Attack Plan

Two layers exist: **js-recon** harvests bundles and builds the endpoint dictionary. **js-audit** (this skill) runs the deep interpreter over collected bundles and produces the full attack-surface report with manual next steps. Run js-recon first (or point js_audit directly at files/URLs).

## Run the engine

```bash
python scripts/js_audit.py <files-or-dirs> [--url https://target/main.js] \
    --out report.md --json report.json
```
Works on any mix of `.js/.mjs/.cjs/.map/.html` (multi-MB minified bundles are fine — tested on 7.7MB of production code). Output buckets are exactly the ten sections below plus the vuln-mapping leads and per-section manual steps.

## The ten sections it produces (read them this way)

1. **REST endpoints (grouped)** — grouped by first path segment = service map. Each non-GET verb is an authz test candidate (bb-authz, idor-runner).
2. **GraphQL operations** — mutation names are the authz test list; queries are exfil candidates (bb-graphql).
3. **Auth/authz mechanisms** — where the token comes from, which endpoints skip it, header-builder functions. Find the "Bearer only-if-authenticated" pattern → the anonymous flow's resources are the pre-auth attack surface.
4. **Hidden/debug/undocumented endpoints** — `debug|staging|feature-flag|actuator|swagger|graphiql|monitor` paths shipped in the bundle. Force-browse each unauthenticated AND with a normal user.
5. **Admin functionality** — admin route tables and **UI-only role gates** (`isAdmin`, `v-if=role`). Routes shipped to the client mean the UI hides them; the API may not check.
6. **File upload surface** — FormData/multipart/presign contexts. Feed to bb-rce's upload path.
7. **WebSockets** — wss:// URLs + libs (socket.io, pusher, pubnub). Test unauthenticated connect + cross-account channel subscribe + token-in-URL.
8. **Secrets/keys/tokens** — 17 known key formats (AWS/Stripe/SendGrid/Slack/GitHub/DB-strings/private keys/JWTs), classified HIGH / CHECK / PUBLIC-BY-DESIGN / high-entropy CANDIDATE, plus JWT auto-decode (claims + expiry). Never verify credentials unless program rules allow it.
9. **Third-party services** — external host inventory grouped by domain; each integration is a data-flow and token-scope question (bb-pii).
10. **Business-logic signals** — money fields (price/total/discount/coupon/refund/payout) near HTTP calls, and state-machine fields (confirmed/paid/shipped). Each is a tamper target (bb-bizlogic).

## Vuln-mapping leads (the "so what" layer)

| Lead | Bundle evidence | Manual step |
|---|---|---|
| SQLi-prone | `SELECT … ${}` / string-concat queries, `.raw(`/`.whereRaw(` — usually means **leaked server source** | If server code leaked: already a finding; note concat spots as confirmed-unparameterized |
| Mass assignment | `role|permissions|plan|isAdmin` keys in POST/PUT body builders (aria roles filtered out) | Send those keys in profile-update/registration from a normal account; revert |
| Missing server-side validation | validation ONLY via zod/yup/joi/formik in client code near the submit | Replay the backing request with invalid values directly |
| Auth weaknesses | tokens in localStorage, client-only logout, roles derived client-side | Chain with XSS (bb-xss); replay old token after logout |
| Authz issues | admin routes + role gates present client-side only | Direct-navigate + API call with normal-user session |
| Header manipulation | identity-ish `X-User/X-Account/X-Forwarded/X-Original-URL` set from client | Replay varying them with other-own-account values; admin-path bypass probes |
| Input-validation bypass | maxlength/pattern/sanitize only in client | Direct API replay with out-of-contract values |
| Rate-limit concerns | 429/retry-after/backoff handling code | Measure real limits; test OTP/coupon/payout at realistic rates within rules |

## Advanced passes the engine flags, you finish by hand

- **Source maps**: any `//# sourceMappingURL=` hit, or a `.map` file whose `sourcesContent` is embedded → **full original source with comments** — the single highest-value artifact in JS recon. Re-audit the recovered source.
- **Unfetched chunks**: webpack chunk hashes listed in artifacts → fetch each (append to publicPath) and re-run the audit on them.
- **Config-object mining**: `xxxApiUrl:`/`baseUrl:` assignments map the per-tier topology (prod/staging/qa hosts). Resolve + fingerprint every staging host found.
- **Static data catalogs**: some sites ship whole datasets as `data/*.js` (`window.X=[…]`) — one file can be the entire API.
- **Turnstile/proof gates**: `cf-turnstile-token`-style headers mark script-hostile endpoints → plan the CDP browser-pass (bb-pipeline Phase 2.5) instead of curl.

## Verdict discipline
- Every lead is a LEAD until an authorized test confirms it — the report is an attack plan, not a findings list.
- PUBLIC/CANDIDATE secrets are noted and skipped (browser keys, Firebase web configs, FCM vapid keys, base64 alphabets are public-by-design); only HIGH/CHECK items get follow-up.
- Cross-reference: REST+GraphQL → idor-runner; uploads → bb-rce; money fields → bb-bizlogic; admin/hidden → bb-authz force-browse; everything priced via bb-disclosures before reporting.
