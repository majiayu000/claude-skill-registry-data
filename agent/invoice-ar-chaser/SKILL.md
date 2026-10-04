---
name: invoice-ar-chaser
description: Capital Flow Recovery & Liquidity Optimization Guard. Orchestrates multi-stage collections choreography and liquidity enforcement across outstanding corporate debits.
version: 3.0.0
author: AgentBoost Quantitative Trading Fleet
enterprise: true
category: Finance & Cashflow
---

### System Instructions
You are equipped with the `invoice-ar-chaser` autonomous agent. This agent monitors accounts receivable outstanding balances and detects transactional payment reconciliation mismatches. It executes heuristic multi-stage collection sequences and structures capital repayment plans based on client liquidity profiles.

### Execution Protocol
Invoke the finance engine by passing strictly formatted JSON:

```json
{
  "client_account_id": "CLI_8841",
  "outstanding_balance_usd": 45000,
  "overdue_days": 15,
  "collection_intensity": "high_stakes_alignment"
}
```

Outputs
- Heuristic collection communication sequence logs.
- Structured capital repayment schedule proposal.
- Predictive cashflow lag model and bad-debt risk score.
- Liquidity enforcement status and accounting alert routing.
