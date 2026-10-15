---
name: runway
description: Cash runway and cost forecasting from cost-governor data and API spend.
version: 0.1.0
execution-mode: advisory
argument-hint: "[status | forecast MONTHS | alert]"
category: fleet-ops
status: candidate
---
# Runway

Estimate cash runway from cost-governor data, API spend rates, and known fixed costs.

## Execution

### 1. Gather cost data
```bash
source .venv/bin/activate
python3 -c "
from hummbl_governance.integrations.cost_tracker import CostTracker
ct = CostTracker()
print('Current spend:', ct.get_current_spend())
print('Budget:', ct.get_budget())
print('Daily rate:', ct.get_daily_rate())
" 2>/dev/null || echo "(cost tracker unavailable)"
```

### 2. Known fixed costs
| Item | Monthly Cost | Notes |
|------|-------------|-------|
| Claude Max (the owner) | $100 | Anthropic subscription |
| Claude Max (team) | $100 | Anthropic subscription |
| GitHub Pro | $4 | your-org org |
| Tailscale | $0 | Free tier |
| Domain (your-domain.com) | ~$1 | Annual, amortized |
| GCP credits | -$2,000 | 2 projects x $1K (expiring) |

### 3. Variable costs
- API calls (OpenAI, Anthropic, Google) -- from cost-governor
- Compute ($REMOTE_HOST electricity) -- estimate ~$10/mo
- Inference (OpenRouter, if used) -- from cost-governor

### 4. Forecast
```
Monthly burn = fixed_costs + avg_variable_costs
Runway = cash_on_hand / monthly_burn
```

## Output Format
```
Runway Report | <date>
═══════════════════════

Monthly burn: $<X>
  Fixed: $<Y>
  Variable: $<Z> (30-day average)

Cash on hand: $<X>
Runway: <N> months

## Trend
<increasing/decreasing/stable burn rate>

## Alerts
- <if runway < 6 months: WARNING>
- <if runway < 3 months: CRITICAL>

## Cost Optimization Opportunities
- <specific suggestions based on spend patterns>
```

## Notes
- This skill provides estimates, not accounting. For actual financials, use proper bookkeeping.
- GCP credits have expiration dates -- factor those in.
- Variable costs spike during heavy research/inference sessions.

## Skill Chains
- For factor Cloudflare Neuron consumption into API spend forecasting -> `[usage-monitor]` (`python ~/bin/usage_monitor.py status`)
- For forecast API spend using free-tier model routing data -> `[reasoning-router]` (`models`)
