---
name: "hack"
description: ">-"
---

# HACKING SKILLS / HackSkills

## Overview

This is the **master quality gate and technical router** for authorized bug bounty, web/API security, pentest, code audit, source-leak work, and (when the task is blue) SOC / detection / IR.

It does not replace specialized techniques. It makes the agent:

1. Pass the start gate (authorization, role, scope, success definition)
2. Spend effort on paths that reach real control
3. Route by observed behavior to the correct category / deep topic skill
4. Prefer structured methodology over baseline-model memory and scanner dumps

This file is a quality gate, not a capability ceiling. Surfaces not listed here stay in play if field evidence exists.

This file is not an exploit cookbook. Weaponized details live in deep topic skills and are used only on authorized targets.

Load on demand:

- Red-team execution → [RED_TEAM.md](./RED_TEAM.md)
- Test matrix and effort → [TEST_MATRIX.md](./TEST_MATRIX.md)
- Blue-team execution → [BLUE_TEAM.md](./BLUE_TEAM.md)
- Code audit → [CODE_AUDIT.md](./CODE_AUDIT.md)
- Source leak → [SOURCE_LEAK.md](./SOURCE_LEAK.md)
- Evidence and report → [EVIDENCE_REPORT.md](./EVIDENCE_REPORT.md)

## 0. Task Start Gate

Complete in order. Stop if any item is missing:

1. **Authorization**: written auth, RoE, scope, prohibitions, contact, emergency stop. No authorization → refuse.
2. **Role**: red-team test / code audit / source leak / middleware audit / blue triage / detection engineering / IR. Parallel work is allowed; there is only one primary role.
3. **Scope mode**:
   - User gave a fixed URL / system / repo → **locked scope**: follow same-product hosts, gateways, API domains, and same-host extra paths that the business flow naturally exposes. Do not scan unrelated brand lines.
   - User gave an org name and asked to find boundary assets → **exploratory scope**: finish the current asset cluster before opening the next. Do not search many seeds shallowly.
4. **Success definition**: what "done" means for this task. Scanner-finished, report-emitted, and ticket-closed are not success.
5. **Destruction boundary**: list actions that must never happen.
6. **Working directory** before any test: `assets/` (URLs, API inventory, script excerpts), `evidence/` (requests, diffs, screenshots), `reports/` (confirmed findings only).
7. **Questions**: if scope is unclear, ask only the 1–3 technical blockers (target, stack, whether an account exists). Do not use "should I continue" as a way to stop. Missing a second account → degrade to what is testable; do not idle waiting for account B.

Do not expand onto unauthorized assets.

## 1. Hard Constraints

- Stay in scope. Out-of-scope clues: record, then request expansion. No silent expansion.
- No destructive testing or destructive containment: delete other people's business data, DROP/TRUNCATE, bulk config change, encrypt/ransom-like actions, unbounded DoS, wipe logs, wipe images.
- Write-ops that prove access: create only identifiable test objects, delete that one object immediately. Do not change other people's orders, addresses, passwords, roles, or bindings. No charge, stock wipe, or account lock.
- Do not log out, revoke, or deactivate a session the user provided. If password/binding change is required to prove impact, revert immediately; if revert fails, stop at the response — do not brick the account.
- Do not cause irreversible damage to prove a break. Prefer read-only, copy, or low-privilege proof.
- Evidence must be readable and reproducible. A conclusion without repro steps is a hypothesis.
- Do not fabricate PoCs, logs, or exploit chains. If path, file, query, and screenshot do not line up, downgrade or withdraw.
- Copied secrets are clues until they pass the **liveness gate**: production accepts the real value (rejects a fake), and one read-only call returns identity or an object list.
- A finding reached with a session is not "anonymous unauthorized". Anonymous only if the break had no login state.
- For internal users, assume false positive or mistake until the timeline proves otherwise.
- If a security control blocks real work, it will be bypassed. Remediation must include a usable safe path.

## 2. Role Routing

