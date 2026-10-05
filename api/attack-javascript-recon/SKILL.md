---
name: attack-javascript-recon
description: "Static JavaScript reconnaissance — endpoint extraction from JS bundles, sourcemap recovery, secret hunting, DOM-XSS sink/source analysis, and hypothesis-gated triage"
category: "information-gathering"
version: "1.0"
author: "bountyreaper-official"
tags:
  - js-recon
  - javascript
  - sourcemaps
  - secrets
  - dom-xss
tech_stack:
  - web
cwe_ids:
  - CWE-200
  - CWE-79
  - CWE-798
chains_with:
  - recon-find-origin
  - recon-hunter
  - attack-file-upload
prerequisites: []
---

# Static JavaScript Reconnaissance

## Objective

Extract testable attack surface from client-side JavaScript: API endpoints, secrets, parameters, DOM-XSS sink/source pairs, and higher-severity vulnerability shapes — before touching the target with active tools.

> **Attribution:** Methodology and extraction discipline adapted from [shaikarifali/bundlebleed](https://github.com/shaikarifali/bundlebleed) (MIT). In BountyReaper this is available as the `js_recon` tool (passive-only); the patterns below also work manually.

## Testing Methodology

### Phase 1: Collect JS (passive)

```bash
# Archive-first (no active probing)
gau example.com | grep -E "\.js($|\?)" > js-urls.txt
waybackurls example.com | grep -E "\.js($|\?)" >> js-urls.txt
# or use the js_recon tool (BundleBleed) — handles collection + extraction + scoring
```

### Phase 2: Extract endpoints & parameters

Hunt for request construction in JS bodies:

```bash
grep -oE "(fetch|axios|\\\$\\.(get|post|ajax)|XMLHttpRequest|sendBeacon)\\(([^)]{0,120})" bundle.js
grep -oE "\"/api/[a-zA-Z0-9_/.{}$-]+\"" bundle.js
grep -oE "'/api/[a-zA-Z0-9_/.{}$-]+'" bundle.js
# Route params (Express/OpenAPI shapes)
grep -oE ":[a-zA-Z_]+(\\?|/)" bundle.js
```

Also extract **server-rendered** `<a href>` and `<form action>` targets — JS-only patterns miss these.

### Phase 3: Sourcemap recovery (zero extra network cost)

```bash
# If bundle.js.map exists and embeds sourcesContent, the ORIGINAL unminified
# source is recoverable and analyzable — endpoints/secrets the minified
# bundle hides (comments, dead code, config) become visible.
curl -s https://target.com/app.js.map -o app.js.map
python3 -c "import json; m=json.load(open('app.js.map')); print(m.get('sourcesContent') is not None)"
```

### Phase 4: Secrets (always redacted before reporting)

31 pattern families: AWS/GCP/Azure keys, Stripe, Slack, Twilio, SendGrid, Discord, Square, Shopify, PayPal/Braintree, private-key blocks, JWTs, generic Bearer tokens.

```bash
grep -oE "(AKIA|ASIA)[A-Z0-9]{16}" bundle.js              # AWS
grep -oE "sk_live_[a-zA-Z0-9]{10,}" bundle.js              # Stripe live
grep -oE "ey[A-Za-z0-9_-]+\\.[eyA-Za-z0-9_-]+\\.[A-Za-z0-9_-]+" bundle.js  # JWTs
```

**Discipline:** report as type + preview + partial hash. NEVER paste a live credential into a finding, log, or report.

### Phase 5: Higher-severity shapes (from real disclosed reports)

- **SSRF-shaped parameters**: `url=`, `next=`, `redirect=`, `webhook=`, `fetch=` accepting URLs
- **Prototype pollution**: deep-merge/extend calls reachable with `__proto__` payloads
- **JWT `alg:none`**: decode every JWT header found (`JSON.parse(atob(h))`) — flag `{"alg":"none"}`
- **CORS misconfig**: `Access-Control-Allow-Origin: *` combined with `Allow-Credentials: true`
- **Firebase-style DBs**: unauthenticated realtime DB URLs in config blobs
- **Third-party script supply chain**: every `<script src>` outside first-party origins

### Phase 6: DOM-XSS sink/source co-occurrence

A DOM-XSS hypothesis is worth raising only when a **source** (`location.hash`, `postMessage` data, `document.referrer`, URL params read via `URLSearchParams`) reaches a **sink** (`innerHTML`, `eval`, `document.write`, `setAttribute('href',...)`, `jQuery.append`) in the same code path.

### Hypothesis discipline (proof-gated)

A raw finding is a **candidate**, not a finding. Score it on: static pattern match, authenticated-only visibility, runtime confirmation, cross-scan recurrence. Only promote with executed evidence — in BountyReaper via `http_replay` + `execution_evidence` re-report (the proof-gated lifecycle handles this).

## What Constitutes a Finding

| Condition | Severity |
|-----------|----------|
| Live secret (verified exploitable) | Critical (P1) |
| Secret shape in JS (unverified) | Candidate — test before reporting |
| DOM-XSS source→sink reachable | High (P2) |
| CORS `*` + credentials | High (P2) |
| Firebase-style unauthenticated DB | High (P2) |
| Endpoint list / wordlists | Intel (not a finding) |

## Tools

- `js_recon` tool — BundleBleed integration (passive-only, auto-ingests intel + hypotheses)
- `grep`/`curl` — manual extraction
- `web_get_request_detail` — confirm runtime behavior after static analysis

## References

- [BundleBleed](https://github.com/shaikarifali/bundlebleed) — MIT
- [OWASP WSTG Information Gathering](https://owasp.org/www-project-web-security-testing-guide/)
