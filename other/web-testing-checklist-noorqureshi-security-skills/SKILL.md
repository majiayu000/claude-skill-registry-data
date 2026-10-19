---
name: web-testing-checklist
description: >
  A fast, ordered checklist for testing a web application end to end — so nothing gets skipped.
  Load when starting on a web target, "checklist", "what should I test", methodology triage, or
  to confirm coverage before reporting. Signals: a new web app in scope, "am I missing anything".
domain: web
type: checklist
stability: learning
modes: [bugbounty, pentest]
severity: info
schema_version: 1
---

# Web application testing checklist

Work top to bottom; each item links to the skill that goes deep. Confirm scope first
(`tradecraft-scope-roe`).

## Recon & mapping
- [ ] Subdomains + live hosts (`recon-subdomain-enum`), DNS (`recon-dns-analysis`)
- [ ] Content/endpoint + param discovery (`recon-content-discovery`), JS mining (`recon-js-analysis`)
- [ ] Fingerprint stack/versions; note WAF/CDN (`web-arsenal`)

## Authentication & session
- [ ] Login/registration flaws, username enumeration, rate limiting
- [ ] Password reset & email change (`web-account-takeover`), OTP/2FA bypass
- [ ] Session handling & JWT (`web-auth-jwt`); OAuth/SSO (`web-oauth`)

## Authorization
- [ ] IDOR / object-level (`web-idor`); function-level / forced browsing
- [ ] Multi-tenant boundary crossing

## Input handling (injection & rendering)
- [ ] XSS reflected/stored/DOM (`web-xss`, `payloads-xss-polyglots`)
- [ ] SQLi (`web-sqli`), NoSQLi; SSTI (`web-ssti`); command injection
- [ ] SSRF (`web-ssrf`); XXE (`web-xxe`); LFI/traversal (`web-lfi-path-traversal`)
- [ ] Deserialization (`web-deserialization`); prototype pollution (`web-prototype-pollution`)

## App logic & client
- [ ] Business logic (`web-business-logic`); race conditions (`web-race-conditions`)
- [ ] File upload (`web-file-upload`); CSRF (`web-csrf`); CORS (`web-cors`); open redirect (`web-open-redirect`)
- [ ] Host-header/cache (`web-cache-poisoning`), request smuggling (`web-request-smuggling`)

## Before reporting
- [ ] Impact proven & reproducible; evidence captured; severity set (`reporting-bug-bounty-writeup`)
- [ ] In scope, within RoE; no real data hoarded

## Notes
A checklist is a coverage aid, not a substitute for judgment — follow the leads that look weird.
