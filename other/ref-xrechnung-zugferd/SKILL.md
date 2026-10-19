---
name: ref-xrechnung-zugferd
description: "UNVERIFIED reference wrapper for the XRechnung/ZUGFeRD e-invoice skill (business-de/xrechnung-zugferd). reviewed_by: UNVERIFIED pending Steuerberater/DPO sign-off in docs/reviews/ref-xrechnung-zugferd.md. Not legal/tax advice."
license: MIT-compat
compatibility: "framework-agnostic; German e-invoicing standards (EN 16931, Factur-X, XRechnung); offline"
reviewed_by: UNVERIFIED
metadata: {}
allowed-tools: []
---

# ref-xrechnung-zugferd — UNVERIFIED

> **Status: UNVERIFIED.** This reference is a sign-off placeholder. It must NOT be quoted
> as certified tax/accounting advice until a Steuerberater/DPO signs
> `docs/reviews/ref-xrechnung-zugferd.md` (signature + date). The canonical, runnable
> implementation lives in `skills/business-de/xrechnung-zugferd/` (owned by
> skills-business-de-r3); this wrapper only marks the reference for adviser sign-off and
> records no new legal claims.

## Scope (carried over from the canonical skill, unverified)

- XRechnung / ZUGFeRD / Factur-X under EN 16931 and the UStG e-invoicing obligation (§14 UStG).
- Profile selection (MINIMUM / BASIC WL / BASIC / EN 16931 COMFORT / EXTENDED).
- KoSIT validator usage and the offline `scripts/validate_invoice.py` subset.
- GoBD-compliant retention (8 years from year-end, BEG IV effective 2025-01-01); the
  original artefact must be retained as-is — a print-to-PDF copy drops the structured XML
  attachment and is not a valid archive artefact.

## What changed in this wrapper

- `reviewed_by: UNVERIFIED` — the reference is now explicitly marked as not certified.
- Sign-off gate: this skill's validator refuses to load it as certified until
  `docs/reviews/ref-xrechnung-zugferd.md` exists with a signature and a date.
- No new legal claims are added; the canonical skill's content is not edited here
  (cross-job ownership).

## Related

- Canonical implementation: `skills/business-de/xrechnung-zugferd/`
- Sign-off placeholder: `docs/reviews/ref-xrechnung-zugferd.md`
