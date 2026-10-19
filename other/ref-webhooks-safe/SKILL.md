---
name: ref-webhooks-safe
description: "UNVERIFIED reference wrapper for the webhooks-safe skill (business-de/webhooks-safe). reviewed_by: UNVERIFIED pending Steuerberater/DPO sign-off in docs/reviews/ref-webhooks-safe.md. Not legal advice."
license: MIT-compat
compatibility: "framework-agnostic; HMAC-SHA256 webhook verification; offline"
reviewed_by: UNVERIFIED
metadata: {}
allowed-tools: []
---

# ref-webhooks-safe — UNVERIFIED

> **Status: UNVERIFIED.** This reference is a sign-off placeholder. It must NOT be quoted
> as certified advice until a Steuerberater/DPO signs `docs/reviews/ref-webhooks-safe.md`
> (signature + date). The canonical, runnable implementation lives in
> `skills/business-de/webhooks-safe/` (owned by skills-business-de-r3); this wrapper only
> marks the reference for adviser sign-off and records no new legal claims.

## Scope (carried over from the canonical skill, unverified)

- Inbound webhook ingestion: HMAC-SHA256 signature verification over the raw body
  (`hmac.compare_digest`, never parse-then-re-encode).
- Dedupe by event id with a TTL; atomic check-and-set.
- Per-stream ordering; respect of the provider's replay window.
- Dead-letter queue for persistent failures; outbound delivery only against an allow-listed
  Ottili endpoint (SSRF prevention).

## What changed in this wrapper

- `reviewed_by: UNVERIFIED` — the reference is now explicitly marked as not certified.
- Sign-off gate: this skill's validator refuses to load it as certified until
  `docs/reviews/ref-webhooks-safe.md` exists with a signature and a date.
- No new legal claims are added; the canonical skill's content is not edited here
  (cross-job ownership).

## Related

- Canonical implementation: `skills/business-de/webhooks-safe/`
- Sign-off placeholder: `docs/reviews/ref-webhooks-safe.md`
