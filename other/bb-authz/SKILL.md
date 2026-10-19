---
name: bb-authz
description: Hunt broken access control — IDOR/BOLA (all 10 variants), BAC, auth bypass, privilege escalation, 403/401 bypass, and capability-URL design flaws — on authorized bug bounty targets. Use whenever the user mentions IDOR, BOLA, access control, authorization bugs, privilege escalation, "can user A access user B's data", 403 bypass, JWT attacks, or an API keyed only by an unguessable ID.
---

# Broken Access Control Hunter

The highest-ROI bug class (1,364 of 11,338 paid disclosures in the local corpus are access-control; top payouts $20k–$35k). Every test needs: authorization context (in-scope program), and object IDs from the user's own accounts. Cross-account reads are proven with own-account PoCs only — never touch a third party's data.

## Real-bug anchors (what actually paid — query bb-disclosures for more)
- **$35,000** Account takeover via **password reset** without user interaction — the money is in reset/recovery flows, not login.
- **$22,300** RepositoryPipeline allows importing **local git repos** — import/migration features move objects across trust boundaries server-side.
- **$20,000** Getting **all CD keys of any game** — anything that vends codes/keys/tickets with a swappable batch ID.
- **$20,000** Steal private objects of other projects **via project import** (IDOR on import target).
- **$13,000** Mass ATO via **alternate auth path** (mobile/legacy endpoint accepted weaker checks).
Delta lesson: the expensive versions were **interaction-free** and **mass-scale**. If your variant needs the victim to do something, keep chaining before submitting.

## Before testing
1. Build the object inventory first (carts, addresses, orders, invoices, tickets, files, API keys). Empty accounts = zero signal; tell the user exactly what to seed.
2. Know the "who am I" endpoint per session. Identify jars before use.
3. Plan the positive control: the owner must succeed at the same request, or every 4xx is meaningless.
4. **Map the auth model from JS bundles first**: which endpoints take IDs in path vs body vs GraphQL args, and which header set identifies the caller (`x-je-auser`-style anonymous IDs count as identity claims — test whether the server actually binds them).

## The 10 IDOR variants (run the table, not one swap)

| # | Variant | Test |
|---|---------|------|
| V1 | Direct path | `/api/users/123` → `/456` (other OWN account) |
| V2 | Body param | `{"user_id": other}` in POST/PUT/PATCH |
| V3 | GraphQL node | `node(id: base64("OtherType:123"))` |
| V4 | Batch/bulk | `?ids=1,2,3` — one foreign ID among own |
| V5 | Nested scope | `/orgs/{own}/users/{other}` — parent own, child foreign |
| V6 | File/path | `?path=.../other-user/file.pdf`, `?file_id=` |
| V7 | Method swap | GET 403 → try PUT/PATCH/DELETE (and POST) |
| V8 | Version rollback | `/api/v2/x` guarded → `/api/v1/x` legacy |
| V9 | Header/param injection | `X-User-ID`, `X-Forwarded-User`, `?user_id=`, `?account=` |
| V10 | Predictable IDs | sequential ints, timestamps, UUID v1, `md5(int)`-style derived IDs |

Use `idor-runner` skill's script to execute matrices with positive controls and evidence logs.

## Capability-URL verdicts (unguessable-ID APIs)
Modern APIs key anonymous objects by unguessable IDs (base64-UUID tokens) with no session at all. Judge them like this:
- Unguessable ID + **no leak vector** + fabrication returns clean 404 → working as designed; note as informational only.
- Unguessable ID **plus a leak vector** (ID appears in URLs shared/logs/referrer/support tools; deterministic/derived IDs; ID predictable from another endpoint) → the capability IS the finding: prove the leak, then demo full read/write with the leaked ID.
- Test whether the capability **expires** and whether **login binds** the object to the account. Permanent unbound capabilities on objects that later hold PII (checkout address) are worth reporting even without a leak PoC — frame as design risk with the ID-leak scenarios.

## Auth bypass additions
- **Remove the auth entirely**: same endpoint, no cookie/token → 200 = unauthenticated access.
- **Force-browse**: `/admin`, `/internal`, `/api/admin/*`, `/_debug`, `/backoffice/*` — 403 (exists, ACL) vs 404 (nothing) is itself intel.
- **Header tricks for edge routers**: `X-Original-URL: /admin`, `X-Rewrite-URL: /admin`, `X-Forwarded-For: 127.0.0.1`.
- **Alternate paths**: the $13k TaxJar bug was the same auth on a parallel channel — check mobile APIs, legacy versions, partner/BFF mirrors of the same resource.
- **JWT**: `alg:none` re-sign; RS256→HS256 confusion (verify with public key as HMAC secret); `kid` path injection; claim tampering (`role`, `sub`, `account_id`). Only report if the server accepts the forged token — never "the token CAN be tampered".
- **Mass assignment**: send role/isAdmin/accountId fields the server didn't ask for in profile-update endpoints. Own account, check what stuck, revert.

## Verdicts (be strict)
- Foreign 2xx **with owner's object body** → confirmed IDOR. Re-run once for the report, capture exact request.
- Explicit ownership error (`"does not belong to current user/cart"`) → TESTED-NEGATIVE with the error string.
- Uniform 400/500 without a green positive control → INCONCLUSIVE, not negative.
- Remember most programs pre-reject: "theoretical" authz issues without a working read/write.

## Impact framing
Read vs write vs delete changes severity: PII read (High) < write/delete (High/Critical). Chain upward: address read → address ID as input to order-refund flow → money impact. See bb-chains skill before writing up, and calibrate against bb-disclosures precedent before setting severity.
