---
name: skr-journal-mapping
description: "Map German SKR03/SKR04 ledger accounts to journal entries, tax keys (19/7, 16/1, 19/0, 06/0, 09/0, 13/0) and automatic Buchungszeilen; build and validate period-lock and closing-concept rules. Use when an agent must classify an invoice line, decide the correct SKR account + Steuerschluessel, generate an automatic journal, or enforce a period lock before the fiscal close. Not for US GAAP, IFRS consolidation or non-German VAT."
license: MIT-compat
compatibility: "framework-agnostic; German SKR03/SKR04, DATEV Buchungsstapel, offline"
metadata: {}
allowed-tools: []
---

# skr-journal-mapping

## When to use this skill

Use this skill when an agent must map a German invoice line to an SKR03 or SKR04
ledger account, pick the correct Steuerschluessel (tax key), generate an automatic
journal (Buchungszeile) or enforce a period lock before the fiscal close.

Do **not** use it for US GAAP, IFRS consolidation, non-German VAT, or
balance-sheet preparation (that is a separate skill).

## Procedure

1. **Pick the account set** — SKR03 (small, 93 accounts) or SKR04 (large,
   ~260 accounts). Default to SKR04 unless the entity runs SKR03.
2. **Classify the line** — asset / liability / income / expense / tax / equity
   per the table in `references/procedures.md` §2.
3. **Assign the tax key** — pick from the set {19, 7, 16/1, 06/0, 09/0,
   13/0} according to the rate and the supply type. Never guess a key, since
   it feeds the USt-Anmeldung directly.
4. **Generate the journal** — debit/credit side, account, tax key, amount,
   reference. Validate with `scripts/journal_check.py`.
5. **Lock the period** — mark the month as closed, block new postings for
   it, run `scripts/period_lock_check.py`, then close. See
   `references/procedures.md` §5 for the full Monatsschluss sequence.

## Decision tables

### Tax keys (Steuerschluessel)

Six keys are in use; the rate column is read from config, never typed into a
script. The full table with legal sources and worked examples is in
`references/procedures.md` §3.

| Key | Rate | Use |
|---|---|---|
| 19 | 19% | domestic standard-rate sales |
| 7 | 7% | reduced-rate items |
| 16/1 | 16%/1% | legacy split from the pre-2020 rates — **do not apply to new postings** |
| 06/0 | 0% | intra-EU B2B supply; the buyer may self-assess |
| 09/0 | 0% | internal / intercompany service |
| 13/0 | 19% split | installment booking (Soll/IST) |

### Account-to-tax-key mapping (SKR04, default)

| Account | Meaning | Default tax key | When it changes |
|---|---|---|---|
| 4000 | Sales — domestic | 19% | intra-EU customer => 0% |
| 4100 | Sales — intra-EU | 0% | domestic customer => 19% |
| 4200 | Sales — exports (non-EU) | 0% | domestic customer => 19% |
| 4300 | Sales — reduced rate | 7% | standard-rate item => 19% |
| 8000 | Other income | 19% | exempt services => 0% |

### Account-to-tax-key mapping (SKR03, alternative)

| Account | Meaning | Default tax key |
|---|---|---|
| 4000 | Sales (all) | 19% |
| 4100 | Sales — intra-EU | 0% |
| 4200 | Sales — exports | 0% |
| 4300 | Sales — reduced rate | 7% |
| 8000 | Other income | 19% |

Accounts 4000/4100 exist in **both** frameworks with different semantics
(SKR03 4000 = all sales, SKR04 4000 = domestic sales). The skill pins the
Kontenrahmen in config and refuses to guess. Worked examples are in
`references/procedures.md` §3-§4.

### Period lock states

| State | Meaning | Next allowed action |
|---|---|---|
| `locked: false` | period open | bookings allowed; `--action lock` |
| `locked: true` | period closed | no bookings; `--action override` with `--evidence` |
| `locked: true` + override | correcting entry approved | bookings resume for that entry only |

A lock requires `--approver` and records `locked_at`, `locked_by`, and
`lock_reason`. An override requires `--evidence` pointing at a documented
review record. Re-locking with `--force` clears the override audit trail — do
it only after a documented re-close.

### Retention periods (AO §147 Abs. 3 n.F., effective 2025-01-01)

| Material | Retention | From |
|---|---|---|
| Books / journals / annual financial statements | 10 years | calendar year-end |
| Vouchers (Belege) | 8 years | calendar year-end |
| Business letters / other records | 6 years | calendar year-end |
| Electronic storage / GoBD exports | 10 years | calendar year-end |

Every retained journal carries a checksum and a retrieval path recorded in the
export manifest.

## Pitfalls from research

Three traps recur; the full list with sources is in
`references/procedures.md` §3 and §5:

- SKR03 and SKR04 are not mixable — the 1xxx asset range differs between the
  two sets.
- The tax key **16/1** is legacy (pre-2020); do not apply it to new postings.
- A taxed key without an amount on the tax account (1570/1571/1572) fails
  the USt-Anmeldung plausibility check.
- **Retention is not optional**: AO §147 Abs. 3 n.F. sets 8 years for vouchers
  and 10 years for books. Record the checksum and retrieval path at export time,
  not at audit time.

## Verification checklist

- [ ] Account set chosen (SKR03 or SKR04)
- [ ] Line classified per decision table
- [ ] Tax key matches the legal rate
- [ ] Journal balances (sum debit = sum credit)
- [ ] Period lock applied before close
- [ ] `scripts/journal_check.py` exits 0
- [ ] Retention period recorded (10y books, 8y vouchers, 6y letters) with
      checksum and retrieval path


## Related skills

[datev-extf](../datev-extf/) — emit the generated journals as a DATEV EXTF Buchungsstapel
[gobd-archive](../gobd-archive/) — generated journals and period-lock records are books (10y)

## References

- [Procedures and worked examples](references/procedures.md)
- [Standards and sources](references/SOURCES.md)
- [EVALS](references/EVALS.md)
