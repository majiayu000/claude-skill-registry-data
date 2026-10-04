---
name: check-security
description: Security and privacy review of a Keelokit project, in depth — a map of every piece of personal data (what, why, where, who sees it, how long), the privacy law of each market, a threat model of the critical journeys, dependency and container scans, an OWASP ZAP scan of staging, and checks for PII in logs and error reports, data export and deletion, retention and encryption. Fixes at the root with a test, and leaves a check per class of problem, like the bug bash. Use when the user says "security", "seguridad", "privacidad", "datos personales", "PII", "GDPR", "vulnerabilidades", "pentest", "auditoría de seguridad", before the first production release, before a release that touches personal data, auth or payments, or every few months.
---

# Check security — what an attacker or a regulator would find first

Autonomous until the report, like `check-bugbash`, with the same exception: a fix that changes a
product rule (what data is kept, for how long, who may see it) is a pending decision for the
user, with options and a recommendation. Legal questions are named and explained, never decided:
the user or their counsel decides.

Scope comes from the profile (`.keelokit/profile.toml`): the data map and privacy law when it has
`personal-data`; the staging scan when it's `hosted`; payment flows when it has `payments`. A
developer-facing project (library, CLI, plugin) gets supply-chain questions instead: what it runs
on the user's machine, which network calls it makes, what permissions it asks for, and whether
anything private ends up in what it distributes.

The day-to-day checks already run on every push: secret scan (SEC-1), `pnpm audit` through `.keelokit/bin/audit.py` (SEC-3: blocks what has a fix, lists what doesn't),
Semgrep (SAST-1), the access matrix (AUTHZ-1). This skill looks for what they can't.

## 1. Data map — `docs/privacy/data-map.md`

From the Prisma schema, the API contracts in `packages/shared`, the logs, analytics and error
reporting, and every third party that receives data (mail, WhatsApp, payments, hosting):

| Data | Where | Kind | Why we keep it | Who can see it | Kept for | Leaves to |
|---|---|---|---|---|---|---|

Kind: `personal` (identifies someone: name, email, phone, IP), `sensitive` (health, finances,
children, location history…), `secret` (passwords, tokens). A field nobody can justify is a
finding: don't collect it. Markets and languages come from `docs/context/product.md`; name the law
that applies to each (e.g. GDPR in the EU, LGPD in Brazil, Ley 25.326 in Argentina, Ley 18.331 in
Uruguay) and what it asks of this product in plain words. Unknowns are gaps with an owner.

## 2. Privacy checks

- **No personal data in logs or error reports**: the logger redacts the map's `personal`,
  `sensitive` and `secret` fields; Sentry's `beforeSend` scrubs them. Proven with a test that logs
  and reports a record full of them and finds none.
- **Export and deletion**: a person can get their data and have it deleted (or anonymised where the
  law requires keeping it), including from third parties; a test per path.
- **Retention**: what the map says is kept for N days is actually removed (a scheduled job and its
  test), backups included.
- **Encryption**: `sensitive` fields encrypted at rest; everything in transit over HTTPS.
- **Consent and notices**: what the product promises in its screens and privacy text matches what
  it does (COPY-1).

## 3. Security checks

- **Threat model** of each critical journey (STRIDE, one table each): who could abuse it, how, what
  stops them, what doesn't yet.
- **Access**: another tenant's ids, another role, an expired session, guessable ids, mass
  assignment, rate limits on login, sign-up and anything that sends a message or costs money.
- **Dependencies and images**: `pnpm audit`, plus
  `docker run --rm -v "$PWD:/src" ghcr.io/google/osv-scanner:latest -r /src` and the image scan of
  the API's Dockerfile; licences that aren't OSI-approved (DEP-1).
- **Staging, from outside**: `docker run --rm -t ghcr.io/zaproxy/zaproxy:stable zap-baseline.py -t
  <staging url>` — headers, cookies, CORS, TLS. Never against production without the user's yes.
- **Secrets and config**: nothing sensitive in the web bundle or the mobile app; production config
  complete (CFG-1).

## 4. Fix and leave a check

Same loop as `check-bugbash`: a failing test first (titled with the finding id), the fix at the
cause, the check that now covers the class (a test, a lint rule, a Semgrep rule in
`.semgrep/`, an invariant of class `isolation`, a house rule registered with
`/keelokit:check-health`), a row in `docs/escapes.md`. What can't be fixed now becomes a backlog
story with `origin = "security:<date> <finding id>"` (`/keelokit:plan-backlog`).

## 5. Report — `docs/security/<date>/report.md`

`## Scope` first (sha, staging URL, what was checked and what couldn't be); the findings table
(id · area · severity P0–P3 · title · status · fix commit · check added) with the same statuses as a
bug bash; `## Pending decisions` (privacy choices and legal questions, with options); the data map's
changes. Refresh the dashboard: its Security section reads these reports.
