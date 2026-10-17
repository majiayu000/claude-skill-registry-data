---
name: verify-ironledger
description: Runs the IronLedger runtime verification harness to enforce financial balance invariants, database migration integrity, tax lot consistency, HUD rendering, and CSV ingest mapping.
---

# SKILL: verify-ironledger

Automated verification engine for IronLedger. Implements the **pstack / Poteto-Rules** framework: requires runtime evidence and hard invariant proofs before claiming tasks are complete.

## 1. MANDATORY PRINCIPLES
- **Evidence Before Confidence**: Never declare code or ledger state valid without running checks and capturing real command logs.
- **Run the Product**: Passing lints or type checks are insufficient; you must execute the double-entry engine and verify live database state.
- **Hard Invariants**: The double-entry balance invariant (\(\sum \text{Debits} = \sum \text{Credits}\)) must evaluate to zero net variance in exact cents across all active accounts.

---

## 2. IRONLEDGER FEATURE MAP

| Domain / Subsystem | Source Path | Verification Command | Expected Invariant |
| :--- | :--- | :--- | :--- |
| **Double-Entry Engine** | `src/ledger/` | `node scripts/verify-ledger.mjs --balance` | \(\sum \text{Debits} - \sum \text{Credits} = 0\) (Exact Cents) |
| **DB Schema Migrations** | `migrations/` | `node scripts/verify-ledger.mjs --migrations` | 0 pending migrations; Schema matches `HEAD` |
| **Tax Lot & Form 8949** | `src/tax/` | `node scripts/verify-ledger.mjs --tax-lots` | 0 orphan lots; Valid non-null acquisition dates & cost basis |
| **Workbench HUD** | `src/hud/` | `node scripts/verify-ledger.mjs --hud` | Component renders without DOM or console exceptions |
| **CSV Ingestion Profiles** | `src/ingest/` | `node scripts/verify-ledger.mjs --ingest` | Staging categories mapped with 100% deterministic rules |

---

## 3. VERIFICATION EXECUTION PROTOCOL

When invoked via `/verify-ironledger` or after modifying code in `IronLedger`:

1. **Execute Invariant Verifier Script**:
   ```bash
   node scripts/verify-ledger.mjs --all
   ```
2. **Audit Verification Gates**:
   - [ ] **Balance Invariant**: Total Debits minus Total Credits === 0¢ across all active accounts.
   - [ ] **Migration Gate**: Local DB schema is synchronized with migration files; 0 pending.
   - [ ] **Tax Lot Gate**: Zero orphan tax lots; valid holding periods and basis.
   - [ ] **Smoke Gates**: Workbench HUD mounts cleanly and CSV ingest mappings pass.

---

## 4. REPORTING PROTOCOL

Return a concise evidence report formatted as follows:

```text
VERDICT: [PASS | FIX | NEEDS HUMAN]

CHECKS EXECUTED:
- Balance Invariant: [PASS/FAIL] (Debits: $X.XX | Credits: $X.XX | Delta: $0.00)
- Migrations:        [PASS/FAIL] (Pending: 0 | Current HEAD: <commit/version>)
- Tax Lot Validation:[PASS/FAIL] (Orphan Lots: 0)
- Workbench HUD:     [PASS/FAIL] (Mounted cleanly)
- CSV Ingestion:     [PASS/FAIL] (Profiles deterministic)

EVIDENCE LOGS:
[Paste raw CLI verification output or script tail]

RECOMMENDED ACTION: [Commit & merge / Apply patch to src/... / Request human sign-off]
```
