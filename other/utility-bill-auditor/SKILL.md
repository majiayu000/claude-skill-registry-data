---
name: utility-bill-auditor
description: Commercial Utility Invoice Auditing & Overcharge Arbitrator. Cross-references facility invoices against rate tariffs to discover billing discrepancies.
version: 3.0.0
author: AgentBoost Quantitative Trading Fleet
enterprise: true
category: Facilities
---

### System Instructions
You are equipped with the `utility-bill-auditor` autonomous agent. This agent cross-checks invoices against commercial utility rate cards and tariffs. It detects meter read discrepancies and automates the generation of formal commercial billing dispute packages.

### Execution Protocol
Invoke the audit engine by passing strictly formatted JSON:

```json
{
  "utility_invoice_id": "BILL_ELEC_OCT_2026",
  "site_location": "Manufacturing_Beta",
  "rate_card_tariff": "Commercial_High_Volume_G10",
  "generate_dispute_package": true
}
```

Outputs
- Invoice cross-check report against commercial rate cards.
- Detection log of meter read and consumption volume errors.
- Automated commercial billing dispute and recovery packages.
- Utility usage surge and tariff framework update alerts.
