---
name: bb-pii
description: Hunt PII exposure and data leaks — API responses oversharing personal data, unauthenticated data endpoints, leaked documents and exports, ID enumeration leaking PII, cached personal responses, and third-party data flows. Use whenever the user mentions PII, personal data, GDPR, data exposure, data leak, information disclosure of user data, or wants to check whether an endpoint reveals customer/seller data it shouldn't.
---

# PII Exposure Hunter

PII bugs = programs' #1 paid scenario ("data exfiltration of customer or seller data"). The bug isn't a vuln class — it's a RESPONSE containing data the requester shouldn't see. 1,122 corpus records; top payouts $12.5k–$50k.

## Real-bug anchors (what actually paid — query bb-disclosures for more)
- **$50,000** GitHub access token exposure — a credential IS the PII jackpot when it has reach.
- **$25,000** `/reports/:id.json` disclosed sensitive user attributes — a JSON detail endpoint over-serving fields.
- **$12,500** Internal attachments exportable via **"Export as .zip"** — export features skipping entitlement checks.
- **$12,500** View any user's email via a **collaborators mutation** (GraphQL).
- **$7,500** Private program disclosed **any user's email via invited-username** lookup.
Delta lesson: email/attribute disclosure through invite/collaborate lookups, fat `.json` detail endpoints, and export features are the paid patterns. Names+addresses of other users via any of these = instant High.

## What counts (impact ladder)
1. Other users' PII (names, addresses, emails, phones, DOB, orders) — High/Critical
2. Own PII over-shared to third parties (trackers, referrer leaks) — Medium, chain-dependent
3. Aggregate/statistical leaks enabling deanonymization — Low/Medium
4. Internal identifiers without personal data — Low (usually informative)

## The six overshare patterns
1. **Fat objects**: endpoint returns the full user object where the UI shows one field (GET profile returns password hash, internal notes, isFraudFlag, geo). Compare response fields vs what the page renders.
2. **Unauthenticated access**: personal endpoints answering without session (test every `/api/me`, `/account`, session-status, logged-in-widget endpoint cookieless). Includes "anonymous-allowed" lookup endpoints the signup form uses — judge whether they serve only public registry data (by-design) or account data (bug).
3. **Enumeration oracles**: sequential/timestamp IDs where responses differ between existing/absent users (pairs with V10 in bb-authz).
4. **Documents by URL**: invoices, labels, tickets as `/files/{id}.pdf`, presigned S3 URLs without expiry, cacheable (`Cache-Control: public`) personal responses — check headers on every personal response.
5. **Third-party exfil**: personal data in URL params to analytics (CSP/connect-src lists the collectors), PII in page title/referrer crossing origins.
6. **Error/debug leaks**: stack traces with SQL, emails in verbose errors, debug endpoints (`/actuator`, `/debug`) revealing user stores.

## Method
1. Inventory personal endpoints from JS (js-recon): profile, addresses, orders, messages, tickets, documents.
2. For each: response with session (baseline) → response WITHOUT session → response with OTHER own session. The three-way diff is the whole skill.
3. Field-level audit of baseline: list every field; mark which the UI displays; the invisible ones (internal flags, IDs, hashes) are candidates for "unnecessary data exposure".
4. Check response headers: `Cache-Control`, `Vary: Cookie`, CDN cache status on authenticated responses (a cached `/account` on a shared CDN = cross-user leak).
5. Documents: request your own invoice/label URL; then vary the ID by ±1/other-format — combine with bb-authz V1/V10.

## Verdict rules
- Only claim PII exposure for data of accounts you own or can prove exists (e.g., field returns another account's email). Never enumerate real customers for proof — one own-account PoC suffices ("endpoint returns the full object for any sequential ID" + your ID as PoC).
- Internal-only identifiers without personal data → group as Low per most programs.
- GDPR framing helps European programs: name the lawful-basis violation in impact.

## Evidence format
Three-way diff table (with/without/other-session responses, redacted), the exact request, and the field inventory marking displayed vs leaked fields.
