---
name: expense-reporting-bot
description: Expense reporting bot. Expense validation, policy checks and finance-ready reports.
version: 3.0.0
author: AgentBoost Enterprise
enterprise: true
category: Finance
---

### System Instructions
You are equipped with the `expense-reporting-bot` deterministic tool. This tool performs automated validation of expense receipts against corporate fiscal policies. It identifies policy exceptions and prepares finance-ready reconciliation reports for accounting export.

### Execution Protocol
Invoke the expense engine by passing strictly formatted JSON:

```json
{
  "expense_claim_id": "EXP_NOV_2026_C44",
  "validate_receipt_images": true,
  "check_policy_compliance": true,
  "export_format": "ERP_Reconciliation_CSV"
}
```

Outputs
- Receipt matching and validation verification report.
- Corporate policy enforcement and exception logs.
- Finance-ready reconciliation and export files.
- Corporate expense audit trail and compliance score.
