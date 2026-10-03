---
name: settlement-financials
description: "Calculates settlement financial statements showing gross, fees, disbursements, and net to client. Use when Mandy says 'settlement financials', 'SFS', 'what would the client get', 'calculate settlement', 'net to client', or provides a settlement amount. Supports multiple scenarios."
---

# Settlement Financials

## Important
- Manual-only. Consult `sfs-format.md` for output format.
- Include s184 LPUL mandatory disclosure.
- Accept multiple amounts for side-by-side comparison.

## Instructions

### Step 0: Resolve Matter

### Step 1: Parse and Gather
Get settlement amount(s). Read `matter.json` financials + `reference/fee-schedule.json`.
If disbursements seem incomplete: ask Mandy about additional items.

### Step 2: Calculate
Per `sfs-format.md`: gross - fees - fees_gst - disbursements - disb_gst = net.
For multiple amounts: side-by-side table.

### Step 3: Save and Commit
Save to `letters/settlement-financial-statement-{date}.md`.
Update financials in `matter.json`. Update index. Log and commit. Present.
