---
name: web-cache-poisoning
description: >
  Web cache poisoning & deception — get a shared cache to serve attacker content to other users,
  or trick it into caching victims' private pages. Load behind a CDN/cache (Cloudflare, Varnish,
  Fastly, Akamai), on unkeyed headers, `X-Forwarded-Host`, cache headers, or static-looking URLs.
  Signals: `Age`/`X-Cache` headers, CDN, reflected headers.
domain: web
type: technique
stability: learning
modes: [bugbounty]
severity: high
owasp: [A05:2021-Security-Misconfiguration]
cwe: [CWE-444, CWE-525]
tools: [burp, param-miner]
schema_version: 1
---

# Web cache poisoning & deception

## When it applies
A shared cache (CDN/reverse proxy) sits in front of the app. Poisoning: an unkeyed input
influences the response but isn't part of the cache key, so your malicious response gets stored
and served to everyone. Deception: the cache is tricked into storing a victim's private page.

## Why it works
Caches key on some request parts (URL, maybe some headers) and ignore others ("unkeyed"). If an
unkeyed header/param changes the response (reflected `X-Forwarded-Host`, a header-driven script
src), you poison the cached copy. Deception exploits path/extension rules that cache things that
shouldn't be cached.

## Method
1. **Map cache behaviour**: `X-Cache: hit/miss`, `Age`, `Cache-Control`, CDN vendor. Send a
   cache-buster param to test safely without poisoning the real key.
2. **Find unkeyed inputs** with Burp **Param Miner** ("guess headers"): `X-Forwarded-Host`,
   `X-Forwarded-Scheme`, `X-Host`, custom headers reflected into the response.
3. **Poison (carefully)**: make the unkeyed input inject a payload (e.g. `X-Forwarded-Host:
   evil.com` → a script/link src) that reflects into a cacheable response; confirm it's stored
   and served to a clean request.
4. **Deception**: request `/account.php/nonexistent.css` — if the cache stores the private page
   under the static-looking URL, another user can fetch victims' cached data.

## Gotchas
- Test with a unique cache-buster so you don't poison production for real users; then prove one controlled hit.
- Impact = what the poisoned response does (XSS, redirect, defacement) × who receives it.
- CDNs normalize/strip headers differently — the win is a specific input this cache doesn't key on.

## Verify success
A clean request (no attacker input) receives your poisoned response, or a victim's private page
is served from cache to you.

## References
James Kettle "Practical Web Cache Poisoning"; PortSwigger cache labs; Param Miner.
