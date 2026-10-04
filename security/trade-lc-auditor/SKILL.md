---
name: trade-lc-auditor
description: Letter of Credit & Trade Auditor. Scans bank LCs, bills of lading, and shipping manifests to eliminate discrepancy rejections.
version: 3.0.0
author: AgentBoost Enterprise
enterprise: true
category: Logistics & Trade
---

### System Instructions
You are equipped with the `trade-lc-auditor` deterministic tool. This tool analyzes bank Letters of Credit (LC) and shipping documentation to ensure total alignment. It detects date mismatches, tolerance breaches, and structural non-compliance with UCP 600 standards.

### Execution Protocol
Invoke the trade engine by passing strictly formatted JSON:

```json
{
  "document_id": "LC_SHIP_9921",
  "lc_value_usd": 1500000,
  "shipping_deadline": "2026-11-15",
  "tolerance_percent": 5,
  "check_ucp_600_compliance": true
}
```

Outputs
- Discrepancy detection report (dates, amounts, description).
- UCP 600 compliance audit status.
- Zero-demurrage risk assessment.
- Bank presentation readiness scorecard.
