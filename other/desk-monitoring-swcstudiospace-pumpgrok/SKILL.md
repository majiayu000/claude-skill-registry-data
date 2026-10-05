---
name: desk-monitoring
description: Continuous oversight of desk health, open positions, daily P&L, and circuit-breaker status. Used primarily by CHIEF.
---

# Desk Monitoring

## Status Block
```
DESK STATUS
UTC: ...
Engagement: research | paper | micro-live
Open Positions: N
Total Exposure: $X
Daily P&L: ...
Circuit Breaker: OK | APPROACHING | HALTED
Active Alerts: ...
```

## Circuit Breaker
When daily loss ≥ 5 % of wallet equity → CHIEF posts `FLOOR HALTED – DAILY LOSS LIMIT` and refuses all new tickets until human reset.
