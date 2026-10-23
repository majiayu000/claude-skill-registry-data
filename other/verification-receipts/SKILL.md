---
name: verification-receipts
description: Attach a ledger-backed receipt to every completion claim so no Bot asserts success without proof the desk can re-check.
bots:
  - all
gates:
  - G-2
required_tools:
  - desk.receipt_check
required_data: []
permissions:
  max_side_effect: read
  network: true
  filesystem: none
fixtures:
  - tests/fixtures/replay/smoke
---

# Verification Receipts

## L1 - Summary

No completion claim without a receipt. Every Bot that reports work done attaches a receipt the desk can re-check with `desk.receipt_check`: what was claimed, which ledger rows prove it, and who approved it. An unreceipted claim is an unmade claim.

```
claim made -> receipt attached (desk.receipt_check exit 0) -> CHIEF accepts
claim made -> no receipt                       -> CHIEF rejects, work repeats
```

## L2 - Method

1. S1 - State the claim narrowly: ticket id, action taken, and the ledger event types that prove it (`OrderPlaced`, `FillRecorded`, `JournalNote`). Vague claims ("looks good") are not claims.
2. S2 - Query the proof with `desk.receipt_check`: pass the ticket id and the expected event kinds. The tool returns PASS only when the ledger holds matching rows; otherwise it names what is missing.
3. S3 - Record the approval: every receipt names `approved_by` (a seat for autonomous steps, `human:<id>` for human-gated steps per G-2). Self-approval is void.
4. S4 - Chain the receipt: the receipt for step N references the receipt for step N-1, so a broken chain points at the exact step that lost its proof.
5. S5 - Surface failures plainly: a FAIL names the missing row and the step to repeat. Never edit the ledger to manufacture a PASS; append-only always wins.

## Failure modes

| Symptom | Cause | Action |
|---|---|---|
| Receipt FAIL on a real fill | Wrong ticket id or event kind in the query | Re-query with the exact ticket id from `pumpgrok ticket list`; check the kind spelling |
| Missing approval | Step ran without an approval record | Route through RISK or the human; backdated approvals are void |
| Broken receipt chain | An intermediate step skipped its receipt | Re-run the missing step with its receipt; do not splice the chain |
| Ledger row absent | The write never happened (crash before append) | Treat the step as not done; repeat the step, never forge the row |

## References

- Tool: `desk.receipt_check` (receipt query; resolvable by every seat via `_core`)
- Receipt schema: `contracts/tool-rosters/_core.yaml` (core eight)
- Gate G-2: approval integrity behind every receipted claim
- Companion skills: `desk-doctor` (desk health proof), `desk-post-trade-review` (graded review rows)
