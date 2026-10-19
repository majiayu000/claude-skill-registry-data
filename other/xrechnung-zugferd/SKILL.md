---
name: xrechnung-zugferd
description: "Generate, validate and archive German e-invoices (XRechnung / ZUGFeRD / Factur-X) compliant with EN 16931 and the UStG e-invoicing obligation (§14 UStG). Use when an agent must create, check, receive, convert or store e-invoices for B2B/B2G flows, decide whether a document is a valid e-invoice, pick the right profile, or set up a GoBD-compliant retention pipeline. Not for PDF-only invoices or non-German jurisdictions."
license: MIT-compat
compatibility: "framework-agnostic; German e-invoicing standards (EN 16931, Factur-X, XRechnung); offline validation"
metadata: {}
allowed-tools: []
---

# xrechnung-zugferd

## When to use this skill

Use this skill when an agent must create, validate, convert, archive or decide the validity of a German e-invoice (XRechnung / ZUGFeRD / Factur-X) under EN 16931 and UStG §14. It applies to B2B and B2G flows where a machine-readable invoice is required or expected. Do **not** use it for PDF-only invoices, non-German jurisdictions, or unstructured credit notes.

## Description

Generate, validate and archive German e-invoices (XRechnung / ZUGFeRD / Factur-X) compliant with EN 16931 and the UStG e-invoicing obligation (§14 UStG). Use when an agent must create, check, receive, convert or store e-invoices for B2B/B2G flows, decide whether a document is a valid e-invoice, pick the right profile, or set up a GoBD-compliant retention pipeline. Not for PDF-only invoices or non-German jurisdictions.

## Procedure

1. **Classify the document** — XML-only (XRechnung), hybrid PDF/A-3 + XML (ZUGFeRD/Factur-X) or other. Reject paper/PDF-only as "sonstige Rechnung".
2. **Pin versions** — read pinned spec+validator versions from `config/versions.json` (never hardcode). Re-verify on a scheduled cadence; record in SOURCES.md.
3. **Choose the profile** — MINIMUM / BASIC WL / BASIC / EN 16931 (COMFORT) / EXTENDED. Default for B2B: EN 16931/COMFORT. EXTENDED only when sector extensions are required.
4. **Validate** — run the KoSIT validator (tag `v2026-08-31`) or the pure-PHP `john-wink/en16931-php` v0.2.0 fallback against the pinned configuration. Treat every error as blocking; warnings must be documented. Run `scripts/validate_invoice.py` for the offline subset; it scopes every BT-* check to the element's own text (see the table below) and exits non-zero on any failure.
5. **Check business rules** — mandatory BT-* fields, Leitweg-ID in BT-10, payment terms syntax in BT-20, tax split per rate.
6. **Archive** — retain the **original** artefact as-is (XML, or PDF/A-3 with embedded XML). Never retain a print-to-PDF copy: a print-to-PDF **drops the structured XML attachment**, so it is not a valid archive artefact. Retention is 8 years from year-end (BEG IV, effective 2025-01-01). Record SHA-256, retrieval path and an export test in the retention log; verify the archive later with `scripts/retention_check.py`.
7. **Re-verify** — on any spec/validator bump, re-validate the whole archive sample; log the run.

## Decision tables

### Profile selection

| Context | Data available | Recipient capability | Recommended profile |
|---|---|---|---|
| B2B domestic | Full EN 16931 data | Factur-X capable | COMFORT (EN 16931) |
| B2B domestic | Basic data only | ZUGFeRD BASIC | BASIC |
| B2G (Offentlicher Auftraggeber) | Full data | XRechnung required | COMFORT or EXTENDED |
| B2B cross-border | Full data | Factur-X capable | COMFORT |
| B2C / private | Minimal data | Any | MINIMUM (rarely an e-invoice) |

## Pitfalls from research

