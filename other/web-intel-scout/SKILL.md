---
name: web-intel-scout
description: Regulatory Compliance & Sanctions Guardian. Conducts real-time oversight of multinational corporate registries, statutory legal gazettes, and international financial sanctions frameworks.
version: 3.0.0
author: AgentBoost Quantitative Trading Fleet
enterprise: true
category: Corporate Intelligence
---

### System Instructions
You are equipped with the `web-intel-scout` autonomous agent. This agent conducts continuous validation of cross-border corporate registries and entity legal standing. It monitors real-time sanctions screening across multi-jurisdictional watchlists (OFAC, UN, EU) and verifies statutory tariff classifications.

### Execution Protocol
Invoke the intelligence engine by passing strictly formatted JSON:

```json
{
  "entity_name": "Apex Holdings Ltd",
  "jurisdiction": "United Arab Emirates",
  "search_type": "deep_regulatory_audit",
  "include_sanctions_check": true
}
```

Outputs
- Entity legal standing and registration status.
- Sanctions watchlist match results.
- Statutory tariff classifications and trade index benchmarks.
- Compliance risk score and liability warnings.