| User intent | Primary flow | Load |
|---|---|---|
| Pentest / red team / foothold / SRC | §§3–5 | [RED_TEAM.md](./RED_TEAM.md), [TEST_MATRIX.md](./TEST_MATRIX.md) |
| Code audit / whitebox / find sinks | §3 R6 | [CODE_AUDIT.md](./CODE_AUDIT.md) |
| Source leak / Git leak / secret leak | §3 R5 | [SOURCE_LEAK.md](./SOURCE_LEAK.md), [insecure-source-code-management](../insecure-source-code-management/SKILL.md) |
| Middleware / gateway / component audit | §3 R7 | [RED_TEAM.md](./RED_TEAM.md) middleware section, [unauthorized-access-common-services](../unauthorized-access-common-services/SKILL.md) |
| Alert triage / SOC / hunting | Blue quality gate | [BLUE_TEAM.md](./BLUE_TEAM.md) |
| Detection rules | Blue B6 | [BLUE_TEAM.md](./BLUE_TEAM.md), template in [EVIDENCE_REPORT.md](./EVIDENCE_REPORT.md) |
| IR / forensics / containment | Blue B7 | [BLUE_TEAM.md](./BLUE_TEAM.md), [memory-forensics-volatility](../memory-forensics-volatility/SKILL.md), [traffic-analysis-pcap](../traffic-analysis-pcap/SKILL.md) |
| Write the report | §6 | [EVIDENCE_REPORT.md](./EVIDENCE_REPORT.md) |

When a task crosses red and blue, freeze evidence for the current phase before switching role.

## 3. Operating Model

### Step 1: Draw the surface from the application

With a URL or an application in hand, map the surface first: [attack-surface-mapping](../attack-surface-mapping/SKILL.md). Portrait, business plane, JS/traffic inventory (keys not just paths), response classes, object graph. Do not scan into a blank portrait. Do not open with directory brute or payload spray.

### Step 2: Route by observed behavior

| Signal | First direction | Load |
|---|---|---|
| Input reflects into HTML / JS | XSS / SSTI | [injection-checking](../injection-checking/SKILL.md) |
| Server fetches a URL / hostname | SSRF | [ssrf-server-side-request-forgery](../ssrf-server-side-request-forgery/SKILL.md) |
| Accepts XML / Office / SVG | XXE | [xxe-xml-external-entity](../xxe-xml-external-entity/SKILL.md) |
| Path, filename, or download is controllable | Path Traversal / LFI | [path-traversal-lfi](../path-traversal-lfi/SKILL.md) |
| Many object IDs in APIs | IDOR / BOLA / BFLA | [auth-sec](../auth-sec/SKILL.md), [idor-broken-object-authorization](../idor-broken-object-authorization/SKILL.md) |
| Login, reset, 2FA, sessions | Auth bypass / JWT / OAuth | [auth-sec](../auth-sec/SKILL.md) |
| Multi-step money, coupons, inventory, approval | Business logic / race | [business-logic-vuln](../business-logic-vuln/SKILL.md) |
| MongoDB / JSON query syntax | NoSQL | [nosql-injection](../nosql-injection/SKILL.md) |
| CLI tools, image processing, importers | Command injection | [cmdi-command-injection](../cmdi-command-injection/SKILL.md) |
| HTTP parse / front-back framing mismatch | Request smuggling | [request-smuggling](../request-smuggling/SKILL.md) |
| Node JSON / controllable `__proto__` | Prototype pollution | [prototype-pollution](../prototype-pollution/SKILL.md) |
| PHP weak compare / `0e` hash | Type juggling | [type-juggling](../type-juggling/SKILL.md) |
| Repeated param names / WAF-app parse mismatch | HPP | [http-parameter-pollution](../http-parameter-pollution/SKILL.md) |
| One-time coupon / inventory / reset / invite | Race | [race-condition](../race-condition/SKILL.md) |
| XML/XSLT templates | XSLT | [xslt-injection](../xslt-injection/SKILL.md) |
| `.git` / `.svn` / `.env` / backups / public buckets | Source leak | [SOURCE_LEAK.md](./SOURCE_LEAK.md) |
| CSV/Excel export | CSV formula | [csv-formula-injection](../csv-formula-injection/SKILL.md) |
| WebSocket upgrade | WebSocket | [websocket-security](../websocket-security/SKILL.md) |
| Internal package names | Dependency confusion | [dependency-confusion](../dependency-confusion/SKILL.md) |
| Business API returns 401/403 | Path / method / header bypass | [401-403-bypass-techniques](../401-403-bypass-techniques/SKILL.md) |
| Public middleware admin / default ports | Default creds, debug, version defects | [unauthorized-access-common-services](../unauthorized-access-common-services/SKILL.md) |
| Chat assistant with command tools | Does the tool actually execute | [llm-prompt-injection](../llm-prompt-injection/SKILL.md) |
| File upload / preview / convert | Upload chain — do not stop at store+download | [upload-insecure-files](../upload-insecure-files/SKILL.md) |
| GraphQL / OAuth JWT / gateway | Matching specialty; tick done or write N/A | [api-sec](../api-sec/SKILL.md), [jwt-oauth-token-attacks](../jwt-oauth-token-attacks/SKILL.md) |

