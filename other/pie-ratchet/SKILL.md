---
name: pie-ratchet
description: Monotonic PIE improvement toward national scale (millions of users, all 50 states, 200K+ ingredients). Every invocation leaves PIE measurably better. Proactive, opportunistic, compounds over time. Use on schedule, after OpenClaw syncs, during idle time, or anytime you want PIE to get better without a specific target.
---

# PIE Ratchet

Proactive, monotonic improvement engine for PIE. Every run finds the highest-ROI
improvement available right now and executes it. Never goes backwards. Compounds
across sessions. Guided by the national vision: `docs/specs/pie-national-vision.md`.

**End goal:** America's food pricing truth layer. Every food professional in the
country gets accurate, local, real-time pricing intelligence without lifting a finger.

## Trigger Conditions (auto-fire)

- After any OpenClaw pull/sync completes
- After any cron job touches pricing data
- User says "improve PIE", "make pricing better", "ratchet", "PIE better"
- Idle time at end of session (before /close-session)
- Scheduled via Hermes overnight runs

## Philosophy

PIE is a ratchet, not a dial. It only turns one way. Each invocation:

1. Measures where we are
2. Finds what moves the needle most right now
3. Does it
4. Proves it worked
5. Logs it so the compound effect is visible

No reports. No recommendations. Code ships every time.

## Strategic Layers (work bottom-up)

The ratchet improves whichever layer has the highest-ROI gap RIGHT NOW:

| Layer                          | What                                                 | Unlock condition       |
| ------------------------------ | ---------------------------------------------------- | ---------------------- |
| **1. Price Resolution**        | Every ingredient returns a price                     | CURRENT FOCUS          |
| **2. Trend Intelligence**      | Detect volatility, seasonality, cost forecasting     | Layer 1 > 90% coverage |
| **3. Menu Economics**          | Auto food cost %, margin alerts, substitution engine | Layer 2 active         |
| **4. Purchasing Intelligence** | Optimal store split, bulk break-even, timing         | Layer 2 active         |
| **5. Market Positioning**      | Regional benchmarks, pricing power detection         | Layer 3 + user base    |
| **6. Predictive Supply Chain** | Origin tracking, shortage prediction                 | Layer 2 + 1yr history  |

Layer 1 is the foundation. Until coverage + freshness + accuracy are solid,
higher layers are premature. But the ratchet should recognize when Layer 1 is
"good enough" and start building Layer 2 infrastructure.

## Data Access

**Pi (SSH):** `davidferra@10.0.0.177` - prices.db (SQLite, 442MB, 245K prices)
**Local PG:** ChefFlow database with openclaw schema (synced from Pi)
**Key tables (Pi):** products, store_products, stores, chains, canonical_ingredients, normalization_map, system_ingredient_prices
**Key tables (Local):** openclaw.\* (mirror), system_ingredients, canonical_ingredients

Always verify which DB has the data you need before querying. Pi is source of
truth for raw prices. Local PG is source of truth for ChefFlow-facing data.

## Pre-flight Check

Before starting any cycle:

1. Is Pi reachable? (`ssh davidferra@10.0.0.177 echo ok`)
2. Is local PG up? (test connection)
3. When was last OpenClaw sync? (check `docs/pie-ratchet-log.md` last entry)

If Pi is down: work only with local data (synthetics, normalization, images).
If PG is down: fix it first (Law 5: Self-Healing).

## Workflow

### Phase 1: Snapshot (measure current state)

