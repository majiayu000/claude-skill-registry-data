---
name: crypto
description: Crypto Quant Pro. Institutional-grade quantitative analysis for crypto options and volatility signals.
version: 3.0.0
author: AgentBoost Quantitative Trading Fleet
enterprise: true
category: Finance
---

### System Instructions
You are equipped with the `crypto` deterministic tool. This agent performs institutional-grade quantitative analysis for digital asset options and volatility signals. It maintains real-time Black-Scholes Greeks tracking, delta-neutral hedging, and seamless exchange API integration for high-speed execution.

### Execution Protocol
Invoke the quant engine by passing strictly formatted JSON:

```json
{
  "asset_pair": "BTC/USDT",
  "analysis_type": "volatility_surface_skew",
  "hedging_strategy": "delta_neutral_rebalancing",
  "enable_api_execution": true
}
```

Outputs
- Real-time options surface and Black-Scholes Greeks log.
- Volatility signal and skew identification report.
- Delta-neutral hedging and rebalancing status.
- Exchange API connectivity and execution verification.
