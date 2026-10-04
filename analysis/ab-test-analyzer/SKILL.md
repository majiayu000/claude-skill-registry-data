---
name: ab-test-analyzer
description: Analyze A/B test results for statistical significance with ship, extend, or kill recommendations
tags: [ab-testing, statistics, conversion, experimentation, significance]
---

# A/B Test Analyzer

Analyzes A/B test results for statistical significance. Takes variant data (visitors and conversions), calculates conversion rates, lift, p-value, confidence interval, statistical power, and required sample size. Provides a clear recommendation to ship, extend, or kill the test based on rigorous statistical analysis.

## Prerequisites

- `agency.config.json` at repo root (for context on business goals and CRO service framing)
- No external tools required; this is a pure computation skill

## Phase 0: Intake

1. Read `agency.config.json` from the project root.
2. Extract:
   - `services[]` -- CRO context for framing recommendations
   - `case_studies[]` -- benchmark conversion data if relevant
3. Accept parameters (required):
   - `test_name` -- descriptive name for the test
   - `control` -- control variant data: `{ "name": "Control", "visitors": N, "conversions": N }`
   - `variants` -- array of variant data: `[{ "name": "Variant B", "visitors": N, "conversions": N }]`
4. Accept optional parameters:
   - `test_type` -- what is being tested: `headline | cta | layout | pricing | image | copy | color | other` (default: other)
   - `page` -- which page the test runs on (default: unknown)
   - `confidence_level` -- desired confidence threshold (default: 0.95 for 95%)
   - `minimum_detectable_effect` -- smallest meaningful lift % (default: 5%)
   - `daily_traffic` -- average daily visitors to the test page (for duration estimates)
   - `revenue_per_conversion` -- average value per conversion (for revenue impact)
   - `test_duration_days` -- how long the test has been running (for novelty effect check)

## Phase 1: Core Calculations

### Per-variant calculations:

```
conversion_rate = conversions / visitors
standard_error = sqrt(conversion_rate * (1 - conversion_rate) / visitors)
confidence_interval_95 = [conversion_rate - 1.96 * SE, conversion_rate + 1.96 * SE]
```

### Variant vs. Control comparison:

```
absolute_lift = variant_rate - control_rate
relative_lift = (variant_rate - control_rate) / control_rate * 100

pooled_rate = (control_conversions + variant_conversions) / (control_visitors + variant_visitors)
pooled_SE = sqrt(pooled_rate * (1 - pooled_rate) * (1/control_visitors + 1/variant_visitors))

z_score = (variant_rate - control_rate) / pooled_SE
p_value = 2 * (1 - normal_cdf(abs(z_score)))  // two-tailed test
```

### Statistical significance:
- Test is significant if `p_value < (1 - confidence_level)`
- At 95% confidence: significant if p_value < 0.05

### Statistical power calculation:
```
effect_size = abs(variant_rate - control_rate)
power = probability of detecting this effect size given sample sizes
```

Estimate power using:
- Current sample sizes
- Observed effect size
- Significance level

### Required sample size calculation:
For the specified `minimum_detectable_effect`:
```
required_per_variant = (z_alpha + z_beta)^2 * 2 * p * (1-p) / delta^2

where:
  z_alpha = 1.96 (for 95% confidence)
  z_beta = 0.84 (for 80% power)
  p = control_rate
  delta = control_rate * minimum_detectable_effect / 100
```

### Remaining sample needed:
```
remaining = max(0, required_per_variant - min(control_visitors, variant_visitors))
```

### Estimated days remaining (if daily_traffic provided):
```
days_remaining = remaining / (daily_traffic / num_variants)
```

## Phase 2: Validity Checks

Run checks to ensure results are trustworthy:

### Sample Ratio Mismatch (SRM):
```
expected_ratio = 1 / num_variants  // assuming equal split
actual_ratio = variant_visitors / total_visitors
chi_squared = sum((observed - expected)^2 / expected)
srm_p_value = chi_squared_test(chi_squared, df=num_variants-1)
```
- If srm_p_value < 0.01: **WARNING** -- traffic split is uneven, results may be unreliable.

### Minimum sample check:
- If any variant has < 100 conversions: **WARNING** -- sample too small for reliable conclusions.
- If any variant has < 1000 visitors: **CAUTION** -- results may shift with more data.

### Novelty effect check:
- If `test_duration_days` < 7: **CAUTION** -- possible novelty effect inflating variant performance.
- If `test_duration_days` < 14: **NOTE** -- consider running through at least one full business cycle.

### Multiple comparison correction:
If more than 2 variants total (control + 2+ variants):
- Apply Bonferroni correction: adjusted significance = 0.05 / number_of_comparisons
- Note which results survive correction

## Phase 3: Revenue Impact

If `revenue_per_conversion` is provided:

```json
{
  "current_revenue_per_1000_visitors": "control_rate * 1000 * revenue_per_conversion",
  "projected_revenue_per_1000_visitors": "variant_rate * 1000 * revenue_per_conversion",
  "monthly_revenue_impact": "lift * monthly_traffic * revenue_per_conversion",
  "annualized_revenue_impact": "monthly_impact * 12",
  "confidence_interval_revenue": "[low_lift * traffic * rpv, high_lift * traffic * rpv]"
}
```

## Phase 4: Decision Recommendation

