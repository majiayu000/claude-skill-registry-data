---
name: expense-audit-sentinel
description: Corporate Card Spend & Fraud Prevention Sentinel. Audits corporate transaction streams and employee travel disbursements against fiscal guidelines.
version: 3.0.0
author: AgentBoost Quantitative Trading Fleet
enterprise: true
category: Finance
---

### System Instructions
You are equipped with the `expense-audit-sentinel` autonomous agent. This agent automates corporate expense documentation validation and ledger cross-matching. It identifies capital disbursement policy exceptions and flags multi-source duplicate reimbursement or billing fraud.

### Execution Protocol
Invoke the audit engine by passing strictly formatted JSON:

```json
{
  "employee_id": "EMP_8841",
  "expense_batch_id": "TRV_OCT_2026",
  "policy_framework": "Enterprise_Travel_Fiscal_Guidelines",
  "fraud_check_sensitivity": "institutional_rigor"
}
```

Outputs
- Expense documentation validation and cross-match report.
- Corporate capital disbursement policy exception log.
- Duplicate reimbursement and billing fraud detection status.
- Fiscal guideline compliance scorecard.
