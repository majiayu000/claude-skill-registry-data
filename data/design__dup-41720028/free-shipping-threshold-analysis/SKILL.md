---
name: free-shipping-threshold-analysis
description: Analyzes Fulfil order data to determine profitable free shipping thresholds using order value distribution, hero product analysis, and shipping economics. Use when merchants ask about free shipping strategy, threshold optimization, shipping offers, AOV analysis, or need data-driven shipping decisions. Requires access to Fulfil data warehouse (sales_orders, shipments tables).
---

# Free Shipping Threshold Analysis

## Overview

This skill analyzes merchant order data in Fulfil to determine the most profitable free shipping threshold. It implements a data-driven methodology that balances conversion gains against margin impact, avoiding the common mistake of setting thresholds based on guesswork or competitor behavior.

## When to Use

Use this skill when merchants need to:
- Determine optimal free shipping thresholds for e-commerce
- Understand order value distribution and clustering patterns
- Identify hero products and their pricing impact
- Calculate profit trade-offs of different threshold options
- Make data-driven shipping strategy decisions before A/B testing

## Required Data

Access to Fulfil data warehouse with these tables:
- `sales_orders` - Order values, line items, channels
- `shipments` - Shipping costs and fulfillment data
- Minimum 6 months of order history (1,000+ orders recommended)

## Critical Constraints

**Marketplace Channel Exclusion**: Always ask if data includes marketplace channels (Amazon, Walmart, eBay, Etsy, Target). Exclude these from analysis because merchants don't control marketplace shipping policies and their inclusion creates misleading recommendations.

**Shipping Line Item Patterns**: Understand how shipping appears in order data:
- SHIPPING line with amount > $0 = customer paid shipping
- SHIPPING line with amount = $0 = explicit free shipping
- No SHIPPING line = implicit free shipping

Product codes vary across merchants ("SHIPPING", "Shipping", "SHIP"). Search flexibly.

## Analysis Workflow

Copy this checklist and track progress:

```
Free Shipping Analysis Progress:
- [ ] Step 0: Identify channels and exclude marketplaces
- [ ] Step 1: Analyze order value distribution
- [ ] Step 2: Identify hero products
- [ ] Step 3: Calculate shipping economics
- [ ] Step 4: Evaluate threshold candidates
- [ ] Step 5: Generate recommendations
```

### Step 0: Channel Discovery & Filtering

**Before running analysis**, identify available sales channels and confirm marketplace exclusions with the merchant.

1. Query available channels with order volumes
2. Ask: "Should I exclude marketplace channels like Amazon, Walmart, or eBay? These have their own shipping policies."
3. Identify shipping line patterns by channel (helps understand current free shipping behavior)
4. Update all subsequent queries to exclude confirmed marketplace channels

**For detailed SQL queries**: See [METHODOLOGY.md](METHODOLOGY.md) Step 0

### Step 1: Map Order Landscape

**Objective**: Understand where customer orders naturally cluster

Analyze:
1. Order value distribution (group into $10 buckets)
2. Identify peak order value ranges
3. Understand order concentration patterns

**For detailed SQL queries**: See [METHODOLOGY.md](METHODOLOGY.md) Step 1

### Step 2: Identify Hero Products

**Objective**: Find products driving most revenue and their price points

Analyze:
1. Top 10-20 products by revenue contribution
2. Average selling prices
3. Product categories and patterns
4. Low-margin products (items under typical threshold ranges)

**For detailed SQL queries**: See [METHODOLOGY.md](METHODOLOGY.md) Step 2

### Step 3: Calculate Shipping Economics

**Objective**: Understand current shipping costs and patterns

Analyze:
1. Average and median shipping costs
2. Current free shipping patterns (if any)
3. Shipping charge distribution for paid orders
4. Order value comparison (free vs paid shipping)

**For detailed SQL queries**: See [METHODOLOGY.md](METHODOLOGY.md) Step 3

### Step 4: Evaluate Threshold Candidates

**Objective**: Calculate financial implications of threshold options

For thresholds: $30, $40, $50, $75, $100, $125, $150, $175, $200

Calculate for each:
1. Orders above/below threshold (volume)
2. Average order values for each group
3. Total shipping cost if threshold implemented
4. Margin-to-shipping ratio (viability metric)
5. Risk assessment

**For detailed SQL queries**: See [METHODOLOGY.md](METHODOLOGY.md) Step 4

### Step 5: Generate Recommendations

**Framework**: Map each threshold to a business hypothesis

| Threshold | Hypothesis | Logic |
|-----------|------------|-------|
| Below Hero Price | Shipping cost blocks conversion on hero items | Above low-margin zone, removes friction |
| Above Hero Price | Customers will add items to qualify | Tests basket expansion, higher AOV offsets cost |

**Three Zones**:

