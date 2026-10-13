---
name: reporting-triage-validation
description: >
  Validate a finding BEFORE you write it up — kill false positives, confirm real impact,
  check scope, and deduplicate. Load after a candidate bug and before reporting-bug-bounty-writeup
  or reporting-pentest-report. Signals: "I think I found", "is this reportable", a scanner hit,
  a reflected value, a 500 error, an open redirect, a CORS wildcard, "should I submit this".
domain: reporting
type: methodology
stability: learning
modes: [bugbounty, pentest]
severity: info
schema_version: 1
---

# Triage & validation — earn the right to report

## When it applies
You have a *candidate* finding and you are about to spend an hour writing it up. Run this gate
first. It applies double on bug bounty (an invalid/duplicate report costs your signal and the
triager's time) and still matters on a pentest (a false positive in the report costs your
credibility with the client).

## Why it works
Most "findings" die on one of a few predictable questions. Asking them up front — cheaply, in
order — kills the weak ones before they cost report-writing time, and forces the survivors to
carry the evidence a triager actually needs. The rule is simple: **one failed gate = stop.**

## Method — four gates, in order

**Gate 0 — Is it real and in scope?**
1. Reproduce it as a raw HTTP request (or exact steps) from a clean session — not from your
   proxy's replay of a stateful flow. If you can't write the request that proves it, it isn't a
   finding yet.
2. Confirm the vulnerable asset is in `scope.txt` and the vuln class is one the program accepts
   (re-read the policy). Staging, third-party, and internal-only hosts are out.

**Gate 1 — Is there real impact?**
Name what the attacker *walks away with*. "Technically possible" is not impact. Common kills:
- **XSS** with no session/action proof — show cookie theft, an action as the victim, or a
  sensitive-context payload; a reflected `alert(1)` on a JSON endpoint that sets
  `Content-Type: application/json` usually doesn't execute.
- **SSRF** that only resolves DNS — get an HTTP response body or reach an internal service
  (`web-ssrf`, `web-ssrf-gopher-redis-rce`), or it's a blind curiosity.
- **IDOR** on *your own* data, or cross-account with identical data — prove access to *another*
  tenant's object (`web-idor`).
- **CORS** wildcard without `Allow-Credentials` and a credentialed, sensitive response — no
  exfil path, no bug.
- **Open redirect / self-XSS / missing headers / version banners** — N/A alone; only count when
  chained (open redirect → OAuth token theft, `web-oauth`; version → a *working* CVE PoC).

**Gate 2 — Is it a duplicate or known behavior?**
Search the program's disclosed reports, your own past submissions, the changelog, and the web
for the same class on the same asset. Confirm it isn't documented intended behavior. Bump the
version and retest if a fix may have landed since you found it.

**Gate 3 — Is the evidence report-grade?**
- Copy-pasteable reproduction (numbered steps or a single request), no manual proxy state.
- A severity you can defend: build the CVSS 3.1 vector and sanity-check the score against the
  impact you actually proved (e.g. cross-tenant read ≈ 6.5; unauthenticated auth bypass ≈ 9.8).
- Redacted proof only — the minimum data that proves it, never hoarded real PII.

## Gotchas
- **Chains need every link proven.** "Open redirect + hypothetical token leak" is one proven bug
  and one guess = still N/A. Prove the leak or don't claim the chain.
- **Two or more preconditions that must all hold** (victim must be admin *and* click a link
  *and* be on an old client) usually means low/again-N/A — say so honestly.
- **Scanner output is a lead, not a finding.** Every automated hit re-enters at Gate 0.
- Don't let sunk cost carry a dead finding forward — a fast N/A you never submit beats a slow one
  the triager closes.

## Verify success
Every gate passes and you can state, in one sentence, the concrete impact and who is affected —
then hand off to `reporting-bug-bounty-writeup` or `reporting-pentest-report`.

## References
CVSS 3.1 specification; program policy and disclosed reports; HackerOne/Bugcrowd triage guidance.
