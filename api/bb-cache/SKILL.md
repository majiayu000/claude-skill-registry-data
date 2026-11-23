---
name: bb-cache
description: Hunt web cache attacks — web cache deception (victim's authenticated response cached under an attacker-guessable URL → cross-user PII read) and web cache poisoning (unkeyed input reflected into a cached response → stored XSS/redirect for every visitor). Use whenever the user mentions cache deception, cache poisoning, CDN, Cloudflare/Varnish/Fastly/Akamai cache, X-Cache, cf-cache-status, "cached PII", "poison the cache", or wants to test whether personal responses are cacheable.
license: Apache-2.0
metadata:
  layer: specialist
  status: under-review
---

# Web Cache Attacks — Deception & Poisoning

Two families, one prerequisite: a cache somewhere (CDN, reverse proxy, microservice-level cache) sits between attacker and app and decides what to store by a KEY that never matches how the app routes/responds.

- **Cache deception** (read path): make the cache store a VICTIM's personal response under a URL an ATTACKER can request later. Impact = cross-user PII read (High/Critical — feeds bb-pii impact ladder rung 1).
- **Cache poisoning** (write path): make the cache store an ATTACKER-controlled response for a URL victims request normally. Impact = persistent XSS/redirect/credential theft for every visitor of that URL ($4k–$40k corpus band).

## When to reach for this skill

Any target with CDN/proxy headers (`cf-cache-status`, `X-Varnish`, `X-Cache`, `X-Served-By`, `Via: varnish`, `X-Akamai-*`, `Age > 0`, `Server: cloudflare`, `Fastly-`), any SPA whose `/api/*` responses you see marked cacheable, and any app where bb-pii found `Cache-Control: public` on an authenticated response (its method step 4 hands off here).

## Part 1 — Web cache deception (WCD)

Goal: victim's authenticated page gets cached, then you read it. The classic trick: append a cacheable "static" extension/path to a dynamic personal URL so the cache keys it as static while the app routes to the personal endpoint.

### Extension/path ladder (test in order, log each)

1. `/account/settings/no.cache.js` (and `.css`, `.png`, `.ico`, `.txt`, `.xml`, `.json` — try all; caches differ per extension)
2. Delimiter confusion: `/account/settings;a.css`, `/account/settings%3ba.css`, `/account/settings;.css`, `/account/settings?.css` (semicolon = path-param on Java; some caches strip to `settings`)
3. Encoded traversal: `/account%2fsettings/a.css`, `/account/..%2fsettings/a.css`, `/%2e/account/settings.css`
4. Prefix/suffix confusion: `/x/../account/settings.css`, `/account/.css/settings` (some caches use the extension, app the dir)
5. Header-based routing (pairs with poisoning): send `X-Original-URL: /account/settings` with a `.css` URL, or `X-Rewrite-URL` when the stack uses them
6. Verb variations: `POHEADER`/`HEAD` to `/account/settings.css`, and GET with `Accept: text/css`

### Executing the deception

1. **Find a personal response worth stealing**: `/account`, `/api/user`, `/settings/profile`, order-history pages — anything bb-pii would rate High.
2. Request it AS THE VICTIM (your account A) through the cache with the appended static path. Check for `cf-cache-status: HIT`/`X-Cache: MISS`→HIT on a repeat, `Age` incrementing.
3. **Prove the cache actually held it**: re-request the SAME poisoned-path URL from a different session (account B, different IP if possible, no cookies). A HIT returning account A's data is the bug.
4. On shared-CDN targets confirm the store scope: does `/account/settings.css` cache per-URL only (needs victim to visit YOUR crafted link — social delivery) or does any user hitting the plain `/account` populate it (worse — automatic)? Report the variant you can prove.
5. Delivery: the crafted URL goes to a victim — frame impact as "link click → full account object cached at public URL → attacker reads name/email/address/orders". If your program needs no-interaction impact, hunt the automatic-population variant or chain into cache poisoning instead.

### Cache-header reading table

| Header | Meaning | Action |
|---|---|---|
| `cf-cache-status: HIT/MISS/BYPASS/DYNAMIC` | Cloudflare edge cached / not eligible | MISS→HIT on repeat = cacheable; DYNAMIC = default-off, look for cache rules |
| `X-Cache: MISS` then `HIT` | Varnish/Akamai cached | Replay with second session |
| `Age: N` | Seconds in cache | Rising on repeats = live cache |
| `Cache-Control: public, max-age/s-maxage` | Explicitly cacheable | Check on EVERY authenticated response (bb-pii step 4) |
| `Vary: User-Agent/Accept-Language` | Key includes these | Vary the same header in attacker replay |
| `Set-Cookie` present in cached response | Cache misconfig (storing cookies) | Extra finding: cache may serve victim cookies |

## Part 2 — Web cache poisoning

Goal: attacker input reaches a response that the cache then serves to everyone. Three steps: find an unkeyed input, get it reflected, make the reflection malicious.

### 1. Find unkeyed inputs (the cache key is usually: method + path + Host)

- **Params first** (GET then POST even on GET-route endpoints): duplicate params (`?utm=1&utm=2`), unknown params — run Param Miner / wordlist (`utm_content`, `utm_source`, `callback`, `redirect`, `next`, `page`, `lang`, `site`, `theme`, `region`) and watch for reflection.
- **Headers that rewrite routing** (try against a cacheable URL): `X-Forwarded-Host`, `X-Forwarded-Scheme`, `X-Forwarded-Proto`, `X-Original-URL`, `X-Rewrite-URL`, `X-Host`, `X-HTTP-Method-Override`, `Forwarded`, `X-Port`, `X-Proto`. A reflected `X-Forwarded-Host` in a script/link/redirect in the response = poisoning primitive.
- **Fat GET / method override**: send a POST body to a GET-routed URL; some stacks read `?param` from the body and the cache keys GET.
- **Unkeyed query ordering/normalization**: `?a=1&b=2` vs `?b=2&a=1` producing different responses = key mismatch to exploit.

### 2. Reflect → exploit

Reflection in a **script src / redirect / JSONP callback / canonical link / import map** beats reflection in text: poisoning a `<script src="https://evil/x.js">` on a cached page = stored XSS on every visitor. Build the payload:

- Redirect capture: poisoned response redirects victims to your host → harvest the OAuth/`redirect_uri` callback (chain bb-oauth).
- Script injection: self-XSS-in-cache is NOT self-XSS — cache delivers it to others (chain bb-xss).
- DOM poisoning: poison a config/JSON response (`/config.json`, i18n dictionaries, `/settings.js`) that the SPA trusts at runtime — flip feature flags, swap API base URL.

### 3. Confirm like a professional

1. Poison with a HARMLESS marker first (`alert(1)` only on test pages you control the audience for — on shared caches use a benign marker string you can verify, e.g. a comment or a redirect to your own logged endpoint).
2. Verify from a SECOND, cache-fresh client (new session, new IP, `Cache-Control: no-cache` absent) that it receives the poisoned content — the same two-client proof as deception.
3. Time-box cache TTL: note `max-age`/`s-maxage` and how long the poison persisted; if you injected anything real, request a purge (`cf-cache-status` purge via program contact / report note) and say so in the report.

## Verdict rules

- **Two-client proof is mandatory**: attacker plants/reads, independent session (different cookie jar, ideally different IP) confirms HIT/poisoned content. A HIT from your own session alone is a lead, not a finding.
- Deception with own-account data shown in the cached object = reportable (matches bb-pii rule: your data as PoC, never enumerate real customers).
- Poisoning on a shared cache: demonstrate with a benign payload + state the malicious equivalent; never leave malicious content cached — purge and document.
- `DYNAMIC`/`BYPASS` everywhere and no header reflection after the full ladder → record tested-negative and move on; the class is dead on that target.

## Chains (hand off to bb-chains)

| Chain | Result |
|---|---|
| WCD on `/account` | Cross-user PII read → bb-pii rung 1 (High) |
| WCD on `/api/user` returning `user_id` | ID→IDOR pivot (idor-runner) on object endpoints |
| Cache poisoning script-src | Stored XSS → session hijack (bb-xss/bb-authz ATO chain) |
| Poisoned redirect + OAuth | `redirect_uri` theft → ATO (bb-oauth) |
| Poisoned `/config.json` | API-base swap → full traffic interception |
| Host-header injection (unkeyed) | + password-reset flow → reset poisoning (bb-chains matrix row) |

## Evidence format

Two-client table: client A request (the plant), cached response headers, client B request (no cookies / different IP) receiving A's data or the poisoned body. Include the exact URL + headers, cache headers on both sides, TTL observed, and purge/cleanup confirmation for poisoning.
