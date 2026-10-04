---
name: real-estate
description: Real Estate Pro. High-precision commercial investment underwriting, calculating Cap Rate and IRR.
version: 3.0.0
author: AgentBoost Enterprise
enterprise: true
category: Real Estate & Assets
---

### System Instructions
You are equipped with the `real-estate` deterministic tool. This tool performs advanced commercial underwriting, modeling multi-year Internal Rate of Return (IRR) projections and Cap Rate analytics. It generates institutional-grade investment memorandums.

### Execution Protocol
Invoke the underwriting engine by passing strictly formatted JSON:

```json
{
  "property_valuation_usd": 25000000,
  "net_operating_income_y1": 1850000,
  "exit_cap_rate_percent": 6.5,
  "holding_period_years": 10,
  "generate_investment_memo": true
}
```

Outputs
- Multi-year IRR and NPV projection models.
- Precise Cap Rate and cash-on-cash return analytics.
- Market comparative analysis and valuation benchmarking.
- Institutional investment memorandum and data package.
