---
name: ref-ust-edge-cases
description: "UNVERIFIED reference wrapper for the German VAT edge-case skill (business-de/ust-edge-cases). Summarises the corrected reverse-charge scope (UStG §13b covers goods AND services, not services only) and the corrected intra-community-delivery citation (igL = UStG §4 Nr. 1b / §6a). reviewed_by: UNVERIFIED pending Steuerberater/DPO sign-off in docs/reviews/ref-ust-edge-cases.md. Not legal advice."
license: MIT-compat
compatibility: "framework-agnostic; German UStG; offline"
reviewed_by: UNVERIFIED
metadata: {}
allowed-tools: []
---

# ref-ust-edge-cases — UNVERIFIED

> **Status: UNVERIFIED.** This reference is a sign-off placeholder. It must NOT be
> quoted as certified tax advice until a Steuerberater/DPO signs
> `docs/reviews/ref-ust-edge-cases.md` (signature + date). The canonical, runnable
> implementation lives in `skills/business-de/ust-edge-cases/` (owned by
> skills-business-de-r3); this wrapper only records the two corrections that the
> canonical skill still carries wrong.

## What this wrapper corrects

The canonical `ust-edge-cases` skill contains two legal errors. This file states the
corrected rule; the canonical skill is NOT edited here (cross-job ownership).

### Correction 1 — §13b reverse charge is NOT "services only"

The canonical skill says reverse charge (§13b) applies to services only and that a goods
supply with a buyer USt-IdNr. uses the general intra-EU rule (§4a) at 0% without reverse
charge. **That is wrong.**

UStG §13b ("Leistungsempfänger als Steuerschuldner" — recipient as tax debtor) shifts the
VAT debt to the recipient for a *defined list of goods and services*, not services alone.
The full scope, quoted from the statutory heading, is:

> §13b Leistungsempfänger als Steuerschuldner
> (1) Der Leistungsempfänger ist Steuerschuldner für die von einem Unternehmer aus einem
> anderen Mitgliedstaat empfangenen Leistungen, soweit diese Leistungen in den folgenden
> Fällen erbracht werden: [list of goods AND services categories — see §13b Abs. 1
> Nr. 1-11 UStG, incl. Werklieferungen, Bau- und Renovierungsleistungen an Immobilien,
> certain intra-community goods acquisitions, IT/consulting/construction services].

A goods supply to a customer holding a USt-IdNr. is therefore **not** automatically a
plain §4a 0% intra-EU delivery — it may fall inside the §13b reverse-charge list (certain
goods categories). The goods-vs-services split used by the canonical skill is an
oversimplification; the full §13b Abs. 1 list must be consulted per transaction.

### Correction 2 — intra-community delivery (igL) is NOT §4a UStG

The canonical skill cites the intra-community delivery as §4a UStG. **That is wrong.**

- Intra-community delivery of goods (innergemeinschaftliche Lieferung, igL) =
  **UStG §4 Nr. 1b** (tax-favourable intra-community supply), with the substantive
  requirement in **UStG §6a** (steuerfreie innergemeinschaftliche Lieferung, requires a
  valid USt-IdNr. and the two-stage test).
- §4a UStG is "Steuervergütung" (tax refund) — a different rule entirely and not the igL
  citation.

## Sign-off gate

This skill's validator refuses to load it as certified until
`docs/reviews/ref-ust-edge-cases.md` exists with a signature and a date. Until then every
consumer must treat this skill as UNVERIFIED.

## Related

- Canonical implementation: `skills/business-de/ust-edge-cases/` (skills-business-de-r3 owns it)
- Journal mapping: `skills/business-de/skr-journal-mapping/`
- Sign-off placeholder: `docs/reviews/ref-ust-edge-cases.md`
