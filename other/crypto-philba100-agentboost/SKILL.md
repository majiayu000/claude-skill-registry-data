---
name: crypto-options-pro
version: "3.0.0"
author: "AgentBoost Enterprise"
description: "Institutional-grade cryptocurrency options analytics with deal tracking, ROI analysis, and automated position monitoring. Integrates with portfolio tracking and CRM for client account management."
enterprise: true
---

# Execution Protocol
To execute this deterministic skill, you MUST invoke the `run_js` tool adhering to the strict JSON schema below. 

## Schema Validation
- `data`: A stringified JSON object containing:
  - `asset` (string): The ticker symbol (Enum: "BTC", "ETH", "SOL"). Default: "BTC".
  - `timeframe` (string): Expiration window (Enum: "24H", "7D", "30D", "90D").
  - `risk_level` (string): Risk tolerance parameter (Enum: "Low", "Medium", "High", "Delta-Neutral").
  - `iv_threshold` (float, optional): Implied volatility trigger threshold.

## Contextual Instructions for the Agent
1. Validate the user's request against supported assets.
2. If the user asks for "market neutral", map `risk_level` to "Delta-Neutral".
3. Invoke the tool exactly as formatted in the example. Do not wrap the JSON payload in markdown code blocks inside the tool call.

## Example Execution
```python
run_js(data='{"asset": "SOL", "timeframe": "7D", "risk_level": "Delta-Neutral", "iv_threshold": 0.85}')