---
name: marketing-attribution
description: 'Attribution and incrementality measurement: attribution models, marketing mix modelling (MMM), multi-touch attribution (MTA), incrementality testing, conversion lift, holdout tests, Shapley values, Robyn, LightweightMMM, iROAS, UTM governance, walled garden discrepancies and difference-in-differences. Use to decide which measurement approach answers the question at hand, credit assignment versus true incremental impact. Triggers: attribution model, MMM, MTA, incrementality, conversion lift, holdout, iROAS, incremental ROAS, causal inference for marketing.'
---

# marketing-attribution

## When to use this skill
Activate when the user asks about: attribution models, marketing mix modeling (MMM), multi-touch attribution (MTA), incrementality testing, conversion lift, holdout tests, Shapley values, Robyn, LightweightMMM, iROAS, UTM governance, walled garden measurement, view-through vs click-through attribution, budget optimization by channel, causal inference for marketing, difference-in-differences.

## Core behavior
- Always clarify which attribution question is being asked: "which channel gets credit?" vs "what is the true incremental impact?"
- Explain the limitations of each model in context (last-click undervalues upper funnel; MMM requires 2+ years of data)
- Recommend the right tool for the objective: MTA for tactical optimization, MMM for strategic budget allocation, incrementality for ground truth
- Flag walled garden data discrepancies (Meta vs Google vs internal)
- Express results as iROAS (incremental ROAS) not just attributed ROAS when possible

## Model selection guide
| Question | Recommended model |
|---|---|
| Which channel to cut budget? | MMM |
| Which keyword drives conversions? | Data-driven MTA |
| Did this campaign actually work? | Geo holdout / Conversion Lift |
| How to split credit across touchpoints? | Shapley MTA |
| Is my Google Ads ROAS real? | Incrementality test |

## Key patterns

### Shapley value MTA (Python)
```python
from itertools import combinations

def shapley_values(channels, conversion_fn):
    n = len(channels)
    shapley = {c: 0 for c in channels}
    for channel in channels:
        others = [c for c in channels if c != channel]
        for r in range(len(others) + 1):
            for subset in combinations(others, r):
                weight = 1 / (n * len(list(combinations(others, r))) )
                marginal = conversion_fn(list(subset) + [channel]) - conversion_fn(list(subset))
                shapley[channel] += weight * marginal
    return shapley
```

### Difference-in-Differences (DiD)
```python
import statsmodels.formula.api as smf
# did = (treated_post - treated_pre) - (control_post - control_pre)
model = smf.ols('conversions ~ treated * post_period + C(region)', data=df).fit()
did_estimate = model.params['treated:post_period']
```

### UTM taxonomy for WPPMedia clients
```
utm_source: google / meta / dv360 / ttd / email / direct
utm_medium: cpc / paid_social / display / video / organic
utm_campaign: {client}_{objective}_{year_month}
utm_content: {creative_id}_{format}
utm_term: {keyword} (Google Ads only)
```

## Output formats
- Model comparison table with pros/cons for the specific use case
- Python or R code for statistical models
- Budget reallocation recommendation based on iROAS by channel

## Tools
Python (Robyn, LightweightMMM, PyMC, pandas, sklearn), R, BigQuery, Google Analytics, Meta Business Suite
