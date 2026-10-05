---
name: desk-risk-limits
description: Interview the user, write, and enforce the capital and loss rules for the PumpGrok desk. Produces risk-limits.md. Used primarily by RISK and CHIEF.
---

# Desk Risk Limits

## Procedure – Initial Interview
Ask the user:
1. Maximum throwaway capital (recommended ≤ $200 USDC)
2. Maximum size per trade
3. Maximum concurrent open positions
4. Daily loss halt percentage (default 5 %)
5. Forbidden criteria
6. Preferred engagement level

## Output
Write `/workspace/trading-desk/risk-limits.md` with the agreed numbers.

## Enforcement
- RISK must refuse any ticket that violates these limits
- CHIEF must check daily loss before allowing new tickets
- Any change requires new human confirmation
