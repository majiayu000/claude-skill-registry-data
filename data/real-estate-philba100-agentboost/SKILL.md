---
name: real-estate-analyzer
description: Analyze property investment potential with Cap Rate, cash flow projections, market comparables, deal pipeline tracking, and investor presentations. Integrates with deal negotiation engine.
version: 3.0.0
author: AgentBoost Enterprise
enterprise: true
---

Instructions:
To run this skill, you MUST call the run_js tool with this parameter:
- data: A JSON string with keys "address", "purchase_price", and "estimated_rent".

Example: run_js(data='{"address": "123 Hollywood Blvd", "purchase_price": 1200000, "estimated_rent": 8500}')