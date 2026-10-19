---
name: idor-runner
description: Run safe cross-account IDOR/BOLA test matrices using two or more authenticated session cookie jars on an authorized bug-bounty target. Use whenever the user mentions IDOR, BOLA, cross-account access, testing with two accounts, session jars, "Copy as cURL", Burp history/REST-API sessions, CDP-extracted cookies, or object-level authorization — including when they paste cookie strings or cURL blocks.
---

# IDOR / BOLA Test Runner

Systematically test object-level authorization between the user's own accounts. Prerequisite: **authorization** (in-scope program) and **sessions the user owns**. Cookie jars are sensitive — never echo them into reports, logs shown to third parties, or external services.

## Step 1 — Ingest sessions (four sources)

1. **Cookie handoff**: user pastes `Cookie: k=v; k=v` headers (Cookie-Editor export) per domain per account, labeled acct1/acct2. Keep each domain's jar separate (app + auth host differ).
2. **"Copy as cURL" blocks** from DevTools — one per account.
3. **Burp**: either the REST API (`GET 127.0.0.1:1337/v0.1/proxy/history` with the user's key — filter by auth domain, lift Set-Cookie/Authorization from post-login responses) or a saved history file ("Save items") parsed for the same.
4. **CDP browser extraction**: if the user logged in inside my driven browser, pull cookies via `Network.getAllCookies` (filter to the target domains) and any bearer tokens from localStorage/sessionStorage or hooked XHR headers.

Parse into jar files: one line of `k=v; k=v` cookies (strip cmd `^` escaping, drop tracking cookies — keep session/SSF/csrf/clearance cookies). Require the matching User-Agent from the source: CDN clearance cookies (cf_clearance) are bound to UA + IP, so every scripted request must reuse the exact UA string.

**Identify before testing.** Hit the app's session-status/identity endpoint with each jar and record who's who (customer number, username). A jar returning `loggedIn:false` is dead — tell the user to paste a fresh one; don't test with it. Note: email-OTP apps may mint sessions only after the OTP step — a pre-OTP "jar" is not a session.

## Step 2 — Build the object inventory

For each session, GET every object-listing endpoint (cart, addresses, orders, wishlists, coupons, loyalty, tickets, payment methods, notifications) and record **object IDs per account** in a table. No objects? The user must create them (add an address, one cheap order, wishlist item) — say exactly what to create and stop until they do. Empty accounts produce identical "empty" responses and zero signal.

## Step 3 — Run the matrix (script enforces the discipline)

`scripts/idor_matrix.py --base https://target --jars a.txt b.txt --tests tests.json`

tests.json format:
```json
[{"method": "GET",    "path": "/api/v1/addresses/{OBJ:acc1.address_id}"},
 {"method": "PATCH",  "path": "/api/v1/addresses/{OBJ:acc1.address_id}", "body": {"name": "x"}},
 {"method": "DELETE", "path": "/api/v1/addresses/{OBJ:acc1.address_id}"}]
```
`{OBJ:<jar>.<dotted.path>}` interpolates IDs discovered in Step 2 (the script deep-searches each jar's recorded responses). The runner:

1. **Positive control first** — owner performs the same request. If the owner can't succeed, the format/token is wrong and every cross-account 4xx is meaningless. Fix the control before concluding anything.
2. Cross-account run from every *other* jar.
3. **Revert** successful mutations via the owner session.
4. Writes `idor_results.json` + `idor_results.log`: method, path, owner status vs foreign status, and the server's error string.

## Step 4 — Read verdicts honestly

- Foreign request returns the **owner's data (200 + body)** → IDOR confirmed. Capture the exact request as PoC, verify once more, revert, and check impact chain (what else hangs off that ID?).
- **Explicit ownership error** (`403 "does not belong to…"`) → authz enforced; record as TESTED-NEGATIVE with the error string.
- Ambiguous 400/500 with no positive control → **inconclusive**, not negative. Fix the control or drop the claim.
- Sequential/guessable IDs are only a finding if an endpoint accepts them as input; identical derived IDs (e.g., an empty-cart sentinel like `uuid(md5("0"))` on every account) are usually meaningless without an accessor — check before reporting.
- Rotating item IDs (server regenerates object IDs on mutation) break cross-request matrices — re-GET fresh IDs before EACH mutation round, or every test 400s spuriously.

## Rules

- Mutations: only on the user's own accounts, always reverted, minimal count (~1.3s between requests; batch ≤ ~25).
- GET/HEAD probes are cheap; state-changing cross-account requests need the positive control green first.
- Never test against accounts/objects that aren't the user's own. Report PII impact without exfiltrating real third-party data — "could read any customer's address" stated with an own-account PoC is enough.