1. **DON'T TEST: Too Low ($30 and below)**
   - Bleeds profit on low-margin items
   - Shipping cost often exceeds order margin

2. **SMART ZONE: ($50-$150)**
   - Has existing demand in data
   - Protects margin on hero products
   - Tests realistic customer behavior

3. **DON'T TEST: Too High ($200+)**
   - Insufficient volume for meaningful testing
   - Beyond natural customer spending patterns

## Output Format

Provide analysis in this structure:

### 1. Executive Summary
- Order clustering patterns and primary zones
- Hero product identification and pricing
- Average shipping costs
- Current free shipping patterns (if applicable)
- Recommended threshold(s) with rationale

### 2. Data Findings

**Order Distribution**:
- Show order count by value bucket ($0-10, $10-20, etc.)
- Highlight primary cluster zones
- Note threshold candidates being considered

**Hero Products**:
- Top 5-10 products by revenue
- Average selling prices
- Revenue contribution percentages

**Shipping Economics**:
- If shipping lines exist: Free vs paid shipping breakdown
- Distribution of shipping charges
- Average order value comparison

### 3. Threshold Recommendations

For each recommended threshold:

**Threshold: $XX**
- **Hypothesis**: What customer behavior this tests
- **Volume**: % of orders at/above this level
- **Margin Protection**: Margin-to-shipping ratio
- **Strategic Logic**: Why this threshold makes sense
- **Risk Assessment**: Potential concerns
- **Expected Impact**: Projected costs

**Viability Assessment** (based on margin-to-shipping ratio):
- < 3:1 = ⚠️ Margin Risk
- 3:1 to 5:1 = ✓ Acceptable
- > 5:1 = ✓✓ Strong

### 4. Do Not Test

List thresholds to avoid:
- Too low: Insufficient margin protection
- Too high: Insufficient order volume

### 5. Next Steps

- Recommended testing sequence
- Key metrics to monitor
- Success criteria definitions

## Sample Output Language

Use clear, actionable language:

```
Based on your order data from the last 6 months:

**Order Landscape**:
Orders cluster between $50-$200 (68% of all orders). Clear peak at $75-$100.

**Hero Products**:
Top driver is [Product X] at $95 (18% of revenue). Next three average $85-$110.

**Shipping Economics**:
Average cost $8.50/order. Most orders $6-$12 to ship.

**Recommended Testing Strategy**:

Test #1: $75 Threshold
✓ Tests friction removal on hero products
✓ 45% of orders would qualify
✓ Margin-to-shipping ratio: 6.2:1 (strong protection)
✓ Estimated monthly cost: $X,XXX

Test #2: $125 Threshold
✓ Tests basket expansion behavior
✓ 28% of orders would qualify
✓ Margin-to-shipping ratio: 8.5:1 (excellent protection)
✓ Lower monthly cost but tests different behavior

Do Not Test:
✗ $40 or below: Margin risk (2:1 ratio only)
✗ $200+: Insufficient volume (8% of orders)
```

## Important Considerations

**Data Quality**:
- Exclude canceled/failed orders
- Filter outlier shipping costs
- Ensure sufficient data volume
- Use recent data (6-12 months)

**Margin Calculations**:
- Work with averages if detailed margin data unavailable
- Account for returns if data available
- Consider category-level margin differences

**Testing Philosophy**:
- This analysis identifies WHERE to test, not WHETHER free shipping works
- Always A/B test before full rollout
- Monitor conversion rate AND profitability
- Track margin dollars, not just revenue

## Common Pitfalls

1. **Testing Too Low**: Threshold below low-margin product zone
2. **Testing Without Volume**: <10% of orders at threshold level
3. **Ignoring Categories**: Different margins may need different thresholds
4. **Focusing Only on AOV**: Revenue gains mean nothing if margins erode
5. **No Control Group**: Always A/B test vs control

## When to Re-run

- Quarterly (seasonal shifts)
- After major product launches
- When hero product pricing changes
- If shipping costs increase substantially
- After major catalog changes

## Integration Points

Coordinates with:
- Shopify/channel shipping settings
- Promotion strategy planning
- Inventory management (threshold-driving products)
- Pricing strategy optimization

## Technical Notes

**Query Optimization**:
- Optimized for BigQuery (Fulfil's warehouse)
- 6-month default lookback (adjust for volume)
- Partition on order_date for performance
- Limit to items with >5 orders (reduce noise)

**Error Handling**:
- Handle NULL shipping costs appropriately
- Validate order_value > 0
- Check sufficient data volume
- Alert if hero products unclear

## Methodology Reference

For complete SQL queries and detailed analysis steps, see [METHODOLOGY.md](METHODOLOGY.md).

Based on Victor Paycro's data-driven threshold optimization framework.

**Version**: 1.0
