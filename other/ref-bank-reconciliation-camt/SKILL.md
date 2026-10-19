---
name: ref-bank-reconciliation-camt
description: "UNVERIFIED reference wrapper for the bank-reconciliation CAMT skill (business-de/bank-reconciliation-camt). reviewed_by: UNVERIFIED pending Steuerberater/DPO sign-off in docs/reviews/ref-bank-reconciliation-camt.md. Not legal/tax advice."
license: MIT-compat
compatibility: "framework-agnostic; ISO 20022 camt.053, SWIFT MT940, EBICS; offline"
reviewed_by: UNVERIFIED
metadata: {}
allowed-tools: []
---

# ref-bank-reconciliation-camt — UNVERIFIED

> **Status: UNVERIFIED.** This reference is a sign-off placeholder. It must NOT be quoted
> as certified tax/accounting advice until a Steuerberater/DPO signs
> `docs/reviews/ref-bank-reconciliation-camt.md` (signature + date). The canonical, runnable
> implementation lives in `skills/business-de/bank-reconciliation-camt/` (owned by
> skills-business-de-r3); this wrapper only marks the reference for adviser sign-off and
> records no new legal claims.

## Scope (carried over from the canonical skill, unverified)

- Parsing CAMT.053 (ISO 20022) and MT940 (SWIFT) bank statements.
- Balance verification (opening balance + entries = closing balance; mismatch is a hard stop).
- Multi-key heuristic matching of postings to open items (customer, supplier, refund).
- Duplicate detection and unallocated-difference flagging.

## What changed in this wrapper

- `reviewed_by: UNVERIFIED` — the reference is now explicitly marked as not certified.
- Sign-off gate: this skill's validator refuses to load it as certified until
  `docs/reviews/ref-bank-reconciliation-camt.md` exists with a signature and a date.
- No new legal claims are added; the canonical skill's content is not edited here
  (cross-job ownership).

## Related

- Canonical implementation: `skills/business-de/bank-reconciliation-camt/`
- Sign-off placeholder: `docs/reviews/ref-bank-reconciliation-camt.md`
