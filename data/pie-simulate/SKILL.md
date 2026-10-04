---
name: pie-simulate
description: Full PIE nationwide price simulation pipeline. Seeds census, generates resolved prices across all 101 US regions, fills gaps with synthetics, verifies coverage. Use when user says "simulate PIE", "seed prices", "nationwide pricing", "PIE for all users", or wants to regenerate/refresh the price database from scratch.
---

# PIE Nationwide Simulation

Populates PIE with prices for every census ingredient in every US pricing region.
Re-runnable (idempotent via ON CONFLICT). Run after adding new ingredients, regions, or system prices.

## Pipeline (4 Steps)

```
npx tsx scripts/seed-pie-nationwide.ts
```

### Step 1: Build Census

- Source: `openclaw.canonical_ingredients` (food categories only)
- Target: `openclaw.ingredient_census`
- Maps 24 OpenClaw categories to 8 census categories (produce, protein, dairy, grain, beverage, spice, condiment, sweet, pantry)
- Expected: ~77K ingredients

### Step 2: Generate Resolved Prices

- SQL cross-join: `system_ingredient_prices` x `pricing_regions`
- Scales `avg_price_cents` by regional `cost_index` (BLS RPP)
- Expected: ~19K prices x 101 regions = ~1.97M resolved prices
- ON CONFLICT: updates existing prices

### Step 3: Synthetic Prices (Gap Fill)

- Pre-computes category medians via CTE (8 categories)
- Fills census ingredients NOT in system_ingredient_prices
- Expected: ~58K gap ingredients x 101 regions = ~5.8M synthetics
- Confidence: 0.35 (low, superseded when real data arrives)

### Step 4: Verify Coverage

- Reads `openclaw.census_coverage` view
- Reads `openclaw.pie_compliance` view (10 Laws)
- Target: 0 unprotected ingredients (Law 10)

## Prerequisites

Run these first if tables don't exist:

```
npx tsx scripts/run-pie-migrations.ts     # Creates openclaw PIE tables
npx tsx scripts/seed-pricing-regions.ts   # Seeds 101 regions + 42K ZIP centroids
```

## Known Pitfalls

| Issue                               | Cause                                                                                                        | Fix                                                                     |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------- |
| `uuid = text` type error            | `system_ingredient_prices.system_ingredient_id` is UUID, census uses text                                    | Cast: `::text`                                                          |
| `column price_cents does not exist` | Column is `avg_price_cents` on system_ingredient_prices                                                      | Use correct name                                                        |
| Step 3 hangs forever                | Correlated subquery per-row is O(n*m*k)                                                                      | Use CTE for category medians                                            |
| Step 3 blocked by locks             | Previous failed runs hold table locks                                                                        | Run `scripts/cancel-stuck-queries.ts` or terminate via pg_stat_activity |
| Coverage shows 25% real             | Expected. 19K/77K ingredients have real prices. Rest = synthetic. Law 10 = 0 unprotected is the real metric. |

## Performance Notes

- Step 2 (1.97M rows): ~30s on local Supabase
- Step 3 (5.8M rows): ~5-10min on local Supabase
- Total: ~10min clean run
- If stuck >5min on step 3: check for lock contention from prior runs

## Success Criteria

```
Law 10 (unprotected): 0          # Every ingredient has a price everywhere
Coverage: >25% real              # Real prices from system data
Synthetic confidence: 0.35       # Low enough to be superseded
Census size: >70K                # Comprehensive food ingredient coverage
Regions: 101                     # All US pricing regions active
```

## When to Re-run

- After Pi sync adds new `system_ingredient_prices`
- After adding new pricing regions
- After expanding `canonical_ingredients` catalog
- After schema changes to PIE tables
- Monthly refresh to pick up new data

## Related Skills

- `/pie` - Dashboard and status
- `/pie-census` - Expand the census manifest
- `/pie-ratchet` - Improve coverage incrementally
- `/pie-measure` - Quick metrics snapshot
- `/pie-accuracy` - Validate price correctness

## Key Files

- `scripts/seed-pie-nationwide.ts` - Main simulation script
- `scripts/run-pie-migrations.ts` - PIE table creation
- `scripts/seed-pricing-regions.ts` - Region + ZIP seeding
- `database/migrations/20260503000009_pricing_regions.sql` - Regions schema
- `database/migrations/20260503000013_pie_census_and_fallback.sql` - Census/synthetic schema
- `lib/pricing/resolve-price.ts` - 10-tier resolution chain (runtime)
- `lib/pricing/census.ts` - Census builder (runtime)
- `lib/pricing/synthetic-engine.ts` - Synthetic pricing (runtime)