```sql
-- Core metrics (run against local PG)
SELECT
  COUNT(*)::int as census_size,
  COUNT(*) FILTER (WHERE has_real_price) as real_prices,
  COUNT(*) FILTER (WHERE has_synthetic) as synthetic_prices,
  COUNT(*) FILTER (WHERE has_real_price OR has_synthetic) as total_covered,
  COUNT(*) FILTER (WHERE has_image) as with_image,
  COUNT(*) FILTER (WHERE NOT has_real_price AND NOT has_synthetic) as naked_ingredients
FROM (
  SELECT ci.ingredient_id,
    EXISTS(SELECT 1 FROM openclaw.normalization_map nm
      JOIN openclaw.products p ON LOWER(TRIM(p.name)) = LOWER(TRIM(nm.raw_name))
      JOIN openclaw.store_products sp ON sp.product_id = p.id AND sp.price_cents > 0
      JOIN openclaw.stores s ON s.id = sp.store_id AND s.is_active = true
      JOIN openclaw.chains c ON c.id = s.chain_id AND c.source_type NOT IN ('convenience','dollar')
      WHERE nm.canonical_ingredient_id = ci.ingredient_id
    ) as has_real_price,
    EXISTS(SELECT 1 FROM system_ingredients si
      JOIN openclaw.system_ingredient_prices sip ON sip.system_ingredient_id = si.id
      WHERE LOWER(TRIM(si.name)) = LOWER(TRIM(ci.name)) AND sip.avg_price_cents > 0
    ) as has_synthetic,
    (ci.off_image_url IS NOT NULL AND ci.off_image_url != '' AND ci.off_image_url != 'none') as has_image
  FROM openclaw.canonical_ingredients ci
) sub;

-- Geographic spread
SELECT COUNT(DISTINCT s.state)::int as states_covered
FROM openclaw.store_products sp
JOIN openclaw.stores s ON s.id = sp.store_id AND s.is_active = true
JOIN openclaw.chains c ON c.id = s.chain_id AND c.source_type NOT IN ('convenience','dollar')
WHERE sp.price_cents > 0;

-- Freshness distribution
SELECT
  COUNT(*) FILTER (WHERE last_seen_at > now() - interval '7 days')::int as fresh_7d,
  COUNT(*) FILTER (WHERE last_seen_at > now() - interval '14 days')::int as fresh_14d,
  COUNT(*) FILTER (WHERE last_seen_at > now() - interval '30 days')::int as fresh_30d,
  COUNT(*) FILTER (WHERE last_seen_at <= now() - interval '30 days')::int as stale,
  COUNT(*)::int as total_prices
FROM openclaw.store_products WHERE price_cents > 0;

-- Source diversity (multi-source = higher confidence)
SELECT
  COUNT(*) FILTER (WHERE source_count = 1)::int as single_source,
  COUNT(*) FILTER (WHERE source_count >= 2)::int as multi_source,
  COUNT(*) FILTER (WHERE source_count >= 3)::int as triangulated
FROM (
  SELECT ci.ingredient_id, COUNT(DISTINCT c.id) as source_count
  FROM openclaw.canonical_ingredients ci
  JOIN openclaw.normalization_map nm ON nm.canonical_ingredient_id = ci.ingredient_id
  JOIN openclaw.products p ON LOWER(TRIM(p.name)) = LOWER(TRIM(nm.raw_name))
  JOIN openclaw.store_products sp ON sp.product_id = p.id AND sp.price_cents > 0
  JOIN openclaw.stores s ON s.id = sp.store_id AND s.is_active = true
  JOIN openclaw.chains c ON c.id = s.chain_id AND c.source_type NOT IN ('convenience','dollar')
  GROUP BY ci.ingredient_id
) sub;
```

Record all numbers. Compare to last run (from history file).

### Phase 2: ROI Ranking (Algorithmic)

Query each opportunity. Pick the one with highest `(gap_count * impact_weight)`.
No subjective judgment. Numbers decide.

```
SCORE = gap_count * weight
```

| Opportunity                                         | Weight | Detection query                             | Layer |
| --------------------------------------------------- | ------ | ------------------------------------------- | ----- |
| **Naked ingredients** (no price at all)             | 10     | `naked_ingredients` count                   | 1     |
| **Contamination** (bad sources leaking)             | 9      | convenience/dollar in active queries        | 1     |
| **Stale prices** (past freshness threshold)         | 8      | `stale` count                               | 1     |
| **Unmapped products** (prices exist, no norm link)  | 7      | products with prices but no norm entry      | 1     |
| **Missing synthetics** (gap-fill available)         | 7      | naked ingredients with computable synthetic | 1     |
| **Geographic gaps** (states with no data)           | 6      | `50 - states_covered`                       | 1     |
| **Single-source ingredients** (fragile)             | 5      | `single_source` count                       | 1     |
| **Confidence upgrades** (synthetic -> real)         | 5      | synthetics where real data now exists       | 1     |
| **Census expansion** (new ingredients to add)       | 4      | products not in canonical list              | 1     |
| **Image gaps** (no visual for catalog)              | 3      | `census - with_image`                       | 1     |
| **Accuracy validation** (spot-check real vs served) | 6      | random sample divergence                    | 1     |
| **Trend detection infra** (volatility scoring)      | 4      | no volatility scores exist yet              | 2     |
| **Seasonal calendar gaps**                          | 3      | ingredients with no seasonal data           | 2     |
| **Regional multiplier gaps**                        | 5      | regions with no local adjustment            | 1-2   |

