---
name: recon-techstack-fingerprinting
description: >
  Passively identify a target's full technology stack — frontend framework, backend runtime,
  server, CMS, CDN/WAF, cloud, and versions — from public signals, then route to the right attack
  skills and CVEs. Load at the start of a web/API assessment, when choosing which techniques apply,
  or when "what is this built with / what CVEs match". Signals: a new domain in scope, unknown
  stack, "fingerprint", "what framework", version-to-CVE matching.
domain: recon
type: methodology
stability: learning
modes: [pentest, bugbounty]
severity: info
mitre: [T1592, T1595]
tools: [httpx, whatweb, wappalyzer, nuclei, subfinder]
schema_version: 1
---

# Tech-stack fingerprinting

## When it applies
The start of any web/API engagement, before you pick techniques. Knowing the stack turns a generic
"test everything" into a targeted plan: a Rails app routes to mass-assignment and deserialization,
a GraphQL backend to `api-graphql`, a WAF in front changes your `payloads-waf-bypass` approach, and
a pinned version turns into a CVE shortlist. It is passive OSINT — public signals only, no exploit.

## Why it works
Applications advertise themselves constantly: response headers, cookie names, HTML generator tags,
JS bundle names, error pages, TLS certs, DNS/CDN records, public repos, and job postings all leak
the stack. Cross-correlating several weak signals gives a high-confidence picture no single tool
produces — and confidence is what keeps you from scoring a CVE against a wrong guess.

## Method
Work outside-in, then correlate. Keep every claim tagged with the signal that supports it and a
confidence level.

1. **Infrastructure first (asset inventory).** CDN/WAF, DNS, TLS/CT logs, cloud provider, and the
   domain/subdomain/IP footprint (`recon-subdomain-enum`, `recon-dns-analysis`). This scopes everything
   else and often reveals origin IPs behind a CDN.
2. **Frontend.** JS frameworks and meta-frameworks (Next/Nuxt/Angular), CSS libs, build tooling,
   and CMS from the DOM, `<meta name="generator">`, bundle filenames, and source maps.
   `whatweb <url>`, Wappalyzer, and reading the loaded JS.
3. **Backend.** Web server, runtime/language, framework, and CMS from `Server`/`X-Powered-By`
   headers, cookie names (`PHPSESSID`, `JSESSIONID`, `_rails_session`, `csrftoken`), default error
   pages, and path conventions (`/wp-json`, `/api/v1`, `.aspx`).
4. **Security surface.** Security headers, CSP (which reveals third-party hosts/SaaS),
   `security.txt`, email auth (SPF/DMARC), and the WAF vendor.
5. **OSINT.** Public GitHub/GitLab repos, job postings/ATS (they name the exact stack), and the
   Wayback Machine for historical/leaked endpoints and migrated tech.
6. **Correlate.** Cross-validate signals, resolve conflicts (a backported `Server` banner vs. a
   framework's real version), score confidence, and produce the routing decision.

## Routing (what the result feeds)
- CMS/framework identified → the matching `web-*` classes (e.g. WordPress → plugin CVEs, upload;
  Rails/Spring → deserialization, mass assignment).
- API style → `api-graphql`, `api-grpc`, `api-bola`.
- WAF present → `payloads-waf-bypass`.
- Pinned versions → CVE shortlist (enrich against the NVD), gated by real applicability, not the banner.
- Cloud/CDN → `cloud-*` and origin-IP discovery.

## Gotchas
- **One signal is a guess; correlation is a finding.** A `Server:` header alone is spoofable and
  backported — don't route a version-specific CVE off it. Require a second corroborating signal.
- **CDN/WAF masks the origin** — the stack you fingerprint at the edge may not be the origin's;
  hunt the origin IP before concluding.
- **Passive means passive** — no auth, no active exploitation here; that's for the domain skills
  this one routes to. Stay within `tradecraft-scope-roe`.
- **Wildcard/parked hosts** and shared infra can attribute the wrong stack to a domain — confirm
  the host actually serves the app.

## Verify success
A stack profile where each component names the signal and confidence behind it, and a concrete
"test these next" list of skills + a CVE shortlist — not a raw dump of tool output.

## References
Wappalyzer/WhatWeb signatures; MITRE ATT&CK T1592/T1595 (reconnaissance); NIST NVD for version→CVE.
