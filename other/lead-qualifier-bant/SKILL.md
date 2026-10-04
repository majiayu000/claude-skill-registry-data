---
name: lead-qualifier-bant
description: Lead Qualifier Bant. Professional enterprise agent for Lead Qualifier Bant within the Sales sector.
version: 3.0.0
author: AgentBoost Enterprise
enterprise: true
category: Sales
---

### System Instructions
You are equipped with the `lead-qualifier-bant` autonomous agent. This agent scrutinizes inbound commercial opportunities against formal BANT (Budget, Authority, Need, Timeline) frameworks. It ensures strategic alignment with sales targets and validates accuracy for prospect firmographic data.

### Execution Protocol
Invoke the qualification engine by passing strictly formatted JSON:

```json
{
  "prospect_id": "LEAD_STE_8841",
  "qualification_framework": "Institutional_BANT_MEDDIC",
  "identify_pacing_gaps": true,
  "generate_qualification_brief": true
}
```

Outputs
- Commercial opportunity BANT qualification and audit log.
- Strategic alignment with sales and growth targets.
- Identification of firmographic accuracy and gaps.
- High-value target account qualification brief.
