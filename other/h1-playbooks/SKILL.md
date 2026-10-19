---
name: h1-playbooks
description: Attack-pattern playbooks distilled from the top-paid HackerOne reports per vulnerability class (from the reddelexc/hackerone-reports corpus, 14.9k reports). Use when PLANNING a hunt for a specific bug class (IDOR, XSS, SSRF, SQLi, business logic, privilege escalation, auth/MFA, ATO/OAuth, info disclosure, RCE/injection, file-read/traversal, GraphQL), when a hunt stalls and needs new angles, or when deciding where a bug class actually pays. Each playbook cites its top-paid reports as evidence.
---

# h1-playbooks — Where each bug class actually pays

Each `references/<class>.md` holds the class's top-15 paid reports (bounty, program, title, link) mined from the corpus. Read the relevant playbook BEFORE hunting a class, and re-read the linked top reports when a hunt stalls — the winning patterns repeat across programs.

## The pattern matrix (what the corpus says pays, per class)

**IDOR** (`idor.md`, $175k paid) — the money is in **bulk/object-transfer flows**, not single records: import/export features, project/file transfers, share-link regeneration, admin "act as user" tools. Ordinary CRUD IDORs cluster at $1–2k; import-flow IDORs hit $20k (GitLab). Hunt: every "copy/move/share/import" feature first.

**Stored XSS** (`xss-stored.md`, $427k) — pays via **privileged context**: payloads landing in admin panels, support inboxes, file names, email subjects rendered by staff. Reflected is commodity; stored-in-privileged-view is the tier jump. Hunt: any field a higher-privileged user will render.

**RCE/Command+Code Injection** (`rce-injection.md`, $836k — the richest class) — the big payouts are **template/SSTI, deserialization, sandbox escapes in sandboxed eval features** (code playgrounds, math evaluators, markdown/latex renderers), not classic shell injection. Hunt: anything that evaluates user input as code "safely".

**Privilege escalation / broken access control** (`priv-esc.md`, $415k) — winners are **role/flag tampering in profile-update mass-assignment** (adding `role`/`isAdmin` to editable objects) and **vertical hops via feature flags**. Hunt: profile/settings update endpoints — replay with role keys appended.

**Info disclosure** (`info-disclosure.md`, $411k) — top payouts are **API responses leaking other tenants' data via mutable identifiers** and **debug/internal endpoints exposed without auth** — not stack traces. Hunt: every response field that isn't yours; every /internal, /debug, /admin route unauthenticated.

**Auth/MFA** (`auth-mfa.md`, $295k) — pays for **OTP flow logic**: missing attempt counters, response-state tampering (changing `verified:false`→`true`), OTP reuse across sessions, login-state race. Password-reset token leakage also lands here. Hunt: the OTP verify request body and response handling.

**Business logic** (`business-logic.md`, $106k, ceiling $12k) — almost all high payouts are **money movement**: double payouts, currency/amount tampering at the payment-provider handoff, coupon/promo reuse and self-referral. Hunt: the exact request sent to the payment provider, and every discount redemption.

**SSRF** (`ssrf.md`, $171k) — big ones are **URL-fetching features** (webhooks, import-from-URL, image-by-URL, PDF generators) escalated to **cloud metadata**. Blind SSRF alone pays little; metadata read pays. Hunt: every field the server fetches.

**SQLi** (`sqli.md`, $174k) — modern payouts concentrate in **filter/sort parameters, JSON/GQL inputs, and legacy report endpoints** rather than login forms. Hunt: `?sort=`, `?filter=`, array params.

**File read / traversal** (`file-read-traversal.md`, $130k) — winners read **server config/source with secrets** (`/proc/self/environ`, app source with DB creds), not `/etc/passwd`. Proof of impact = a secret, not a file.

**ATO/OAuth** (`ato-oauth.md`, 142 paid, title-mined) — recurring patterns: **`redirect_uri` partial-match bypasses, state-parameter absence, token leakage via referrer/postMessage, email-change-without-verification account merging**, and subdomain takeover of logout/redirect hosts.

**GraphQL** (`graphql.md`, 29 paid) — winning angles: **introspection-gated-but-aliasable brute force, mutation authz gaps (the UI hides it, the API doesn't), batching rate-limit bypass** for OTP/login brute force.

## Usage in the chain

1. Recon (`recon-engine`) → surface known → pick classes by feature present (import feature → read `idor.md`; webhook → `ssrf.md`; OTP → `auth-mfa.md`).
2. Hunt with the matching `bb-*` skill; on stall, open this skill's playbook and diff your target's surface against the top-15 patterns.
3. Before reporting, calibrate severity with `h1-reports --program/--vuln` and `bb-disclosures`; write with `vuln-report`.

Regenerate playbooks after `h1-reports --refresh` by re-running the generator (pattern: filter corpus by class → top-15 by bounty → markdown).
