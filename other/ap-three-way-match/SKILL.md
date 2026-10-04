---
name: ap-three-way-match
description: Invoice & PO 3-Way Matcher. Autonomous reconciliation of vendor invoices against purchase orders and warehouse goods receipts.
version: 3.0.0
author: AgentBoost Enterprise
enterprise: true
category: Finance & Accounting
---

### System Instructions
You are equipped with the `ap-three-way-match` deterministic tool. This tool performs high-precision reconciliation between vendor invoices, purchase orders (PO), and goods received notes (GRN). It detects overbilling, shortfalls, and VAT/tax recalculation errors.

### Execution Protocol
Invoke the accounting engine by passing strictly formatted JSON:

```json
{
  "invoice_id": "INV_VEN_8841",
  "po_id": "PO_PURCHASE_001",
  "grn_id": "GRN_RECV_442",
  "variance_tolerance_usd": 10.0,
  "recalculate_vat": true
}
```

Outputs
- Overbilling and shortfall detection log.
- VAT and tax recalculation verification.
- Three-way match reconciliation status (MATCHED/DISCREPANCY).
- Automated vendor credit note generation directives.
