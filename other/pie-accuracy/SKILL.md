---
name: pie-accuracy
description: Weekly PIE accuracy validation. Spot-checks served prices against ground truth (fresh scrapes, USDA data). Measures how trustworthy PIE actually is. Tracks accuracy over time. Recalibrates confidence scores when they lie.
---

# PIE Accuracy

The trust engine. Without this, PIE is just numbers. With this, PIE is
numbers you can bet your business on.

## Trigger Conditions

- Weekly scheduled run (Hermes, Sunday night)
- User says "accuracy", "how accurate", "spot check", "validate prices"
- After major data event (new chain added, large sync, model change)
- After any confidence scoring change (verify it's still honest)

## Philosophy

A pricing engine nobody trusts is worthless. Trust is built by:

1. Measuring accuracy honestly (including when it's bad)
2. Showing users confidence scores that MATCH reality
3. Improving accuracy monotonically over time
4. Never hiding failures

PIE Law 3 (Honesty Over Silence) demands this skill exists.

## Workflow

### Phase 1: Select Sample

Pick 200 ingredients stratified across:

- 5 volatility categories (produce, protein, dairy, dry goods, specialty)
- 4 confidence levels (high, medium, low, synthetic)
- Multiple regions (at least 5 states with data)

```sql
-- Sample selection (stratified)
WITH ranked AS (
  SELECT
    ci.ingredient_id,
    ci.name,
    ci.category,
    -- confidence from latest resolution
    CASE
      WHEN EXISTS(SELECT 1 FROM ingredient_price_history iph
        WHERE iph.ingredient_id = ci.ingredient_id
        AND iph.observed_at > now() - interval '7 days'
        AND iph.source_type = 'store_scrape') THEN 'high'
      WHEN EXISTS(SELECT 1 FROM ingredient_price_history iph
        WHERE iph.ingredient_id = ci.ingredient_id
        AND iph.observed_at > now() - interval '14 days') THEN 'medium'
      ELSE 'low'
    END as confidence_tier,
    ROW_NUMBER() OVER (
      PARTITION BY ci.category
      ORDER BY RANDOM()
    ) as rn
  FROM openclaw.canonical_ingredients ci
  WHERE EXISTS(SELECT 1 FROM ingredient_price_history iph
    WHERE iph.ingredient_id = ci.ingredient_id)
)
SELECT * FROM ranked WHERE rn <= 40  -- 40 per category = 200 total
```

### Phase 2: Get Ground Truth

For each sampled ingredient, find the most recent VERIFIED price:

1. **Store scrape < 24h old** (best ground truth)
2. **USDA weekly report** (for commodities)
3. **Multiple-source agreement** (3+ sources within 5% = ground truth)

If no ground truth available for an ingredient: skip it, note as "unvalidatable."

### Phase 3: Compare

For each ingredient with ground truth:

```
served_price = resolvePrice(ingredient, region)  // what PIE would show
ground_truth = latest verified price
error_pct = abs(served_price - ground_truth) / ground_truth * 100
pass = error_pct <= 15
```

### Phase 4: Score

Compute:

- **Overall accuracy:** % of sample within 15% of ground truth
- **Mean absolute error:** average error_pct across all samples
- **By confidence tier:** accuracy within each tier
- **By category:** accuracy within each food category
- **By region:** accuracy within each state/region
- **Worst offenders:** top 10 ingredients with highest error

### Phase 5: Validate Confidence Scores

Confidence scores must correlate with accuracy:

| Confidence | Required accuracy                            |
| ---------- | -------------------------------------------- |
| HIGH       | > 95% of high-confidence prices within 15%   |
| MEDIUM     | > 80% of medium-confidence prices within 15% |
| LOW        | > 60% of low-confidence prices within 15%    |

If a tier misses its target: confidence scoring is lying.
Action: recalibrate the confidence assignment logic.

### Phase 6: Fix Worst Offenders

For the top 10 worst errors:

1. Diagnose WHY the price is wrong (stale? wrong source? bad normalization?)
2. Fix the root cause (not just the number)
3. Re-resolve and verify improvement

### Phase 7: Log

Append to `docs/pie-accuracy-log.md`:

```markdown
## [ISO date]

**Sample:** 200 ingredients, N regions, N unvalidatable (skipped)
**Overall accuracy:** X% within 15%
**Mean absolute error:** X%

**By confidence:**

- HIGH: X% accurate (target: >95%) [PASS/FAIL]
- MEDIUM: X% accurate (target: >80%) [PASS/FAIL]
- LOW: X% accurate (target: >60%) [PASS/FAIL]

**By category:**

- Produce: X%
- Protein: X%
- Dairy: X%
- Dry goods: X%
- Specialty: X%

**Worst offenders:**

1. [ingredient] - served $X, actual $Y, error Z% (reason)
2. ...

**Actions taken:** [fixes applied]
**Confidence recalibration needed:** yes/no
**Delta from last run:** +/-X% overall
```

### Phase 8: Trend

Compare to previous runs. Accuracy must trend UP (ratchet).
If it dropped: investigate immediately. Likely causes:

- Source went stale without detection
- New data introduced noise
- Seasonal shift not accounted for
- Regional pricing changed faster than sync cycle

## Regression Alerts

If accuracy drops > 5 points from previous run:

- Flag as CRITICAL
- Identify which category/region/tier degraded
- Trigger `/pie-ratchet` focused on that area
- Do NOT wait for next weekly run

## Existing Code to Leverage

- `lib/pricing/resolve-price.ts` - `resolvePrice()` for getting served prices
- `lib/pricing/coverage-report.ts` - state/category breakdowns
- `lib/pricing/anomaly-detector.ts` - quarantine logic (may overlap)
- `lib/pricing/evaluate.ts` - price evaluation (check what it does)
- `lib/pricing/compound-learning.ts` - feeds calibration data back
- `lib/openclaw/price-validator.ts` - validation rules

## Constraints

- **Honest reporting.** Never inflate accuracy. Bad numbers are data, not failures.
- **Stratified sampling.** Don't just check easy ingredients. Cover the hard ones.
- **Fix, don't just measure.** Phase 6 is mandatory. Every run improves something.
- **Track over time.** Single accuracy number is meaningless. Trend is everything.
- **Never fabricate ground truth.** If you can't verify, say "unvalidatable."
- **Confidence must be honest.** If HIGH confidence prices are only 70% accurate, the confidence system is broken. Fix it.

## Key Files

- Price resolution: `lib/pricing/resolve-price.ts`
- Accuracy log: `docs/pie-accuracy-log.md`
- Anomaly detector: `lib/pricing/anomaly-detector.ts`
- Compound learning: `lib/pricing/compound-learning.ts`
- Price evaluator: `lib/pricing/evaluate.ts`
- Validator: `lib/openclaw/price-validator.ts`
- PIE Laws: `docs/specs/pie-laws.md` (Laws 3, 7, 11)
- National vision: `docs/specs/pie-national-vision.md`

## Relationship to Other PIE Skills

```
/pie-measure  -> how much coverage? (quantity)
/pie-accuracy -> how trustworthy? (quality)
/pie-ratchet  -> make coverage better
/pie-forecast -> make intelligence deeper
/pie-fix      -> fix worst violation now
```

Measure and accuracy together give the full picture.
Coverage without accuracy is a lie. Accuracy without coverage is incomplete.
Both must improve together.
