---
name: supplier-negotiator
description: Strategic Sourcing & Commercial Terms Arbitrator. Conducts automated commercial term arbitrage and contract reinforcement with global vendor networks to optimize working capital.
version: 3.0.0
author: AgentBoost Quantitative Trading Fleet
enterprise: true
category: Procurement & Supply
---

### System Instructions
You are equipped with the `supplier-negotiator` autonomous agent. This agent monitors supply chain delivery variances and vendor price increase requests. It automates proactive commercial term renegotiation and generates liquidated damages documentation for contractual breaches.

### Execution Protocol
Invoke the procurement engine by passing strictly formatted JSON:

```json
{
  "vendor_id": "vendor_99",
  "negotiation_objective": "extend_payment_terms_net_90",
  "performance_history_lookback_days": 180,
  "generate_discrepancy_notice": true
}
```

Outputs
- Vendor performance index and risk score.
- Automated renegotiation script and counter-offer text.
- Liquidated damages and breach documentation drafts.
- Working capital optimization impact projection.
