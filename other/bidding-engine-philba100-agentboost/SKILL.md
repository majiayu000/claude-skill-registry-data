---
name: bidding-engine
description: Enterprise dynamic bidding and pricing optimization. Generates competitive bids, RFQ responses, margin-optimized quotes, and price strategies based on market data and deal characteristics.
version: 3.0.0
author: AgentBoost Enterprise
enterprise: true
---

### System Instructions
You are equipped with the `bidding-engine` skill for professional proposal pricing. This tool calculates optimal pricing, generates RFQ responses, and provides margin-aware bidding strategies.

**CRITICAL:** Always optimize for margin while remaining competitive. Track competitive pricing intelligence. Never exceed customer budget without documented business case.

### Execution Protocol
Call the `run_js` tool with strictly formatted JSON:

```json
{
  "rfq_id": "RFQ-2026-4521",
  "prospect_industry": "Financial Services",
  "project_scope": "API integration, 3 use cases, 1-year support",
  "customer_budget": 150000,
  "customer_size": "Enterprise",
  "competitive_landscape": ["Competitor A", "Competitor B"],
  "your_cost_basis": 45000,
  "desired_margin_percent": 65,
  "bid_strategy": "aggressive",
  "market_rate_range": {"low": 120000, "high": 200000},
  "custom_pricing_factors": {"urgency": "high", "contract_length": 36, "volume_discount": false}
}
```

### Outputs
The skill delivers:
- **Recommended Price:** Optimal bid balancing margin and win probability
- **Price Justification:** Value breakdown by component
- **Margin Analysis:** Profitability at different price points
- **Competitive Positioning:** How bid compares to market
- **Scenario Analysis:** Win probability at $X, $Y, $Z price points
- **Alternative Packages:** Different feature/price combinations
- **Proposal Package:** Ready-to-send quote document

### Example Tool Call
```javascript
run_js(data='{"rfq_id": "RFQ-2026-4573", "prospect_industry": "SaaS", "project_scope": "Full platform migration, training, 2-year support", "customer_budget": 250000, "customer_size": "Mid-Market", "competitive_landscape": ["MarketLeader", "GrowthCo"], "your_cost_basis": 80000, "desired_margin_percent": 60, "bid_strategy": "balanced", "market_rate_range": {"low": 200000, "high": 350000}, "custom_pricing_factors": {"urgency": "medium", "contract_length": 24, "volume_discount": true}}')
```

### Integration Points
- **Negotiation Engine:** Align with deal strategy
- **Meeting Scheduler:** Schedule pricing discussions
- **CRM Sync:** Store all bid history and outcomes
- **Analytics Hub:** Track bid win rates and average deal size
- **Email Orchestrator:** Send proposals automatically
