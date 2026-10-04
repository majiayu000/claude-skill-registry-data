---
name: pie-forecast
description: PIE Layer 2 intelligence builder. Computes trend data, volatility scores, seasonal calendars, and cost forecasts from existing price history. Transforms raw prices into actionable intelligence. Only runs when Layer 1 coverage exceeds threshold.
---

# PIE Forecast

Layer 2 intelligence engine. Takes raw price data and produces the intelligence
that makes PIE valuable beyond "here's a number." This is what separates PIE
from a price database.

## Trigger Conditions

- After `/pie-ratchet` reports Layer 1 gap < 100 (ready for Layer 2)
- User says "forecast", "trends", "volatility", "seasonal patterns"
- After large sync (1000+ new prices) brings enough history
- Weekly scheduled run (Hermes overnight)

## Gate Check

**Do NOT run if Layer 1 is weak.** Check first:

- Total coverage > 80%? If no, run `/pie-ratchet` instead.
- At least 30 days of price history for target ingredients? If no, wait.
- Pi sync within last 48 hours? If no, sync first.

Layer 2 without Layer 1 is decoration on a broken house.

## Intelligence Products

### 1. Volatility Scores

For each ingredient with 30+ days of price history:

```
volatility_score = std_dev(prices_last_90d) / mean(prices_last_90d)
```

Classification:

- **STABLE** (CV < 0.10): dry goods, canned, oils. Safe for fixed menus.
- **MODERATE** (CV 0.10-0.25): dairy, bakery, frozen. Plan around.
- **VOLATILE** (CV 0.25-0.50): fresh produce, proteins. Margin risk.
- **EXTREME** (CV > 0.50): seasonal specialties, luxury proteins. Avoid fixed pricing.

Storage: `ingredient_volatility_scores` table or JSON column on canonical_ingredients.

Chef-facing value: "This ingredient has HIGH price volatility. Consider a
substitution or build margin buffer into your quote."

### 2. Seasonal Calendars

For each ingredient with 12+ months of data:

```sql
SELECT
  ingredient_id,
  EXTRACT(MONTH FROM observed_at) as month,
  AVG(price_cents) as avg_price,
  AVG(price_cents) / (SELECT AVG(price_cents) FROM same_ingredient) as seasonal_index
FROM price_history
GROUP BY ingredient_id, month
```

A seasonal_index of 0.8 means "20% cheaper than annual average in this month."
A seasonal_index of 1.3 means "30% more expensive."

Chef-facing value: "Asparagus is cheapest in April-May (index 0.75).
Current price reflects peak season pricing."

### 3. Trend Detection

For each ingredient, compute:

- **7-day trend:** price now vs 7 days ago (%)
- **30-day trend:** price now vs 30 days ago (%)
- **Direction:** rising / falling / stable (within 3% = stable)
- **Acceleration:** is the trend speeding up or slowing down?

```
trend_7d = (current_price - price_7d_ago) / price_7d_ago * 100
trend_30d = (current_price - price_30d_ago) / price_30d_ago * 100
direction = 'rising' if trend_7d > 3, 'falling' if < -3, else 'stable'
acceleration = trend_7d - (price_7d_ago - price_14d_ago) / price_14d_ago * 100
```

Chef-facing value: "Chicken thighs up 12% this month and accelerating.
Consider locking in pricing now or switching to pork loin (-2% this month)."

### 4. Cost Forecasting

For ingredients with trend + seasonal data:

```
forecast_30d = current_price * (1 + trend_30d_annualized/12) * seasonal_adjustment_next_month
```

Confidence: HIGH if stable + seasonal match, LOW if volatile + no pattern.

Chef-facing value: "Your 'Summer Dinner' menu costs $847 today.
Forecast for July: $892 (+5.3%) due to seasonal protein increases."

### 5. Substitution Scoring

When an ingredient is volatile or trending up, score alternatives:

```
substitution_score = (
  flavor_similarity * 0.3 +
  texture_similarity * 0.2 +
  application_match * 0.3 +
  price_advantage * 0.2
)
```

Only suggest substitutions where:

