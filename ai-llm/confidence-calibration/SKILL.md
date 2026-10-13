---
name: confidence-calibration
description: "AGI: SteerConf confidence calibration protocol — generates calibrated confidence scores for any analytical output using three-pass prompting (conservative/neutral/optimistic) with consistency measurement. Triggers on any investment analysis, credit memo, deal screening, underwriting, or financial model output. Also triggers when user asks 'how confident are you', 'what's the reliability', 'confidence level', or 'how sure'."
---

# Confidence Calibration (SteerConf Protocol)

Every analytical output must include a calibrated confidence assessment. This skill implements the SteerConf protocol — a prompt-only technique that halves calibration error with zero infrastructure requirements.

## Why Calibrated Confidence?

Standard AI outputs don't indicate reliability. A model may express identical certainty for a well-supported analysis backed by audited financials and a speculative estimate based on a single data point. SteerConf solves this by measuring internal consistency across calibration perspectives.

## Three-Pass Calibration Protocol

### Pass 1: Conservative Analysis
Generate the analysis assuming pessimistic interpretations:
- Use lower-bound estimates for uncertain metrics
- Weight risks more heavily than opportunities
- Apply wider discount rates and lower growth assumptions
- Flag any data point with less than 2 independent sources

### Pass 2: Neutral Analysis
Generate the analysis using balanced judgment:
- Use median estimates
- Weight risks and opportunities equally
- Apply market-consensus assumptions where available
- Standard analytical framework

### Pass 3: Optimistic Analysis
Generate the analysis assuming favorable interpretations:
- Use upper-bound estimates for uncertain metrics
- Weight opportunities more heavily
- Apply tighter spreads and higher growth assumptions
- Give benefit of the doubt on management execution

## Consistency Measurement

After all three passes, measure agreement:

| Consistency Level | Score Range | Interpretation |
|-------------------|-------------|----------------|
| **High** (3/3 agree on direction) | 0.80 - 1.00 | Strong analytical foundation, reliable output |
| **Medium** (2/3 agree) | 0.50 - 0.79 | Reasonable analysis, some uncertainty |
| **Low** (all 3 diverge) | 0.20 - 0.49 | High uncertainty, flag for human review |
| **Conflicting** (conservative and optimistic oppose) | 0.00 - 0.19 | Insufficient data or fundamental ambiguity |

### Score Calculation

```
base_score = (agreement_count / total_dimensions) * 0.6
data_quality = (verified_datapoints / total_datapoints) * 0.25
source_diversity = (unique_sources / max_expected_sources) * 0.15
confidence = base_score + data_quality + source_diversity
```

## Output Format

Every analysis that uses this protocol must append:

```markdown
## Confidence Assessment
- **Score**: 0.XX
- **Calibration**: conservative | neutral | optimistic
- **Confidence Drivers**:
  - [Factor 1 that supports reliability]
  - [Factor 2 that supports reliability]
- **Data Gaps**:
  - [Missing data point 1 — would improve confidence by ~X%]
  - [Missing data point 2 — would improve confidence by ~X%]
- **Three-Pass Agreement**:
  - Conservative: [key conclusion]
  - Neutral: [key conclusion]
  - Optimistic: [key conclusion]
  - Agreement level: High | Medium | Low | Conflicting
```

## Application by Domain

### Credit Memos (Quick-Cut)
- Calibrate: capital structure accuracy, valuation multiples, trade thesis
- Key drivers: number of independent data sources, data recency, market liquidity
- Common gaps: private company financials, real-time pricing, management access

### Deal Screening
- Calibrate: each scoring dimension independently + overall score
- Key drivers: completeness of financial data, market comp availability
- Common gaps: management quality assessment, customer concentration data

### CRE Underwriting
- Calibrate: NOI projection, cap rate assumption, return estimates
- Key drivers: T12 quality, rent comp depth, cap rate transaction volume
- Common gaps: tenant credit data, capex reserve adequacy, environmental

### Financial Models
- Calibrate: key assumptions (growth, margins, exit multiple)
- Key drivers: historical data depth, comp set quality, assumption reasonableness
- Common gaps: forward-looking projections, synergy estimates, terminal assumptions

## Integration with Other Skills

This skill is automatically invoked by:
- `quick-cut` — appends confidence to the credit memo
- `deal-screener` — calibrates the 100-point score
- `cre-underwriter` — calibrates return projections
- `financial-modeling` — calibrates model outputs
- `adversarial-debate` — calibrates the synthesized view

When another skill references "confidence calibration", it means: run the three-pass protocol on the output and append the confidence assessment block.
