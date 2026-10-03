---
name: bug-bounty-workflow
description: Bug bounty workflow skill for program scope mapping, recon-to-report automation, deduplication against prior submissions, and high-signal reporting on HackerOne, Bugcrowd, Intigriti, YesWeHack, and self-hosted programs. Use to organize bounty work end to end while staying inside program rules.
---

# Bug Bounty Workflow

## Program Rules First

- Parse and pin the program brief: in-scope, out-of-scope, allowed techniques, rate, retesting, safe harbor, disclosure.
- Refuse any step that violates program rules or applicable law, even if technically possible.
- Track per-target state so you never test out-of-scope assets accidentally.

## Workflow

1. Scope ingest: domains, mobile apps, APIs, source repos, partner services; tag each with `in/out/maybe` and rate.
2. Recon: passive OSINT, subdomain/asset discovery, screenshot, tech fingerprint, content discovery; store as snapshots.
3. Triage surface: prioritize high-value endpoints (auth, payments, admin, file upload, SSO, webhook, API gateway).
4. Test: auth/authorization, IDOR, SSRF, RCE, business logic, secrets exposure, race conditions; minimize impact.
5. Reproduce cleanly: minimal steps, no extra access, redacted PoC, controlled test accounts.
6. Dedupe: search prior public disclosures, hacker activity, changelogs; cross-check internal notes.
7. Report: clear title, severity rationale (CVSS + program rubric), impact narrative, reproduction, remediation.

## Quality Bar

- One vulnerability per report. Chain only when chaining is the bug.
- Include log/HTTP evidence with secrets redacted, plus suggested fix and detection.
- Offer collaborative retest after the fix.

## Output Contract

- `programs/<name>/scope.yaml`, `recon/`, `notes.md`, `reports/<id>.md`, `metrics.csv` (submissions, accepted, paid, dupes).
