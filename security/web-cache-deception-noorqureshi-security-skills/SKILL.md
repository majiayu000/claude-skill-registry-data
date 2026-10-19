---
name: web-cache-deception
description: >
  Trick a CDN/cache into storing a victim's authenticated response at a public URL, then read it.
  Load on "web cache deception", when a CDN/cache sits in front of an app that serves per-user
  content, or to test whether private pages can be cached. Signals: `X-Cache`/`CF-Cache-Status`
  headers, caching by file extension, static-looking suffixes on dynamic endpoints.
domain: web
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: high
owasp: [A05]
cwe: [CWE-525]
tools: [burp, param-miner]
schema_version: 1
---

# Web cache deception

## When it applies
A caching layer (CDN, reverse proxy) fronts an app that returns per-user content, and the cache
decides what to store by URL pattern/extension. If you can make an authenticated response *look*
cacheable, the cache stores it — and anyone can then fetch that victim's data.

## Why it works
The cache and the origin disagree about the URL. The cache sees `/account.css` and thinks "static,
cache it"; the origin ignores the `.css` suffix (or a delimiter) and serves the dynamic
`/account` page. The victim's private response gets stored under a public key you can request.

## Method
1. **Confirm the mismatch**: request an authenticated page with a static suffix — `/account/foo.css`,
   `/account%0a.css`, `/account;foo.js`, `/account%2ffoo.css`. If the origin still returns the
   account page (not 404), the origin is ignoring the suffix.
2. **Confirm caching**: repeat and watch `X-Cache`/`CF-Cache-Status` flip to `HIT`, or a `Age`
   header appear. A cached, authenticated response is the vulnerability.
3. **Prove cross-user impact**: as the *victim*, visit the crafted URL once (or have them); then as
   an unauthenticated attacker request the same URL and receive the victim's private data.
4. **Explore delimiters/normalisation**: caches and origins normalise `;`, `%2f`, `//`, `..`,
   trailing dots differently — Param Miner's rules or manual fuzzing find the pair that splits them.
5. **Report with least data**: prove one private field leaked; don't hoard victim data.

## Gotchas
- This is **not** cache poisoning: deception caches a *victim's* real response; poisoning injects a
  malicious response via unkeyed input. Different bug, different report (`web-cache-poisoning`).
- Needs a genuinely cacheable-looking key *and* an origin that ignores it — confirm both.
- Some CDNs cache by content-type, not extension — test path-based tricks too.

## Verify success
An unauthenticated request retrieves another user's authenticated content from the cache
(`HIT`/`Age` present), reproducibly.

## References
Omer Gil "Web Cache Deception"; PortSwigger web cache deception labs; CDN caching-rule docs.
