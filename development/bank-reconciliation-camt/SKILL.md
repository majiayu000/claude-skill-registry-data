---
name: bank-reconciliation-camt
description: "Parse CAMT.053/MT940 bank statements, match postings to open items with multi-key heuristics, detect duplicates and unallocated differences, and produce a reconciled Kontoauszug. Use when an agent must reconcile a bank account, auto-allocate payments to customers/suppliers, or flag unexplained differences. Not for card acquirer statements or non-SEPA currencies."
license: MIT-compat
compatibility: "framework-agnostic; ISO 20022 camt.053, SWIFT MT940, EBICS, offline"
metadata: {}
allowed-tools: []
---

# bank-reconciliation-camt

## When to use this skill

Use this skill when an agent must reconcile a bank account from a
**CAMT.053** (ISO 20022) or **MT940** (SWIFT) statement — parse the file,
assign each posting to an open item (customer, supplier or refund), spot
duplicate bookings and unexplained differences, and produce a reconciled
Kontoauszug.

Do **not** use it for card acquirer (card scheme) statements, non-SEPA
currencies, or cash-counting tasks.

## Procedure

1. **Parse the statement** — XML (camt.053) or MT940 (SWIFT plain text).
   Extract account, opening/closing balance, and every entry (amount, date,
   reference, counterparty, purpose).
2. **Verify balances** — opening balance + entries = closing balance. A
   mismatch is a hard stop.
3. **Match postings** — run the heuristic cascade in
   `references/procedures.md` §3 (amount → reference → counterparty → date).
4. **Flag duplicates** — an entry whose amount, reference and value date all
   match an earlier entry is a duplicate.
5. **Allocate** — assign each matched entry to an open item; clear any
   remaining difference with a reason code.
6. **Verify** — run `scripts/recon_check.py`; the verification checklist.

## Decision tables

### Match priority

Apply these four rules in order and stop at the first one that fires:

| Step | Signal | Wins when |
|---|---|---|
| 1 | amount exact + ledger reference | unambiguous |
| 2 | amount exact + counterparty name | reference missing or free text |
| 3 | amount within ±tolerance + date in window | partial match |
| 4 | reference only | allocation by mandate/SEPA ID |

Never allocate on amount alone when two open items share the amount. The
full cascade with worked examples is in `references/procedures.md` §3.

### Duplicate detection

| Signal | Threshold |
|---|---|
| Same amount | exact to cents |
| Same reference (Verwendungszweck) | exact |
| Same value date | same calendar day |
| All three true | **duplicate** — block allocation |

### Reason codes

| Code | Use when |
|---|---|
| ROUNDING | difference under EUR 0.01 |
| BANK_FEE | bank charge not in the ledger |
| FX | currency conversion delta |
| UNALLOCATED | entry with no open item, documented |

## Worked examples

### Good output — exact amount + reference match
Input: camt.053 entry `-1.200,00`, Verwendungszweck `RECHNUNG INV-001`,
value date 2026-03-10. Open item INV-001 for customer A, EUR 1,200.00.
Expected behaviour: step 1 fires (amount exact + ledger reference) → allocate
to INV-001, clear the item. `scripts/recon_check.py` exits 0, report shows
`1 matched, 0 unallocated, 0 duplicate`.

### Bad output — amount-only allocation when two items share the amount
Input: two open items both at EUR 1,200.00 (INV-001 and INV-002), and the
statement entry has no usable reference.
Expected behaviour: step 1 fails (no reference), step 2 fails (no counterparty
name either) → the entry is **not** allocated by amount alone.
`scripts/recon_check.py` exits 1 with:
`UNALLOCATED: entry -1.200,00 on 2026-03-10 matches no open item uniquely`
Fix: escalate to the accountant with the two candidate items. Guessing
allocates the wrong customer and the off-by-one follows the ledger into the
USt-Anmeldung.

### Good output — duplicate detected and blocked
Input: two entries, both `-1.200,00`, reference `INV-001`, value date
2026-03-10 (second one at 2026-03-10 14:00).
Expected behaviour: the second entry matches all three duplicate signals →
flagged `duplicate`, blocked from allocation, listed in the report.
`scripts/recon_check.py` exits 1 with `1 duplicate blocked`.

### Bad output — legacy `.008.01` namespace accepted silently
Input: a camt.053 file whose root element declares
`xmlns="urn:iso:std:iso:20022:tech:xsd:camt.053.001.08"` but the file itself
says `.008.01` in the XML schema location.
Expected behaviour: the parser rejects the legacy namespace rather than
accepting it. `.008.01` is a draft; the current schema is `.001.08`.
Re-parse with the newer schema; do not trust the declaration.

### Good output — rounding difference cleared as ROUNDING
Input: closing balance off by EUR 0.003 (bank rounding on a SEPA transfer).
Expected behaviour: difference under EUR 0.01 → reason code `ROUNDING`,
cleared automatically, no escalation. Report: `1 rounding, 0 unallocated`.

## Pitfalls from research

The single trap that catches most agents: **camt.053 files declaring the
`.008.01` namespace are legacy drafts** — the current version is
`camt.053.001.08`; re-parse with the newer schema rather than accepting the
older namespace silently. The full list of five traps, with sources, is in
`references/procedures.md` (format selection, duplicates, differences).

## Verification checklist

- [ ] Statement parsed (camt.053 or MT940)
- [ ] Opening + entries = closing balance
- [ ] Every entry matched or explicitly unallocated
- [ ] Duplicates blocked, not silently allocated
- [ ] Differences under EUR 0.01 are rounding
- [ ] `scripts/recon_check.py` exits 0


## Related skills

[gobd-archive](../gobd-archive/) — reconciled bank statements are vouchers (8y)

## References

- [Procedures and worked examples](references/procedures.md)
- [Standards and sources](references/SOURCES.md)
- [EVALS](references/EVALS.md)