- Same general category (protein for protein, not protein for vegetable)
- Price advantage > 15%
- Culinary application overlap > 70%

Chef-facing value: "Salmon is up 18% and volatile. Suggested alternatives:
Arctic char (similar flavor, -22%), steelhead trout (similar application, -31%)."

## Workflow

### Phase 1: Identify Candidates

```sql
-- Ingredients with enough history for intelligence
SELECT ci.ingredient_id, ci.name,
  COUNT(DISTINCT DATE(iph.observed_at)) as data_days,
  COUNT(*) as total_observations,
  MIN(iph.observed_at) as first_seen,
  MAX(iph.observed_at) as last_seen
FROM canonical_ingredients ci
JOIN ingredient_price_history iph ON iph.ingredient_id = ci.ingredient_id
WHERE iph.price_cents > 0
GROUP BY ci.ingredient_id, ci.name
HAVING COUNT(DISTINCT DATE(iph.observed_at)) >= 30
ORDER BY total_observations DESC
```

### Phase 2: Compute Intelligence (batch)

For each candidate:

1. Pull price history (all observations)
2. Compute volatility score
3. Compute seasonal index (if 12+ months)
4. Compute 7d/30d trends
5. Generate 30d forecast (if seasonal data exists)
6. Score substitutions for volatile/rising ingredients

### Phase 3: Store Results

Write to appropriate tables/columns. Intelligence data must be:

- Timestamped (computed_at)
- Versioned (overwrite, but keep previous in history)
- Queryable by the price resolution chain
- Surfaceable in UI components

### Phase 4: Validate

Spot-check: do forecasts from 30 days ago match today's reality?
Track forecast accuracy over time. This feeds Law 7 (Compound Learning).

## Output

After each run, report:

```
PIE FORECAST RUN [timestamp]
  Ingredients scored: N
  New volatility scores: N (X stable, Y moderate, Z volatile, W extreme)
  Seasonal calendars built: N
  Active trends detected: N rising, N falling
  Forecasts generated: N
  Substitutions scored: N
  Forecast accuracy (30d lookback): X%
```

## Existing Code to Leverage

- `lib/openclaw/trend-forecaster.ts` - already exists, check what it does
- `lib/openclaw/seasonal-analyzer.ts` - already exists
- `lib/pricing/seasonal-analysis.ts` - already exists
- `lib/openclaw/substitute-mapper.ts` - already exists
- `lib/pricing/compound-learning.ts` - already exists

**IMPORTANT:** Before building anything new, read these files. Much of Layer 2
may already be partially implemented. Wire it up, don't rebuild.

## Constraints

- **Layer 1 gate:** Never run if coverage < 80%. Check first.
- **History gate:** Never compute intelligence on < 30 days of data. Garbage in = garbage out.
- **Honest confidence:** Forecasts with low confidence say so. Never present a guess as a prediction.
- **No user labor:** All intelligence is computed from machine-acquired data.
- **Compound learning:** Track forecast accuracy. Models must improve over time (Law 7).
- **Read-then-build:** Check existing code before writing new. Wire up what exists.

## Key Files

- Trend forecaster: `lib/openclaw/trend-forecaster.ts`
- Seasonal analyzer: `lib/openclaw/seasonal-analyzer.ts`
- Seasonal analysis: `lib/pricing/seasonal-analysis.ts`
- Substitute mapper: `lib/openclaw/substitute-mapper.ts`
- Compound learning: `lib/pricing/compound-learning.ts`
- Price history: `ingredient_price_history` table
- Coverage report: `lib/pricing/coverage-report.ts`
- National vision: `docs/specs/pie-national-vision.md`
- PIE Laws: `docs/specs/pie-laws.md` (esp. Laws 7, 11)

## Relationship to Other PIE Skills

```
/pie-measure  -> snapshot (read-only, fast)
/pie-ratchet  -> Layer 1 improvement (coverage, freshness, accuracy)
/pie-forecast -> Layer 2 building (trends, volatility, seasonality)
/pie-fix      -> reactive repair (worst violation after edits)
```

The forecast skill is the transition from "price database" to "pricing
intelligence engine." It's what justifies the I in PIE.
