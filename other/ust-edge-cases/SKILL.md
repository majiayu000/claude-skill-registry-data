---
name: ust-edge-cases
description: "Apply German VAT edge cases correctly: reverse charge (§13b UStG — the buyer is the tax debtor, services only), Kleinunternehmer §19, intra-EU B2B (06/0), OSS/IOSS, rounding to cents, and the e-invoice interplay. Use when an agent must decide the tax treatment of a cross-border or small-business invoice, pick the right Steuerschlüssel, or avoid the reverse-charge trap. Not for domestic standard-rate B2C sales."
license: MIT-compat
compatibility: "framework-agnostic; German UStG, EU VAT rules, offline"
metadata: {}
allowed-tools: []
---

# ust-edge-cases

## When to use this skill

Use this skill when an agent must decide the VAT treatment of a German invoice
that is **not** a plain domestic 19%/7% B2C sale — i.e. cross-border supplies,
small-business invoicing, installment payments, cent-level rounding, or the
interaction with e-invoicing rules.

Do **not** use it for domestic standard-rate B2C sales (covered by
`skr-journal-mapping`), for non-EU third-country supplies, or for tax advice
beyond what the sources below support.

## Procedure

1. **Identify the edge case** — reverse charge, small business, intra-EU,
   OSS, rounding, or e-invoice interplay (see decision table).
2. **Apply the rule** — pick the Steuerschlüssel and the tax amount.
3. **Check the precondition** — reverse charge (§13b) needs both a valid
   customer USt-IdNr. **and** a supply of **services** (IT, consulting,
   construction). §13b covers services, not goods; a goods supply with a buyer
   USt-IdNr. uses the general intra-EU rule (§4a) at 0% without reverse charge.
   **Article number re-verified 2026-10-09:** the UStG was restructured and
   §3g is now "Ort der Lieferung von Gas, Elektrizität, Wärme oder Kälte" — the
   reverse-charge article is §13b ("Leistungsempfänger als Steuerschuldner").
   Kleinunternehmer requires the prior-year turnover ≤ EUR 20,000 (UStG §19
   Abs. 1, read from config). A USt-IdNr. alone is not enough to trigger
   reverse charge.
4. **Generate the journal** — use `skr-journal-mapping` for the accounts and
   `scripts/ust_check.py` for the arithmetic.
5. **Verify** — run `scripts/ust_check.py` and the verification checklist.

## Decision tables

All tables below — edge-case selection, the goods-vs-services split, and the
e-invoice interplay — are expanded with worked examples and legal sources in
`references/procedures.md` §1-§6. The condensed rules:

Condensed rules: reverse charge (§13b) shifts the VAT debt to the buyer for
intra-community **services** only; a goods supply to a customer with a
USt-IdNr. is 0% under the general intra-EU rule (§4a) and is not reverse
charge. Kleinunternehmer (§19, turnover under EUR 20,000) charge no VAT and
issue a sonstige Rechnung; invoices under EUR 250 gross are exempt from the
issuing obligation. Worked examples and legal sources are in
`references/procedures.md` §1–§6.

## Worked examples

### Good output — intra-EU IT services, reverse charge
Input: German IT consultancy delivers a SaaS licence to a French customer
(USt-IdNr. FR12345678901, valid), EUR 5,000.00 net, supply_type `service`.
Expected output: tax key `06/0`, tax amount `0.00`, journal debits the customer
and credits the service account, and the invoice carries the reverse-charge
note "Steuerschuldner ist der Leistungsempfänger (§13b UStG)".
`scripts/ust_check.py invoice.json` → `OK VAT treatment valid, 1 lines`.

### Good output — intra-EU goods, no reverse charge
Input: a German wholesaler ships EUR 12,000.00 of goods to a Dutch customer
with a valid USt-IdNr., supply_type `goods`.
Expected output: tax key `06/0`, tax amount `0.00`, but `reverse_charge: false`
and the note reads "Innergemeinschaftliche Lieferung (§4a UStG)" — no
reverse-charge statement. `ust_check.py` exits 0.

### Bad output — reverse charge claimed on goods (the trap)
Input: same goods shipment, but the agent sets `reverse_charge: true`.
`ust_check.py` exits 2 with:
`FAIL line 1: reverse charge (§13b) applies to services only — supply_type 'goods' cannot use reverse charge; the general intra-EU rule (§4a) applies`
The agent must re-issue with `reverse_charge: false` and the §4a note.

### Bad output — Kleinunternehmer charging 19%
Input: a Kleinunternehmer (prior-year turnover EUR 18,000) invoices EUR 300.00
net with tax key `19` and tax amount EUR 57.00.
`ust_check.py` exits 2 with:
`FAIL line 1: Kleinunternehmer cannot charge VAT (key 19)`
Fix: re-issue as a sonstige Rechnung with tax key `0`, tax amount `0.00`.

### Bad output — unrounded tax amount
Input: EUR 33.33 net at 19% → stated tax amount EUR 6.3327.
`ust_check.py` exits 2 with:
`FAIL line 1: tax amount 6.3327 is not rounded to cents (§23 UStDV)`
Fix: state `6.33` (half-up) and re-run.

## Pitfalls from research

The single trap that catches most agents: **reverse charge (§13b) is services
only** — a goods supply to a customer that supplies a USt-IdNr. is taxed at
0% under the general intra-EU rule (§4a), not reverse charge. The article
number was re-verified 2026-10-09 (dejure.org: §3g is now the gas/electricity
place-of-supply rule). The full list of five traps, with sources, is in
`references/procedures.md` §1–§6.

## Verification checklist

- [ ] Edge case identified per decision table
- [ ] Precondition checked (USt-IdNr., turnover threshold, services category)
- [ ] Tax key matches the legal rate
- [ ] Tax amount computed and rounded to cents
- [ ] `scripts/ust_check.py` exits 0
- [ ] E-invoice interplay documented (e-invoice vs sonstige Rechnung)

## Related skills

[skr-journal-mapping](../skr-journal-mapping/) — the Steuerschlüssel this skill validates are assigned by the journal mapper
[gobd-archive](../gobd-archive/) — tax decisions and ruling evidence are correspondence (6y)

## References

- [Procedures and worked examples](references/procedures.md)
- [Standards and sources](references/SOURCES.md)
- [EVALS](references/EVALS.md)
