---
name: vendor-nda-streamliner
description: Commercial NDA & Mutual Agreement Intake Director. Reviews incoming non-disclosure and commercial agreements, highlighting non-standard terms.
version: 3.0.0
author: AgentBoost Quantitative Trading Fleet
enterprise: true
category: Legal
---

### System Instructions
You are equipped with the `vendor-nda-streamliner` autonomous agent. This agent identifies text variations against pre-approved corporate NDA standards. It provides contextual clause recommendations and prioritizes legal team intake based on commercial deal value.

### Execution Protocol
Invoke the NDA engine by passing strictly formatted JSON:

```json
{
  "vendor_id": "VEN_PARTNER_99",
  "document_type": "Mutual_NDA",
  "deal_value_usd": 1500000,
  "generate_clause_recommendations": true
}
```

Outputs
- Identification report of variations against corporate NDA standards.
- Contextual clause recommendation and redline drafts.
- Intake queue prioritization for legal team review.
- Partnership contract modification and risk assessment logs.
