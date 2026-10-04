---
name: pie-fix
description: Systematic PIE (Pricing Intelligence Engine) audit and fix. Measures all 10 PIE Laws, finds the worst violation, fixes it, measures again. Use when touching pricing code, catalog, ingredients, costing, or when user mentions PIE, pricing coverage, price quality, missing prices, bad prices, images missing, convenience stores, or data gaps.
---

# PIE Fix

Audit PIE against its 10 Immutable Laws, find the worst violation, fix it, measure improvement.

**Not a report. A fix-it skill.** Every invocation leaves PIE measurably better.

## Trigger Conditions (auto-fire)

- Editing files in `lib/pricing/`, `lib/openclaw/`, `components/pricing/`
- Editing catalog browser, costing pages, ingredient pages
- User mentions pricing, PIE, coverage, images, estimates, data quality
- After any OpenClaw sync or pull completes

## Workflow

### Phase 1: Measure (30 seconds)

Run the PIE health query against local PG:

```sql
-- Coverage
SELECT COUNT(*)::int as total_canonical,
  COUNT(*) FILTER (WHERE has_price) as with_store_price,
  COUNT(*) FILTER (WHERE has_estimate) as with_estimate,
  COUNT(*) FILTER (WHERE has_image) as with_image
FROM (
  SELECT ci.ingredient_id,
    EXISTS(SELECT 1 FROM openclaw.normalization_map nm
      JOIN openclaw.products p ON LOWER(TRIM(p.name)) = LOWER(TRIM(nm.raw_name))
      JOIN openclaw.store_products sp ON sp.product_id = p.id AND sp.price_cents > 0
      JOIN openclaw.stores s ON s.id = sp.store_id AND s.is_active = true
      JOIN openclaw.chains c ON c.id = s.chain_id AND c.source_type NOT IN ('convenience','dollar')
      WHERE nm.canonical_ingredient_id = ci.ingredient_id
    ) as has_price,
    EXISTS(SELECT 1 FROM system_ingredients si
      JOIN openclaw.system_ingredient_prices sip ON sip.system_ingredient_id = si.id
      WHERE LOWER(TRIM(si.name)) = LOWER(TRIM(ci.name)) AND sip.avg_price_cents > 0
    ) as has_estimate,
    (ci.off_image_url IS NOT NULL AND ci.off_image_url != '' AND ci.off_image_url != 'none') as has_image
  FROM openclaw.canonical_ingredients ci
) sub;

-- Geographic spread
SELECT COUNT(DISTINCT s.state)::int as states_with_prices
FROM openclaw.store_products sp
JOIN openclaw.stores s ON s.id = sp.store_id
WHERE sp.price_cents > 0;

-- Convenience/dollar contamination
SELECT COUNT(*)::int as contaminated_rows
FROM openclaw.store_products sp
JOIN openclaw.stores s ON s.id = sp.store_id
JOIN openclaw.chains c ON c.id = s.chain_id
WHERE c.source_type IN ('convenience','dollar') AND sp.price_cents > 0;

-- Freshness
SELECT COUNT(*) FILTER (WHERE last_seen_at > now() - interval '7 days')::int as fresh_7d,
  COUNT(*) FILTER (WHERE last_seen_at > now() - interval '30 days')::int as fresh_30d,
  COUNT(*)::int as total
FROM openclaw.store_products WHERE price_cents > 0;
```

### Phase 2: Score against 10 Laws

| Law                        | Check                                             | PASS threshold |
| -------------------------- | ------------------------------------------------- | -------------- |
| 1. Total Autonomy          | No chef data dependency in pricing pipeline       | Binary         |
| 2. Universal Coverage      | >95% canonical ingredients have price OR estimate | 95%            |
| 3. Honesty Over Silence    | Estimates labeled as estimates, never hidden      | Binary         |
| 4. Freshness               | Volatile <7d, Moderate <14d, Stable <30d          | 80% fresh      |
| 5. Self-Healing            | Zero unresolved pipeline errors                   | 0 errors       |
| 6. Geographic Intelligence | Prices in 40+ states                              | 40 states      |
| 7. Compound Learning       | Month-over-month accuracy improving               | Positive trend |
| 8. The Census              | 10K+ ingredients in Census                        | 10,000         |
| 9. Synthetic Pricing       | Every Census gap has synthetic estimate           | 100%           |
| 10. No Unprotected Price   | Zero ingredients fall through all 11 tiers        | 0 failures     |

### Phase 3: Identify worst violation

Rank failures by impact:

1. Coverage gaps (Law 2) > anything else
2. Geographic dead zones (Law 6)
3. Missing images (visual trust)
4. Stale prices (Law 4)
5. Contaminated sources (convenience/dollar leaking through)
6. Missing synthetics (Law 9)

### Phase 4: Fix it

Apply the fix. Not a recommendation. Code changes, migrations, data updates.

### Phase 5: Re-measure

Run Phase 1 queries again. Report delta:

```
PIE Health: [before] -> [after]
Coverage: 45% -> 67% (+22%)
Images: 1.2% -> 12% (+10.8%)
States: 17 -> 17 (no change, Pi offline)
Law violations: 6 -> 4 (-2)
```

## Key Files

- Canonical spec: `docs/specs/pie-laws.md`
- Pricing strategy: `docs/specs/openclaw-nationwide-pricing-strategy.md`
- Catalog query: `lib/openclaw/catalog-actions.ts`
- Price resolution: `lib/pricing/resolve-price.ts`
- Synthetic engine: `lib/pricing/synthetic-engine.ts`
- Image enrichment: `lib/ingredients/image-actions.ts`
- Pi sync: `lib/openclaw/sync.ts`
- Pull script: `scripts/openclaw-pull/pull.mjs`
- Census: `lib/pricing/census.ts`
- Compliance: `lib/pricing/pie-compliance.ts`

## Rules

- **Fix, don't report.** Every invocation ships a code change.
- **Measure before AND after.** No unmeasured improvements.
- **Convenience/dollar stores NEVER surface to chefs.** Filter at query level.
- **Estimates shown as estimates.** "Market Estimate" label, confidence badge. Never hidden.
- **Images:** product image > OFF image > category SVG. Never broken `<img>`.
- **No crowdsourced data.** OpenClaw builds everything. Chef data is personal QoL only.
- **Colony expansion:** outward from anchor, not random scatter.