**Rule:** Layer 1 opportunities ALWAYS outrank Layer 2+ at same score.
Only work Layer 2 when no Layer 1 opportunity scores above threshold (gap < 100).

Pick the TOP opportunity. Only one per cycle. Small bites, always forward.

### Phase 3: Execute

Based on what Phase 2 identified, execute ONE of these playbooks:

#### A. Fix Naked Ingredients

1. Find unmapped products that match naked ingredient names (fuzzy)
2. Create normalization_map entries
3. OR generate synthetic prices from category baselines

#### B. Map Unmapped Products

1. Query products with prices but no norm link
2. Match against canonical_ingredients (Levenshtein, token overlap)
3. Insert normalization_map rows for high-confidence matches (>0.85)

#### C. Refresh Stale Prices

1. Identify stale store_products past freshness tier
2. If scraper exists for that chain: trigger re-scrape (Pi cron)
3. If no scraper: generate fresh synthetic from latest regional data

#### D. Deepen Source Diversity

1. Find single-source ingredients
2. Check if other chains carry same product (unmapped)
3. Create cross-chain normalization links

#### E. Generate Missing Synthetics

1. For each naked ingredient, compute synthetic from:
   - Category average (same food group)
   - Regional multiplier (chef's state vs national)
   - Seasonal factor (current month)
   - Yield-adjusted unit price
2. Insert into system_ingredient_prices

#### F. Expand Geographic Coverage

1. Find states with zero/few stores
2. Check OSM store data for that state
3. Queue new store ingestion targets for OpenClaw

#### G. Fill Image Gaps

1. Query canonical_ingredients with no image
2. Attempt OFF (Open Food Facts) lookup by name
3. Fall back to category placeholder SVG path

#### H. Upgrade Synthetics to Real

1. Find synthetic prices where real data now exists (from recent scrapes)
2. Replace synthetic with real, upgrade confidence score

#### I. Expand Census

1. Find products in store_products not linked to any canonical_ingredient
2. Group by similarity, create new canonical entries
3. Immediately link via normalization_map

#### J. Clean Contamination

1. Find convenience/dollar store prices leaking into resolution queries
2. Add missing chain source_type classifications
3. Verify filter clauses in all pricing queries

### Phase 4: Re-measure

Run Phase 1 queries again. Compute deltas.

### Phase 5: Log

Append to `docs/pie-ratchet-log.md`:

```markdown
## [ISO timestamp]

**Opportunity:** [what was identified]
**Action:** [what was done]
**Delta:**

- Coverage: X% -> Y% (+Z%)
- Real prices: N -> M (+K)
- Synthetics: N -> M (+K)
- Images: N -> M (+K)
- States: N -> M
- Freshness (7d): N% -> M%
  **Files changed:** [list]
  **Law impact:** [which laws improved]
```

### Phase 6: Chain Check

After logging, check: is there another sub-5-minute improvement available? If yes AND total session time allows, run another cycle. Max 3 cycles per invocation to avoid runaway sessions.

### Phase 3 (Extended): Layer 2 Playbooks

Only execute these when Layer 1 scores are below threshold (gap < 100):

#### K. Build Volatility Scores

1. Query price history for each ingredient (min 30 days of data needed)
2. Compute coefficient of variation (std_dev / mean)
3. Store volatility_score on canonical_ingredient or new table
4. Flag HIGH volatility ingredients (CV > 0.3) for trend alerts

#### L. Build Seasonal Calendars

1. Query 12-month price history by ingredient
2. Detect seasonal patterns (monthly average vs annual average)
3. Store peak/trough months per ingredient
4. Enable "cheapest window" predictions

#### M. Build Regional Multipliers

1. Compare same ingredient across pricing regions
2. Compute region-specific multiplier vs national average
3. Store per-region adjustment factors
4. Improve geographic resolution (Law 6)

#### N. Accuracy Validation (spot-check)

1. Pick 20 random ingredients with HIGH confidence
2. Compare served price vs actual store shelf (via latest scrape)
3. Compute accuracy % (within 15% = pass)
4. Log accuracy metric. If below 90%, investigate worst offenders.

---

## Constraints

- **Never remove data.** Ratchet only turns forward.
- **Never surface convenience/dollar store prices.** Filter, never delete.
- **Never crowdsource.** All improvements come from OpenClaw pipeline or synthesis.
- **Never modify chef overrides.** Chef data is sacred personal QoL.
- **Confidence scores must be honest.** Synthetic = synthetic. Estimated = estimated.
- **Max 3 cycles per invocation.** Prevent runaway.
- **Log every action.** Compound learning requires visible history.
- **Verify data access before querying.** Don't assume tables/columns exist.
- **Layer 1 before Layer 2.** Always. No skipping ahead.

## Success Metrics (compound over time, keyed to national targets)

Track these in the log. They should ONLY go up:

| Metric                                   | Actual (2026-05-04)                   | 6mo target | 1yr target |
| ---------------------------------------- | ------------------------------------- | ---------- | ---------- |
| Census size                              | 141,553                               | 175K       | 200K       |
| Norm-linked % (has product match)        | 87.1%                                 | 93%        | 97%        |
| Total coverage % (real+synthetic/census) | TBD (freshness)                       | 90%        | 98%        |
| Priced store_products                    | 39,012,269                            | 50M        | 75M        |
| Image coverage %                         | TBD                                   | 60%        | 80%        |
| States/territories                       | 62 (all)                              | 62         | 62         |
| Active stores                            | 196,964                               | 220K       | 250K       |
| Norm map entries                         | 180,644                               | 220K       | 280K       |
| Multi-source %                           | 42.9% (52K/123K)                      | 55%        | 65%        |
| 7-day freshness (volatile)               | 0% (Pi down; 92% of 30d when syncing) | 70%        | 90%        |
| Accuracy (within 15% of shelf)           | unmeasured                            | 75%        | 85%        |
| Active chains                            | 15,089                                | 16K        | 18K        |

Each ratchet log entry must include at least: coverage %, real %, states, freshness.

## Key Files

- PIE Laws: `docs/specs/pie-laws.md`
- National Vision: `docs/specs/pie-national-vision.md`
- Price resolution: `lib/pricing/resolve-price.ts`
- Synthetic engine: `lib/pricing/synthetic-engine.ts`
- Census: `lib/pricing/census.ts`
- Compliance: `lib/pricing/pie-compliance.ts`
- Catalog queries: `lib/openclaw/catalog-actions.ts`
- Normalization: `lib/openclaw/normalization.ts`
- Image enrichment: `lib/ingredients/image-actions.ts`
- Pi sync: `lib/openclaw/sync.ts`
- Pull script: `scripts/openclaw-pull/pull.mjs`
- Ratchet history: `docs/pie-ratchet-log.md`
- Pi prices.db: `davidferra@10.0.0.177:~/prices.db` (SQLite source of truth)

## Relationship to /pie-fix

`/pie-fix` is reactive: triggered by pricing edits, fixes the worst violation.
`/pie-ratchet` is proactive: runs opportunistically, always finds the next improvement.

They complement each other. `/pie-fix` is the fire extinguisher. `/pie-ratchet` is the gym membership.

## Relationship to National Vision

This skill is the daily mechanism that moves PIE toward
`docs/specs/pie-national-vision.md`. The vision describes WHERE.
The ratchet describes HOW (one cycle at a time).

Every metric in this skill maps to a row in the vision's success table.
When the ratchet runs, it's building toward millions of users even if
today there's one.
