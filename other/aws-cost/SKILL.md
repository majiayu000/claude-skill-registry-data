---
name: aws-cost-optimizer
description: Enterprise AWS cost analysis with optimization recommendations, budget forecasting, ROI tracking, and automated savings alerts. Integrates with CRM for customer account mapping.
version: 3.0.0
author: AgentBoost Enterprise
enterprise: true
---
### System Instructions
You MUST call `run_js` with a strictly formatted JSON string into `data`.
```json
{
  "type": "object",
  "properties": {
    "region": { "type": "string" },
    "resource_type": { "type": "string" }
  },
  "required": ["region", "resource_type"]
}
