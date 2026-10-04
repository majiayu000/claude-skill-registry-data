---
name: pie-census
description: PIE Law 8 enforcement. Manages the Census (master manifest of every food ingredient in American commerce). Expands census from new product discoveries, USDA data, and category analysis. Ensures coverage is always measured against a known denominator.
---

# PIE Census

Law 8 says: "Before Pi can find a single price, it must know exactly how
many prices it NEEDS to find." This skill manages that denominator.

The Census is not a static list. It grows as new ingredients are discovered
in scrapes, USDA databases, and product catalogs. It shrinks (marks inactive)
when ingredients are discontinued. It's the living manifest of American food.

## Trigger Conditions

- After large OpenClaw sync (1000+ new products)
- User says "census", "expand census", "how many ingredients"
- Weekly scheduled (Hermes, Monday overnight)
- After `/pie-ratchet` identifies "Census expansion" as top ROI opportunity
- After new chain added to scraping pipeline

## Existing Implementation

**Already built (`lib/pricing/census.ts`):**

- `buildCensus()` - scans canonical_ingredients, assigns tiers (core/extended/specialty), upserts to `openclaw.ingredient_census`
- `getCensusStats()` - reads from `openclaw.census_coverage` materialized view
- Category mapping (17 census categories)
- Tier assignment based on store presence + USDA baseline match
- Batch upsert with conflict handling

**Already built (`lib/pricing/pie-categories.ts`):**

- PIE food category taxonomy

**Table:** `openclaw.ingredient_census` (ingredient_id, census_category, census_tier, standard_unit, data_sources, updated_at)

## Workflow

### Phase 1: Current State

```typescript
import { getCensusStats } from '@/lib/pricing/census'
const stats = await getCensusStats()
// Returns: totalIngredients, core, extended, specialty, totalRegions,
//          totalPriceCellsNeeded, filledPriceCells, coveragePct, byCategory
```

Report:

```
CENSUS STATE [timestamp]
  Total ingredients: 70,234
  Core (5+ stores or USDA): 28,102
  Extended (2-4 stores): 19,847
  Specialty (1 store only): 22,285
  Total pricing regions: 400
  Price cells needed: 28,093,600
  Price cells filled: 17,137,096
  Coverage: 61.0%
```

### Phase 2: Discover New Ingredients

Sources for census expansion:

**A. Unlinked Products (highest yield)**
Products in `openclaw.store_products` with no `normalization_map` link to any canonical_ingredient. These are real products on real shelves that we haven't categorized yet.

```sql
SELECT p.name, COUNT(DISTINCT sp.store_id) as store_count
FROM openclaw.products p
JOIN openclaw.store_products sp ON sp.product_id = p.id
LEFT JOIN openclaw.normalization_map nm ON nm.raw_name = p.name
WHERE nm.id IS NULL
  AND p.is_food = true
  AND sp.price_cents > 0
GROUP BY p.name
HAVING COUNT(DISTINCT sp.store_id) >= 3
ORDER BY store_count DESC
LIMIT 500
```

**B. USDA FDC Database**
USDA Food Data Central has ~380K food items. Compare against our census to find gaps.

**C. Recipe Ingredient References**
Ingredients referenced in recipes (`recipe_ingredients` table) that don't exist in the census. These are ingredients chefs actually USE.

```sql
SELECT ri.ingredient_name, COUNT(*) as recipe_count
FROM recipe_ingredients ri
LEFT JOIN openclaw.canonical_ingredients ci
  ON LOWER(TRIM(ri.ingredient_name)) = LOWER(TRIM(ci.name))
WHERE ci.ingredient_id IS NULL
GROUP BY ri.ingredient_name
HAVING COUNT(*) >= 2
ORDER BY recipe_count DESC
```

**D. Category Gap Analysis**
For each category, compare our census against expected diversity:

| Category   | Expected (USDA benchmark) | Our census | Gap |
| ---------- | ------------------------- | ---------- | --- |
| Protein    | ~5,000                    | ?          | ?   |
| Seafood    | ~3,000                    | ?          | ?   |
| Produce    | ~8,000                    | ?          | ?   |
| Dairy      | ~4,000                    | ?          | ?   |
| Grain      | ~6,000                    | ?          | ?   |
| Spice/Herb | ~2,000                    | ?          | ?   |

### Phase 3: Expand Census

For each discovered ingredient:

1. Verify it's a real, distinct food ingredient (not a brand variant of existing)
2. Assign to census category
3. Determine standard unit (lb, oz, each, bunch, etc.)
4. Assign tier based on store presence
5. Insert into `openclaw.canonical_ingredients` and `openclaw.ingredient_census`
6. Create `normalization_map` entries linking product names to new canonical