- A PDF/A-3 with an unstructured attachment is **not** a ZUGFeRD invoice; the XML must be a Factur-X/ZUGFeRD structured attachment.
- KoSIT validator 5.x treats missing BT-14 (invoice issue date) as a hard error in every profile; do not suppress it.
- The 2025-2028 transitional period allows paper-to-PDF migration, but the e-invoicing obligation for B2B still applies from 2020-01-01.
- Version pinning matters: the standard moves twice a year; always read `config/versions.json`.
- **BT-18 ≠ BT-20.** Both are "payment" rules and some UBL exports use the same
  local name `PaymentTerms` for both. BT-18 is the **payment account (IBAN)**,
  BT-20 is the **payment terms (free text)**. A whole-document content regex
  therefore false-passes: an IBAN satisfies BT-20's "contains a digit" test and a
  Leitweg-ID satisfies BT-18's IBAN-shaped test. Always scope the check to the
  element's own text content (see `references/procedures.md` §5). Verified
  2026-10-09 against the KoSIT `guidelines.json`.
- BT-19 (tax amount per rate) is required in COMFORT/EXTENDED; a BG-19 tax split
  whose per-rate amounts do not sum to the invoice total is a hard error.
- A `print-to-PDF` of an e-invoice **drops the structured XML attachment**,
  so it is **not** a valid archive artefact — keep the original file (XML,
  or PDF/A-3 with embedded XML) and record its SHA-256.

## Element-scoped BT-* table

Verified 2026-10-09 against the KoSIT `validator-configuration-xrechnung`
rule IDs and `cbc:` element names. Scope every check to the element's own
text — never run a content regex over the whole document.

| Rule | Element | What it is | Mandatory in |
|---|---|---|---|
| BT-10 | `cbc:EndpointID` / `LeitwegID` | buyer/seller identifier (Leitweg-ID) | B2B |
| BT-14 | `cbc:IssueDate` | invoice issue date | **every profile** |
| BT-15 | `cbc:DeliveryDate` | delivery date | BASIC WL+ |
| BT-17 | `cbc:PaymentDueDate` | payment due date | BASIC+ |
| BT-18 | `cbc:PaymentAllowedAccountID` | payment account (IBAN) | BASIC+ |
| BT-19 | `cbc:TaxAmount` | tax amount per rate | COMFORT/EXTENDED |
| BT-20 | `cbc:PaymentTerms` | payment terms (free text) | **every profile** |

**The trap:** BT-18 (`PaymentAllowedAccountID`, an IBAN) and BT-20
(`PaymentTerms`, free text) share the local name `PaymentTerms` in some UBL
exports, and BT-10's `DE...` Leitweg-ID matches an IBAN regex. A whole-document
check false-passes both ways. `scripts/validate_invoice.py` extracts each
rule's element text by tag via `_element_text()` and tests the regex on that
text only.

## Archive retention

| Invoice year | Retention (BEG IV, 8y vouchers) | Retention end |
|---|---|---|
| 2026 | 8 years from year-end | 2034-12-31 |
| 2025 | 8 years from year-end | 2033-12-31 |
| 2024 | 8 years from year-end | 2032-12-31 |
| 2020 | 8 years from year-end | 2028-12-31 |
| 2017 | 8 years from year-end | 2025-12-31 |

Books/annual accounts are 10 years (2026 -> 2036-12-31); commercial
correspondence is 6 years (2026 -> 2032-12-31). The clock starts at the end
of the calendar year of creation, not on the document's own date.

## Verification checklist

- [ ] Document classified correctly (XML / hybrid / other)
- [ ] Profile selected per decision table
- [ ] Versions pinned and re-verification date recorded
- [ ] Validator run returns 0 errors (all errors blocking)
- [ ] BT-10 Leitweg-ID present for B2B
- [ ] BT-20 payment terms syntactically valid
- [ ] BT-18 payment account (IBAN) present and distinct from BT-20
- [ ] BT-19 tax amount per rate present; BG-19 sums to invoice total
- [ ] Every BT-* check scoped to the element's own text, not the whole document
- [ ] Original file archived unchanged; SHA-256 recorded
- [ ] Retention end date computed (8 years from year-end)
- [ ] Export test passed


## Related skills

[datev-extf](../datev-extf/) — feed the archived invoice into a DATEV EXTF Buchungsstapel
[ust-edge-cases](../ust-edge-cases/) — the tax amounts on the invoice are decided here
[gobd-archive](../gobd-archive/) — archived e-invoices are vouchers (8y); keep the original XML

## References

- [Procedures and worked examples](references/procedures.md)
- [Standards and sources](references/SOURCES.md)
- [EVALS](references/EVALS.md)
