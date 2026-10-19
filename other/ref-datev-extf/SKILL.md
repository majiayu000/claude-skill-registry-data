---
name: ref-datev-extf
description: "UNVERIFIED reference wrapper for the DATEV EXTF skill (business-de/datev-extf). reviewed_by: UNVERIFIED pending Steuerberater/DPO sign-off in docs/reviews/ref-datev-extf.md. Not legal/tax advice."
license: MIT-compat
compatibility: "framework-agnostic; German DATEV EXTF; offline"
reviewed_by: UNVERIFIED
metadata: {}
allowed-tools: []
---

# ref-datev-extf — UNVERIFIED

> **Status: UNVERIFIED.** This reference is a sign-off placeholder. It must NOT be quoted
> as certified tax/accounting advice until a Steuerberater/DPO signs
> `docs/reviews/ref-datev-extf.md` (signature + date). The canonical, runnable implementation
> lives in `skills/business-de/datev-extf/` (owned by skills-business-de-r3); this wrapper
> only marks the reference for adviser sign-off and records no new legal claims.

## Scope (carried over from the canonical skill, unverified)

- DATEV EXTF interface specification: export format for accounting data (accounts,
  journals, bookings, tax keys, customer/vendor master).
- Steuerschlüssel mapping and the interplay with `skr-journal-mapping`.
- GoBD-compliant export hygiene (completeness, audit trail, retention).

## What changed in this wrapper

- `reviewed_by: UNVERIFIED` — the reference is now explicitly marked as not certified.
- Sign-off gate: this skill's validator refuses to load it as certified until
  `docs/reviews/ref-datev-extf.md` exists with a signature and a date.
- No new legal claims are added; the canonical skill's content is not edited here
  (cross-job ownership).

## Related

- Canonical implementation: `skills/business-de/datev-extf/`
- Journal mapping: `skills/business-de/skr-journal-mapping/`
- Sign-off placeholder: `docs/reviews/ref-datev-extf.md`