Opening one check class does not mean firing only that one shot. Walk the rest of the matrix.

### Step 3: Spend effort in this order

Full pass/fail rules: [TEST_MATRIX.md](./TEST_MATRIX.md). Default order:

1. Unauthenticated access to another user, tenant, or subject
2. Auth takeover (issue session, reset, rebind, swap ticket) — in-session or password change counts
3. Swap object identifiers (any field name: `id` / `userId` / `tenantId` / `fileKey` / `openid` / ciphertext PK)
4. With a session, walk the object graph: list → detail → attachment/export/approval, then writes and business logic
5. Injection / SSRF / XSS / command or template execution only on surfaces that show a **diff**
6. Salts, hardcoded keys, demo accounts in pages and scripts

**Do not stop on a half-chain.** Upload that stores, OTP that sends, or a copied secret string is not done. Confirmed medium on an object: follow it to write / cross-user / takeover / execution before changing targets.

A full "please log in" with no business fields is not an injection surface. Empty list, error, and timeout are not "please log in".

Finish the current asset cluster before expanding.

### R1. Impact, not compliance

Shortest path to influential control first. Each candidate: can the attacker harm a real user or system *now*? The report narrative is the attack chain; CVSS is an appendix. Tenant-admin "allowed in role" is still a finding if it reaches platform admin, other tenants, or other users. Rank findings with the impact ladder in [RED_TEAM.md](./RED_TEAM.md); layer 7 (pure compliance) is appendix-only.

### R5. Source leak: mine the clue to the end

Do not stop at "`.git` exposed" or "repo is public". [SOURCE_LEAK.md](./SOURCE_LEAK.md): full tree plus history → inventory secrets and hidden surface → live-verify still-valid secrets with minimal read-only calls → treat the leak as a new attack-surface list.

### R6. Code audit: sink→source, or source forward

[CODE_AUDIT.md](./CODE_AUDIT.md). No complete taint path, or sanitizer proven effective → do not file as confirmed.

### R7. Middleware audit is document-driven

Read official docs for the exact major version, build a checklist, leave a trace per item. A middleware conclusion with no comparison table is unfinished.

### Blue quality gate (when the primary role is blue)

Success is shorter dwell time, not close-rate. Details: [BLUE_TEAM.md](./BLUE_TEAM.md).

- **B1.** Ask first whether this loses data, privilege, or the business *now*. One high-confidence event plus a timeline beats a hundred context-free alerts.
- **B2.** Alert fatigue is the main risk. Enrich before a human; every rule has an owner, FP profile, retro window, and retirement condition. Six months silent → check the log source first.
- **B3.** Containment defaults to reversible. Preserve evidence, then contain, then eradicate. Wiping logs is not containment.
- **B4.** Conclusions need a reproducible query, timezone, asset/user/src IP, raw excerpt, and a label (TP / benign TP / FP / insufficient evidence).
- **B5.** Expand the same user, host, IP, token, hash inside the window. Intel, IOCs, and leak samples entering a case are handled at source-leak severity.
- **B6.** Detection engineering walks backward from the behavior that must be caught. Strict high-confidence rules first. Quality gate in [BLUE_TEAM.md](./BLUE_TEAM.md).
- **B7.** IR follows an approved playbook. New log sources get a field dictionary, coverage map, known FPs, owner, and retirement bar before rules ship.

## 4. Core Skill Map

If the full repository is present, prefer these together. Previously separate mini skills (payload-selection, brute-selection) were merged back into their main skills.

- [Attack Surface Mapping](../attack-surface-mapping/SKILL.md) · [Recon and Methodology](../recon-and-methodology/SKILL.md)
- [XSS](../xss-cross-site-scripting/SKILL.md) · [SQLi](../sqli-sql-injection/SKILL.md) · [SSRF](../ssrf-server-side-request-forgery/SKILL.md) · [XXE](../xxe-xml-external-entity/SKILL.md) · [SSTI](../ssti-server-side-template-injection/SKILL.md)
- [IDOR](../idor-broken-object-authorization/SKILL.md) · [CMDi](../cmdi-command-injection/SKILL.md) · [Path Traversal / LFI](../path-traversal-lfi/SKILL.md) · [CSRF](../csrf-cross-site-request-forgery/SKILL.md)
- [API Security Router](../api-sec/SKILL.md) · [JWT / OAuth](../jwt-oauth-token-attacks/SKILL.md) · [OAuth / OIDC](../oauth-oidc-misconfiguration/SKILL.md) · [SAML](../saml-sso-assertion-attacks/SKILL.md) · [Auth Bypass](../authbypass-authentication-flaws/SKILL.md)
- [Business Logic](../business-logic-vulnerabilities/SKILL.md) · [Upload](../upload-insecure-files/SKILL.md) · [NoSQL](../nosql-injection/SKILL.md) · [Request Smuggling](../request-smuggling/SKILL.md)
- [Prototype Pollution](../prototype-pollution/SKILL.md) · [Type Juggling](../type-juggling/SKILL.md) · [HPP](../http-parameter-pollution/SKILL.md) · [Race](../race-condition/SKILL.md)
- [XSLT](../xslt-injection/SKILL.md) · [Insecure SCM](../insecure-source-code-management/SKILL.md) · [CSV Formula](../csv-formula-injection/SKILL.md) · [WebSocket](../websocket-security/SKILL.md) · [Dependency Confusion](../dependency-confusion/SKILL.md)
- [CORS](../cors-cross-origin-misconfiguration/SKILL.md) · [Ghost Bits Cast](../ghost-bits-cast-attack/SKILL.md) · [401/403 Bypass](../401-403-bypass-techniques/SKILL.md) · [Common Services](../unauthorized-access-common-services/SKILL.md)

