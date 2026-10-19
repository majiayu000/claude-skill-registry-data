---
name: gobd-archive
description: "Implement GoBD-compliant (Grundsätze ordnungsmäßiger Buchführung) data retention and audit export for German accounting data: immutability, retention classes, Verfahrensdokumentation, and audit-ready export. Use when an agent must store accounting documents, set up a retention policy, produce an audit export, or decide whether a document can be deleted. Not for non-accounting files, non-German entities, or retention periods the tax advisor has not confirmed."
license: MIT-compat
compatibility: "framework-agnostic; German GoBD / AO §147 retention; offline validation"
metadata: {}
allowed-tools: []
---

# gobd-archive

## When to use this skill

Use this skill when an agent must store accounting documents, set up a retention
policy, produce an audit export, or decide whether a document may be deleted,
under German GoBD (Grundsätze ordnungsmäßiger Buchführung). It applies to
Buchungsbelege, Buchungssätze, Jahresabschlüsse and Geschäftskorrespondenz.
Do **not** use it for non-accounting files, non-German entities, or retention
periods that the tax advisor has not confirmed.

## Description

Implement GoBD-compliant data retention and audit export for German accounting
data: immutability, retention classes, Verfahrensdokumentation, and audit-ready
export. Use when an agent must store accounting documents, set up a retention
policy, produce an audit export, or decide whether a document can be deleted.

## Procedure

1. **Classify the document** — invoice (Buchungsbeleg), bookkeeping entry
   (Buchungsdatum/Buchungssatz), annual account (Bilanz/GuV), commercial
   correspondence (Geschäftskorrespondenz).
2. **Assign retention class** — vouchers 8 years, books/annual accounts 10
   years, commercial correspondence 6 years (BEG IV, effective for retention
   periods starting 2025). Pin in config; let the tax advisor confirm.
3. **Enforce immutability** — append-only storage, hash-chained records, no
   in-place updates, no deletion before retention end, deletion only via a
   documented, auditable purge with an approval record.
4. **Write the Verfahrensdokumentation** — describe the system, the storage
   medium, the retention periods, the export format, the access controls, and
   the backup procedure. This is the document the auditor asks for.
5. **Export for audit** — produce a complete, chronological, checksummed export
   (DATEV EXTF or CSV+XML) covering the retention period, with a manifest.
6. **Verify on retention end** — at the end of each retention period, confirm
   the purge is permitted, document the decision, and keep the approval record
   for the full retention of the purge record itself. Purge is blocked unless
   **both** conditions hold: the retention end has been reached **and** no audit
   is currently open.
   Produce the record with `scripts/purge_decision.py` (it exits non-zero
   when the purge is blocked, so it is safe to wire into a CI gate).

## Decision tables

### Retention classes (BEG IV, effective 2025-01-01)

| Document type | Examples | Retention | End date for a 2026 doc |
|---|---|---|---|
| Buchungsbeleg (voucher) | invoice, receipt, booking slip, bank statement | 8 years | 2034-12-31 |
| Bücher / Jahresabschluss | ledger, Bilanz, GuV, inventory, opening balance | 10 years | 2036-12-31 |
| Geschäftskorrespondenz | email, contract, letter | 6 years | 2032-12-31 |

