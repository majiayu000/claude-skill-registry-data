---
name: legal-risk
description: Legal Counsel Pro. High-liability risk assessment for NDAs and enterprise vendor agreements.
version: 3.0.0
author: AgentBoost Enterprise
enterprise: true
category: Legal & Compliance
---

### System Instructions
You are equipped with the `legal-risk` deterministic tool. This tool identifies IP traps, unfavorable indemnity clauses, and enforceability risks in legal agreements. It provides high-precision risk scoring and redlined counter-offer suggestions for legal teams.

### Execution Protocol
Invoke the legal engine by passing strictly formatted JSON:

```json
{
  "agreement_type": "Enterprise_Vendor_Master_Service_Agreement",
  "document_id": "DOC_LEGAL_2026_881",
  "risk_sensitivity": "institutional_tier",
  "generate_redline_suggestions": true
}
```

Outputs
- High-liability risk detection and IP trap identification.
- Enforceability risk scoring and liability heatmap.
- Redlined counter-offer and clause adjustment suggestions.
- Legal framework alignment and compliance validation.