## 5. High-Value Expert Intuitions

Points baseline models miss that hit often in real bounty work:

1. **The same filter is reused across pages**: one bypass usually ports.
2. **Parameter names are an attack surface**: WAFs often inspect values, not names.
3. **Second-order is common**: safe at store time is not safe when later read into a dangerous context.
4. **BOLA is "authenticated but unauthorized"**: replay while switching account A/B.
5. **Older API versions miss patches**: fixing v2 does not retire v1.
6. **Business-logic bugs often have the highest impact**: scanners miss them; they last.
7. **Race conditions: prioritize one-time actions**: redeem, claim, reset, invite, trial, stock decrement.
8. **JWT: inspect key and algorithm context first**: `alg`, `kid`, JWKS, key source — do not blindly spray.

## 6. Output Standard

Default three layers by audience:

1. Decision: what happened, impact, what to do now (one page)
2. Technical: attack chain or event timeline, repro or query, evidence
3. Improvement: fix / detection / log gap / process gap, each with owner and verification

Use templates in [EVIDENCE_REPORT.md](./EVIDENCE_REPORT.md). Medium and above: write to disk immediately. Severe: notify the authorized contact immediately.

Two gates before a finding is "confirmed":

- **Session-attribution gate**: if the breaking request carried a session, write IDOR/auth — not "anonymous unauthorized".
- **Secret liveness gate**: fake rejected + real accepted, and one read-only call returns identity or a list. Otherwise it is a clue.

## 7. Anti-patterns

- Scanner output as a pentest report; CVSS in place of business impact; filing unexploitable theory to pad count
- Reporting `.git` or a secret string as mere info-leak; code audit that lists dangerous function names without source→sink
- Middleware conclusions from memory, no official-doc comparison
- Spraying passwords before reading lockout policy; one quote per path as "injection done"
- Stopping at upload-stores, OTP-sends, or copied secret
- Writing a session finding as anonymous unauthorized
- Scanning with an empty portrait, or a script that extracted only paths
- Pouring the full matrix into the same "please log in" response
- Blue team measured by close-rate; marking under-evidenced alerts FP and forgetting them; shipping rules never tested on real logs; wiping the only evidence during containment
- Designing a "secure" flow nobody can use, forcing shadow IT
- Pretending an unlisted field surface is not there
- Treating anything this file omitted as forbidden

## Suggested Prompts

- "I only have this URL; draw the attack surface from the application before testing."
- "Plan the test route for this target using bounty methodology, impact-first."
- "This is a REST API; prioritize BOLA, BFLA, mass assignment, and JWT."
- "This parameter triggers server-side requests; list SSRF validation points."
- "Payment / coupon / inventory flow: business logic and race first."
- "I only see login and password-reset: Auth Bypass + OAuth/JWT + CSRF."
- "Audit this repo sink-to-source; no finding without a taint path."
- "`.git` is exposed: mine history and live-verify secrets, then treat it as a new surface list."

## Installation Notes

Recommended skill name: `hack`

Search keywords: `HackSkills`, `HACKING SKILLS`, `bug bounty`, `security engineer ops`

## Guidelines

- Route by target type and observed behavior, not random payload enumeration.
- Payloads: use first-pass samples in the matching deep skill; do not add another intermediate router.
- Prefer reusable filters, shared components, and cross-page reproduction.
- Confirm authn, authz, and version boundaries before deeper exploitation.
- Keep the process explainable, auditable, and reproducible.
- With full repo context, return to topic documents for exploitation detail.
