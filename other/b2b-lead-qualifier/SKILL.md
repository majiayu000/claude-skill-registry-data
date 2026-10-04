---
name: b2b-lead-qualifier
description: Corporate Firmographic Alignment & Pipeline Optimizer. Evaluates inbound commercial opportunities against formal enterprise alignment matrices.
version: 3.0.0
author: AgentBoost Quantitative Trading Fleet
enterprise: true
category: Sales & Growth
---

### System Instructions
You are equipped with the `b2b-lead-qualifier` autonomous agent. This agent analyzes inbound inquiries against registry-backed firmographic asset sizing and corporate structure maps. It indexes commercial readiness based on financial parameters and generates customized enterprise engagement proposals.

### Execution Protocol
Invoke the sales engine by passing strictly formatted JSON:

```json
{
  "prospect_domain": "global-logistics.com",
  "inquiry_text": "Looking for institutional trade financing and LC auditing services.",
  "qualification_framework": "BANT_Institutional",
  "score_threshold": 75
}
```

Outputs
- Firmographic sizing and corporate hierarchy map.
- Commercial readiness index and BANT qualification score.
- Custom enterprise engagement proposal and strategy brief.
- High-value target account match confirmation.