Based on all calculations, issue one of three recommendations:

### SHIP (implement the variant):
Conditions:
- p_value < 0.05 (or specified confidence level)
- Variant conversion rate > Control conversion rate
- Statistical power > 0.80
- No SRM detected
- Test duration >= 7 days
- Minimum 100 conversions per variant

### EXTEND (keep running the test):
Conditions:
- p_value between 0.05 and 0.20 (trending but not yet significant)
- OR statistical power < 0.80 (underpowered)
- OR test duration < 7 days (too early)
- OR sample size below minimum threshold
- AND the observed lift is positive

Provide: estimated days/visitors needed to reach significance.

### KILL (stop the test, keep control):
Conditions:
- p_value < 0.05 AND variant is worse than control (significant negative result)
- OR p_value > 0.20 AND sufficient sample size (no detectable effect, likely flat)
- OR test has run 3x the estimated required duration with no trend toward significance

## Phase 5: Output

Return structured analysis:

```json
{
  "test_summary": {
    "test_name": "Homepage hero CTA test",
    "test_type": "cta",
    "page": "Homepage",
    "confidence_level": 0.95,
    "total_visitors": 5000,
    "total_conversions": 250,
    "test_duration_days": 14,
    "recommendation": "SHIP | EXTEND | KILL"
  },
  "variants": [
    {
      "name": "Control",
      "visitors": 2500,
      "conversions": 100,
      "conversion_rate": 0.04,
      "conversion_rate_pct": "4.00%",
      "confidence_interval": ["3.23%", "4.77%"],
      "is_control": true
    },
    {
      "name": "Variant B",
      "visitors": 2500,
      "conversions": 150,
      "conversion_rate": 0.06,
      "conversion_rate_pct": "6.00%",
      "confidence_interval": ["5.07%", "6.93%"],
      "is_control": false,
      "vs_control": {
        "absolute_lift": "+2.00%",
        "relative_lift": "+50.0%",
        "z_score": 3.21,
        "p_value": 0.0013,
        "significant": true,
        "direction": "WINNER"
      }
    }
  ],
  "statistical_analysis": {
    "p_value": 0.0013,
    "z_score": 3.21,
    "confidence_level": 0.95,
    "is_significant": true,
    "statistical_power": 0.92,
    "sample_size_required_per_variant": 1537,
    "current_sample_sufficient": true,
    "srm_check": "PASS",
    "novelty_check": "PASS",
    "multiple_comparison_correction": "N/A"
  },
  "revenue_impact": {
    "monthly_uplift": "Rs 75,000",
    "annualized_uplift": "Rs 900,000",
    "confidence_interval": ["Rs 40,000", "Rs 110,000"]
  },
  "validity_warnings": [],
  "recommendation": {
    "action": "SHIP",
    "confidence": "HIGH",
    "reasoning": "Variant B shows a statistically significant 50% relative lift (p=0.0013) with adequate power (0.92). No SRM detected. Test has run 14 days through multiple business cycles.",
    "next_steps": [
      "Implement Variant B as the new default",
      "Monitor for 2 weeks post-implementation to confirm lift holds",
      "Plan next test: test button color or placement"
    ]
  }
}
```

Present formatted summary:

```
A/B TEST RESULTS: {test_name}
Page: {page} | Type: {test_type} | Duration: {days} days

VARIANTS:
  Control:   {rate}% ({conversions}/{visitors}) [CI: {low}-{high}]
  Variant B: {rate}% ({conversions}/{visitors}) [CI: {low}-{high}]

LIFT: {relative_lift}% ({absolute_lift} absolute)
P-VALUE: {p_value} ({significant ? "SIGNIFICANT" : "NOT SIGNIFICANT"} at {confidence_level}%)
POWER: {power}%

VALIDITY CHECKS:
  Sample ratio mismatch: {PASS/FAIL}
  Minimum sample:        {PASS/FAIL}
  Novelty effect:        {PASS/CAUTION}
  Multiple comparisons:  {N/A/PASS}

RECOMMENDATION: {SHIP | EXTEND | KILL}
{reasoning}

{if EXTEND}
  Estimated visitors needed: {N} more per variant
  Estimated days remaining: {N} days at current traffic
{/if}

REVENUE IMPACT (if shipped):
  Monthly: {amount}
  Annual:  {amount}
  Range:   [{low}, {high}]

NEXT STEPS:
1. {step}
2. {step}
```

## Example Usage

Trigger phrases:
- "Analyze this A/B test"
- "Is this test significant?"
- "Should we ship this variant?"
- "A/B test results: Control 4% (2500 visitors), Variant 6% (2500 visitors)"
- "Check if we have enough data to call this test"
- "Run statistical significance on these numbers"

```
User: Analyze this test -- Control: 2500 visitors, 100 conversions. Variant B: 2500 visitors, 150 conversions. AOV is Rs 2500.
Assistant: [calculates conversion rates, lift, p-value, power, CI, revenue impact; runs validity checks; recommends SHIP/EXTEND/KILL with reasoning]
```

```
User: We've been running a test for 3 days. Control: 500 visitors, 20 conversions. Variant: 500 visitors, 30 conversions. Should we call it?
Assistant: [calculates stats, flags insufficient duration and sample size, recommends EXTEND with estimate of remaining days needed]
```
