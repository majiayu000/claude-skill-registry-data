---
name: reporting-bug-bounty-writeup
description: >
  Turn a confirmed finding into a triage-friendly bug-bounty report (HackerOne/Bugcrowd) with
  correct severity and clean evidence. Load when a bug is validated and needs submitting, on
  "write the report", "CVSS", "severity", or before disclosure. Signals: a reproduced finding,
  a program's VRT/severity policy.
domain: reporting
type: reference
stability: locked
modes: [bugbounty]
severity: info
schema_version: 1
---

# Bug-bounty report & severity

## When it governs
After you've *reproduced* a finding and confirmed it's in scope. A great report gets triaged
fast and paid fairly; a sloppy one gets closed as informational regardless of the bug.

## Structure (what triagers want)
1. **Title** — `[Vuln class] on <asset> allows <impact>` (specific, no hype).
2. **Summary** — 2–3 sentences: what, where, why it matters.
3. **Severity** — CVSS 3.1 vector + score, reconciled with the program's VRT/policy. Justify the
   Impact metrics from *demonstrated* impact, not theoretical maximum.
4. **Steps to reproduce** — numbered, copy-pasteable, from a clean session. Include exact
   requests (method, URL, headers, body) and account roles used.
5. **Proof** — minimal PoC that proves impact (a screenshot with the URL bar, a request/response
   pair, a short video). `document.domain` for XSS; `sts get-caller-identity` for cloud, etc.
6. **Impact** — the realistic business consequence, tied to what you proved.
7. **Remediation** — the correct fix (allowlist, output encoding, object-level authz…).

## Evidence hygiene (do before you submit)
- **Redact real PII/secrets** — prove the class with your own/test data, not customer records.
- Scrub cookies/tokens/authorization headers from pasted requests.
- Deduplicate: one report per root cause; note additional affected endpoints inside it.
- Stay within RoE: no data hoarding, no lateral movement beyond proof, no DoS.

## Severity gotchas
- Don't claim Critical for a self-XSS or a bug needing implausible preconditions — inflated
  severity gets you closed as N/A.
- Chain low bugs into a higher-impact narrative when they genuinely combine (and show the chain).
- Map to the program's own scale; CVSS is the starting point, the program policy is the ruling.

## Verify before sending
A colleague (or you, from a fresh session) can reproduce it from your steps alone, the PoC
proves impact, and nothing sensitive is exposed in the report.

## References
FIRST CVSS 3.1 calculator; Bugcrowd VRT; HackerOne report best-practices.