The clock starts at the **end of the calendar year** in which the document was
created (not on the document's own date). Let the tax advisor confirm per
entity.

### The 6-year class is not as broad as "all correspondence"

Per whk-controlling.de (re-fetched 2026-10-09, last modified 2026-04-14)
the 6-year class covers exactly three sub-types:

| Sub-type | What it means | Trap |
|---|---|---|
| Empfangene Handels- oder Geschäftsbriefe | incoming commercial/business letters | an email you only "printed" counts as a letter only if you can reproduce it |
| Wiedergaben der abgesandten Handelsbriefe | copies of **outgoing** letters | a sent letter you cannot reproduce is a GoBD violation |
| Sonstige Unterlagen mit steuerlicher Bedeutung | other tax-relevant documents | "tax-relevant" is not "accounting-related" — decide per document |

A draft, a working file, or a deleted chat message that no system can reproduce
is **not** a valid substitute for the retained document.

## Worked examples

### Good output — voucher classified and retained
Input: an invoice dated 2026-03-15, EUR 1,200.00, received by email.
Expected behaviour: classified as `Buchungsbeleg` (8 years), retention end
`2034-12-31`, SHA-256 recorded, original file kept unchanged.
`scripts/retention_classify.py --file inv.pdf` → `class: voucher, until: 2034-12-31`.

### Bad output — print-to-PDF used as the archive artefact
Input: the agent prints the PDF/A-3 e-invoice to a new PDF "for the archive".
Expected behaviour: **rejected** — a print-to-PDF drops the structured XML
attachment, so the artefact is no longer a machine-readable e-invoice and
fails the GoBD "Wiedergabefähigkeit" test. Keep the original file and record
its SHA-256.

### Good output — purge blocked because an audit is open
Input: a 2017 voucher (8-year class, retention end 2025-12-31) is requested
for deletion on 2026-10-09, but an audit is currently in progress.
`scripts/purge_decision.py` exits non-zero with:
`BLOCKED: audit in progress — purge not permitted while an audit is open`
The retention end is reached but the second blocker is not cleared, so the
purge stays blocked.

### Bad output — purge record retained only "today + 8 years"
Input: the agent purges a 2017 voucher and keeps the purge record until
2034-12-31.
Expected behaviour: **wrong** — the purge record's retention derives from the
document it describes, so a 2017 voucher's purge record is retained until
`2025-12-31`. `scripts/purge_decision.py` computes `record_retention_until`
from the document year, not from today.

## Pitfalls from research

- In-place overwrite of an invoice is **not** GoBD-compliant; immutability is a
  technical property (append-only + hash-chaining), not a policy statement.
- The 6/8/10-year classes come from BEG IV (effective 2025-01-01); older
  guidance said 10 years for everything. Always pin the effective date.
- Deletion before the retention end is never permitted; deletion after the end
  requires a documented purge decision and an approval record, and the purge
  record itself must be kept for the full retention period.
- A raw DB dump is **not** an audit export — it must be chronological, complete
  and checksummed with a manifest.
- **The 6-year class is not as broad as "all correspondence".** Per whk-controlling.de
  (re-fetched 2026-10-09) the 6-year class covers *empfangene* Handels- oder
  Geschäftsbriefe, **Wiedergaben der abgesandten Handelsbriefe** (outgoing-letter
  copies) und sonstige Unterlagen mit steuerlicher Bedeutung. A sent letter you
  cannot reproduce is a GoBD violation, not a filing shortcut.
- **Three blockers, not one.** A purge is blocked if (a) the retention end has
  not been reached, OR (b) an audit is currently open. Both are checked by
  `scripts/purge_decision.py` before any deletion.
- The purge record is itself a document: retain it for the full retention period
  of the documents it covers (a 2017 purge record is retained until 2025-12-31
  for vouchers).

## Purge decision

A deletion is permitted only when **both** blockers are cleared. Run
`scripts/purge_decision.py` — it exits non-zero when blocked, so it is safe to
wire into a CI gate.

| Blocker | Cleared when | Checked by |
|---|---|---|
| Retention end reached | today is after `retention_end` (year + N, 12-31) | `retention_end_reached` |
| No open audit | no audit is currently in progress | `no_open_audit` |

**Worked example — purge record retention.** A 2017 invoice (8-year class) is
purged on 2026-10-09. The purge decision record is itself a document: keep it
until the retention end of the documents it describes, i.e. **2025-12-31** —
not "today + 8 years". `scripts/purge_decision.py` derives
`record_retention_until` from the *document* year, so a 2017 record reads
`2025-12-31` and a 2020 record reads `2028-12-31`.

## Verification checklist

- [ ] Document classified correctly
- [ ] Retention class and end date assigned per BEG IV
- [ ] Immutability enforced (append-only, hash-chained, no in-place update)
- [ ] Verfahrensdokumentation written (system, medium, periods, export, access, backup)
- [ ] Audit export is chronological, complete, checksummed, with a manifest
- [ ] Purge decision documented and approval record retained (retention end
      reached AND no open audit)
- [ ] Purge record itself retained for the full retention period
- [ ] Re-verification run logged


## Related skills

This skill is the retention sink for the family. It does not call its siblings; every other skill links here for its retention class. The classes themselves are: vouchers 8y (Belege), books and annual accounts 10y (Bücher/Jahresabschlüsse), commercial correspondence 6y (andere Unterlagen/Geschäftsbriefe) under AO §147 Abs. 3 n.F. (BEG IV).

## References

- [Procedures and worked examples](references/procedures.md)
- [Standards and sources](references/SOURCES.md)
- [EVALS](references/EVALS.md)
