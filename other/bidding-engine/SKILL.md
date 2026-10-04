---
name: bidding-engine
description: Dynamic pricing and RFQ responses. Formulates high-margin corporate bids and scenario-based pricing matrices.
version: 3.0.0
author: AgentBoost Enterprise
enterprise: true
category: Finance
---

### System Instructions
You are equipped with the `bidding-engine` deterministic tool. This tool calculates optimal corporate bid prices using margin protection and scenario analysis. It generates automated professional proposal documentation for high-value requests for quotation (RFQs).

### Execution Protocol
Invoke the bidding engine by passing strictly formatted JSON:

```json
{
  "rfq_id": "RFQ_LOG_2026_011",
  "target_margin_percent": 22.5,
  "variable_costs_usd": 125000,
  "competitor_price_baseline_usd": 165000,
  "generate_proposal_document": true
}
```

Outputs
- Margin-optimized bid price calculation.
- Scenario-based pricing matrix and sensitivity analysis.
- Automated professional RFQ proposal documentation.
- Bid win probability and margin protection score.
