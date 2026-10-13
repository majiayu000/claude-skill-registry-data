---
name: web-subdomain-takeover
description: >
  Claim a dangling DNS record pointing to a deprovisioned service (subdomain takeover). Load
  after subdomain enum, on CNAMEs to cloud services, "NoSuchBucket"/"404 there isn't a GitHub
  Pages site here", or dangling A/CNAME. Signals: CNAME → S3/GitHub/Heroku/Azure/Fastly with a
  fingerprint error page.
domain: web
type: technique
stability: learning
modes: [bugbounty]
severity: high
owasp: [A05:2021-Security-Misconfiguration]
cwe: [CWE-350]
tools: [subjack, nuclei, dig]
schema_version: 1
---

# Subdomain takeover

## When it applies
A subdomain's DNS still points (CNAME/A) to a third-party service that no longer has the
resource provisioned, so you can register it and serve content on the victim's subdomain.

## Why it works
The org deleted the S3 bucket / GitHub Pages / Heroku app but left the DNS record. The provider
now serves that hostname to whoever claims the resource next — you. You control content on a
trusted subdomain (phishing, cookie theft on the parent domain, OAuth redirect_uri allowlist).

## Method
1. **Find candidates**: from subdomain enum, resolve CNAMEs (`dig CNAME sub.target.com`) and look
   for third-party targets with a "not claimed" fingerprint (`nuclei -t takeovers`, `subjack`).
2. **Confirm the fingerprint**: the provider's specific unclaimed-resource error (e.g. S3
   `NoSuchBucket`, GitHub Pages 404, Heroku "no such app").
3. **Claim it**: register the exact resource name on that provider (bucket/app/pages repo) and
   serve a proof file — do NOT phish; a harmless proof page is the report.
4. **Assess chained impact**: cookie scope on parent domain, OAuth `redirect_uri` allowlist,
   CSP `script-src` including the subdomain, SPF/email.

## Gotchas
- Only some providers are claimable and only with the right fingerprint — a generic 404 isn't takeover.
- Prove with a benign marker page; don't collect data or run phishing.
- Note the chained impact (why it matters) — a bare takeover of an unused subdomain may be low without it.

## Verify success
You serve attacker-controlled content at the victim's subdomain (proof file loads at
`sub.target.com`), captured with the DNS record + your claimed resource.

## References
can-i-take-over-xyz; subjack/nuclei takeover templates; HackerOne takeover reports.
