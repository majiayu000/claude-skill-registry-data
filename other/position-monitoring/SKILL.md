---
name: position-monitoring
description: Continuous post-entry safety and performance watches for every open position. Used by RUG (safety) and EXIT (P&L and exit rules).
---

# Position Monitoring

## Red-Flag Triggers (RUG)
- Significant LP removal or unlock
- Any mint event after entry
- Large insider / top-holder sells
- Freeze or tax change
- Suspicious program interactions

## Alert Schema
```
POSITION / TICKET-ID: ...
Red Flag: <precise description>
Evidence: <links + UTC>
Recommended Action: Emergency Exit / Watch / Escalate
```

## EXIT Rules
- Apply pre-agreed take-profit, stop-loss, or trailing rules
- On RUG alert → prepare emergency exit ticket and request human confirmation (unless auto-exit pre-authorised)