**Deduplication rules:**

- "Chicken Breast Boneless Skinless" and "Boneless Skinless Chicken Breast" = same ingredient
- "Organic Chicken Breast" = DIFFERENT ingredient (organic matters for pricing)
- "Tyson Chicken Breast 3lb" = product, not ingredient (links to "chicken breast")
- Use `lib/pricing/name-normalizer.ts` for fuzzy matching

### Phase 4: Prune Inactive

Mark ingredients inactive (don't delete) when:

- Zero store products link to them for 180+ days
- USDA marks the item discontinued
- Category is deprecated (e.g., banned substances)

```sql
UPDATE openclaw.ingredient_census
SET is_active = false, deactivated_at = now()
WHERE ingredient_id IN (
  SELECT ic.ingredient_id
  FROM openclaw.ingredient_census ic
  LEFT JOIN openclaw.normalization_map nm ON nm.canonical_ingredient_id = ic.ingredient_id
  LEFT JOIN openclaw.products p ON p.name = nm.raw_name
  LEFT JOIN openclaw.store_products sp ON sp.product_id = p.id
    AND sp.last_seen_at > now() - interval '180 days'
  WHERE sp.id IS NULL
    AND ic.is_active = true
)
```

### Phase 5: Rebuild Stats

```typescript
import { buildCensus } from '@/lib/pricing/census'
const result = await buildCensus()
// Rebuilds tier assignments, data_sources, category mappings
```

Then refresh materialized view:

```sql
REFRESH MATERIALIZED VIEW CONCURRENTLY openclaw.census_coverage;
```

### Phase 6: Log

Append to ratchet log (census expansion is a ratchet action):

```markdown
## [timestamp]

**Opportunity:** Census expansion
**Action:** Added N new ingredients from [source]
**Delta:**

- Census: X -> Y (+Z)
- Core tier: +N
- Extended tier: +N
- New categories covered: [list]
  **Pruned:** N inactive ingredients marked
```

## Census Quality Rules

1. **Every ingredient has exactly one canonical entry.** No duplicates.
2. **Every ingredient has a category.** No "uncategorized" allowed long-term.
3. **Every ingredient has a standard unit.** Required for price comparison.
4. **Tier reflects reality.** Core = widely available, Specialty = rare.
5. **Census grows, rarely shrinks.** Inactive != deleted.
6. **Census drives coverage %.** All PIE metrics reference census as denominator.

## National Scale Targets

| Milestone                     | Census size | Notes                                   |
| ----------------------------- | ----------- | --------------------------------------- |
| Current (measured 2026-05-04) | 141,553     | 87.1% norm-linked, 18K naked            |
| 6 months                      | 175K        | + USDA FDC integration, close naked gap |
| 1 year                        | 200K        | + wholesale catalogs, specialty items   |
| 2 years                       | 250K+       | Approaching full American food commerce |

For reference: USDA FDC has ~380K food items, but many are brand variants
of the same ingredient. After deduplication to ingredient level, estimate
200-250K distinct food ingredients in American commerce.

**Current strength:** 196K stores, 15K chains, 39M priced products, all 62
states/territories. The Census is already bigger than spec assumed. Primary
gap is freshness (last sync 26 days ago) not coverage.

## Constraints

- **Never delete.** Mark inactive only.
- **No duplicates.** Dedup before insert. Use normalizer.
- **Standard units required.** Can't compare prices without units.
- **Food only.** `is_food = true` gate. No household products, pet food, etc.
- **Tier honesty.** Don't inflate tier. If only 1 store carries it, it's specialty.

## Key Files

- Census builder: `lib/pricing/census.ts`
- Categories: `lib/pricing/pie-categories.ts`
- Name normalizer: `lib/pricing/name-normalizer.ts`
- Canonical ingredients: `openclaw.canonical_ingredients` table
- Census table: `openclaw.ingredient_census` table
- Coverage view: `openclaw.census_coverage` materialized view
- Normalization map: `openclaw.normalization_map` table
- PIE Laws: `docs/specs/pie-laws.md` (Law 8)

## Relationship to Other PIE Skills

The Census is the denominator for everything:

- `/pie-measure` reports coverage AS % OF CENSUS
- `/pie-ratchet` identifies "naked ingredients" relative to census
- `/pie-accuracy` validates prices that exist in census
- `/pie-forecast` builds intelligence for census ingredients with history

Without a growing, accurate Census, PIE can't know what "100%" means.
